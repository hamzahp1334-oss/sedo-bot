"""
Admin Management Panel Handlers for SEDO MARTIAL ART Telegram Bot System.
Used by @sedoadmin_bot and authorized admins on @officialsedo_bot.
"""

import logging
from telegram import Update, InputFile
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import config
import database
import keyboards
import notifications
from states import (
    ADMIN_BROADCAST_CONTENT,
    ADMIN_BROADCAST_CONFIRM,
    ADMIN_REPLY_MSG_ID,
    ADMIN_REPLY_TEXT,
    ADMIN_ADD_NOTE_TEXT
)

logger = logging.getLogger(__name__)


def require_admin(func):
    """Decorator to enforce admin authorization."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user or not config.is_admin(user.id):
            if update.message:
                await update.message.reply_text("⛔ ይቅርታ፣ ይህንን ትዕዛዝ ለመጠቀም የአስተዳዳሪ ፈቃድ የለዎትም።")
            elif update.callback_query:
                await update.callback_query.answer("⛔ የአስተዳዳሪ ፈቃድ ያስፈልጋል።", show_alert=True)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


@require_admin
async def show_admin_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display real-time statistics dashboard."""
    stats = await database.get_dashboard_stats()

    text = (
        "⚡ <b>የሴዶ ማርሻል አርትስ አስተዳዳሪ ዳሽቦርድ (ADMIN PANEL)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 <b>ጠቅላላ ተጠቃሚዎች:</b> {stats['total_users']}\n\n"
        f"📢 <b>ጠቅላላ ማስታወቂያዎች:</b> {stats['total_ads']}\n"
        f"⏳ <b>በመጠባበቅ ላይ ያሉ ማስታወቂያዎች:</b> {stats['pending_ads']}\n\n"
        f"🤝 <b>ጠቅላላ አጋርነቶች:</b> {stats['total_partnerships']}\n"
        f"⏳ <b>በመጠባበቅ ላይ ያሉ አጋርነቶች:</b> {stats['pending_partnerships']}\n\n"
        f"📩 <b>ያልተነበቡ መልዕክቶች:</b> {stats['unread_messages']}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "ከታች ያሉትን አዝራሮች በመጫን ዝርዝሮችን ማየትና ማስተዳደር ይችላሉ።"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=keyboards.get_admin_main_menu(),
        parse_mode=ParseMode.HTML
    )


@require_admin
async def show_pending_ads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show pending advertisement requests."""
    async with database.aiosqlite.connect(config.SQLITE_DB_PATH) as db:
        db.row_factory = database.aiosqlite.Row
        async with db.execute("""
            SELECT * FROM advertisement_requests
            WHERE status = 'pending'
            ORDER BY created_at DESC
            LIMIT 10;
        """) as cursor:
            rows = await cursor.fetchall()

    if not rows:
        await update.message.reply_text("✅ በአሁኑ ወቅት በመጠባበቅ ላይ ያለ አዲስ የማስታወቂያ ጥያቄ የለም።")
        return

    for r in rows:
        req_id = r["id"]
        cat = keyboards.resolve_category_label(r["category"] or "", "am")
        fmt = keyboards.resolve_format_label(r["format"] or "", "am")
        env = keyboards.resolve_environment_label(r["environment"] or "", "am")
        bud = keyboards.resolve_budget_label(r["budget"] or "", "am")

        text = (
            f"📢 <b>የማስታወቂያ ጥያቄ:</b> <code>{req_id}</code>\n\n"
            f"👤 <b>ስም:</b> {r['full_name']}\n"
            f"🏢 <b>ድርጅት:</b> {r['company_name']}\n"
            f"📍 <b>አድራሻ:</b> {r['company_address'] or 'N/A'}\n"
            f"🏷 <b>ዘርፍ:</b> {cat}\n"
            f"🎥 <b>ቅርጸት:</b> {fmt}\n"
            f"🏢 <b>የቀረጻ ቦታ:</b> {env}\n"
            f"💰 <b>በጀት:</b> {bud}\n"
            f"📅 <b>ቀን:</b> {r['preferred_date']}\n"
            f"📱 <b>ስልክ:</b> {r['phone']}\n"
            f"✈️ <b>ቴሌግራም:</b> {r['username']}\n\n"
            f"📝 <b>መግለጫ:</b> {r['description']}\n"
        )
        markup = keyboards.get_admin_request_actions_keyboard(req_id)
        await update.message.reply_text(
            text=text,
            reply_markup=markup,
            parse_mode=ParseMode.HTML
        )


@require_admin
async def show_pending_partnerships(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show pending partnership requests."""
    async with database.aiosqlite.connect(config.SQLITE_DB_PATH) as db:
        db.row_factory = database.aiosqlite.Row
        async with db.execute("""
            SELECT * FROM partnership_requests
            WHERE status = 'pending'
            ORDER BY created_at DESC
            LIMIT 10;
        """) as cursor:
            rows = await cursor.fetchall()

    if not rows:
        await update.message.reply_text("✅ በአሁኑ ወቅት በመጠባበቅ ላይ ያለ አዲስ የትብብር ጥያቄ የለም።")
        return

    for r in rows:
        req_id = r["id"]
        collab = keyboards.resolve_collab_label(r["collab_type"] or "", "am")

        text = (
            f"🤝 <b>የትብብር ጥያቄ:</b> <code>{req_id}</code>\n\n"
            f"👤 <b>ስም:</b> {r['full_name']}\n"
            f"🏢 <b>ድርጅት:</b> {r['company_name']}\n"
            f"💼 <b>ድርሻ:</b> {r['position']}\n"
            f"🌟 <b>አይነት:</b> {collab}\n"
            f"📱 <b>ስልክ:</b> {r['phone']}\n"
            f"✈️ <b>ቴሌግራም:</b> {r['username']}\n\n"
            f"💡 <b>አቅርቦት:</b> {r['offer_description']}\n"
            f"💬 <b>መልዕክት:</b> {r['message']}\n"
        )
        markup = keyboards.get_admin_request_actions_keyboard(req_id)
        await update.message.reply_text(
            text=text,
            reply_markup=markup,
            parse_mode=ParseMode.HTML
        )


@require_admin
async def show_contact_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show recent customer direct messages."""
    msgs = await database.get_recent_contact_messages(limit=10)
    if not msgs:
        await update.message.reply_text("✅ ምንም አዲስ ያልተነበበ መልዕክት የለም።")
        return

    for m in msgs:
        text = (
            f"📩 <b>መልዕክት:</b> <code>{m['id']}</code>\n"
            f"👤 <b>ላኪ:</b> {m['name']} (ID: <code>{m['user_id']}</code>)\n"
            f"🕒 <b>ቀን:</b> {m['created_at']}\n\n"
            f"💬 {m['message']}\n"
        )
        await update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


@require_admin
async def export_csv_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Export advertising and partnership records as CSV files."""
    try:
        ads_csv = await database.export_data_as_csv("advertisement_requests")
        await update.message.reply_document(
            document=InputFile(ads_csv, filename="sedo_advertisements.csv"),
            caption="📊 የማስታወቂያ ጥያቄዎች ዝርዝር (CSV)"
        )

        parts_csv = await database.export_data_as_csv("partnership_requests")
        await update.message.reply_document(
            document=InputFile(parts_csv, filename="sedo_partnerships.csv"),
            caption="📊 የትብብር ጥያቄዎች ዝርዝር (CSV)"
        )
    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        await update.message.reply_text(f"⚠️ CSV ፋይሎችን በማዘጋጀት ላይ ስህተት ተፈጥሯል፦ {e}")


@require_admin
async def admin_action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle approval, rejection and quick replies."""
    query = update.callback_query
    await query.answer()

    data = query.data
    prefix, req_id = data.split(":", 1)

    customer_bot = context.application.bot_data.get("customer_bot") or context.bot

    if prefix == "adm_appr":
        # Check if ad or partnership
        if req_id.startswith("AD-"):
            await database.update_advertisement_status(req_id, "approved")
            rec = await database.get_advertisement_request(req_id)
        else:
            await database.update_partnership_status(req_id, "approved")
            rec = await database.get_partnership_request(req_id)

        if rec:
            lang = await database.get_user_language(rec["user_id"])
            await notifications.notify_user_status_update(
                customer_bot=customer_bot,
                user_id=rec["user_id"],
                req_id=req_id,
                status="approved",
                lang=lang
            )
        await query.message.reply_text(f"✅ ጥያቄ <code>{req_id}</code> ጸድቋል! ተጠቃሚው ማሳወቂያ ደርሶታል።", parse_mode=ParseMode.HTML)

    elif prefix == "adm_rej":
        if req_id.startswith("AD-"):
            await database.update_advertisement_status(req_id, "rejected")
            rec = await database.get_advertisement_request(req_id)
        else:
            await database.update_partnership_status(req_id, "rejected")
            rec = await database.get_partnership_request(req_id)

        if rec:
            lang = await database.get_user_language(rec["user_id"])
            await notifications.notify_user_status_update(
                customer_bot=customer_bot,
                user_id=rec["user_id"],
                req_id=req_id,
                status="rejected",
                lang=lang
            )
        await query.message.reply_text(f"❌ ጥያቄ <code>{req_id}</code> ውድቅ ተደርጓል። ተጠቃሚው ማሳወቂያ ደርሶታል።", parse_mode=ParseMode.HTML)

    elif prefix == "adm_reply":
        markup = keyboards.get_admin_quick_reply_keyboard(req_id)
        await query.message.reply_text("💬 ፈጣን ምላሽ ለመስጠት ከአማራጮቹ አንዱን ይምረጡ፦", reply_markup=markup)

    elif prefix == "adm_qr":
        # adm_qr:action:req_id
        parts = data.split(":")
        action_type = parts[1]
        target_id = parts[2]

        if target_id.startswith("AD-"):
            rec = await database.get_advertisement_request(target_id)
        else:
            rec = await database.get_partnership_request(target_id)

        if not rec:
            await query.message.reply_text("⚠️ ጥያቄው አልተገኘም።")
            return

        lang = await database.get_user_language(rec["user_id"])
        reply_text = ""

        if action_type == "accept":
            reply_text = "ሰላም፣ ያቀረቡት ጥያቄ ተቀባይነት አግኝቷል። በቅርቡ ከስራ ባልደረባችን ጋር ዝርዝሩን እናመቻቻለን።" if lang == "am" else "Hello, your request has been accepted. We will finalize details with you shortly."
        elif action_type == "schedule":
            reply_text = "ሰላም፣ የቀረጻ እና የፕሮሞሽን ቀጠሮ ለማመቻቸት እባክዎ አመቺ ጊዜዎን ይግለጹልን።" if lang == "am" else "Hello, please let us know your convenient time to schedule the shooting date."
        elif action_type == "call":
            reply_text = "ሰላም፣ ዝርዝሩን ለመወያየት በሰጡን ስልክ ቁጥር በቅርቡ እንደውላለን።" if lang == "am" else "Hello, our team will call you directly via your provided phone number shortly."

        if reply_text:
            await notifications.notify_user_status_update(
                customer_bot=customer_bot,
                user_id=rec["user_id"],
                req_id=target_id,
                status="reviewed",
                lang=lang,
                admin_note=reply_text
            )
            await query.message.reply_text(f"✅ መልዕክቱ ለተጠቃሚው ተልኳል፦\n\"{reply_text}\"")
