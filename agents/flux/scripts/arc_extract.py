#!/usr/bin/env python3
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

LOG_DIR = "/home/prime/arc_ai_angels/shared/internet/direct_logs"


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def env_required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


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
            "error": "usage: arc_extract.py '<url>'"
        }, ensure_ascii=False))
        sys.exit(1)

    url = sys.argv[1].strip()
    call_id = f"arc-extract-{uuid.uuid4()}"

    try:
        result = firecrawl_extract(url)
        payload = {
            "ok": True,
            "id": call_id,
            "provider": "firecrawl",
            "url": url,
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
            "provider": "firecrawl",
            "url": url,
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
            "provider": "firecrawl",
            "url": url,
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
            "provider": "firecrawl",
            "url": url,
            "completedAt": now_iso(),
            "error": str(e)
        }
        write_log(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
