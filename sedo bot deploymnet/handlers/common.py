"""
Common and Core Handlers for SEDO MARTIAL ART Telegram Bot.
Handles /start, language selection, About, TikTok link, and cancellation.
"""

import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import config
import database
import keyboards
from i18n import get_text

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command. Prompts language selection first."""
    user = update.effective_user
    if not user:
        return

    # Record or update user in database
    await database.upsert_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Prompt user to select language
    await update.message.reply_text(
        text=(
            "🌐 **እባክዎ ቋንቋ ይምረጡ / Please choose your language:**\n\n"
            "🇪🇹 **አማርኛ** ለመጠቀም ከታች ያለውን አዝራር ይጫኑ።\n"
            "🇬🇧 Click the button below to use in **English**."
        ),
        reply_markup=keyboards.get_language_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process language selection callback."""
    query = update.callback_query
    await query.answer()

    data = query.data
    lang = "am"
    if data == "lang:en":
        lang = "en"
    elif data == "lang:am":
        lang = "am"

    context.user_data["lang"] = lang
    user = update.effective_user
    if user:
        await database.set_user_language(user.id, lang)

    welcome_title = get_text("welcome_title", lang)
    welcome_sub = get_text("welcome_subtitle", lang)
    full_caption = f"{welcome_title}\n\n{welcome_sub}"

    is_admin_user = config.is_admin(user.id) if user else False
    main_menu_markup = keyboards.get_customer_main_menu(is_admin_user=is_admin_user, lang=lang)

    # Send logo image if exists, otherwise text
    if config.LOGO_PATH.exists():
        try:
            with open(config.LOGO_PATH, "rb") as logo_file:
                await query.message.reply_photo(
                    photo=logo_file,
                    caption=full_caption,
                    reply_markup=main_menu_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        except Exception as e:
            logger.warning(f"Failed to send logo photo: {e}")

    await query.message.reply_text(
        text=full_caption,
        reply_markup=main_menu_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt user to change language."""
    await update.message.reply_text(
        text="🌐 **እባክዎ ቋንቋ ይምረጡ / Please choose your language:**",
        reply_markup=keyboards.get_language_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display information about SEDO MARTIAL ART."""
    lang = context.user_data.get("lang") or await database.get_user_language(update.effective_user.id)
    about_text = get_text("about_text", lang)
    await update.message.reply_text(
        text=about_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def show_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display TikTok profile link and information."""
    lang = context.user_data.get("lang") or await database.get_user_language(update.effective_user.id)
    tiktok_text = get_text("tiktok_text", lang)
    await update.message.reply_text(
        text=tiktok_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel any active conversation and return to main menu."""
    user = update.effective_user
    lang = context.user_data.get("lang") or (await database.get_user_language(user.id) if user else "am")
    is_admin = config.is_admin(user.id) if user else False

    context.user_data.pop("ad_data", None)
    context.user_data.pop("partnership_data", None)
    context.user_data.pop("contact_data", None)

    await update.message.reply_text(
        text=get_text("cancelled", lang),
        reply_markup=keyboards.get_customer_main_menu(is_admin_user=is_admin, lang=lang)
    )
    return ConversationHandler.END


async def error_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fallback handler for unhandled or unexpected inputs."""
    user = update.effective_user
    lang = context.user_data.get("lang") or (await database.get_user_language(user.id) if user else "am")
    await update.message.reply_text(
        text=get_text("err_generic", lang),
        parse_mode=ParseMode.MARKDOWN
    )
