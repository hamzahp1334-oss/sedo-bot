"""
File and Media Storage Management for SEDO MARTIAL ART Telegram Bot System.
Handles local storage and downloads from Telegram.
"""

import os
import uuid
import logging
from pathlib import Path
from typing import Optional, Tuple
from telegram import File, PhotoSize, Document, Video

import config

logger = logging.getLogger(__name__)

# Allowed file extensions for security
ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp",
    ".mp4", ".mov", ".avi", ".mkv",
    ".pdf", ".doc", ".docx", ".zip"
}


def is_allowed_file(filename: str) -> bool:
    """Validate file extension against safe whitelist."""
    if not filename:
        return False
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


async def save_telegram_media(
    media_obj,
    bot,
    subfolder: str = "general"
) -> Tuple[Optional[str], Optional[str]]:
    """
    Downloads media file from Telegram and stores locally in uploads/.
    Returns (local_relative_path, error_message).
    """
    try:
        dest_dir = config.UPLOADS_DIR / subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)

        file_id = None
        ext = ".jpg"

        if isinstance(media_obj, list):  # photo list
            photo: PhotoSize = media_obj[-1]
            file_id = photo.file_id
            ext = ".jpg"
        elif isinstance(media_obj, PhotoSize):
            file_id = media_obj.file_id
            ext = ".jpg"
        elif isinstance(media_obj, Video):
            file_id = media_obj.file_id
            ext = Path(media_obj.file_name or "video.mp4").suffix.lower() or ".mp4"
        elif isinstance(media_obj, Document):
            file_id = media_obj.file_id
            ext = Path(media_obj.file_name or "doc.pdf").suffix.lower() or ".pdf"

        if not file_id:
            return None, "Invalid media object"

        if ext not in ALLOWED_EXTENSIONS:
            return None, f"Unsupported file extension: {ext}"

        tg_file: File = await bot.get_file(file_id)
        if tg_file.file_size and tg_file.file_size > config.MAX_FILE_SIZE:
            return None, "File exceeds maximum allowed size (20MB)."

        unique_name = f"{uuid.uuid4().hex[:12]}{ext}"
        destination = dest_dir / unique_name

        await tg_file.download_to_drive(custom_path=str(destination))
        logger.info("Saved media locally: %s", destination)

        rel_path = f"uploads/{subfolder}/{unique_name}"
        return rel_path, None

    except Exception as e:
        logger.error("Error saving media from Telegram: %s", e)
        return None, str(e)
