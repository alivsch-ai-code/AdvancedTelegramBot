# config/__init__.py
# Macht den Ordner zu einem Python-Paket

import json
from pathlib import Path

# Define the path to the JSON files
CONFIG_DIR = Path(__file__).parent

# Load generation_config from generation_config.json
with open(CONFIG_DIR / "generation_config.json", "r") as f:
    generation_config = json.load(f)

# Load safety_settings from safety_setting.json
with open(CONFIG_DIR / "safety_settings.json", "r") as f:
    safety_settings = json.load(f)

# Load safety_settings from safety_setting.json
with open(CONFIG_DIR / "bot_role_settings.json", "r") as f:
    bot_role_settings = json.load(f)