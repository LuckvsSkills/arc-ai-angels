#!/usr/bin/env python3
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

LOG_DIR = "/home/prime/arc_ai_angels/shared/internet/direct_logs"

PRESETS = {
    "general": {
        "domains": None,
        "query_prefix": "",
        "query_suffix": "",
    },
    "youtube_song": {
        "domains": ["youtube.com"],
        "query_prefix": "site:youtube.com",
        "query_suffix": "official music video OR audio OR song -playlist -mix -compilation -live",
    },
    "youtube_short": {
        "domains": ["youtube.com"],
        "query_prefix": "site:youtube.com/shorts",
        "query_suffix": "motivational OR discipline OR success OR mindset -playlist",
    },
    "docs": {
        "domains": None,
        "query_prefix": "",
        "query_suffix": "documentation OR docs OR api OR reference",
    },
}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def env_required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def normalize_query(user_query, preset_name):
    preset = PRESETS.get(preset_name, PRESETS["general"])
    parts = []
    if preset["query_prefix"]:
        parts.append(preset["query_prefix"])
    parts.append(user_query.strip())
    if preset["query_suffix"]:
        parts.append(preset["query_suffix"])
    return " ".join(parts).strip()


def tavily_search(query, max_results=5, domains=None):
    api_key = env_required("TAVILY_API_KEY")
    payload = {
        "query": query,
        "search_depth": "basic",
        "max_results": max_results
    }
    if domains:
        payload["include_domains"] = domains

    req = urlrequest.Request(
        "https://api.tavily.com/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urlrequest.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def score_result(item, preset_name):
    url = (item.get("url") or "").lower()
    title = (item.get("title") or "").lower()
    content = (item.get("content") or "").lower()
    score = float(item.get("score") or 0)

    if preset_name == "youtube_song":
        if "youtube.com/watch" in url:
            score += 0.25
        if "official" in title:
            score += 0.20
        if "playlist" in url or "playlist" in title:
            score -= 0.35
        if "mix" in title or "compilation" in title:
            score -= 0.20

    elif preset_name == "youtube_short":
        if "youtube.com/shorts/" in url:
            score += 0.40
        if "shorts" in title:
            score += 0.10
        if "playlist" in url or "playlist" in title:
            score -= 0.40

    elif preset_name == "docs":
        if "docs." in url or "/docs" in url or "documentation" in url:
            score += 0.30
        if "api" in title or "reference" in title or "documentation" in title:
            score += 0.15

    else:
        if "medium.com" in url:
            score -= 0.20

    if "youtube.com/playlist" in url:
        score -= 0.25

    if "official" in content:
        score += 0.05

    return score


def rerank_results(results, preset_name):
    enriched = []
    for item in results:
        item = dict(item)
        item["_adjusted_score"] = score_result(item, preset_name)
        enriched.append(item)

    enriched.sort(key=lambda x: x["_adjusted_score"], reverse=True)

    for item in enriched:
        item.pop("_adjusted_score", None)

    return enriched


def write_log(data):
    os.makedirs(LOG_DIR, exist_ok=True)
    log_id = data.get("id", str(uuid.uuid4()))
    path = os.path.join(LOG_DIR, f"{log_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "ok": False,
            "error": "usage: arc_search.py '<query>' [max_results] [preset]"
        }, ensure_ascii=False))
        sys.exit(1)

    user_query = sys.argv[1].strip()
    max_results = 5
    preset_name = "general"

    if len(sys.argv) >= 3:
        try:
            max_results = int(sys.argv[2])
        except ValueError:
            print(json.dumps({
                "ok": False,
                "error": "max_results must be an integer"
            }, ensure_ascii=False))
            sys.exit(1)

    if len(sys.argv) >= 4:
        preset_name = sys.argv[3].strip()
        if preset_name not in PRESETS:
            print(json.dumps({
                "ok": False,
                "error": f"unknown preset: {preset_name}",
                "allowed_presets": list(PRESETS.keys())
            }, ensure_ascii=False))
            sys.exit(1)

    preset = PRESETS[preset_name]
    effective_query = normalize_query(user_query, preset_name)
    call_id = f"arc-search-{uuid.uuid4()}"

    try:
        result = tavily_search(
            effective_query,
            max_results=max_results,
            domains=preset["domains"]
        )

        result["results"] = rerank_results(result.get("results", []), preset_name)

        payload = {
            "ok": True,
            "id": call_id,
            "provider": "tavily",
            "preset": preset_name,
            "query": user_query,
            "effectiveQuery": effective_query,
            "maxResults": max_results,
            "completedAt": now_iso(),
            "result": result
        }
        write_log(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    except HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        payload = {
            "ok": False,
            "id": call_id,
            "provider": "tavily",
            "preset": preset_name,
            "query": user_query,
            "completedAt": now_iso(),
            "error": f"HTTPError {e.code}: {body}"
        }
        write_log(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(1)

    except URLError as e:
        payload = {
            "ok": False,
            "id": call_id,
            "provider": "tavily",
            "preset": preset_name,
            "query": user_query,
            "completedAt": now_iso(),
            "error": f"URLError: {e}"
        }
        write_log(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(1)

    except Exception as e:
        payload = {
            "ok": False,
            "id": call_id,
            "provider": "tavily",
            "preset": preset_name,
            "query": user_query,
            "completedAt": now_iso(),
            "error": str(e)
        }
        write_log(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
