"""
Configuration and Environment Management for SEDO MARTIAL ART Telegram Bot System.
Supports Customer Bot (@officialsedo_bot) and Admin Bot (@sedoadmin_bot).
Render / Cloud Deployer ready.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Brand identity
BRAND_NAME = "SEDO MARTIAL ART"
TIKTOK_URL = os.getenv("TIKTOK_URL", "https://www.tiktok.com/@sedomartialart3")
LOGO_PATH = ASSETS_DIR / "sedo_logo.jpg"

# Telegram Bot Tokens
CUSTOMER_BOT_TOKEN = os.getenv("CUSTOMER_BOT_TOKEN", "8684430105:AAFGXfNwKVTC_tteTIEnrFYL93CfsUZNSCY")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8742362718:AAFS31WL2zFFJNTX_hrcrzou1JWrAs002Tw")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", CUSTOMER_BOT_TOKEN)

# Authorized numeric Admin IDs
raw_admin_ids = os.getenv("ADMIN_IDS", "8798202536,406274598")
ADMIN_IDS = [int(i.strip()) for i in raw_admin_ids.split(",") if i.strip().isdigit()]
if not ADMIN_IDS:
    ADMIN_IDS = [8798202536, 406274598]


def is_admin(user_id: int) -> bool:
    """Check if given Telegram user ID is an authorized admin."""
    return user_id in ADMIN_IDS


# Database settings
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(BASE_DIR / "sedo_bot.db"))

# Webhook & Server settings for Render
PORT = int(os.getenv("PORT", "8080"))
MODE = os.getenv("MODE", "polling").lower()

# Security & Limits
RATE_LIMIT_SECONDS = float(os.getenv("RATE_LIMIT_SECONDS", "1.0"))
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB limit
