#!/usr/bin/env python3
import json
import os
import shutil
import glob
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

BASE = "/home/prime/arc_ai_angels"
INBOX = f"{BASE}/shared/internet/inbox"
OUTBOX = f"{BASE}/shared/internet/outbox"
ARCHIVE = f"{BASE}/shared/internet/archive"
INVALID = f"{BASE}/shared/internet/invalid"

REGISTRY = f"{BASE}/shared/registry"
INTERNET_GATEWAY = f"{REGISTRY}/internet_gateway.json"
TOOL_AUTH = f"{REGISTRY}/tool_authorization.json"
RUNTIME_MODE = f"{REGISTRY}/runtime_mode.json"

REQUIRED_KEYS = {"id", "agent", "type", "provider", "useCase", "status"}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def env_required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def runtime_allows_internet():
    cfg = load_json(RUNTIME_MODE)
    mode = cfg["mode"]
    safe = cfg.get("safeMode", False)
    if safe:
        return cfg["safeModePolicy"]["internetEnabled"]
    return cfg["modes"][mode]["internetEnabled"]


def agent_allowed(agent, provider, use_case):
    gateway = load_json(INTERNET_GATEWAY)
    tool_auth = load_json(TOOL_AUTH)

    if not gateway.get("enabled", False):
        return False, "internet gateway disabled"

    policy = gateway["agentPolicies"].get(agent)
    if not policy:
        return False, f"agent '{agent}' has no internet policy"

    if not policy.get("mayRequestGateway", False):
        return False, f"agent '{agent}' may not request gateway"

    if provider not in policy.get("allowedProviders", []):
        return False, f"provider '{provider}' not allowed for agent '{agent}'"

    if use_case not in policy.get("allowedUseCases", []):
        return False, f"use case '{use_case}' not allowed for agent '{agent}'"

    auth = tool_auth.get(provider)
    if not auth:
        return False, f"provider '{provider}' missing in tool_authorization"

    if auth.get("mode") != "gateway_only":
        return False, f"provider '{provider}' not configured as gateway_only"

    if agent not in auth.get("allowedAgents", []):
        return False, f"agent '{agent}' not authorized for provider '{provider}'"

    return True, None


def tavily_search(query, max_results):
    api_key = env_required("TAVILY_API_KEY")
    payload = json.dumps({
        "query": query,
        "search_depth": "basic",
        "max_results": max_results
    }).encode("utf-8")

    req = urlrequest.Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urlrequest.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def firecrawl_extract(url):
    api_key = env_required("FIRECRAWL_API_KEY")
    payload = json.dumps({
        "url": url,
        "formats": ["markdown"]
    }).encode("utf-8")

    req = urlrequest.Request(
        "https://api.firecrawl.dev/v2/scrape",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urlrequest.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def move_invalid(path, reason):
    os.makedirs(INVALID, exist_ok=True)
    base = os.path.basename(path)
    target = f"{INVALID}/{base}"
    shutil.move(path, target)
    print(f"invalid request moved: {base} -> {target} ({reason})")


def validate_request(req):
    missing = REQUIRED_KEYS - set(req.keys())
    if missing:
        return False, f"missing keys: {', '.join(sorted(missing))}"

    if req["type"] == "search":
        if not req.get("query"):
            return False, "search request missing query"
    elif req["type"] == "extract":
        if not req.get("url"):
            return False, "extract request missing url"
    else:
        return False, f"unsupported type: {req['type']}"

    return True, None


def process_one(path):
    try:
        req = load_json(path)
    except Exception as e:
        move_invalid(path, f"invalid json: {e}")
        return

    ok, err = validate_request(req)
    if not ok:
        move_invalid(path, err)
        return

    req_id = req["id"]
    agent = req["agent"]
    req_type = req["type"]
    provider = req["provider"]
    use_case = req["useCase"]

    response = {
        "id": req_id,
        "agent": agent,
        "providerUsed": provider,
        "type": req_type,
        "status": "failed",
        "requestedAt": req.get("requestedAt"),
        "completedAt": now_iso(),
        "query": req.get("query"),
        "url": req.get("url"),
        "result": {},
        "error": None
    }

    try:
        if not runtime_allows_internet():
            raise RuntimeError("internet disabled by runtime_mode")

        ok, err = agent_allowed(agent, provider, use_case)
        if not ok:
            raise RuntimeError(err)

        if req_type == "search" and provider == "tavily":
            result = tavily_search(req["query"], int(req.get("maxResults", 3)))
        elif req_type == "extract" and provider == "firecrawl":
            result = firecrawl_extract(req["url"])
        else:
            raise RuntimeError(f"unsupported request combination: type={req_type}, provider={provider}")

        response["status"] = "completed"
        response["result"] = result

    except HTTPError as e:
        response["error"] = f"HTTPError {e.code}: {e.read().decode('utf-8', errors='ignore')}"
    except URLError as e:
        response["error"] = f"URLError: {e}"
    except Exception as e:
        response["error"] = str(e)

    out_path = f"{OUTBOX}/{req_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)

    archive_path = f"{ARCHIVE}/{os.path.basename(path)}"
    shutil.move(path, archive_path)

    print(f"processed: {req_id} -> {out_path}")


def main():
    os.makedirs(OUTBOX, exist_ok=True)
    os.makedirs(ARCHIVE, exist_ok=True)
    os.makedirs(INVALID, exist_ok=True)

    files = sorted(glob.glob(f"{INBOX}/*.json"))
    if not files:
        print("no pending internet requests")
        return

    for path in files:
        process_one(path)


if __name__ == "__main__":
    main()
