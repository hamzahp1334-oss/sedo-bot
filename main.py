"""
Main Entrypoint for SEDO MARTIAL ART Telegram Bot System.
Runs Customer Bot (@officialsedo_bot), Admin Bot (@sedoadmin_bot),
and a Lightweight Health-Check HTTP Server (port 8080 / $PORT) for Render deployment.
"""

import asyncio
import logging
import os
import re
import sys
from aiohttp import web
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

import config
import database
import keyboards
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
    AD_CONFIRM,
    PART_NAME,
    PART_COMPANY,
    PART_ROLE,
    PART_USERNAME,
    PART_PHONE,
    PART_OFFER,
    PART_TYPE,
    PART_MESSAGE,
    PART_FILE,
    PART_CONFIRM,
    CONTACT_NAME,
    CONTACT_MESSAGE
)
from handlers import common, advertise, partnership, contact, my_requests, admin

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("sedo_bot")


# ---------------------------------------------------------
# HEALTHCHECK HTTP SERVER (for Render, Railway, VPS, etc.)
# ---------------------------------------------------------
async def health_check_handler(request: web.Request) -> web.Response:
    """Return 200 OK for platform health checkers."""
    return web.json_response({
        "status": "healthy",
        "brand": "SEDO MARTIAL ART",
        "customer_bot": "@officialsedo_bot",
        "admin_bot": "@sedoadmin_bot"
    })


def create_health_app() -> web.Application:
    """Create lightweight aiohttp application."""
    app = web.Application()
    app.router.add_get("/", health_check_handler)
    app.router.add_get("/health", health_check_handler)
    return app


# ---------------------------------------------------------
# BUILD CONVERSATION HANDLERS
# ---------------------------------------------------------
def build_advertising_conversation_handler() -> ConversationHandler:
    """Assemble the Advertising conversation workflow."""
    return ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex(r"^(📢 ማስታወቂያ አስታውቅ|📢 Advertise)$"),
                advertise.start_ad_flow
            ),
            CommandHandler("advertise", advertise.start_ad_flow)
        ],
        states={
            AD_CATEGORY: [
                CallbackQueryHandler(advertise.ad_category_callback, pattern=r"^adcat:")
            ],
            AD_CUSTOM_CATEGORY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_custom_category_received)
            ],
            AD_FORMAT: [
                CallbackQueryHandler(advertise.ad_format_callback, pattern=r"^adformat:")
            ],
            AD_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_name_received)
            ],
            AD_COMPANY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_company_received)
            ],
            AD_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_address_received)
            ],
            AD_ENVIRONMENT: [
                CallbackQueryHandler(advertise.ad_environment_callback, pattern=r"^adenviron:")
            ],
            AD_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_username_received)
            ],
            AD_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_phone_received)
            ],
            AD_DESC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_desc_received)
            ],
            AD_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_date_received)
            ],
            AD_BUDGET_TIER: [
                CallbackQueryHandler(advertise.ad_budget_callback, pattern=r"^adbudget:")
            ],
            AD_CUSTOM_BUDGET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_custom_budget_received)
            ],
            AD_MEDIA: [
                MessageHandler(
                    filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.TEXT,
                    advertise.ad_media_received
                )
            ],
            AD_NOTES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, advertise.ad_notes_received)
            ],
            AD_CONFIRM: [
                CallbackQueryHandler(advertise.ad_confirm_callback, pattern=r"^ad_(submit|edit|cancel)$")
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex(r"^(❌ ሰርዝ|❌ Cancel)$"), common.cancel_handler),
            CommandHandler("cancel", common.cancel_handler)
        ],
        allow_reentry=True,
        per_message=False
    )


def build_partnership_conversation_handler() -> ConversationHandler:
    """Assemble the Partnership conversation workflow."""
    return ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex(r"^(🤝 አጋርነት እና ትብብር|🤝 Partnership & Collab)$"),
                partnership.start_partnership_flow
            ),
            CommandHandler("partnership", partnership.start_partnership_flow)
        ],
        states={
            PART_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_name_received)
            ],
            PART_COMPANY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_company_received)
            ],
            PART_ROLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_role_received)
            ],
            PART_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_username_received)
            ],
            PART_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_phone_received)
            ],
            PART_OFFER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_offer_received)
            ],
            PART_TYPE: [
                CallbackQueryHandler(partnership.part_type_callback, pattern=r"^collabtype:")
            ],
            PART_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, partnership.part_message_received)
            ],
            PART_FILE: [
                MessageHandler(
                    filters.Document.ALL | filters.PHOTO | filters.TEXT,
                    partnership.part_file_received
                )
            ],
            PART_CONFIRM: [
                CallbackQueryHandler(partnership.part_confirm_callback, pattern=r"^part_(submit|edit|cancel)$")
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex(r"^(❌ ሰርዝ|❌ Cancel)$"), common.cancel_handler),
            CommandHandler("cancel", common.cancel_handler)
        ],
        allow_reentry=True,
        per_message=False
    )


def build_contact_conversation_handler() -> ConversationHandler:
    """Assemble the Contact & Support conversation workflow."""
    return ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex(r"^(📩 አግኙን|📩 Contact Us)$"),
                contact.start_contact_flow
            ),
            CommandHandler("contact", contact.start_contact_flow)
        ],
        states={
            CONTACT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, contact.contact_name_received)
            ],
            CONTACT_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, contact.contact_message_received)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex(r"^(❌ ሰርዝ|❌ Cancel)$"), common.cancel_handler),
            CommandHandler("cancel", common.cancel_handler)
        ],
        allow_reentry=True,
        per_message=False
    )


# ---------------------------------------------------------
# BOT SETUP
# ---------------------------------------------------------
def setup_customer_bot(customer_app: Application) -> None:
    """Register all customer-facing handlers."""
    # 1. Start and Language handlers
    customer_app.add_handler(CommandHandler("start", common.start_command))
    customer_app.add_handler(CommandHandler("language", common.cmd_language))
    customer_app.add_handler(CallbackQueryHandler(common.language_callback, pattern=r"^lang:"))

    # 2. Main Conversation Handlers
    customer_app.add_handler(build_advertising_conversation_handler())
    customer_app.add_handler(build_partnership_conversation_handler())
    customer_app.add_handler(build_contact_conversation_handler())

    # 3. Main Menu Navigation Button Handlers
    customer_app.add_handler(MessageHandler(
        filters.Regex(r"^(📂 የእኔ ጥያቄዎች|📂 My Requests)$"),
        my_requests.show_my_requests
    ))
    customer_app.add_handler(CallbackQueryHandler(my_requests.my_requests_callback, pattern=r"^myreq_"))

    customer_app.add_handler(MessageHandler(
        filters.Regex(r"^(🥋 ስለ SEDO|🥋 About SEDO)$"),
        common.show_about
    ))
    customer_app.add_handler(CommandHandler("about", common.show_about))

    customer_app.add_handler(MessageHandler(
        filters.Regex(r"^(🎵 ቲክቶክ|🎵 TikTok)$"),
        common.show_tiktok
    ))
    customer_app.add_handler(CommandHandler("tiktok", common.show_tiktok))

    customer_app.add_handler(MessageHandler(
        filters.Regex(r"^(🌐 ቋንቋ ቀይር|🌐 Change Language)$"),
        common.cmd_language
    ))

    # Admin access from customer bot if authorized
    customer_app.add_handler(MessageHandler(
        filters.Regex(r"^(⚡ የአስተዳዳሪ ክፍል|⚡ Admin Panel)$"),
        admin.show_admin_dashboard
    ))
    customer_app.add_handler(CommandHandler("admin", admin.show_admin_dashboard))

    # Generic cancel button fallback
    customer_app.add_handler(MessageHandler(
        filters.Regex(r"^(❌ ሰርዝ|❌ Cancel)$"),
        common.cancel_handler
    ))


def setup_admin_bot(admin_app: Application) -> None:
    """Register all admin-exclusive management handlers."""
    admin_app.add_handler(CommandHandler("start", admin.show_admin_dashboard))
    admin_app.add_handler(CommandHandler("dashboard", admin.show_admin_dashboard))

    admin_app.add_handler(MessageHandler(filters.Regex(r"^📊 ዳሽቦርድ$"), admin.show_admin_dashboard))
    admin_app.add_handler(MessageHandler(filters.Regex(r"^📢 አዳዲስ ማስታወቂያዎች$"), admin.show_pending_ads))
    admin_app.add_handler(MessageHandler(filters.Regex(r"^🤝 አዳዲስ አጋርነቶች$"), admin.show_pending_partnerships))
    admin_app.add_handler(MessageHandler(filters.Regex(r"^📩 አዳዲስ መልዕክቶች$"), admin.show_contact_messages))
    admin_app.add_handler(MessageHandler(filters.Regex(r"^📥 CSV አውርድ$"), admin.export_csv_data))

    # Callback actions
    admin_app.add_handler(CallbackQueryHandler(admin.admin_action_callback, pattern=r"^adm_"))


# ---------------------------------------------------------
# MAIN ASYNC LIFECYCLE
# ---------------------------------------------------------
async def main() -> None:
    """Initialize DB, launch bot pollers and health server."""
    logger.info("Initializing SEDO MARTIAL ART Database...")
    await database.init_db()

    logger.info("Building Telegram Bot Applications...")
    customer_app = Application.builder().token(config.CUSTOMER_BOT_TOKEN).build()
    admin_app = Application.builder().token(config.ADMIN_BOT_TOKEN).build()

    # Share references for cross-bot alerts
    customer_app.bot_data["admin_bot"] = admin_app.bot
    admin_app.bot_data["customer_bot"] = customer_app.bot

    # Attach handlers
    setup_customer_bot(customer_app)
    setup_admin_bot(admin_app)

    # Initialize bot applications
    await customer_app.initialize()
    await admin_app.initialize()

    await customer_app.start()
    await admin_app.start()

    logger.info("Starting Polling for Customer Bot & Admin Bot...")
    await customer_app.updater.start_polling(drop_pending_updates=True)
    await admin_app.updater.start_polling(drop_pending_updates=True)

    # Start health HTTP server (Render port binding)
    health_app = create_health_app()
    runner = web.AppRunner(health_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.PORT)
    await site.start()
    logger.info(f"Health server running at http://0.0.0.0:{config.PORT}/health")

    logger.info("SEDO MARTIAL ART Bot System is FULLY OPERATIONAL 🥋")

    try:
        # Keep alive indefinitely
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Shutting down SEDO MARTIAL ART Bot System...")
    finally:
        await runner.cleanup()
        await customer_app.updater.stop()
        await admin_app.updater.stop()
        await customer_app.stop()
        await admin_app.stop()
        await customer_app.shutdown()
        await admin_app.shutdown()
        logger.info("Shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Application exited.")
