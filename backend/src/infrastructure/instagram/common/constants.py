# INSTAGRAM CLIENT CONSTANTS

BASE_INSTAGRAM_URL = "https://i.instagram.com"
BASE_INSTAGRAM_API_URL = BASE_INSTAGRAM_URL + "/api"
INSTAGRAM_API_V1_URL = BASE_INSTAGRAM_API_URL + "/v1"

BASE_INSTAGRAM_B_URL = "https://b.i.instagram.com"
BASE_INSTAGRAM_API_B_URL = BASE_INSTAGRAM_URL + "/api"
INSTAGRAM_API_B_V1_URL = BASE_INSTAGRAM_API_B_URL + "/v1"

BLOKS_SEND_LOGIN_REQUEST_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/"
)
BLOKS_PROCESS_CLIENT_DATA_AND_REDIRECT_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.login.process_client_data_and_redirect/"
)
BLOKS_YOUTH_REGULATION_DELETE_PREGENT_URI = "bloks/async_action/com.bloks.www.bloks.caa.reg.youthregulation.deletepregent.async/"
BLOKS_PHONE_NUMBER_PREFILL_ASYNC_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.phone.number.prefill.async.controller/"
)
BLOKS_LOGIN_SAVE_CREDENTIALS_URI = (
    "bloks/apps/com.bloks.www.caa.login.save-credentials/"
)

ZR_DUAL_TOKENS_URI = "zr/dual_tokens/"
ATTESTATION_CREATE_ANDROID_KEYSTORE_URI = "attestation/create_android_keystore/"

MULTIPLE_ACCOUNTS_GET_ACCOUNT_FAMILY_URI = "multiple_accounts/get_account_family/"

FRIENDSHIPS_CREATE_URI = "friendships/create/{user_id}/"
FRIENDSHIPS_USER_FOLLOWERS_URI = "friendships/{user_id}/followers/"

USERS_USER_INFO_URI = "users/{user_id}/info/"
USERS_GET_LIMITED_INTERACTIONS_REMINDER_URI = "users/get_limited_interactions_reminder/"

FEED_TIMELINE_URI = "feed/timeline/"
FEED_REELS_TRAY_URI = "feed/reels_tray/"


DIRECT_V2_GET_PRESENCE_URI = "direct_v2/get_presence/"
DIRECT_V2_GET_PRESENCE_ACTIVE_NOW_URI = "direct_v2/get_presence_active_now/"
DIRECT_V2_GET_PENDING_REQUESTS_PREVIEW_URI = (
    "direct_v2/async_get_pending_requests_preview/"
)
DIRECT_V2_INBOX_URI = "direct_v2/inbox/"


LAUNCHER_MOBILE_CONFIG_URI = "launcher/mobileconfig/"


NOTIFICATIONS_GET_NOTIFICATION_SETTINGS_URI = "notifications/get_notification_settings/"
NOTIFICATIONS_BADGE_URI = "notifications/badge/"

NEWS_INBOX_URI = "news/inbox/"

MEDIA_BLOCKED_URI = "media/blocked/"
