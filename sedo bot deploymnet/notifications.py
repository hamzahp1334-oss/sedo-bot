"""
Notification Service for SEDO MARTIAL ART Telegram Bot System.
Dispatches alerts to Admins (@sedoadmin_bot) and status updates to Users (@officialsedo_bot).
"""

import logging
from typing import Dict, Any, Optional
from telegram import Bot
from telegram.constants import ParseMode

import config
import keyboards
from i18n import get_text, format_status_badge

logger = logging.getLogger(__name__)


async def notify_admins_new_ad(
    admin_bot: Bot,
    ad_data: Dict[str, Any],
    customer_bot: Optional[Bot] = None
) -> None:
    """Send immediate notification to all admins about a new advertising submission."""
    req_id = ad_data.get("id", "N/A")
    cat = keyboards.resolve_category_label(ad_data.get("category", "N/A"), "am")
    fmt = keyboards.resolve_format_label(ad_data.get("format", "N/A"), "am")
    env = keyboards.resolve_environment_label(ad_data.get("environment", "N/A"), "am")
    bud = keyboards.resolve_budget_label(ad_data.get("budget", "N/A"), "am")

    text = (
        f"🚨 <b>አዲስ የማስታወቂያ ጥያቄ ደርሷል! (New Ad Request)</b>\n\n"
        f"🆔 <b>መለያ:</b> <code>{req_id}</code>\n"
        f"👤 <b>ስም:</b> {ad_data.get('full_name', 'N/A')}\n"
        f"🏢 <b>ድርጅት:</b> {ad_data.get('company_name', 'N/A')}\n"
        f"📍 <b>አድራሻ:</b> {ad_data.get('company_address', 'N/A')}\n"
        f"🏷 <b>ዘርፍ:</b> {cat}\n"
        f"🎥 <b>ቅርጸት:</b> {fmt}\n"
        f"🏢 <b>የቀረጻ ቦታ:</b> {env}\n"
        f"💰 <b>በጀት:</b> {bud}\n"
        f"📅 <b>የሚፈለግበት ቀን:</b> {ad_data.get('preferred_date', 'N/A')}\n"
        f"📱 <b>ስልክ:</b> {ad_data.get('phone', 'N/A')}\n"
        f"✈️ <b>ቴሌግራም:</b> {ad_data.get('username', 'N/A')}\n\n"
        f"📝 <b>ዝርዝር መግለጫ:</b>\n{ad_data.get('description', 'N/A')}\n\n"
        f"📌 <b>ተጨማሪ ማስታወሻ:</b> {ad_data.get('notes', 'የለም')}\n"
    )

    reply_markup = keyboards.get_admin_request_actions_keyboard(req_id)

    for admin_id in config.ADMIN_IDS:
        sent = False
        try:
            await admin_bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
            sent = True
        except Exception as e:
            logger.warning(f"Admin bot failed to send ad alert to {admin_id}: {e}")

        if not sent and customer_bot:
            try:
                await customer_bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
            except Exception as e2:
                logger.error(f"Customer bot also failed to send ad alert to {admin_id}: {e2}")


async def notify_admins_new_partnership(
    admin_bot: Bot,
    part_data: Dict[str, Any],
    customer_bot: Optional[Bot] = None
) -> None:
    """Send immediate notification to all admins about a new partnership request."""
    req_id = part_data.get("id", "N/A")
    collab = keyboards.resolve_collab_label(part_data.get("collab_type", "N/A"), "am")

    text = (
        f"🤝 <b>አዲስ የትብብር/አጋርነት ጥያቄ ደርሷል! (New Partnership)</b>\n\n"
        f"🆔 <b>መለያ:</b> <code>{req_id}</code>\n"
        f"👤 <b>ስም:</b> {part_data.get('full_name', 'N/A')}\n"
        f"🏢 <b>ድርጅት:</b> {part_data.get('company_name', 'N/A')}\n"
        f"💼 <b>የስራ ድርሻ:</b> {part_data.get('position', 'N/A')}\n"
        f"🌟 <b>የትብብር አይነት:</b> {collab}\n"
        f"📱 <b>ስልክ:</b> {part_data.get('phone', 'N/A')}\n"
        f"✈️ <b>ቴሌግራም:</b> {part_data.get('username', 'N/A')}\n\n"
        f"💡 <b>የትብብር አቅርቦት/ጥቅም:</b>\n{part_data.get('offer_description', 'N/A')}\n\n"
        f"💬 <b>መልዕክት:</b>\n{part_data.get('message', 'N/A')}\n"
    )

    reply_markup = keyboards.get_admin_request_actions_keyboard(req_id)

    for admin_id in config.ADMIN_IDS:
        sent = False
        try:
            await admin_bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
            sent = True
        except Exception as e:
            logger.warning(f"Admin bot failed to send partnership alert to {admin_id}: {e}")

        if not sent and customer_bot:
            try:
                await customer_bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
            except Exception as e2:
                logger.error(f"Customer bot also failed to send partnership alert to {admin_id}: {e2}")


async def notify_admins_new_contact(
    admin_bot: Bot,
    msg_id: str,
    user_id: int,
    name: str,
    user_message: str,
    customer_bot: Optional[Bot] = None
) -> None:
    """Send immediate notification to admins about contact message."""
    text = (
        f"📩 <b>አዲስ ቀጥተኛ መልዕክት ደርሷል! (Direct Message)</b>\n\n"
        f"🆔 <b>መለያ:</b> <code>{msg_id}</code>\n"
        f"👤 <b>ስም:</b> {name}\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n\n"
        f"💬 <b>መልዕክት:</b>\n{user_message}\n"
    )

    for admin_id in config.ADMIN_IDS:
        sent = False
        try:
            await admin_bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode=ParseMode.HTML
            )
            sent = True
        except Exception as e:
            logger.warning(f"Admin bot failed to send contact alert to {admin_id}: {e}")

        if not sent and customer_bot:
            try:
                await customer_bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode=ParseMode.HTML
                )
            except Exception as e2:
                logger.error(f"Customer bot also failed to send contact alert to {admin_id}: {e2}")


async def notify_user_status_update(
    customer_bot: Bot,
    user_id: int,
    req_id: str,
    status: str,
    lang: str = "am",
    admin_note: Optional[str] = None
) -> None:
    """Notify the customer in their chosen language about request approval/rejection."""
    badge = format_status_badge(status, lang)

    if lang == "am":
        text = (
            f"🔔 <b>የጥያቄዎ ሁኔታ ተዘምኗል!</b>\n\n"
            f"🆔 <b>መለያ:</b> <code>{req_id}</code>\n"
            f"📊 <b>አዲስ ሁኔታ:</b> {badge}\n"
        )
        if admin_note:
            text += f"\n💬 <b>ከአስተዳዳሪው የተሰጠ መልዕክት:</b>\n{admin_note}\n"
        text += "\nማንኛውንም ጥያቄ ካለዎት በዋናው ሜኑ '📩 አግኙን' የሚለውን በመጫን ሊያገኙን ይችላሉ።"
    else:
        text = (
            f"🔔 <b>Your Request Status Has Been Updated!</b>\n\n"
            f"🆔 <b>Reference ID:</b> <code>{req_id}</code>\n"
            f"📊 <b>New Status:</b> {badge}\n"
        )
        if admin_note:
            text += f"\n💬 <b>Message from Administration:</b>\n{admin_note}\n"
        text += "\nIf you have any questions, you can reach out via '📩 Contact Us' in the main menu."

    try:
        await customer_bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Failed to notify user {user_id} of status update: {e}")
