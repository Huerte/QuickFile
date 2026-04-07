import json
import os
from pathlib import Path

VALID_KEYS = {
    "prefix": str
}

DEFAULT_CONFIG = {
    "prefix": "file"
}

def get_config_path():
    home_dir = Path.home()
    config_dir = home_dir / ".quickfile"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"

def load_config():
    config_path = get_config_path()
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure defaults for missing keys
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONFIG.copy()

def save_config(data):
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_value(key):
    config = load_config()
    return config.get(key, DEFAULT_CONFIG.get(key))

def set_value(key, value):
    if key not in VALID_KEYS:
        raise ValueError(f"Invalid configuration key: '{key}'")
    
    expected_type = VALID_KEYS[key]
    try:
        # Cast value to expected type
        casted_value = expected_type(value)
    except ValueError:
        raise ValueError(f"Invalid type for '{key}'. Expected {expected_type.__name__}.")
    
    config = load_config()
    config[key] = casted_value
    save_config(config)

def reset_config():
    save_config(DEFAULT_CONFIG)
