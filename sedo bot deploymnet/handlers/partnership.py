"""
Partnership & Collaboration Conversation Handler for SEDO MARTIAL ART.
Guarantees pure language isolation and clean compact callbacks.
"""

import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import config
import database
import keyboards
import notifications
import storage
from states import (
    PART_NAME,
    PART_COMPANY,
    PART_ROLE,
    PART_USERNAME,
    PART_PHONE,
    PART_OFFER,
    PART_TYPE,
    PART_MESSAGE,
    PART_FILE,
    PART_CONFIRM
)
from i18n import get_text

logger = logging.getLogger(__name__)


async def start_partnership_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate partnership and collaboration inquiry conversation."""
    user = update.effective_user
    lang = context.user_data.get("lang") or await database.get_user_language(user.id)
    context.user_data["lang"] = lang
    context.user_data["partnership_data"] = {
        "user_id": user.id,
        "username": f"@{user.username}" if user.username else "የለም" if lang == "am" else "None"
    }

    await update.message.reply_text(
        text=get_text("part_prompt_name", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_NAME


async def part_name_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle partner's contact name."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["full_name"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_company", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_COMPANY


async def part_company_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle partner organization name."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["company_name"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_role", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_ROLE


async def part_role_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle professional role/position."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["position"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_username", lang),
        reply_markup=keyboards.get_skip_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_USERNAME


async def part_username_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Telegram username."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    skip_word = get_text("btn_skip", lang)

    if text != skip_word:
        context.user_data["partnership_data"]["username"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_phone", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_PHONE


async def part_phone_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone number."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["phone"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_offer", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_OFFER


async def part_offer_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle collaboration proposal details."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["offer_description"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_collab_type", lang),
        reply_markup=keyboards.get_collab_type_inline_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_TYPE


async def part_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle collaboration type selection."""
    query = update.callback_query
    await query.answer()

    collab_code = query.data.split(":", 1)[1]
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["collab_type"] = collab_code

    await query.message.reply_text(
        text=get_text("part_prompt_message", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_MESSAGE


async def part_message_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle custom message or pitch."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["partnership_data"]["message"] = text

    await update.message.reply_text(
        text=get_text("part_prompt_file", lang),
        reply_markup=keyboards.get_skip_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_FILE


async def part_file_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle proposal document or skip."""
    lang = context.user_data.get("lang", "am")
    skip_word = get_text("btn_skip", lang)

    if update.message.text and update.message.text.strip() == skip_word:
        context.user_data["partnership_data"]["file_path"] = None
    elif update.message.document:
        path, _ = await storage.save_telegram_media(update.message.document, context.bot, "partnerships")
        context.user_data["partnership_data"]["file_path"] = path
    elif update.message.photo:
        path, _ = await storage.save_telegram_media(update.message.photo, context.bot, "partnerships")
        context.user_data["partnership_data"]["file_path"] = path
    else:
        context.user_data["partnership_data"]["file_path"] = None

    return await send_partnership_review(update, context)


async def send_partnership_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send review card strictly in user's selected language."""
    lang = context.user_data.get("lang", "am")
    data = context.user_data.get("partnership_data", {})

    collab_label = keyboards.resolve_collab_label(data.get("collab_type", ""), lang)
    none_label = "የለም" if lang == "am" else "None"
    attached_label = "ተያይዟል ✅" if lang == "am" else "Attached ✅"
    media_display = attached_label if data.get("file_path") else none_label

    if lang == "am":
        review_text = (
            "📋 **የትብብር ጥያቄዎ ማጠቃለያ**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 **ስም:** {data.get('full_name', none_label)}\n"
            f"🏢 **ድርጅት:** {data.get('company_name', none_label)}\n"
            f"💼 **የስራ ድርሻ:** {data.get('position', none_label)}\n"
            f"🌟 **የትብብር አይነት:** {collab_label}\n"
            f"✈️ **ቴሌግራም:** {data.get('username', none_label)}\n"
            f"📱 **ስልክ:** {data.get('phone', none_label)}\n"
            f"💡 **አቅርቦት:** {data.get('offer_description', none_label)}\n"
            f"💬 **መልዕክት:** {data.get('message', none_label)}\n"
            f"📎 **ሰነድ:** {media_display}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "እባክዎ መረጃውን አረጋግጠው **'✅ ጥያቄውን ላክ'** የሚለውን ይጫኑ።"
        )
    else:
        review_text = (
            "📋 **Partnership Request Summary**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 **Name:** {data.get('full_name', none_label)}\n"
            f"🏢 **Company:** {data.get('company_name', none_label)}\n"
            f"💼 **Position:** {data.get('position', none_label)}\n"
            f"🌟 **Collab Type:** {collab_label}\n"
            f"✈️ **Telegram:** {data.get('username', none_label)}\n"
            f"📱 **Phone:** {data.get('phone', none_label)}\n"
            f"💡 **Offer:** {data.get('offer_description', none_label)}\n"
            f"💬 **Message:** {data.get('message', none_label)}\n"
            f"📎 **Document:** {media_display}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Please verify your details and click **'✅ Submit Request'**."
        )

    await update.message.reply_text(
        text=review_text,
        reply_markup=keyboards.get_partnership_review_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return PART_CONFIRM


async def part_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle final submission, edit or cancellation."""
    query = update.callback_query
    await query.answer()

    action = query.data
    lang = context.user_data.get("lang", "am")
    user = update.effective_user

    if action == "part_cancel":
        context.user_data.pop("partnership_data", None)
        await query.message.reply_text(
            text=get_text("cancelled", lang),
            reply_markup=keyboards.get_customer_main_menu(config.is_admin(user.id), lang)
        )
        return ConversationHandler.END

    if action == "part_edit":
        prompt = "✏️ እባክዎ እንደገና ይጀምሩ:" if lang == "am" else "✏️ Let's edit your request from the beginning:"
        await query.message.reply_text(
            text=f"{prompt}\n\n{get_text('part_prompt_name', lang)}",
            reply_markup=keyboards.get_cancel_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return PART_NAME

    if action == "part_submit":
        data = context.user_data.get("partnership_data", {})
        req_id = await database.create_partnership_request(data)
        data["id"] = req_id

        admin_bot = context.application.bot_data.get("admin_bot") or context.bot
        await notifications.notify_admins_new_partnership(
            admin_bot=admin_bot,
            part_data=data,
            customer_bot=context.bot
        )

        success_msg = get_text("part_submitted_success", lang).format(id=req_id)
        await query.message.reply_text(
            text=success_msg,
            reply_markup=keyboards.get_customer_main_menu(config.is_admin(user.id), lang),
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data.pop("partnership_data", None)
        return ConversationHandler.END

    return PART_CONFIRM
