"""
Advertising Workflow Conversation Handler for SEDO MARTIAL ART Telegram Bot.
Guarantees pure language isolation:
- In Amharic mode ('am'): 100% Amharic without English labels.
- In English mode ('en'): 100% English without Amharic labels.
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
    AD_CATEGORY,
    AD_CUSTOM_CATEGORY,
    AD_FORMAT,
    AD_NAME,
    AD_COMPANY,
    AD_ADDRESS,
    AD_ENVIRONMENT,
    AD_USERNAME,
    AD_PHONE,
    AD_DESC,
    AD_DATE,
    AD_BUDGET_TIER,
    AD_CUSTOM_BUDGET,
    AD_MEDIA,
    AD_NOTES,
    AD_CONFIRM
)
from i18n import get_text

logger = logging.getLogger(__name__)


async def start_ad_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate advertising inquiry conversation."""
    user = update.effective_user
    lang = context.user_data.get("lang") or await database.get_user_language(user.id)
    context.user_data["lang"] = lang
    context.user_data["ad_data"] = {
        "user_id": user.id,
        "username": f"@{user.username}" if user.username else "የለም" if lang == "am" else "None"
    }

    await update.message.reply_text(
        text=get_text("ad_prompt_category", lang),
        reply_markup=keyboards.get_ad_category_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_CATEGORY


async def ad_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle ad category inline selection."""
    query = update.callback_query
    await query.answer()

    data = query.data
    lang = context.user_data.get("lang", "am")
    category_code = data.split(":", 1)[1]

    if category_code == "custom_manual":
        prompt = "✍️ እባክዎ የድርጅትዎን ወይም የምርትዎን ዘርፍ በጽሁፍ ያስገቡ:" if lang == "am" else "✍️ Please enter your business or product sector:"
        await query.message.reply_text(
            text=prompt,
            reply_markup=keyboards.get_cancel_keyboard(lang)
        )
        return AD_CUSTOM_CATEGORY

    context.user_data["ad_data"]["category"] = category_code

    await query.message.reply_text(
        text=get_text("ad_prompt_format", lang),
        reply_markup=keyboards.get_ad_campaign_format_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_FORMAT


async def ad_custom_category_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle custom typed category."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["category"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_format", lang),
        reply_markup=keyboards.get_ad_campaign_format_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_FORMAT


async def ad_format_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle format style selection."""
    query = update.callback_query
    await query.answer()

    format_code = query.data.split(":", 1)[1]
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["format"] = format_code

    await query.message.reply_text(
        text=get_text("ad_prompt_name", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_NAME


async def ad_name_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle contact person full name."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["full_name"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_company", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_COMPANY


async def ad_company_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle company or brand name."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["company_name"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_address", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_ADDRESS


async def ad_address_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle company physical address and location."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["company_address"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_environment", lang),
        reply_markup=keyboards.get_shooting_environment_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_ENVIRONMENT


async def ad_environment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle shooting environment inline choice."""
    query = update.callback_query
    await query.answer()

    env_code = query.data.split(":", 1)[1]
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["environment"] = env_code

    await query.message.reply_text(
        text=get_text("ad_prompt_username", lang),
        reply_markup=keyboards.get_skip_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_USERNAME


async def ad_username_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Telegram username."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    skip_word = get_text("btn_skip", lang)

    if text != skip_word:
        context.user_data["ad_data"]["username"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_phone", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_PHONE


async def ad_phone_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone number."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["phone"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_desc", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_DESC


async def ad_desc_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle description of product or promotion."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["description"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_date", lang),
        reply_markup=keyboards.get_cancel_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_DATE


async def ad_date_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle preferred campaign release date."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["preferred_date"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_budget", lang),
        reply_markup=keyboards.get_budget_tier_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_BUDGET_TIER


async def ad_budget_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle budget tier selection."""
    query = update.callback_query
    await query.answer()

    budget_code = query.data.split(":", 1)[1]
    lang = context.user_data.get("lang", "am")

    if budget_code == "tier_manual":
        prompt = "✍️ እባክዎ ያሰቡትን በጀት በጽሁፍ ያስገቡ (ለምሳሌ፦ 120,000 ብር):" if lang == "am" else "✍️ Please enter your planned budget manually (e.g. 120,000 ETB):"
        await query.message.reply_text(
            text=prompt,
            reply_markup=keyboards.get_cancel_keyboard(lang)
        )
        return AD_CUSTOM_BUDGET

    context.user_data["ad_data"]["budget"] = budget_code

    await query.message.reply_text(
        text=get_text("ad_prompt_media", lang),
        reply_markup=keyboards.get_skip_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_MEDIA


async def ad_custom_budget_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle custom budget text."""
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "am")
    context.user_data["ad_data"]["budget"] = text

    await update.message.reply_text(
        text=get_text("ad_prompt_media", lang),
        reply_markup=keyboards.get_skip_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_MEDIA


async def ad_media_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle media upload or skip."""
    lang = context.user_data.get("lang", "am")
    skip_word = get_text("btn_skip", lang)

    if update.message.text and update.message.text.strip() == skip_word:
        context.user_data["ad_data"]["file_path"] = None
    elif update.message.photo:
        path, err = await storage.save_telegram_media(update.message.photo, context.bot, "ads")
        context.user_data["ad_data"]["file_path"] = path
    elif update.message.video:
        path, err = await storage.save_telegram_media(update.message.video, context.bot, "ads")
        context.user_data["ad_data"]["file_path"] = path
    elif update.message.document:
        path, err = await storage.save_telegram_media(update.message.document, context.bot, "ads")
        context.user_data["ad_data"]["file_path"] = path
    else:
        context.user_data["ad_data"]["file_path"] = None

    await update.message.reply_text(
        text=get_text("ad_prompt_notes", lang),
        reply_markup=keyboards.get_skip_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_NOTES


async def ad_notes_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle notes and show final review screen."""
    lang = context.user_data.get("lang", "am")
    skip_word = get_text("btn_skip", lang)
    text = update.message.text.strip() if update.message.text else ""

    none_label = "የለም" if lang == "am" else "None"
    context.user_data["ad_data"]["notes"] = none_label if text == skip_word or not text else text

    return await send_ad_review(update, context)


async def send_ad_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send review confirmation card strictly in user's selected language."""
    lang = context.user_data.get("lang", "am")
    data = context.user_data.get("ad_data", {})

    category_label = keyboards.resolve_category_label(data.get("category", ""), lang)
    format_label = keyboards.resolve_format_label(data.get("format", ""), lang)
    environment_label = keyboards.resolve_environment_label(data.get("environment", ""), lang)
    budget_label = keyboards.resolve_budget_label(data.get("budget", ""), lang)
    none_label = "የለም" if lang == "am" else "None"
    attached_label = "ተያይዟል ✅" if lang == "am" else "Attached ✅"
    media_display = attached_label if data.get("file_path") else none_label

    if lang == "am":
        review_text = (
            "📋 **የማስታወቂያ ጥያቄዎ ማጠቃለያ**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🏷 **ዘርፍ:** {category_label}\n"
            f"🎥 **ቅርጸት:** {format_label}\n"
            f"👤 **ስም:** {data.get('full_name', none_label)}\n"
            f"🏢 **ድርጅት:** {data.get('company_name', none_label)}\n"
            f"📍 **አድራሻ:** {data.get('company_address', none_label)}\n"
            f"🏢 **የቀረጻ ቦታ:** {environment_label}\n"
            f"✈️ **ቴሌግራም:** {data.get('username', none_label)}\n"
            f"📱 **ስልክ:** {data.get('phone', none_label)}\n"
            f"📝 **መግለጫ:** {data.get('description', none_label)}\n"
            f"📅 **ቀን:** {data.get('preferred_date', none_label)}\n"
            f"💰 **በጀት:** {budget_label}\n"
            f"📎 **ፋይል/ፎቶ:** {media_display}\n"
            f"📌 **ማስታወሻ:** {data.get('notes', none_label)}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "እባክዎ መረጃውን አረጋግጠው **'✅ ጥያቄውን ላክ'** የሚለውን ይጫኑ።"
        )
    else:
        review_text = (
            "📋 **Advertisement Request Summary**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🏷 **Sector:** {category_label}\n"
            f"🎥 **Format:** {format_label}\n"
            f"👤 **Name:** {data.get('full_name', none_label)}\n"
            f"🏢 **Company:** {data.get('company_name', none_label)}\n"
            f"📍 **Address:** {data.get('company_address', none_label)}\n"
            f"🏢 **Environment:** {environment_label}\n"
            f"✈️ **Telegram:** {data.get('username', none_label)}\n"
            f"📱 **Phone:** {data.get('phone', none_label)}\n"
            f"📝 **Description:** {data.get('description', none_label)}\n"
            f"📅 **Date:** {data.get('preferred_date', none_label)}\n"
            f"💰 **Budget:** {budget_label}\n"
            f"📎 **File/Photo:** {media_display}\n"
            f"📌 **Notes:** {data.get('notes', none_label)}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Please verify your details and click **'✅ Submit Request'**."
        )

    await update.message.reply_text(
        text=review_text,
        reply_markup=keyboards.get_ad_review_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )
    return AD_CONFIRM


async def ad_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle final submit, edit or cancel from review screen."""
    query = update.callback_query
    await query.answer()

    action = query.data
    lang = context.user_data.get("lang", "am")
    user = update.effective_user

    if action == "ad_cancel":
        context.user_data.pop("ad_data", None)
        await query.message.reply_text(
            text=get_text("cancelled", lang),
            reply_markup=keyboards.get_customer_main_menu(config.is_admin(user.id), lang)
        )
        return ConversationHandler.END

    if action == "ad_edit":
        prompt = "✏️ እባክዎ እንደገና ይጀምሩ:" if lang == "am" else "✏️ Let's edit your request from the beginning:"
        await query.message.reply_text(
            text=f"{prompt}\n\n{get_text('ad_prompt_category', lang)}",
            reply_markup=keyboards.get_ad_category_keyboard(lang),
            parse_mode=ParseMode.MARKDOWN
        )
        return AD_CATEGORY

    if action == "ad_submit":
        data = context.user_data.get("ad_data", {})
        req_id = await database.create_advertisement_request(data)
        data["id"] = req_id

        admin_bot = context.application.bot_data.get("admin_bot") or context.bot
        await notifications.notify_admins_new_ad(
            admin_bot=admin_bot,
            ad_data=data,
            customer_bot=context.bot
        )

        success_msg = get_text("ad_submitted_success", lang).format(id=req_id)
        await query.message.reply_text(
            text=success_msg,
            reply_markup=keyboards.get_customer_main_menu(config.is_admin(user.id), lang),
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data.pop("ad_data", None)
        return ConversationHandler.END

    return AD_CONFIRM
