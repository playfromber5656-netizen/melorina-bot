# code_engine.py
import json

# این دیکشنری می‌تونه بعداً از دیتابیس بیاد
MODULES = {}


def register_module(name: str, raw_code: str):
    """
    ثبت یک ماژول جدید بر اساس کدی که به صورت JSON یا متن ساختارمند می‌فرستی.
    مثال JSON:
    {
        "type": "feature",
        "title": "بازی امتیازی",
        "description": "گیم گروهی با امتیاز",
        "enabled": true
    }
    """
    try:
        data = json.loads(raw_code)
    except json.JSONDecodeError:
        # اگر JSON نبود، فعلاً به عنوان متن ساده ذخیره می‌کنیم
        data = {
            "type": "raw",
            "content": raw_code
        }

    MODULES[name] = data
    return data


def list_modules():
    """
    لیست ماژول‌های ثبت‌شده
    """
    return MODULES


def get_module(name: str):
    """
    گرفتن یک ماژول بر اساس اسم
    """
    return MODULES.get(name)


def apply_module_to_bot(bot_state: dict, module_name: str):
    """
    اعمال یک ماژول به وضعیت ربات (مثلاً اضافه کردن قابلیت جدید)
    اینجا هیچ کد پایتونی اجرا نمی‌شه، فقط داده‌ها رو تغییر می‌دیم.
    """
    module = MODULES.get(module_name)
    if not module:
        return bot_state

    # مثال ساده: اگر نوع ماژول feature بود، به لیست قابلیت‌ها اضافه کن
    features = bot_state.get("features", [])

    if module.get("type") == "feature":
        features.append({
            "title": module.get("title", module_name),
            "description": module.get("description", ""),
        })
        bot_state["features"] = features

    # می‌تونی انواع دیگه مثل "behavior", "game", "premium" و ... اضافه کنی

    return bot_state
