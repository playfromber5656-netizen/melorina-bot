# github_sync.py
import os
import json
import requests

from code_engine import register_module, apply_module_to_bot, BOT_STATE

GITHUB_MODULES_URL = os.getenv("GITHUB_MODULES_URL")


def fetch_modules_from_github():
    if not GITHUB_MODULES_URL:
        raise ValueError("GITHUB_MODULES_URL تنظیم نشده")

    resp = requests.get(GITHUB_MODULES_URL, timeout=10)
    resp.raise_for_status()

    return resp.json()


def sync_modules():
    data = fetch_modules_from_github()

    for item in data.get("modules", []):
        name = item.get("name")
        code = item.get("code")

        if not name or code is None:
            continue

        raw_code = json.dumps(code, ensure_ascii=False)
        register_module(name, raw_code)
        apply_module_to_bot(BOT_STATE, name)

    return len(data.get("modules", []))
