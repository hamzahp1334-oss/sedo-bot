"""
Finite State Machine (FSM) States for SEDO MARTIAL ART Conversation Handlers.
"""

# Advertising Conversation States
(
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
) = range(16)

# Partnership Conversation States
(
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
) = range(16, 26)

# Contact Conversation States
(
    CONTACT_NAME,
    CONTACT_MESSAGE
) = range(26, 28)

# Admin States
(
    ADMIN_BROADCAST_CONTENT,
    ADMIN_BROADCAST_CONFIRM,
    ADMIN_SEARCH_USER,
    ADMIN_DIRECT_MSG_USER,
    ADMIN_DIRECT_MSG_TEXT,
    ADMIN_REPLY_MSG_ID,
    ADMIN_REPLY_TEXT,
    ADMIN_ADD_NOTE_TEXT,
    ADMIN_EDIT_CONTENT_VALUE,
    ADMIN_NOTIFICATION_USER_ID,
    ADMIN_NOTIFICATION_TEXT
) = range(28, 39)
