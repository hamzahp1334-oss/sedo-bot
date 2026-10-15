"""
Customer Request History Handlers for SEDO MARTIAL ART Telegram Bot.
Pure language separation for 'My Requests' tracking.
"""

import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import database
import keyboards
from i18n import get_text, format_status_badge

logger = logging.getLogger(__name__)


async def show_my_requests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display history of ads and partnerships submitted by current user."""
    user = update.effective_user
    lang = context.user_data.get("lang") or await database.get_user_language(user.id)

    ads = await database.get_user_advertisements(user.id)
    partnerships = await database.get_user_partnerships(user.id)

    if not ads and not partnerships:
        empty_msg = get_text("req_empty", lang)
        await update.message.reply_text(
            text=empty_msg,
            parse_mode=ParseMode.MARKDOWN
        )
        return

    lines = []
    if lang == "am":
        lines.append("📂 **የእርስዎ ጥያቄዎች ታሪክ**")
        lines.append("━━━━━━━━━━━━━━━━━━━━\n")

        if ads:
            lines.append("📢 **የማስታወቂያ ጥያቄዎች:**")
            for a in ads:
                badge = format_status_badge(a.get("status", "pending"), "am")
                cat = keyboards.resolve_category_label(a.get("category", ""), "am")
                lines.append(f"• 🆔 `{a['id']}` | 🏷 {cat}\n  ሁኔታ: {badge}\n  ቀን: {a.get('created_at', '')[:10]}\n")

        if partnerships:
            lines.append("🤝 **የትብብር ጥያቄዎች:**")
            for p in partnerships:
                badge = format_status_badge(p.get("status", "pending"), "am")
                collab = keyboards.resolve_collab_label(p.get("collab_type", ""), "am")
                lines.append(f"• 🆔 `{p['id']}` | 🌟 {collab}\n  ሁኔታ: {badge}\n  ቀን: {p.get('created_at', '')[:10]}\n")

        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("ጥያቄዎ በአስተዳዳሪው ሲገመገም በዚህ ቦት በኩል ማሳወቂያ ይደርስዎታል።")
    else:
        lines.append("📂 **Your Request History**")
        lines.append("━━━━━━━━━━━━━━━━━━━━\n")

        if ads:
            lines.append("📢 **Advertisement Requests:**")
            for a in ads:
                badge = format_status_badge(a.get("status", "pending"), "en")
                cat = keyboards.resolve_category_label(a.get("category", ""), "en")
                lines.append(f"• 🆔 `{a['id']}` | 🏷 {cat}\n  Status: {badge}\n  Date: {a.get('created_at', '')[:10]}\n")

        if partnerships:
            lines.append("🤝 **Partnership Requests:**")
            for p in partnerships:
                badge = format_status_badge(p.get("status", "pending"), "en")
                collab = keyboards.resolve_collab_label(p.get("collab_type", ""), "en")
                lines.append(f"• 🆔 `{p['id']}` | 🌟 {collab}\n  Status: {badge}\n  Date: {p.get('created_at', '')[:10]}\n")

        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("You will receive real-time notifications here once reviewed.")

    await update.message.reply_text(
        text="\n".join(lines),
        reply_markup=keyboards.get_my_requests_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )


async def my_requests_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle refresh button in requests view."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    lang = context.user_data.get("lang") or await database.get_user_language(user.id)

    ads = await database.get_user_advertisements(user.id)
    partnerships = await database.get_user_partnerships(user.id)

    if not ads and not partnerships:
        await query.message.reply_text(
            text=get_text("req_empty", lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    lines = []
    if lang == "am":
        lines.append("📂 **የእርስዎ ጥያቄዎች ታሪክ (የታደሰ)**")
        lines.append("━━━━━━━━━━━━━━━━━━━━\n")
        if ads:
            lines.append("📢 **የማስታወቂያ ጥያቄዎች:**")
            for a in ads:
                badge = format_status_badge(a.get("status", "pending"), "am")
                cat = keyboards.resolve_category_label(a.get("category", ""), "am")
                lines.append(f"• 🆔 `{a['id']}` | 🏷 {cat}\n  ሁኔታ: {badge}\n")
        if partnerships:
            lines.append("🤝 **የትብብር ጥያቄዎች:**")
            for p in partnerships:
                badge = format_status_badge(p.get("status", "pending"), "am")
                collab = keyboards.resolve_collab_label(p.get("collab_type", ""), "am")
                lines.append(f"• 🆔 `{p['id']}` | 🌟 {collab}\n  ሁኔታ: {badge}\n")
    else:
        lines.append("📂 **Your Request History (Refreshed)**")
        lines.append("━━━━━━━━━━━━━━━━━━━━\n")
        if ads:
            lines.append("📢 **Advertisement Requests:**")
            for a in ads:
                badge = format_status_badge(a.get("status", "pending"), "en")
                cat = keyboards.resolve_category_label(a.get("category", ""), "en")
                lines.append(f"• 🆔 `{a['id']}` | 🏷 {cat}\n  Status: {badge}\n")
        if partnerships:
            lines.append("🤝 **Partnership Requests:**")
            for p in partnerships:
                badge = format_status_badge(p.get("status", "pending"), "en")
                collab = keyboards.resolve_collab_label(p.get("collab_type", ""), "en")
                lines.append(f"• 🆔 `{p['id']}` | 🌟 {collab}\n  Status: {badge}\n")

    await query.message.reply_text(
        text="\n".join(lines),
        reply_markup=keyboards.get_my_requests_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
