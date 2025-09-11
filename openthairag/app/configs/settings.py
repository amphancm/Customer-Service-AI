import logging
from db import Connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
mongo = Connection('otg_db')

def get_model_env():
    setting = mongo.setting.find_one(
        {},
        {"_id": 0, "server": 1, "local": 1},
        sort=[("_id", -1)]
    )
    logger.info(f"Fetched latest setting from Mongo: {setting}")

    if not setting:
        return {
            "isServer": False,
            "isLocal": False,
            "apikey": "",
            "domainname": "",
            "modelname": "",
            "temperature": 0.01,
            "system_prompt": ""
        }

    sp = mongo.systemPrompt.find_one({}, {"_id": 0, "content": 1, "temperature": 1}) or {}
    system_prompt = sp.get("content") or ""   # ✅ fallback to empty string
    try:
        temperature = float(sp.get("temperature", 0.01))  # ✅ force cast
    except (ValueError, TypeError):
        temperature = 0.01  # ✅ safe default

    setting = {
        "isServer": setting.get("server", {}).get("enabled", False),
        "isLocal": setting.get("local", {}).get("enabled", False),
        "apikey": setting.get("server", {}).get("apikey", "") if setting.get("server", {}).get("enabled", False) else setting.get("local", {}).get("apikey", ""),
        "domainname": setting.get("server", {}).get("domainname", "") if setting.get("server", {}).get("enabled", False) else setting.get("local", {}).get("domainname", ""),
        "modelname": setting.get("server", {}).get("modelname", "") if setting.get("server", {}).get("enabled", False) else setting.get("local", {}).get("modelname", ""),
        "temperature": temperature,
        "system_prompt": system_prompt
    }

    logger.info(f"Final model env: {setting}")
    return setting
