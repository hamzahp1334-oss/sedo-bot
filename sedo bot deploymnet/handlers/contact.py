"""
Contact & Support Conversation Handler for SEDO MARTIAL ART Telegram Bot.
"""

import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import config
import database
import keyboards
import notifications
from states import CONTACT_NAME, CONTACT_MESSAGE
from i18n import get_text

logger = logging.getLogger(__name__)


async def start_contact_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate customer direct contact workflow."""
    user = update.effective_user
    lang = context.user_data.get("lang") or await database.get_user_language(user.id)
    context.user_data["lang"] = lang
    context.user_data["contact_data"] = {
        "user_id": user.id
    }

    await update.message.reply_text(
        text=get_text("contact_prompt_name", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return CONTACT_NAME


async def contact_name_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle contact name input."""
    name = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["contact_data"]["name"] = name

    await update.message.reply_text(
        text=get_text("contact_prompt_msg", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return CONTACT_MESSAGE


async def contact_message_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save customer contact message and dispatch notification to admins."""
    user = update.effective_user
    msg_text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    data = context.user_data.get("contact_data", {})
    name = data.get("name", user.full_name)

    msg_id = await database.create_contact_message(
        user_id=user.id,
        name=name,
        message=msg_text
    )

    admin_bot = context.application.bot_data.get("admin_bot") or context.bot
    await notifications.notify_admins_new_contact(
        admin_bot=admin_bot,
        msg_id=msg_id,
        user_id=user.id,
        name=name,
        user_message=msg_text,
        customer_bot=context.bot
    )

    await update.message.reply_text(
        text=get_text("contact_success", lang),
        reply_markup=keyboards.get_customer_main_menu(config.is_admin(user.id), lang),
        parse_mode=ParseMode.MARKDOWN
    )
    context.user_data.pop("contact_data", None)
    return ConversationHandler.END
