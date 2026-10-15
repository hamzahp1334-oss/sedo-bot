"""
Keyboards and Button Layouts for SEDO MARTIAL ART Telegram Bot System.
Strict language separation:
- Amharic mode ('am'): 100% Amharic labels, no English in parentheses.
- English mode ('en'): 100% English labels, no Amharic in parentheses.
- Compact ASCII callback_data (< 25 bytes) to guarantee zero Telegram 'Button_data_invalid' errors.
"""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from i18n import get_text


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Prompt user to choose language with clear flags."""
    keyboard = [
        [
            InlineKeyboardButton("🇪🇹 አማርኛ (Amharic)", callback_data="lang:am"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_customer_main_menu(is_admin_user: bool = False, lang: str = "am") -> ReplyKeyboardMarkup:
    """Customer bot main navigation keyboard."""
    btn_adv = get_text("btn_advertise", lang)
    btn_part = get_text("btn_partnership", lang)
    btn_req = get_text("btn_my_requests", lang)
    btn_about = get_text("btn_about", lang)
    btn_contact = get_text("btn_contact", lang)
    btn_tiktok = get_text("btn_tiktok", lang)
    btn_lang = get_text("btn_lang_toggle", lang)

    keyboard = [
        [KeyboardButton(btn_adv), KeyboardButton(btn_part)],
        [KeyboardButton(btn_req), KeyboardButton(btn_about)],
        [KeyboardButton(btn_contact), KeyboardButton(btn_tiktok)],
        [KeyboardButton(btn_lang)]
    ]
    if is_admin_user:
        btn_admin = get_text("btn_admin_panel", lang)
        keyboard.append([KeyboardButton(btn_admin)])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def get_cancel_keyboard(lang: str = "am") -> ReplyKeyboardMarkup:
    """Standard cancel reply keyboard."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton(get_text("btn_cancel", lang))]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_skip_keyboard(lang: str = "am") -> ReplyKeyboardMarkup:
    """Reply keyboard offering Skip and Cancel."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(get_text("btn_skip", lang))],
            [KeyboardButton(get_text("btn_cancel", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# ---------------------------------------------------------
# ADVERTISING CATEGORIES
# ---------------------------------------------------------
AD_CATEGORIES = {
    "cars": {
        "am": "🚗 የመኪና ሽያጭና መለዋወጫ",
        "en": "🚗 Cars & Auto Sales"
    },
    "real_estate": {
        "am": "🏢 ሪል እስቴት እና ቤቶች",
        "en": "🏢 Real Estate & Housing"
    },
    "electronics": {
        "am": "📱 ኤሌክትሮኒክስ እና ስልኮች",
        "en": "📱 Electronics & Phones"
    },
    "gym_fitness": {
        "am": "🥋 ጂም፣ ስፖርትና ማርሻል አርትስ",
        "en": "🥋 Gym, Fitness & Martial Arts"
    },
    "fashion": {
        "am": "👔 ልብስ፣ ጫማ እና ፋሽን",
        "en": "👔 Fashion, Shoes & Clothing"
    },
    "restaurant": {
        "am": "🍔 ሆቴል፣ ካፌ እና ሬስቶራንት",
        "en": "🍔 Hotel, Cafe & Restaurant"
    },
    "cosmetics": {
        "am": "💄 ኮስሞቲክስና የውበት ሳሎን",
        "en": "💄 Beauty & Cosmetics"
    },
    "services": {
        "am": "💼 የንግድ አገልግሎቶችና አስመጪ",
        "en": "💼 Business & Import Services"
    },
    "event_promo": {
        "am": "🎪 የዝግጅት እና ኮንሰርት ማስታወቂያ",
        "en": "🎪 Events & Entertainment"
    },
    "custom_manual": {
        "am": "✍️ ሌላ ዘርፍ (በእጅ ለመጻፍ)",
        "en": "✍️ Other Sector (Type manually)"
    }
}


def get_ad_category_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Compact callback categories avoiding 64-byte Telegram limit."""
    keyboard = []
    keys = list(AD_CATEGORIES.keys())
    for i in range(0, len(keys) - 1, 2):
        k1 = keys[i]
        row = [InlineKeyboardButton(AD_CATEGORIES[k1][lang], callback_data=f"adcat:{k1}")]
        if i + 1 < len(keys) - 1:
            k2 = keys[i + 1]
            row.append(InlineKeyboardButton(AD_CATEGORIES[k2][lang], callback_data=f"adcat:{k2}"))
        keyboard.append(row)

    # Last manual option full width
    k_last = keys[-1]
    keyboard.append([InlineKeyboardButton(AD_CATEGORIES[k_last][lang], callback_data=f"adcat:{k_last}")])
    return InlineKeyboardMarkup(keyboard)


def resolve_category_label(code: str, lang: str = "am") -> str:
    """Resolve category code to localized text."""
    if code in AD_CATEGORIES:
        return AD_CATEGORIES[code].get(lang, AD_CATEGORIES[code]["en"])
    return code


# ---------------------------------------------------------
# ADVERTISING FORMATS
# ---------------------------------------------------------
AD_FORMATS = {
    "full_video": {
        "am": "🎥 የተሟላ ራሱን የቻለ ቲክቶክ ቪዲዮ",
        "en": "🎥 Dedicated Full TikTok Video"
    },
    "in_video_demo": {
        "am": "🥋 በማርሻል አርትስ ልምምድ ወቅት ማስተዋወቅ",
        "en": "🥋 In-Video Martial Arts Demo"
    },
    "ambassador": {
        "am": "🌟 የረጅም ጊዜ የብራንድ አምባሳደርነት",
        "en": "🌟 Brand Ambassador / Long-Term Sponsor"
    },
    "video_series": {
        "am": "🎬 ተከታታይ የቪዲዮ ዘመቻ",
        "en": "🎬 Multi-Video Campaign Series"
    },
    "cross_platform": {
        "am": "📱 በሁሉም ማህበራዊ ገጾች (TikTok + Telegram + Reels)",
        "en": "📱 Cross-Platform (TikTok + Telegram + Reels)"
    },
    "custom_format": {
        "am": "✨ የተለየ የፈጠራ ቅርጸት",
        "en": "✨ Custom Promotion Style"
    }
}


def get_ad_campaign_format_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Campaign style selection."""
    keyboard = []
    for k, v in AD_FORMATS.items():
        keyboard.append([InlineKeyboardButton(v[lang], callback_data=f"adformat:{k}")])
    return InlineKeyboardMarkup(keyboard)


def resolve_format_label(code: str, lang: str = "am") -> str:
    """Resolve format code to localized text."""
    if code in AD_FORMATS:
        return AD_FORMATS[code].get(lang, AD_FORMATS[code]["en"])
    return code


# ---------------------------------------------------------
# SHOOTING ENVIRONMENTS
# ---------------------------------------------------------
SHOOTING_ENVIRONMENTS = {
    "client_location": {
        "am": "🏢 በድርጅትዎ/መደብርዎ ውስጥ የሚቀረጽ",
        "en": "🏢 On-Site at Client Showroom / Compound"
    },
    "sedo_studio": {
        "am": "🥋 በሴዶ ማርሻል አርትስ ስቱዲዮ/ጂም ውስጥ",
        "en": "🥋 In SEDO Martial Arts Studio / Gym"
    },
    "outdoor": {
        "am": "🏙️ ውጪያዊ / የተፈጥሮ እና የከተማ ቦታ",
        "en": "🏙️ Outdoor / Scenic Urban Setting"
    },
    "hybrid": {
        "am": "🔄 ቅይጥ (ስቱዲዮ + የድርጅትዎ ቦታ)",
        "en": "🔄 Hybrid (Studio + Client Showroom)"
    },
    "custom_environ": {
        "am": "✨ የተለየ የቪዲዮ መቅረጫ ቦታ",
        "en": "✨ Other / Custom Shooting Location"
    }
}


def get_shooting_environment_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Shooting location and environment selection."""
    keyboard = []
    for k, v in SHOOTING_ENVIRONMENTS.items():
        keyboard.append([InlineKeyboardButton(v[lang], callback_data=f"adenviron:{k}")])
    return InlineKeyboardMarkup(keyboard)


def resolve_environment_label(code: str, lang: str = "am") -> str:
    """Resolve environment code to localized text."""
    if code in SHOOTING_ENVIRONMENTS:
        return SHOOTING_ENVIRONMENTS[code].get(lang, SHOOTING_ENVIRONMENTS[code]["en"])
    return code


# ---------------------------------------------------------
# BUDGET TIERS
# ---------------------------------------------------------
BUDGET_TIERS = {
    "tier_standard": {
        "am": "💰 መደበኛ (ከ50,000 ብር በታች)",
        "en": "💰 Standard (< 50,000 ETB)"
    },
    "tier_executive": {
        "am": "💎 ኤክስኪዩቲቭ (ከ50,000 - 150,000 ብር)",
        "en": "💎 Executive (50,000 - 150,000 ETB)"
    },
    "tier_vip": {
        "am": "👑 ቪአይፒ (ከ150,000 - 500,000+ ብር)",
        "en": "👑 VIP Millionaire (150,000 - 500,000+ ETB)"
    },
    "tier_intl": {
        "am": "💵 አለም አቀፍ ($1,000 - $10,000+ USD)",
        "en": "💵 International ($1,000 - $10,000+ USD)"
    },
    "tier_manual": {
        "am": "✍️ በእጅ ለመጻፍ",
        "en": "✍️ Custom Budget (Type manually)"
    }
}


def get_budget_tier_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Budget tier options."""
    keyboard = []
    for k, v in BUDGET_TIERS.items():
        keyboard.append([InlineKeyboardButton(v[lang], callback_data=f"adbudget:{k}")])
    return InlineKeyboardMarkup(keyboard)


def resolve_budget_label(code: str, lang: str = "am") -> str:
    """Resolve budget tier code to localized text."""
    if code in BUDGET_TIERS:
        return BUDGET_TIERS[code].get(lang, BUDGET_TIERS[code]["en"])
    return code


# ---------------------------------------------------------
# COLLABORATION TYPES
# ---------------------------------------------------------
COLLAB_TYPES = {
    "brand_collab": {
        "am": "🌟 የብራንድ ትብብር",
        "en": "🌟 Brand Collaboration"
    },
    "sponsorship": {
        "am": "🏆 ስፖንሰርሺፕ",
        "en": "🏆 Sponsorship"
    },
    "content_collab": {
        "am": "🎬 የይዘት እና ቪዲዮ ትብብር",
        "en": "🎬 Content Collaboration"
    },
    "event_collab": {
        "am": "🥋 የዝግጅት እና ስፖርት ትብብር",
        "en": "🥋 Event Collaboration"
    },
    "biz_partner": {
        "am": "💼 የንግድ አጋርነት",
        "en": "💼 Business Partnership"
    },
    "other_collab": {
        "am": "✨ ሌላ የትብብር አይነት",
        "en": "✨ Other Collaboration"
    }
}


def get_collab_type_inline_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Partnership/collaboration type selection."""
    keyboard = []
    for k, v in COLLAB_TYPES.items():
        keyboard.append([InlineKeyboardButton(v[lang], callback_data=f"collabtype:{k}")])
    return InlineKeyboardMarkup(keyboard)


def resolve_collab_label(code: str, lang: str = "am") -> str:
    """Resolve collaboration type code to localized text."""
    if code in COLLAB_TYPES:
        return COLLAB_TYPES[code].get(lang, COLLAB_TYPES[code]["en"])
    return code


# ---------------------------------------------------------
# REVIEW & CONFIRMATION KEYBOARDS
# ---------------------------------------------------------
def get_ad_review_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Review screen confirmation buttons with zero language mixing."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text("btn_submit", lang), callback_data="ad_submit")],
        [
            InlineKeyboardButton(get_text("btn_edit", lang), callback_data="ad_edit"),
            InlineKeyboardButton(get_text("btn_cancel", lang), callback_data="ad_cancel")
        ]
    ])


def get_partnership_review_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Review screen confirmation for partnerships."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text("btn_submit", lang), callback_data="part_submit")],
        [
            InlineKeyboardButton(get_text("btn_edit", lang), callback_data="part_edit"),
            InlineKeyboardButton(get_text("btn_cancel", lang), callback_data="part_cancel")
        ]
    ])


# ---------------------------------------------------------
# ADMIN KEYBOARDS
# ---------------------------------------------------------
def get_admin_main_menu() -> ReplyKeyboardMarkup:
    """Admin bot main navigation keyboard."""
    keyboard = [
        [KeyboardButton("📊 ዳሽቦርድ"), KeyboardButton("📢 አዳዲስ ማስታወቂያዎች")],
        [KeyboardButton("🤝 አዳዲስ አጋርነቶች"), KeyboardButton("📩 አዳዲስ መልዕክቶች")],
        [KeyboardButton("🔍 ተጠቃሚ ፈልግ"), KeyboardButton("📢 ብሮድካስት ላክ")],
        [KeyboardButton("📥 CSV አውርድ"), KeyboardButton("🏠 ወደ ዋናው ገጽ")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_request_actions_keyboard(request_id: str) -> InlineKeyboardMarkup:
    """Action buttons for handling incoming requests."""
    keyboard = [
        [
            InlineKeyboardButton("✅ አጽድቅ (Approve)", callback_data=f"adm_appr:{request_id}"),
            InlineKeyboardButton("❌ ውድቅ አድርግ (Reject)", callback_data=f"adm_rej:{request_id}")
        ],
        [
            InlineKeyboardButton("💬 ቀጥታ መልስ (Reply)", callback_data=f"adm_reply:{request_id}"),
            InlineKeyboardButton("📌 ማስታወሻ ጻፍ (Note)", callback_data=f"adm_note:{request_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_quick_reply_keyboard(request_id: str) -> InlineKeyboardMarkup:
    """Quick templated responses for fast admin triage."""
    keyboard = [
        [InlineKeyboardButton("✅ ጥያቄዎ ተቀባይነት አግኝቷል", callback_data=f"adm_qr:accept:{request_id}")],
        [InlineKeyboardButton("📅 የቀረጻ ቀጠሮ ለማመቻቸት", callback_data=f"adm_qr:schedule:{request_id}")],
        [InlineKeyboardButton("📞 በስልክ እንደውላለን", callback_data=f"adm_qr:call:{request_id}")],
        [InlineKeyboardButton("✍️ ራስዎ መልዕክት ይጻፉ", callback_data=f"adm_qr:custom:{request_id}")],
        [InlineKeyboardButton("⬅️ ተመለስ", callback_data=f"adm_qr:back:{request_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ---------------------------------------------------------
# MY REQUESTS & DETAILS
# ---------------------------------------------------------
def get_my_requests_keyboard(lang: str = "am") -> InlineKeyboardMarkup:
    """Menu inside user's 'My Requests' history view."""
    btn_text = "🔄 አድስ" if lang == "am" else "🔄 Refresh"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btn_text, callback_data="myreq_refresh")]
    ])


def get_request_detail_keyboard(req_id: str, lang: str = "am") -> InlineKeyboardMarkup:
    """Detail view keyboard for a specific request."""
    btn_text = "⬅️ ወደ ዝርዝሩ ተመለስ" if lang == "am" else "⬅️ Back to List"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btn_text, callback_data="myreq_back")]
    ])
