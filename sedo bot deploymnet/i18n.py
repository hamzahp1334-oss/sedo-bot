"""
Internationalization (i18n) and UI Text Module for SEDO MARTIAL ART.
Primary languages: Amharic (አማርኛ) and English.
Strictly separated: No English in Amharic mode, and no Amharic in English mode.
"""

MESSAGES = {
    "am": {
        # Brand & Header
        "brand_name": "SEDO MARTIAL ART 🥋",
        "welcome_title": "🥋 እንኳን ወደ **SEDO MARTIAL ART** በደህና መጡ!",
        "welcome_subtitle": (
            "ማህበራዊ ሚዲያ • ማርሻል አርትስ • የንግድ ትብብር\n\n"
            "ከታች ያሉትን አማራጮች በመጠቀም የንግድ ማስታወቂያ ጥያቄዎችን፣ የትብብር ጥያቄዎችን "
            "ወይም መልዕክትዎን በቀጥታ ማቅረብ ይችላሉ።"
        ),

        # Main Menu Buttons
        "btn_about": "🥋 ስለ SEDO",
        "btn_advertise": "📢 ማስታወቂያ አስታውቅ",
        "btn_partnership": "🤝 አጋርነት እና ትብብር",
        "btn_contact": "📩 አግኙን",
        "btn_tiktok": "🎵 ቲክቶክ",
        "btn_support": "ℹ️ መረጃ እና ድጋፍ",
        "btn_my_requests": "📂 የእኔ ጥያቄዎች",
        "btn_admin_panel": "⚡ የአስተዳዳሪ ክፍል",
        "btn_lang_toggle": "🌐 ቋንቋ ቀይር",
        "choose_language": "🌐 **እባክዎ ቋንቋ ይምረጡ / Please choose your language:**",
        "lang_changed": "✅ ቋንቋ ወደ አማርኛ ተቀይሯል።",

        # Navigation & Controls
        "btn_back": "⬅️ ተመለስ",
        "btn_main_menu": "🏠 ዋና ሜኑ",
        "btn_cancel": "❌ ሰርዝ",
        "btn_skip": "⏭️ ዝለል",
        "btn_submit": "✅ ጥያቄውን ላክ",
        "btn_edit": "✏️ አስተካክል",
        "cancelled": "❌ ክዋኔው ተሰርዟል። ወደ ዋናው ገጽ ተመልሰዋል።",

        # Status Badges
        "status_pending": "🟡 በመጠባበቅ ላይ",
        "status_reviewing": "🔵 በግምገማ ላይ",
        "status_reviewed": "🔵 ተገምግሟል",
        "status_approved": "🟢 ጸድቋል",
        "status_rejected": "🔴 ውድቅ ተደርጓል",
        "status_completed": "⚪ ተጠናቋል",

        # Advertising Flow Prompts
        "ad_prompt_category": "🎯 **የማስታወቂያውን ዘርፍ ይምረጡ:**",
        "ad_prompt_format": "🎥 **የማስታወቂያውን ቅርጸት ይምረጡ:**",
        "ad_prompt_name": "👤 እባክዎ **ሙሉ ስምዎን** ያስገቡ:",
        "ad_prompt_company": "🏢 **የድርጅት ወይም የንግድ ስምዎን** ያስገቡ:",
        "ad_prompt_address": "📍 **የድርጅትዎን ትክክለኛ አድራሻ እና ቦታ** ያስገቡ (ለምሳሌ፦ ቦሌ፣ መደብር ቁጥር 4):",
        "ad_prompt_environment": "🏢 **ቪዲዮው የት እንዲቀረጽ ይፈልጋሉ? (የቀረጻ አካባቢ ይምረጡ):**",
        "ad_prompt_username": "💬 የእርስዎን **ቴሌግራም ዩዘርኔም** ያስገቡ (ምሳሌ: @username):",
        "ad_prompt_phone": "📱 እባክዎ **ስልክ ቁጥርዎን** ያስገቡ:",
        "ad_prompt_desc": "📝 **የማስታወቂያውን ዝርዝር መግለጫ** ያስገቡ (የምርቱን አይነትና ዋና መልዕክት):",
        "ad_prompt_date": "📅 ማስታወቂያው እንዲተላለፍ የሚፈልጉትን **ቀን** ያስገቡ (ምሳሌ: 'በጥቅምት 20' ወይም 'በተቻለ ፍጥነት'):",
        "ad_prompt_budget": "💰 **ያቀዱትን የበጀት መጠን ይምረጡ:**",
        "ad_prompt_media": "📎 የማስታወቂያ **ፎቶ፣ ቪዲዮ ወይም ሰነድ** ይላኩ:\n(ማያያዝ ካልፈለጉ ከታች **'⏭️ ዝለል'** የሚለውን ይጫኑ)",
        "ad_prompt_notes": "📌 **ተጨማሪ ማስታወሻ ወይም ልዩ ፍላጎት** ካለዎት ያስገቡ:\n(ከሌለዎት **'⏭️ ዝለል'** ይጫኑ)",
        "ad_submitted_success": (
            "✅ **የማስታወቂያ ጥያቄዎ በተሳካ ሁኔታ ቀርቧል!**\n\n"
            "🆔 መለያ ቁጥር: `{id}`\n\n"
            "የ SEDO MARTIAL ART አስተዳዳሪዎች መረጃዎን ገምግመው በቅርቡ በቴሌግራም ወይም በስልክ ያነጋግሩዎታል። "
            "ሁኔታውን ለመከታተል '📂 የእኔ ጥያቄዎች' የሚለውን ይጠቀሙ።"
        ),

        # Partnership Flow Prompts
        "part_prompt_name": "👤 እባክዎ **ሙሉ ስምዎን** ያስገቡ:",
        "part_prompt_company": "🏢 **የድርጅት ወይም የተቋም ስም** ያስገቡ:",
        "part_prompt_role": "💼 በድርጅቱ ውስጥ ያለዎት **የስራ ድርሻ ወይም ሀላፊነት**:",
        "part_prompt_username": "💬 የእርስዎን **ቴሌግራም ዩዘርኔም** ያስገቡ (ምሳሌ: @username):",
        "part_prompt_phone": "📱 እባክዎ **ስልክ ቁጥርዎን** ያስገቡ:",
        "part_prompt_offer": "💡 **ምን ያቀርባሉ?**\n(ለ SEDO MARTIAL ART ምን አይነት ጥቅም ወይም አጋርነት ይዘው መጥተዋል?):",
        "part_prompt_collab_type": "🤝 **የትብብሩን አይነት ይምረጡ:**",
        "part_prompt_message": "📝 **ዝርዝር መልዕክት እና የትብብር ሀሳብዎን ያስገቡ:**",
        "part_prompt_file": "📎 ተጨማሪ **ፋይል ወይም የፕሮፖዛል ሰነድ** ይላኩ:\n(ከሌለዎት **'⏭️ ዝለል'** ይጫኑ)",
        "part_submitted_success": (
            "✅ **የትብብር ጥያቄዎ በተሳካ ሁኔታ ተልኳል!**\n\n"
            "🆔 መለያ ቁጥር: `{id}`\n\n"
            "አስተዳዳሪዎቻችን ጥያቄዎን ተመልክተው በቅርቡ ምላሽ ይሰጣሉ። እናመሰግናለን!"
        ),

        # Contact Flow Prompts
        "contact_prompt_name": "👤 እባክዎ **ሙሉ ስምዎን** ያስገቡ:",
        "contact_prompt_msg": "💬 እባክዎ ለ SEDO ማስተላለፍ የሚፈልጉትን **መልዕክት ወይም ጥያቄ** ይጻፉ:",
        "contact_success": (
            "✅ **መልዕክትዎ ለ SEDO አስተዳዳሪዎች ተልኳል!**\n\n"
            "አስተዳዳሪዎች መልዕክትዎን አይተው በዚሁ ቦት በቀጥታ ምላሽ ይሰጡዎታል።"
        ),

        # Informational Texts
        "about_text": (
            "🥋 **ስለ SEDO MARTIAL ART**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "SEDO MARTIAL ART በኢትዮጵያ ውስጥ በሚሊዮኖች የሚቆጠሩ ተከታዮች ያሉት ግንባር ቀደም የማርሻል አርትስ እና የአካል ብቃት ይዘት ፈጣሪ ነው።\n\n"
            "✨ **ምን እንሰራለን?**\n"
            "• ምርጥ የማርሻል አርትስ ማሳያዎች እና ስልጠናዎች\n"
            "• ተደራሽ እና ፈጣን ውጤት የሚያመጡ የንግድ ማስታወቂያዎች\n"
            "• የረጅም ጊዜ የብራንድ አምባሳደርነት እና ስፖንሰርሺፕ\n\n"
            "ከእኛ ጋር አብረው በመስራት ምርትዎን እና አገልግሎትዎን በሚሊዮኖች ዘንድ ተወዳጅ ያድርጉ!"
        ),
        "tiktok_text": (
            "🎵 **የሴዶ ማርሻል አርትስ ይፋዊ ቲክቶክ ገጽ**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "የቅርብ ጊዜ ቪዲዮዎችን፣ ልምምዶችን እና ስራዎችን ለመከታተል:\n\n"
            "🔗 https://www.tiktok.com/@sedomartialart3\n\n"
            "ተከታትለው አብረውን ይሁኑ! 🥋🔥"
        ),
        "req_empty": "📂 እስካሁን ያስገቧቸው ጥያቄዎች የሉም።\nከዋናው ሜኑ '📢 ማስታወቂያ አስታውቅ' ወይም '🤝 አጋርነት እና ትብብር' በመጫን ጥያቄ ማቅረብ ይችላሉ።",
        "err_generic": "⚠️ ይቅርታ፣ ጊዜያዊ ችግር አጋጥሟል። እባክዎ እንደገና ይሞክሩ።"
    },

    "en": {
        # Brand & Header
        "brand_name": "SEDO MARTIAL ART 🥋",
        "welcome_title": "🥋 Welcome to **SEDO MARTIAL ART**!",
        "welcome_subtitle": (
            "Social Media • Martial Arts • Business Collaboration\n\n"
            "Use the options below to submit advertising inquiries, partnership proposals, "
            "or contact the team directly."
        ),

        # Main Menu Buttons
        "btn_about": "🥋 About SEDO",
        "btn_advertise": "📢 Advertise",
        "btn_partnership": "🤝 Partnership & Collab",
        "btn_contact": "📩 Contact Us",
        "btn_tiktok": "🎵 TikTok",
        "btn_support": "ℹ️ Support & Info",
        "btn_my_requests": "📂 My Requests",
        "btn_admin_panel": "⚡ Admin Panel",
        "btn_lang_toggle": "🌐 Change Language",
        "choose_language": "🌐 **Please choose your language / እባክዎ ቋንቋ ይምረጡ:**",
        "lang_changed": "✅ Language changed to English.",

        # Navigation & Controls
        "btn_back": "⬅️ Back",
        "btn_main_menu": "🏠 Main Menu",
        "btn_cancel": "❌ Cancel",
        "btn_skip": "⏭️ Skip",
        "btn_submit": "✅ Submit Request",
        "btn_edit": "✏️ Edit",
        "cancelled": "❌ Operation cancelled. Returned to main menu.",

        # Status Badges
        "status_pending": "🟡 Pending",
        "status_reviewing": "🔵 Reviewing",
        "status_reviewed": "🔵 Reviewed",
        "status_approved": "🟢 Approved",
        "status_rejected": "🔴 Rejected",
        "status_completed": "⚪ Completed",

        # Advertising Flow Prompts
        "ad_prompt_category": "🎯 **Select Promotion Industry Category:**",
        "ad_prompt_format": "🎥 **Select Campaign Format & Style:**",
        "ad_prompt_name": "👤 Please enter your **Full Name**:",
        "ad_prompt_company": "🏢 Enter your **Company or Business Name**:",
        "ad_prompt_address": "📍 Enter your **Physical Company Address & Location** (e.g. Bole Medhanialem, Shop #4):",
        "ad_prompt_environment": "🏢 **Where should the shooting take place? (Select Shooting Environment):**",
        "ad_prompt_username": "💬 Enter your **Telegram Username** (e.g. @yourusername):",
        "ad_prompt_phone": "📱 Please enter your **Phone or WhatsApp Number**:",
        "ad_prompt_desc": "📝 Enter **Campaign Goals & Description**:",
        "ad_prompt_date": "📅 Enter your **Preferred Launch Date** (e.g. 'Next Friday' or 'ASAP'):",
        "ad_prompt_budget": "💰 **Select your Planned Budget Tier:**",
        "ad_prompt_media": "📎 Send promotion **photo, video, or proposal document**:\n(Or click **'⏭️ Skip'** below)",
        "ad_prompt_notes": "📌 Enter any **Special Notes or Requests**:\n(Or click **'⏭️ Skip'** below)",
        "ad_submitted_success": (
            "✅ **Your advertising request has been submitted successfully!**\n\n"
            "🆔 Reference ID: `{id}`\n\n"
            "The SEDO MARTIAL ART team will review your submission and contact you directly. "
            "You can track the status anytime under '📂 My Requests'."
        ),

        # Partnership Flow Prompts
        "part_prompt_name": "👤 Please enter your **Full Name**:",
        "part_prompt_company": "🏢 **Company / Organization Name**:",
        "part_prompt_role": "💼 Your **Role / Position**:",
        "part_prompt_username": "💬 Enter your **Telegram Username** (e.g. @username):",
        "part_prompt_phone": "📱 Please enter your **Phone Number**:",
        "part_prompt_offer": "💡 **What do you offer?**\n(What value or opportunity do you bring to SEDO MARTIAL ART?):",
        "part_prompt_collab_type": "🤝 **Select Collaboration Type:**",
        "part_prompt_message": "📝 **Enter Detailed Message & Proposal:**",
        "part_prompt_file": "📎 Attach **Proposal File or Document**:\n(Or click **'⏭️ Skip'** below)",
        "part_submitted_success": (
            "✅ **Your partnership proposal has been submitted successfully!**\n\n"
            "🆔 Reference ID: `{id}`\n\n"
            "Our team will review your proposal and get in touch shortly. Thank you!"
        ),

        # Contact Flow Prompts
        "contact_prompt_name": "👤 Please enter your **Full Name**:",
        "contact_prompt_msg": "💬 Please type your **Message or Inquiry** for SEDO:",
        "contact_success": (
            "✅ **Your message has been sent to SEDO admins!**\n\n"
            "Admins will reply to you directly through this bot."
        ),

        # Informational Texts
        "about_text": (
            "🥋 **About SEDO MARTIAL ART**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "SEDO MARTIAL ART is a premier Ethiopian martial arts athlete and top-tier content creator with millions of dedicated followers.\n\n"
            "✨ **What We Offer:**\n"
            "• High-impact martial arts demos & fitness showcases\n"
            "• Viral social media marketing & brand advertisements\n"
            "• Long-term brand ambassador & sponsorship deals\n\n"
            "Partner with SEDO to elevate your brand to millions of engaged viewers!"
        ),
        "tiktok_text": (
            "🎵 **Official SEDO MARTIAL ART TikTok**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Catch the latest videos, stunts, and martial arts showcases:\n\n"
            "🔗 https://www.tiktok.com/@sedomartialart3\n\n"
            "Follow and stay inspired! 🥋🔥"
        ),
        "req_empty": "📂 You have not submitted any requests yet.\nUse '📢 Advertise' or '🤝 Partnership & Collab' to submit one.",
        "err_generic": "⚠️ Sorry, a temporary error occurred. Please try again."
    }
}


def get_text(key: str, lang: str = "am", **kwargs) -> str:
    """Retrieve localized message string with safe formatting fallback."""
    text_dict = MESSAGES.get(lang, MESSAGES["am"])
    text = text_dict.get(key, MESSAGES["am"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


# Alias for concise usage
t = get_text


def format_status_badge(status: str, lang: str = "am") -> str:
    """Format status with color indicator emoji in chosen language."""
    st = (status or "").lower()
    mapping = {
        "pending": get_text("status_pending", lang),
        "reviewing": get_text("status_reviewing", lang),
        "reviewed": get_text("status_reviewed", lang),
        "approved": get_text("status_approved", lang),
        "rejected": get_text("status_rejected", lang),
        "completed": get_text("status_completed", lang)
    }
    return mapping.get(st, st)


# Alias for concise usage
format_status = format_status_badge
