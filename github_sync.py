# github_sync.py
import os
import json
import requests

from code_engine import register_module, apply_module_to_bot

# این آدرس رو تو Railway به صورت ENV بذار
# مثلا:
# GITHUB_MODULES_URL = "https://raw.githubusercontent.com/USER/REPO/BRANCH/modules.json"
GITHUB_MODULES_URL = os.getenv("GITHUB_MODULES_URL")


def fetch_modules_from_github():
    """
    گرفتن فایل ماژول‌ها از گیت‌هاب (مثلاً modules.json)
    """
    if not GITHUB_MODULES_URL:
        raise ValueError("GITHUB_MODULES_URL تنظیم نشده 🌸")

    resp = requests.get(GITHUB_MODULES_URL, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    return data


def sync_modules(bot_state: dict):
    """
    سینک کردن ماژول‌ها با ربات:
    - خواندن از گیت‌هاب
    - ثبت ماژول‌ها در code_engine
    - اعمال روی وضعیت ربات
    """
    modules_data = fetch_modules_from_github()

    # فرض: ساختار JSON مثل:
    # {
    #   "modules": [
    #       {"name": "game", "code": {...}},
    #       {"name": "premium", "code": {...}}
    #   ]
    # }
    for item in modules_data.get("modules", []):
        name = item.get("name")
        code = item.get("code")

        if not name or code is None:
            continue

        # تبدیل code به JSON رشته‌ای برای register_module
        raw_code = json.dumps(code, ensure_ascii=False)
        register_module(name, raw_code)
        apply_module_to_bot(bot_state, name)

    return modules_data
