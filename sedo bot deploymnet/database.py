"""
Database Management Layer for SEDO MARTIAL ART Telegram Bot System.
Supports Local SQLite with full asynchronous queries (aiosqlite)
and optional Supabase cloud synchronization.
"""

import os
import io
import csv
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import aiosqlite

import config

logger = logging.getLogger(__name__)

DB_PATH = config.SQLITE_DB_PATH


async def init_db() -> None:
    """Initialize SQLite database tables with required schema."""
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA foreign_keys=ON;")

        # Users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'am',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Advertisement Requests table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS advertisement_requests (
                id TEXT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                category TEXT,
                format TEXT,
                full_name TEXT,
                company_name TEXT,
                company_address TEXT,
                environment TEXT,
                username TEXT,
                phone TEXT,
                description TEXT,
                preferred_date TEXT,
                budget TEXT,
                file_path TEXT,
                notes TEXT,
                status TEXT DEFAULT 'pending',
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Partnership Requests table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS partnership_requests (
                id TEXT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                full_name TEXT,
                company_name TEXT,
                position TEXT,
                username TEXT,
                phone TEXT,
                offer_description TEXT,
                collab_type TEXT,
                message TEXT,
                file_path TEXT,
                status TEXT DEFAULT 'pending',
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Contact Messages table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id TEXT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                name TEXT,
                message TEXT,
                status TEXT DEFAULT 'unread',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # System Logs / Audit table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT,
                event TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        await db.commit()
    logger.info("Database schema initialized successfully.")


# ---------------------------------------------------------
# USER OPERATIONS
# ---------------------------------------------------------
async def upsert_user(
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    language: Optional[str] = None
) -> None:
    """Record or update user info and activity."""
    async with aiosqlite.connect(DB_PATH) as db:
        if language:
            await db.execute("""
                INSERT INTO users (telegram_id, username, first_name, last_name, language, last_active_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name,
                    language = excluded.language,
                    last_active_at = CURRENT_TIMESTAMP;
            """, (telegram_id, username, first_name, last_name, language))
        else:
            await db.execute("""
                INSERT INTO users (telegram_id, username, first_name, last_name, last_active_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name,
                    last_active_at = CURRENT_TIMESTAMP;
            """, (telegram_id, username, first_name, last_name))
        await db.commit()


async def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user record."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def set_user_language(telegram_id: int, language: str) -> None:
    """Explicitly switch user's language ('am' or 'en')."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, language, last_active_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(telegram_id) DO UPDATE SET
                language = excluded.language,
                last_active_at = CURRENT_TIMESTAMP;
        """, (telegram_id, language))
        await db.commit()


async def get_user_language(telegram_id: int) -> str:
    """Get preferred language for user, defaulting to 'am'."""
    user = await get_user(telegram_id)
    if user and user.get("language"):
        return user["language"]
    return "am"


# ---------------------------------------------------------
# ADVERTISEMENT REQUESTS
# ---------------------------------------------------------
async def create_advertisement_request(data: Dict[str, Any]) -> str:
    """Save newly confirmed advertisement submission."""
    req_id = data.get("id") or f"AD-{uuid.uuid4().hex[:8].upper()}"
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO advertisement_requests (
                id, user_id, category, format, full_name, company_name,
                company_address, environment, username, phone, description,
                preferred_date, budget, file_path, notes, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
        """, (
            req_id,
            data.get("user_id"),
            data.get("category"),
            data.get("format"),
            data.get("full_name"),
            data.get("company_name"),
            data.get("company_address"),
            data.get("environment"),
            data.get("username"),
            data.get("phone"),
            data.get("description"),
            data.get("preferred_date"),
            data.get("budget"),
            data.get("file_path"),
            data.get("notes")
        ))
        await db.commit()
    return req_id


async def get_advertisement_request(req_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve single advertisement request."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM advertisement_requests WHERE id = ?", (req_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_user_advertisements(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve history of advertisements for specific user."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM advertisement_requests
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def update_advertisement_status(req_id: str, status: str, admin_notes: Optional[str] = None) -> bool:
    """Update status of advertisement request."""
    async with aiosqlite.connect(DB_PATH) as db:
        if admin_notes:
            await db.execute("""
                UPDATE advertisement_requests
                SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
            """, (status, admin_notes, req_id))
        else:
            await db.execute("""
                UPDATE advertisement_requests
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
            """, (status, req_id))
        await db.commit()
        return True


# ---------------------------------------------------------
# PARTNERSHIP REQUESTS
# ---------------------------------------------------------
async def create_partnership_request(data: Dict[str, Any]) -> str:
    """Save confirmed partnership request."""
    req_id = data.get("id") or f"PRT-{uuid.uuid4().hex[:8].upper()}"
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO partnership_requests (
                id, user_id, full_name, company_name, position, username,
                phone, offer_description, collab_type, message, file_path,
                status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
        """, (
            req_id,
            data.get("user_id"),
            data.get("full_name"),
            data.get("company_name"),
            data.get("position"),
            data.get("username"),
            data.get("phone"),
            data.get("offer_description"),
            data.get("collab_type"),
            data.get("message"),
            data.get("file_path")
        ))
        await db.commit()
    return req_id


async def get_partnership_request(req_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve single partnership request."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM partnership_requests WHERE id = ?", (req_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_user_partnerships(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve history of partnerships for specific user."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM partnership_requests
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def update_partnership_status(req_id: str, status: str, admin_notes: Optional[str] = None) -> bool:
    """Update status of partnership request."""
    async with aiosqlite.connect(DB_PATH) as db:
        if admin_notes:
            await db.execute("""
                UPDATE partnership_requests
                SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
            """, (status, admin_notes, req_id))
        else:
            await db.execute("""
                UPDATE partnership_requests
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
            """, (status, req_id))
        await db.commit()
        return True


# ---------------------------------------------------------
# CONTACT MESSAGES
# ---------------------------------------------------------
async def create_contact_message(user_id: int, name: str, message: str) -> str:
    """Save customer contact message."""
    msg_id = f"MSG-{uuid.uuid4().hex[:8].upper()}"
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO contact_messages (id, user_id, name, message, status, created_at)
            VALUES (?, ?, ?, ?, 'unread', CURRENT_TIMESTAMP);
        """, (msg_id, user_id, name, message))
        await db.commit()
    return msg_id


async def get_recent_contact_messages(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve recent contact messages for admin."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM contact_messages
            ORDER BY created_at DESC
            LIMIT ?;
        """, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


# ---------------------------------------------------------
# DASHBOARD STATS & EXPORTS
# ---------------------------------------------------------
async def get_dashboard_stats() -> Dict[str, Any]:
    """Retrieve aggregate counters for admin dashboard."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users;") as c:
            total_users = (await c.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM advertisement_requests;") as c:
            total_ads = (await c.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM advertisement_requests WHERE status = 'pending';") as c:
            pending_ads = (await c.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM partnership_requests;") as c:
            total_partnerships = (await c.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM partnership_requests WHERE status = 'pending';") as c:
            pending_partnerships = (await c.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM contact_messages WHERE status = 'unread';") as c:
            unread_messages = (await c.fetchone())[0]

        return {
            "total_users": total_users,
            "total_ads": total_ads,
            "pending_ads": pending_ads,
            "total_partnerships": total_partnerships,
            "pending_partnerships": pending_partnerships,
            "unread_messages": unread_messages
        }


async def export_data_as_csv(table_name: str) -> io.BytesIO:
    """Export table data as an in-memory CSV file."""
    allowed_tables = ["users", "advertisement_requests", "partnership_requests", "contact_messages"]
    if table_name not in allowed_tables:
        raise ValueError(f"Table '{table_name}' is not allowed for export.")

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(f"SELECT * FROM {table_name} ORDER BY id DESC;") as cursor:
            rows = await cursor.fetchall()

    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))
    else:
        output.write("No records found.\n")

    bytes_out = io.BytesIO()
    bytes_out.write(output.getvalue().encode("utf-8-sig"))
    bytes_out.seek(0)
    return bytes_out
