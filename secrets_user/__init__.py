# secrets_user/__init__.py
import json
from pathlib import Path

# Define the path to the JSON files
SECRETS_DIR = Path(__file__).parent

# Load access_tokens from safety_setting.json
with open(SECRETS_DIR / "access_secrets.json", "r") as f:
    access_secrets = json.load(f)