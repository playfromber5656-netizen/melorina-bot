# code_engine.py
import json

MODULES = {}

BOT_STATE = {
    "features": [],
    "behaviors": [],
    "games": []
}


def register_module(name: str, raw_code: str):
    try:
        data = json.loads(raw_code)
    except json.JSONDecodeError:
        data = {"type": "raw", "content": raw_code}

    MODULES[name] = data
    return data


def list_modules():
    return MODULES


def get_module(name: str):
    return MODULES.get(name)


def apply_module_to_bot(bot_state: dict, module_name: str):
    module = MODULES.get(module_name)
    if not module:
        return bot_state

    mtype = module.get("type")

    if mtype == "feature":
        bot_state["features"].append({
            "title": module.get("title", module_name),
            "description": module.get("description", "")
        })

    elif mtype == "behavior":
        bot_state["behaviors"].append(module)

    elif mtype == "game":
        bot_state["games"].append(module)

    return bot_state
