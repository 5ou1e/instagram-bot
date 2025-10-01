import gzip
from urllib.parse import urlencode

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common.utils import build_signed_body, dumps_orjson
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class TestAuthSection:

    def __init__(
        self,
        state: MobileInstagramClientState,
        request_handler: RequestHandler,
        logger: Logger,
    ):
        self._state = state
        self._request_handler = request_handler
        self.logger = logger

        self._device_info = self._state.device_info
        self._local_data = self._state.local_data
        self._version_info = self._state.version_info

    async def send_requests(self):
        """Выполняет запросы как в моб. приложении после успешной авторизации"""

        await self._3_graphql_www_FxIgFetaInfoQuery()
        await self._4_graphql_www_FxIgLinkageCacheQuery()
        await self._5_multiple_accounts_get_account_family()
        await self._6_zr_dual_tokens()
        await self._7_graphql_www_FxIgXavSwitcherBadgingDataQuery()
        await self._8_loom_fetch_config()
        await self._9_launcher_mobile_config()
        await self._10_bloks_login_save_credentials()
        await self._11_graphql_www_FxIgFetaInfoQuery()
        await self._12_graph_rmd_access_token()
        await self._13_graphql_www_FxIgFetaInfoQuery()
        await self._14_graphql_www_IGSharedAccountsQuery()
        await self._15_launcher_mobile_config()
        await self._16_graphql_www_BasicAdsOptInQuery()
        await self._17_graphql_www_AFSOptInQuery()
        await self._18_users_get_limited_interactions_reminder()
        await self._19_feed_timeline()
        await self._20_notifications_badge()
        # await self._21_cdn_instagram()
        await self._22_graphql_www_IGContentFilterDictionaryLookupQuery()
        await self._23_graphql_query_GetResurrectedUserNUXEligibility()
        # await self._24_cdn_instagram()
        await self._25_graphql_query_GetOnboardingNuxEligibility()
        await self._26_graphql_www_QuickPromotionSurfaceQueryV3()
        await self._27_graphql_query_IGRealtimeRegionHintQuery()
        await self._28_graphql_www_IGPaginatedShareSheetQuery()
        await self._29_banyan_banyan()
        await self._30_feed_reels_tray()
        # await self._31_cdn_instagram()
        await self._32_graphql_www_GenAINuxConsentStatusQuery()
        await self._33_clips_discover_stream()
        await self._34_graphql_www_FxIgXavSwitcherBadgingDataQuery()
        await self._35_graphql_www_FxIgLinkageCacheQuery()
        await self._36_graphql_www_FxIgXavSwitcherBadgingDataQuery()
        await self._37_feed_injected_reels_media()
        # await self._38_cdn_instagram()
        await self._39_creatives_write_supported_capabilities()
        # await self._40_cdn_instagram()
        await self._41_graphql_www_IGFXAccessLibrarySSOAndRegFlagQuery()
        await self._42_notifications_store_client_push_permissions()
        await self._43_users_user_info()
        await self._44_graphql_www_ZeroDayLanguageSignalUpload()
        await self._45_graphql_www_HasAvatarQuery()
        await self._46_graphql_www_IGFxLinkedAccountsQuery()
        await self._47_clips_user_share_to_fb_config()
        await self._48_graphql_www_CrosspostingUnifiedConfigsQuery()
        await self._49_graphql_www_FxIgConnectedServicesInfoQuery()
        await self._50_direct_v2_inbox()
        await self._51_graphql_www_SyncCXPNoticeStateMutation()
        await self._52_android_modules_download()
        await self._53_accounts_ge_presence_disabled()
        await self._54_direct_v2_has_interop_upgraded()
        await self._55_direct_v2_async_get_pending_requests_preview()
        await self._56_direct_v2_get_presence()
        await self._57_notifications_badge()
        await self._58_direct_v2_async_get_pending_requests_preview()
        await self._59_direct_v2_inbox()
        await self._60_graphql_www_CXPFbStoriesCurrentPrivacyQuery()

    async def _3_graphql_www_FxIgFetaInfoQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "11424838746690953787234584958",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgFetaInfoQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "fx_pf_feta_info",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgFetaInfoQuery",
            "client_doc_id": "11424838746690953787234584958",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _4_graphql_www_FxIgLinkageCacheQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "11674382495679744485820947859",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgLinkageCacheQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xe_client_cache_accounts",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgLinkageCacheQuery",
            "client_doc_id": "11674382495679744485820947859",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"caller_name":"fx_product_foundation_client_FXOnline_client_cache"}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _5_multiple_accounts_get_account_family(self):
        # GET /api/v1/multiple_accounts/get_account_family/?request_source=com.bloks.www.caa.login.login_homepage
        url = "https://b.i.instagram.com/api/v1/multiple_accounts/get_account_family/?request_source=com.bloks.www.caa.login.login_homepage"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: multiple_accounts/get_account_family/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922774.116",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "89d981be53f477548440fabd74cb159c",
            "x-fb-http-engine": "MNS/TCP",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _6_zr_dual_tokens(self):
        # POST /api/v1/zr/dual_tokens/
        url = "https://b.i.instagram.com/api/v1/zr/dual_tokens/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": self._local_data.authorization,
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": "LLA",
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: zr/dual_tokens/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": str(self._local_data.family_device_id),
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922774.235",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "dcc71394a1e382782faa47d06a4cf183",
            "x-fb-http-engine": "MNS/TCP",
        }

        payload = {
            "device_id": "android-dcf4b72e82a08913",
            "_uuid": "a0737f0c-d663-4fc1-b2e9-fed88b3a874f",
            "custom_device_id": "a0737f0c-d663-4fc1-b2e9-fed88b3a874f",
            "fetch_reason": "token_expired",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _7_graphql_www_FxIgXavSwitcherBadgingDataQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "83794259218148585413504099631",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgXavSwitcherBadgingDataQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "switcher_accounts_data",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgXavSwitcherBadgingDataQuery",
            "client_doc_id": "83794259218148585413504099631",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"should_force_badge_refresh":false,"family_device_id":"","caller_name":"fx_company_identity_switcher"}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _8_loom_fetch_config(self):
        # GET /api/v1/loom/fetch_config/
        url = "https://b.i.instagram.com/api/v1/loom/fetch_config/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: loom/fetch_config/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.save-credentials",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::,com.bloks.www.caa.login.save-credentials:com.bloks.www.caa.login.save-credentials:3:button:1755922774.355::",
            "x-ig-salt-ids": "132191320",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922774.718",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "9096dfe0a72545ceec1e09a9ee988544",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _9_launcher_mobile_config(self):
        # POST /api/v1/launcher/mobileconfig/
        url = "https://b.i.instagram.com/api/v1/launcher/mobileconfig/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": "0",
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: launcher/mobileconfig/sessionless",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.save-credentials",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::,com.bloks.www.caa.login.save-credentials:com.bloks.www.caa.login.save-credentials:3:button:1755922774.355::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "0",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922774.654",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "89d981be53f477548440fabd74cb159c",
            "x-fb-http-engine": "MNS/TCP",
        }

        data = {
            "bool_opt_policy": "0",
            "mobileconfigsessionless": "",
            "api_version": "10",
            "client_context": '["opt,value_hash"]',
            "unit_type": "1",
            "use_case": "STANDARD",
            "query_hash": "464db3b19f7c9bc4be6a32adafb0d83c63c20ab88427123f500c5b1a15fb533c",
            "ts": "1755922638",
            "device_id": self._local_data.device_id,
            "fetch_mode": "CONFIG_SYNC_ONLY",
            "fetch_type": "ASYNC_FULL",
            "family_device_id": self._local_data.device_id.upper(),
        }

        payload = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _10_bloks_login_save_credentials(self):
        # POST /api/v1/bloks/apps/com.bloks.www.caa.login.save-credentials/
        url = "https://b.i.instagram.com/api/v1/bloks/apps/com.bloks.www.caa.login.save-credentials/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: bloks/apps/com.bloks.www.caa.login.save-credentials/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922774.252",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "5edc5357cd8dd588e4f801e727aacf80",
            "x-fb-http-engine": "MNS/TCP",
        }

        payload = {
            "qe_device_id": self._local_data.device_id,
            "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
            "_uuid": self._local_data.device_id,
            "family_device_id": self._local_data.family_device_id,
            "bk_client_context": '{"bloks_version":"382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21","styles_id":"instagram"}',
            "bloks_versioning_id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _11_graphql_www_FxIgFetaInfoQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "11424838746690953787234584958",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgFetaInfoQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "fx_pf_feta_info",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgFetaInfoQuery",
            "client_doc_id": "11424838746690953787234584958",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _12_graph_rmd_access_token(self):
        # POST /rmd?access_token=567067343352427%7Cf249176f09e26ce54212b472dbab8fa8&rule_context=instagram_prod&net_iface=Unknown&reason=SESSION_CHANGE
        url = "https://graph.instagram.com/rmd?access_token=567067343352427%7Cf249176f09e26ce54212b472dbab8fa8&rule_context=instagram_prod&net_iface=Unknown&reason=SESSION_CHANGE"

        headers = {
            "priority": "u=3, i",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "rmd-mapfetcher",
            "x-fb-privacy-context": "4760009080727693",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","retry_attempt":"0"},"application_tags":"rmd"}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "54f57347883e321a3a22bd94ae5115ed",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _13_graphql_www_FxIgFetaInfoQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "11424838746690953787234584958",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgFetaInfoQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "fx_pf_feta_info",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgFetaInfoQuery",
            "client_doc_id": "11424838746690953787234584958",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _14_graphql_www_IGSharedAccountsQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "18737527476309823412641144201",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "IGSharedAccountsQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "me",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "afbc580454295d4ac0269d5ad49b796",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "IGSharedAccountsQuery",
            "client_doc_id": "18737527476309823412641144201",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _15_launcher_mobile_config(self):
        # POST /api/v1/launcher/mobileconfig/
        url = "https://b.i.instagram.com/api/v1/launcher/mobileconfig/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: launcher/mobileconfig/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.save-credentials",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::,com.bloks.www.caa.login.save-credentials:com.bloks.www.caa.login.save-credentials:3:button:1755922774.355::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922774.667",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "dcc71394a1e382782faa47d06a4cf183",
            "x-fb-http-engine": "MNS/TCP",
        }

        data = {
            "bool_opt_policy": "0",
            "mobileconfig": "",
            "api_version": "10",
            "unit_type": "2",
            "use_case": "STANDARD",
            "query_hash": "afbf25f577b10c6784e55995f46fac65b39623739edd37210e7b39e830c28026",
            "_uid": self._local_data.user_id,
            "device_id": self._local_data.device_id,
            "_uuid": self._local_data.device_id,
            "fetch_mode": "CONFIG_SYNC_ONLY",
            "fetch_type": "ASYNC_FULL",
            "request_data_query_hash": "afbf25f577b10c6784e55995f46fac65b39623739edd37210e7b39e830c28026",
        }

        payload = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _16_graphql_www_BasicAdsOptInQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "33052919472135518510885263591",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "BasicAdsOptInQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xfb_user_basic_ads_preferences",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "BasicAdsOptInQuery",
            "client_doc_id": "33052919472135518510885263591",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _17_graphql_www_AFSOptInQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "35850666251457231147855668495",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "AFSOptInQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "AFSStatusGraphQLWrapper",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "AFSOptInQuery",
            "client_doc_id": "35850666251457231147855668495",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _18_users_get_limited_interactions_reminder(self):
        # GET /api/v1/users/get_limited_interactions_reminder/?signed_body=SIGNATURE.%7B%7D
        url = "https://i.instagram.com/api/v1/users/get_limited_interactions_reminder/?signed_body=SIGNATURE.%7B%7D"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: users/get_limited_interactions_reminder/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922781.599",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _19_feed_timeline(self):
        # POST /api/v1/feed/timeline/
        url = "https://i.instagram.com/api/v1/feed/timeline/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=0",
            "x-ads-opt-out": "0",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-cm-bandwidth-kbps": "-1.000",
            "x-cm-latency": "31.676",
            "x-device-id": self._local_data.device_id,
            "x-fb": "1",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: feed/timeline/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"critical_api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-google-ad-id": self._local_data.google_ad_id,
            "x-ig-app-start-request": "1",
            "x-ig-accept-hint": "feed",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-salt-ids": "220140399,332020310,974466465,974460658",
            "x-ig-timezone-offset": "10800",
            "x-ig-transfer-encoding": "chunked",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922781.893",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        data = {
            "has_camera_permission": "0",
            "feed_view_info": "[]",
            "phone_id": self._local_data.family_device_id,
            "reason": "cold_start_fetch",
            "battery_level": "80",
            "timezone_offset": "10800",
            "client_recorded_request_time_ms": "1755922781725",
            "device_id": self._local_data.device_id,
            "request_id": "8140da9d-f1ef-4976-8c8c-e9c6ac66546b",
            "is_pull_to_refresh": "0",
            "_uuid": self._local_data.device_id,
            "push_disabled": "true",
            "is_charging": "1",
            "is_dark_mode": "0",
            "will_sound_on": "0",
            "session_id": "5b4f5e51-28a8-40ba-91e2-5a7b4addb3df",
            "bloks_versioning_id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
        }

        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _20_notifications_badge(self):
        # POST /api/v1/notifications/badge/
        url = "https://i.instagram.com/api/v1/notifications/badge/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: notifications/badge/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-salt-ids": "220140399,332020310,974466465,974460658",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922781.904",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        payload = {
            "phone_id": self._local_data.family_device_id,
            "trigger": "NOTIFICATION_FEED_HEART_ICON",
            "user_ids": self._local_data.user_id,
            "device_id": self._local_data.device_id,
            "_uuid": self._local_data.device_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _21_cdn_instagram(self):
        # GET /v/t51.2885-19/369590590_1045338860152910_5671089304644217155_n.jpg?efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-fra5-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QGq5Hn70enUih3gAXAUPgWM722qQt9-eswwtUmj56tU2EF7qurWWfg_LyzimX8AWfU&_nc_ohc=11MWwUm0Ow8Q7kNvwFG53jd&edm=AAAAAAABAAAA&ccb=7-5&oh=00_AfWL_g5jIvo2XAQnUfHK-SbGBIn4ZqIoCGwrDF0xB-nhfA&oe=68AEF94C&_nc_sid=328259
        url = "https://scontent-fra5-1.cdninstagram.com/v/t51.2885-19/369590590_1045338860152910_5671089304644217155_n.jpg?efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-fra5-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QGq5Hn70enUih3gAXAUPgWM722qQt9-eswwtUmj56tU2EF7qurWWfg_LyzimX8AWfU&_nc_ohc=11MWwUm0Ow8Q7kNvwFG53jd&edm=AAAAAAABAAAA&ccb=7-5&oh=00_AfWL_g5jIvo2XAQnUfHK-SbGBIn4ZqIoCGwrDF0xB-nhfA&oe=68AEF94C&_nc_sid=328259"

        headers = {
            "accept-language": "ru-RU, en-US",
            "priority": "u=2, i",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "ImageNodeUtils:image",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"ImageNodeUtils","request_category":"image","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "72fc470c373d95591d4f1a0172492ebd",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "fail=Server:NoUrlMap,Default:INVALID_MAP;v=;ip=;tkn=;reqTime=1819242338;recvTime=72",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _22_graphql_www_IGContentFilterDictionaryLookupQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "20527889283312263939147305606",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "IGContentFilterDictionaryLookupQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "ig_content_filter_dictionary_lookup_query",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "IGContentFilterDictionaryLookupQuery",
            "client_doc_id": "20527889283312263939147305606",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"service_ids":["MUTED_WORDS"],"languages":["nolang"]}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _23_graphql_query_GetResurrectedUserNUXEligibility(self):
        # POST /graphql/query
        url = "https://i.instagram.com/graphql/query"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "221788370615369272591224122891",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "GetResurrectedUserNUXEligibility",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xdt_async_should_show_resurrected_user_flow",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "GetResurrectedUserNUXEligibility",
            "client_doc_id": "221788370615369272591224122891",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"request_data":{"is_push_enabled":true,"dp_nux_eligible":true,"ci_nux_eligible":true}}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _24_cdn_instagram(self):
        # GET /v/t51.2885-19/369590590_1045338860152910_5671089304644217155_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-fra5-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QGq_UHLijoj4LwYn16JNSa264CUvLvnE3Anf9NCB6dZqY-w1obXMlPVnB0jl5BNuvg&_nc_ohc=11MWwUm0Ow8Q7kNvwFG53jd&edm=AAAAAAABAAAA&ccb=7-5&oh=00_AfVsIxZNLE7fKDRqT5ia24ekQOa2os8wfn3VuTjdzYBG8Q&oe=68AEF94C&_nc_sid=328259
        url = "https://scontent-fra5-1.cdninstagram.com/v/t51.2885-19/369590590_1045338860152910_5671089304644217155_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-fra5-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QGq_UHLijoj4LwYn16JNSa264CUvLvnE3Anf9NCB6dZqY-w1obXMlPVnB0jl5BNuvg&_nc_ohc=11MWwUm0Ow8Q7kNvwFG53jd&edm=AAAAAAABAAAA&ccb=7-5&oh=00_AfVsIxZNLE7fKDRqT5ia24ekQOa2os8wfn3VuTjdzYBG8Q&oe=68AEF94C&_nc_sid=328259"

        headers = {
            "accept-language": "ru-RU, en-US",
            "priority": "u=2, i, u=2, i",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "self_profile:image",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"self_profile","request_category":"image","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "72fc470c373d95591d4f1a0172492ebd",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _25_graphql_query_GetOnboardingNuxEligibility(self):
        # POST /graphql/query
        url = "https://i.instagram.com/graphql/query"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "222791017215896159003559603708",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "GetOnboardingNuxEligibility",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xdt_async_should_show_nux_flow",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "76cd0ea4f0283cc0fe0aea08a1be9034",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "GetOnboardingNuxEligibility",
            "client_doc_id": "222791017215896159003559603708",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"request_data":{"push_permission_requested":false,"ci_nux_eligible":true}}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _26_graphql_www_QuickPromotionSurfaceQueryV3(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "40925026811885364213860968489",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "QuickPromotionSurfaceQueryV3",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "ig_quick_promotion_batch_fetch_root",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        data = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "QuickPromotionSurfaceQueryV3",
            "client_doc_id": "40925026811885364213860968489",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"trigger_context":{"context_data_tuples":[]},"surface_triggers":[{"triggers":["app_foreground","session_start"],"surface_id":"INSTAGRAM_FOR_ANDROID_LOGIN_INTERSTITIAL_QP"}],"scale":3,"bloks_version":"382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21"}',
        }

        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _27_graphql_query_IGRealtimeRegionHintQuery(self):
        # POST /graphql/query
        url = "https://i.instagram.com/graphql/query"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "52232106018313849661757113193",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "IGRealtimeRegionHintQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xdt_igd_msg_region",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "IGRealtimeRegionHintQuery",
            "client_doc_id": "52232106018313849661757113193",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _28_graphql_www_IGPaginatedShareSheetQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "344505991810867181149711451826",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "IGPaginatedShareSheetQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "get_paginated_ig_share_sheet_ranking_query",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "f6113c138478937f683dbed9ca2a1a2",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        data = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "IGPaginatedShareSheetQuery",
            "client_doc_id": "344505991810867181149711451826",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"input":{"views":["reshare_share_sheet"],"ibc_share_sheet_params":{"size":3,"position":5},"page_max_id":null,"count_per_page":150}}',
        }

        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _29_banyan_banyan(self):
        # GET /api/v1/banyan/banyan/?is_private_share=false&views=%5B%22direct_user_search_keypressed%22%2C%22direct_user_search_nullstate%22%2C%22direct_inbox_active_now%22%2C%22call_recipients%22%5D&IBCShareSheetParams=%7B%22size%22%3A5%7D&is_real_time=false
        url = "https://i.instagram.com/api/v1/banyan/banyan/?is_private_share=false&views=%5B%22direct_user_search_keypressed%22%2C%22direct_user_search_nullstate%22%2C%22direct_inbox_active_now%22%2C%22call_recipients%22%5D&IBCShareSheetParams=%7B%22size%22%3A5%7D&is_real_time=false"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: banyan/banyan/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-salt-ids": "220140399,332020310",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922781.719",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "afbc580454295d4ac0269d5ad49b796",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _30_feed_reels_tray(self):
        # POST /api/v1/feed/reels_tray/
        url = "https://i.instagram.com/api/v1/feed/reels_tray/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=0",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: feed/reels_tray/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"critical_api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-salt-ids": "220140399,332020310,974466465,974460658",
            "x-ig-timezone-offset": "10800",
            "x-ig-transfer-encoding": "chunked",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-ig-app-start-time": "1755922718066",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922781.895",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        payload = {
            "reason": "cold_start",
            "timezone_offset": "10800",
            "tray_session_id": "0fce6b5f-5d08-453b-a84c-df8802b336f5",
            "request_id": "94c834e9-9b0a-4cb2-99eb-7c11571ba56f",
            "_uuid": self._local_data.device_id,
            "page_size": "50",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _31_cdn_instagram(self):
        # GET /v/t51.2885-19/520154130_17912822694155714_1860112374400904776_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-fra5-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QELvz31aeQCSX2NFWyiuLMLSQZ4JKT6eZjmGvtr6ZKeZP9wvXnHcf5QRvRIzAwr2Nk&_nc_ohc=QahHxr40m2sQ7kNvwGZcQhS&_nc_gid=gsSAndGBXIRhb-aw0D7CtQ&edm=ALlQn9MBAAAA&ccb=7-5&oh=00_AfWh5lO2c_YghWdsuIKyDrPpTUaGBPRAyjfLqOgkZCWaNA&oe=68AF2CEC&_nc_sid=e7f676
        url = "https://scontent-fra5-1.cdninstagram.com/v/t51.2885-19/520154130_17912822694155714_1860112374400904776_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-fra5-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QELvz31aeQCSX2NFWyiuLMLSQZ4JKT6eZjmGvtr6ZKeZP9wvXnHcf5QRvRIzAwr2Nk&_nc_ohc=QahHxr40m2sQ7kNvwGZcQhS&_nc_gid=gsSAndGBXIRhb-aw0D7CtQ&edm=ALlQn9MBAAAA&ccb=7-5&oh=00_AfWh5lO2c_YghWdsuIKyDrPpTUaGBPRAyjfLqOgkZCWaNA&oe=68AF2CEC&_nc_sid=e7f676"

        headers = {
            "accept-language": "ru-RU, en-US",
            "priority": "u=2, i",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "feed_timeline:image",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"feed_timeline","request_category":"image","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "72fc470c373d95591d4f1a0172492ebd",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _32_graphql_www_GenAINuxConsentStatusQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "22964137455619044644239243163",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "GenAINuxConsentStatusQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xfb_messenger_gen_ai_nux_consent_status_query",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "GenAINuxConsentStatusQuery",
            "client_doc_id": "22964137455619044644239243163",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _33_clips_discover_stream(self):
        # POST /api/v1/clips/discover/stream/
        url = "https://i.instagram.com/api/v1/clips/discover/stream/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: clips/discover/stream/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"clips_viewer_clips_tab","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-prefetch-request": "foreground",
            "x-ig-timezone-offset": "10800",
            "x-ig-transfer-encoding": "chunked",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.060",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        payload = {
            "seen_reels": "[]",
            "client_flashcache_size": "0",
            "enable_mixed_media_chaining": "true",
            "device_status": "{}",
            "should_refetch_chaining_media": "false",
            "_uuid": self._local_data.device_id,
            "prefetch_trigger_type": "cold_start",
            "viewer_session_id": "96d62f5f-ace3-4735-b61f-ccff4307888d",
            "server_driven_cache_config": '{"serve_from_server_cache":true,"cohort_to_ttl_map":"","serve_on_foreground_prefetch":"true","serve_on_background_prefetch":"true","meta":""}',
            "container_module": "clips_viewer_clips_tab",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _34_graphql_www_FxIgXavSwitcherBadgingDataQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "83794259218148585413504099631",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgXavSwitcherBadgingDataQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "switcher_accounts_data",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgXavSwitcherBadgingDataQuery",
            "client_doc_id": "83794259218148585413504099631",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"should_force_badge_refresh":false,"family_device_id":"","caller_name":"fx_company_identity_switcher"}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _35_graphql_www_FxIgLinkageCacheQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "11674382495679744485820947859",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgLinkageCacheQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xe_client_cache_accounts",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "645d19195b86907d2d6de6bf9bf6a5e6",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgLinkageCacheQuery",
            "client_doc_id": "11674382495679744485820947859",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"caller_name":"fx_product_foundation_client_FXOnline_client_cache"}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _36_graphql_www_FxIgXavSwitcherBadgingDataQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "83794259218148585413504099631",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgXavSwitcherBadgingDataQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "switcher_accounts_data",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "f6113c138478937f683dbed9ca2a1a2",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgXavSwitcherBadgingDataQuery",
            "client_doc_id": "83794259218148585413504099631",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"should_force_badge_refresh":false,"family_device_id":"","caller_name":"fx_company_identity_switcher"}',
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _37_feed_injected_reels_media(self):
        # POST /api/v1/feed/injected_reels_media/
        url = "https://i.instagram.com/api/v1/feed/injected_reels_media/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-ads-opt-out": "0",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-cm-bandwidth-kbps": "619.744",
            "x-cm-latency": "19.849",
            "x-device-id": self._local_data.device_id,
            "x-fb": "1",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: feed/injected_reels_media/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-google-ad-id": self._local_data.google_ad_id,
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.133",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        data = {
            "num_items_in_pool": "0",
            "has_camera_permission": "0",
            "is_ad_pod_enabled": "true",
            "is_prefetch": "true",
            "is_self_pog_chaining": "false",
            "is_inventory_based_request_enabled": "true",
            "is_refresh": "false",
            "is_media_based_insertion_enabled": "true",
            "phone_id": self._local_data.family_device_id,
            "is_ads_sensitive": "false",
            "entry_point_index": "0",
            "earliest_request_position": "0",
            "ad_request_index": "0",
            "battery_level": "80",
            "client_recorded_request_time_ms": "1755922784123",
            "tray_session_id": "66eb9e68-9942-4e50-8c0d-1746d3c103ed",
            "_uid": self._local_data.user_id,
            "is_carry_over_first_page": "false",
            "_uuid": self._local_data.device_id,
            "client_doc_id": "33469793811500731569328700797",
            "is_charging": "1",
            "is_async_prepare_enabled": "false",
            "reel_position": "0",
            "is_dark_mode": "0",
            "viewer_session_id": "66eb9e68-9942-4e50-8c0d-1746d3c103ed",
            "will_sound_on": "0",
            "container_module": "",
            "is_first_page": "true",
            "inserted_ad_indices": [],
            "inserted_netego_indices": [],
            "odml": {"story_prefetch_score": 0.12128931283950806},
            "tray_user_ids": [
                str(self._local_data.user_id),
                "4263859518",
                "67697508577",
                "64776963713",
                "3497714510",
                "181403753",
                "1538036112",
                "1727357981",
                "7210969523",
                "8173105297",
                "26564517793",
                "1289286502",
                "47678821853",
                "54317291503",
                "8201088492",
                "4541274901",
                "19978768704",
                "1491289929",
                "16097062",
                "61451570881",
                "49858156776",
                "50694735719",
                "2076950474",
                "61238184713",
                "270075132",
                "48401162912",
                "48903523637",
                "51403156044",
                "48073972154",
                "44187154693",
                "2001322713",
                "25707649255",
                "56671247996",
                "44176814630",
                "65456672099",
                "45485980480",
                "1539372892",
                "30495427",
                "34868778349",
                "44530901818",
                "4976792623",
                "2325751068",
                "44528813038",
                "5820159345",
                "30109797",
                "38902754",
                "64751068183",
                "30086311348",
                "2685309700",
                "60538971992",
                "3284915195",
                "4810064195",
                "21459335533",
                "55057895145",
                "3257299",
                "1585739799",
                "43586820065",
                "48657472317",
                "58752056547",
                "16104906222",
                "49071564381",
                "51795275335",
                "47706480045",
                "71073373538",
                "63290153052",
                "1518581294",
                "46152006203",
                "16706442481",
                "55788839181",
                "2370291410",
                "46295429913",
                "50210614710",
                "21976029772",
                "3966267013",
                "1546101748",
                "12575702157",
                "44912132796",
                "25477487802",
                "54255381572",
                "55202968597",
                "47482526223",
                "5723529025",
                "50347464211",
                "47397369171",
                "4298587588",
                "45613301226",
                "17194366678",
                "44448365682",
                "2059015970",
                "44654597503",
                "5923988073",
                "1571056342",
                "6762912768",
                "1938896920",
                "51307021402",
                "29123073107",
                "54153675563",
                "10320989777",
                "1292044376",
                "60316266790",
                "59183665447",
                "48720124420",
                "56798635732",
                "31452800",
                "44566221660",
                "36729733437",
                "72938311377",
                "55527822148",
                "10847340282",
                "27427350193",
                "52676330232",
                "58656316691",
                "56662576653",
                "47229432389",
                "44200374425",
                "61941425839",
                "26825075115",
                "59154260241",
                "46700665711",
                "52051084095",
                "39747881267",
                "56503527508",
                "9299074202",
                "4397702959",
                "6081310161",
                "3656852613",
                "53125363",
                "55354005213",
                "32563888819",
                "51575265426",
                "8327011518",
                "48928198102",
                "2044967924",
                "24004222992",
                "12378346374",
                "39565909372",
                "70666175392",
                "6904685032",
                "8744125484",
                "6250216367",
                "48310808010",
                "53597618034",
                "64780600662",
                "47734613158",
                "12294046086",
                "60904195215",
                "5701454840",
                "701243118",
                "5740075657",
                "43026101327",
                "6101979832",
            ],
            "ad_and_netego_request_information": [],
        }

        data = build_signed_body(dumps_orjson(data))

        payload = gzip.compress(data.encode("utf-8"))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _38_cdn_instagram(self):
        # GET /v/t51.2885-19/502054156_17889102447260578_6681353768532498114_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDI0LmMyIn0&_nc_ht=scontent-fra3-2.cdninstagram.com&_nc_cat=1&_nc_oc=Q6cZ2QELvz31aeQCSX2NFWyiuLMLSQZ4JKT6eZjmGvtr6ZKeZP9wvXnHcf5QRvRIzAwr2Nk&_nc_ohc=Q8eGVcgsPcoQ7kNvwEuhlyU&_nc_gid=gsSAndGBXIRhb-aw0D7CtQ&edm=ALlQn9MBAAAA&ccb=7-5&oh=00_AfW04Wne0oiSYGbqSO0eHu_lvYCl5gMB1dWf5anVKg9wOw&oe=68AF02E1&_nc_sid=e7f676
        url = "https://scontent-fra3-2.cdninstagram.com/v/t51.2885-19/502054156_17889102447260578_6681353768532498114_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDI0LmMyIn0&_nc_ht=scontent-fra3-2.cdninstagram.com&_nc_cat=1&_nc_oc=Q6cZ2QELvz31aeQCSX2NFWyiuLMLSQZ4JKT6eZjmGvtr6ZKeZP9wvXnHcf5QRvRIzAwr2Nk&_nc_ohc=Q8eGVcgsPcoQ7kNvwEuhlyU&_nc_gid=gsSAndGBXIRhb-aw0D7CtQ&edm=ALlQn9MBAAAA&ccb=7-5&oh=00_AfW04Wne0oiSYGbqSO0eHu_lvYCl5gMB1dWf5anVKg9wOw&oe=68AF02E1&_nc_sid=e7f676"

        headers = {
            "accept-language": "ru-RU, en-US",
            "priority": "u=2, i, u=2, i",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "feed_timeline:image",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"feed_timeline","request_category":"image","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "82e8c7e39c6162e37608e7d7581e1fdc",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _39_creatives_write_supported_capabilities(self):
        # POST /api/v1/creatives/write_supported_capabilities/
        url = "https://i.instagram.com/api/v1/creatives/write_supported_capabilities/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: creatives/write_supported_capabilities/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.025",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "76cd0ea4f0283cc0fe0aea08a1be9034",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        data = {
            "supported_capabilities_new": '[{"name":"SUPPORTED_SDK_VERSIONS","value":"149.0,150.0,151.0,152.0,153.0,154.0,155.0,156.0,157.0,158.0,159.0,160.0,161.0,162.0,163.0,164.0,165.0,166.0,167.0,168.0,169.0,170.0,171.0,172.0,173.0,174.0,175.0,176.0,177.0,178.0,179.0,180.0,181.0,182.0,183.0,184.0,185.0,186.0,187.0,188.0,189.0,190.0,191.0"},{"name":"SUPPORTED_BETA_SDK_VERSIONS","value":"182.0-beta,183.0-beta,184.0-beta,185.0-beta,186.0-beta,187.0-beta,188.0-beta,189.0-beta,190.0-beta,191.0-beta,192.0-beta,193.0-beta,194.0-beta,195.0-beta,196.0-beta,197.0-beta,198.0-beta,199.0-beta,200.0-beta,201.0-beta"},{"name":"FACE_TRACKER_VERSION","value":"14"},{"name":"segmentation","value":"segmentation_enabled"},{"name":"COMPRESSION","value":"ETC2_COMPRESSION"},{"name":"world_tracker","value":"world_tracker_enabled"},{"name":"gyroscope","value":"gyroscope_enabled"}]',
            "_uid": self._local_data.user_id,
            "_uuid": self._local_data.device_id,
        }

        payload = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _40_cdn_instagram(self):
        # GET /v/t51.2885-19/485956858_512896371632178_161747111791640351_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby43NjguYzIifQ&_nc_ht=scontent-fra5-2.cdninstagram.com&_nc_cat=106&_nc_oc=Q6cZ2QELvz31aeQCSX2NFWyiuLMLSQZ4JKT6eZjmGvtr6ZKeZP9wvXnHcf5QRvRIzAwr2Nk&_nc_ohc=MniSmLoebf4Q7kNvwEhT4hh&_nc_gid=gsSAndGBXIRhb-aw0D7CtQ&edm=ALlQn9MBAAAA&ccb=7-5&oh=00_AfX7toC7b9qDOCZf2SFEIQiBylOf-Yry8INU_X6udEmy4Q&oe=68AF17A5&_nc_sid=e7f676
        url = "https://scontent-fra5-2.cdninstagram.com/v/t51.2885-19/485956858_512896371632178_161747111791640351_n.jpg?stp=dst-jpg_e0_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby43NjguYzIifQ&_nc_ht=scontent-fra5-2.cdninstagram.com&_nc_cat=106&_nc_oc=Q6cZ2QELvz31aeQCSX2NFWyiuLMLSQZ4JKT6eZjmGvtr6ZKeZP9wvXnHcf5QRvRIzAwr2Nk&_nc_ohc=MniSmLoebf4Q7kNvwEhT4hh&_nc_gid=gsSAndGBXIRhb-aw0D7CtQ&edm=ALlQn9MBAAAA&ccb=7-5&oh=00_AfX7toC7b9qDOCZf2SFEIQiBylOf-Yry8INU_X6udEmy4Q&oe=68AF17A5&_nc_sid=e7f676"

        headers = {
            "accept-language": "ru-RU, en-US",
            "priority": "u=2, i, u=2, i",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "feed_timeline:image",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"feed_timeline","request_category":"image","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "f7310e01a53700966482808eab61bc26",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _41_graphql_www_IGFXAccessLibrarySSOAndRegFlagQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "2245869636858707557133739912",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "IGFXAccessLibrarySSOAndRegFlagQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "fx_waffle_wfs_and_nta_eligibility",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "IGFXAccessLibrarySSOAndRegFlagQuery",
            "client_doc_id": "2245869636858707557133739912",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _42_notifications_store_client_push_permissions(self):
        # POST /api/v1/notifications/store_client_push_permissions/
        url = "https://i.instagram.com/api/v1/notifications/store_client_push_permissions/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: notifications/store_client_push_permissions/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.692",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        payload = {
            "enabled": "false",
            "device_id": self._local_data.device_id,
            "_uuid": self._local_data.device_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _43_users_user_info(self):
        # GET /api/v1/users/.../info/
        url = f"https://i.instagram.com/api/v1/users/{self._local_data.user_id}/info/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": f"IgApi: users/{self._local_data.user_id}/info/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922783.988",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "afbc580454295d4ac0269d5ad49b796",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _44_graphql_www_ZeroDayLanguageSignalUpload(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "421504111017775862006551019971",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "ZeroDayLanguageSignalUpload",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xfb_post_new_user_day_zero_language_signal",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        data = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "ZeroDayLanguageSignalUpload",
            "client_doc_id": "421504111017775862006551019971",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"input_methods":[{"name":"com.samsung.android.honeyboard/.service.HoneyBoardService","languages":[{"locale":"en_us","display_name":"English (US)"},{"locale":"ru","display_name":"Русский"}]}],"current_language":{"locale":"en_us","display_name":"English (US)"}}',
        }

        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _45_graphql_www_HasAvatarQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "176575339113814643398381488942",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "HasAvatarQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "viewer",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "645d19195b86907d2d6de6bf9bf6a5e6",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "HasAvatarQuery",
            "client_doc_id": "176575339113814643398381488942",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _46_graphql_www_IGFxLinkedAccountsQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "43230821013683556483393399494",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "IGFxLinkedAccountsQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "fx_linked_accounts",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "f6113c138478937f683dbed9ca2a1a2",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "IGFxLinkedAccountsQuery",
            "client_doc_id": "43230821013683556483393399494",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _47_clips_user_share_to_fb_config(self):
        # GET /api/v1/clips/user/share_to_fb_config/?device_status=%7B%22hw_av1_dec%22%3Afalse%2C%22hw_vp9_dec%22%3Atrue%2C%22hw_avc_dec%22%3Atrue%2C%2210bit_hw_av1_dec%22%3Afalse%2C%2210bit_hw_vp9_dec%22%3Afalse%2C%22is_hlg_supported%22%3Afalse%2C%22chip_vendor%22%3A%22mediatek%22%2C%22chip_name%22%3A%22mt6789v%5C%2Fcd%22%2C%22core_count%22%3A8%2C%22max_ghz_sum%22%3A16.4%2C%22min_ghz_sum%22%3A4.45%7D
        url = "https://i.instagram.com/api/v1/clips/user/share_to_fb_config/?device_status=%7B%22hw_av1_dec%22%3Afalse%2C%22hw_vp9_dec%22%3Atrue%2C%22hw_avc_dec%22%3Atrue%2C%2210bit_hw_av1_dec%22%3Afalse%2C%2210bit_hw_vp9_dec%22%3Afalse%2C%22is_hlg_supported%22%3Afalse%2C%22chip_vendor%22%3A%22mediatek%22%2C%22chip_name%22%3A%22mt6789v%5C%2Fcd%22%2C%22core_count%22%3A8%2C%22max_ghz_sum%22%3A16.4%2C%22min_ghz_sum%22%3A4.45%7D"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: clips/user/share_to_fb_config/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.832",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _48_graphql_www_CrosspostingUnifiedConfigsQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "216179630710424327622729278241",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "CrosspostingUnifiedConfigsQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xcxp_unified_crossposting_configs_root",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        data = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "CrosspostingUnifiedConfigsQuery",
            "client_doc_id": "216179630710424327622729278241",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"configs_request":{"source_app":"IG","crosspost_app_surface_list":[{"source_surface":"STORY","destination_surface":"STORY","destination_app":"FB"},{"source_surface":"FEED","destination_surface":"FEED","destination_app":"FB"},{"source_surface":"REELS","destination_surface":"REELS","destination_app":"FB"}]}}',
        }
        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _49_graphql_www_FxIgConnectedServicesInfoQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "2163151994804975974238986080",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "FxIgConnectedServicesInfoQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "fx_service_cache",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "afbc580454295d4ac0269d5ad49b796",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        data = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "FxIgConnectedServicesInfoQuery",
            "client_doc_id": "2163151994804975974238986080",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"service_names":["CROSS_POSTING_SETTING"],"custom_partner_params":[{"value":"FB","key":"CROSSPOSTING_DESTINATION_APP"},{"value":"","key":"CROSSPOSTING_SHARE_TO_SURFACE"},{"value":"true","key":"OVERRIDE_USER_VALIDATION_WITH_CXP_ELIGIBILITY_RULE"}],"client_caller_name":"ig_android_service_cache_crossposting_setting","caller_name":"fx_product_foundation_client_FXOnline_client_cache"}',
        }
        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _50_direct_v2_inbox(self):
        # GET /api/v1/direct_v2/inbox/?visual_message_return_type=unseen&igd_request_log_tracking_id=7dd6e8e8-8f9e-4006-83c4-2897cc347448&no_pending_badge=true&thread_message_limit=5&persistentBadging=true&limit=15&push_disabled=true&is_prefetching=false&fetch_reason=initial_snapshot
        url = "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&igd_request_log_tracking_id=7dd6e8e8-8f9e-4006-83c4-2897cc347448&no_pending_badge=true&thread_message_limit=5&persistentBadging=true&limit=15&push_disabled=true&is_prefetching=false&fetch_reason=initial_snapshot"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: direct_v2/inbox/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.042",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _51_graphql_www_SyncCXPNoticeStateMutation(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-encoding": "gzip",
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "14088097634272511800572157181",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "SyncCXPNoticeStateMutation",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xcxp_sync_notice_state",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "76cd0ea4f0283cc0fe0aea08a1be9034",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        data = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "SyncCXPNoticeStateMutation",
            "client_doc_id": "14088097634272511800572157181",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": '{"client_states":[{"variant":"BOTTOMSHEET_AUDIENCE_CHANGE_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_MIGRATION_FEED_WAVE2","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_MIGRATION_STORIES_WAVE2","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_REEL_CCP_MIGRATION_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_REEL_CCP_MIGRATION_STORY","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_STORY_REEL_CCP_MIGRATION_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_FEED_REEL_CCP_MIGRATION_STORY","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_UNIFIED_STORIES_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_UNLINKED_USER_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"BOTTOMSHEET_XAR_REELS","sequence_number":2,"last_impression_time":0,"impression_count":0},{"variant":"DIALOG_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"DIALOG_STORY","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"TOOLTIP_AUTOSHARE_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"TOOLTIP_CURRENTLY_SHARING_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"TOOLTIP_NUX_STORIES","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"TOOLTIP_PAGE_SHARE_FEED","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"TOOLTIP_SHORTCUT_DESTINATION_PICKER_NOT_SHARING_STORIES","sequence_number":0,"last_impression_time":0,"impression_count":0},{"variant":"TOOLTIP_SHORTCUT_DESTINATION_PICKER_STORIES","sequence_number":0,"last_impression_time":1755922784,"impression_count":0},{"variant":"BOTTOMSHEET_CCP_REELS_THREADS_FIRST_TOGGLE_CLICK","sequence_number":0,"last_impression_time":0,"impression_count":0}]}',
        }

        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _52_android_modules_download(self):
        # POST /api/v1/android_modules/download/
        url = "https://i.instagram.com/api/v1/android_modules/download/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: android_modules/download/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"prefetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.087",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "51b42699f6113591f61319c08053bc4f",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        data = {
            "_uid": self._local_data.user_id,
            "_uuid": self._local_data.device_id,
            "hashes": [
                "50b2a8f3ac5fec83e70988463fb695adb29d10e9fef26d61724ff39bebf5b6e9",
                "59508dd222b8bb6a0af90331f016f9632f8147c91a2a6767dfb36d504a0f7679",
            ],
        }

        payload = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _53_accounts_ge_presence_disabled(self):
        # GET /api/v1/workers/get_presence_disabled/?signed_body=SIGNATURE.%7B%7D
        url = "https://i.instagram.com/api/v1/accounts/get_presence_disabled/?signed_body=SIGNATURE.%7B%7D"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: workers/get_presence_disabled/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.989",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _54_direct_v2_has_interop_upgraded(self):
        # GET /api/v1/direct_v2/has_interop_upgraded/
        url = "https://i.instagram.com/api/v1/direct_v2/has_interop_upgraded/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: direct_v2/has_interop_upgraded/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.007",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "645d19195b86907d2d6de6bf9bf6a5e6",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _55_direct_v2_async_get_pending_requests_preview(self):
        # GET /api/v1/direct_v2/async_get_pending_requests_preview/?pending_inbox_filters=%5B%5D
        url = "https://i.instagram.com/api/v1/direct_v2/async_get_pending_requests_preview/?pending_inbox_filters=%5B%5D"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: direct_v2/async_get_pending_requests_preview/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.037",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "afbc580454295d4ac0269d5ad49b796",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _56_direct_v2_get_presence(self):
        # GET /api/v1/direct_v2/get_presence/?suggested_followers_limit=100
        url = "https://i.instagram.com/api/v1/direct_v2/get_presence/?suggested_followers_limit=100"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: direct_v2/get_presence/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922784.977",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "f6113c138478937f683dbed9ca2a1a2",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _57_notifications_badge(self):
        # POST /api/v1/notifications/badge/
        url = "https://i.instagram.com/api/v1/notifications/badge/"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: notifications/badge/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.235",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        payload = {
            "phone_id": self._local_data.family_device_id,
            "trigger": "NOTIFICATION_FEED_HEART_ICON",
            "user_ids": self._local_data.user_id,
            "device_id": self._local_data.device_id,
            "_uuid": self._local_data.device_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)

    async def _58_direct_v2_async_get_pending_requests_preview(self):
        # GET /api/v1/direct_v2/async_get_pending_requests_preview/?pending_inbox_filters=%5B%5D
        url = "https://i.instagram.com/api/v1/direct_v2/async_get_pending_requests_preview/?pending_inbox_filters=%5B%5D"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: direct_v2/async_get_pending_requests_preview/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.406",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "645d19195b86907d2d6de6bf9bf6a5e6",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _59_direct_v2_inbox(self):
        # GET /api/v1/direct_v2/inbox/?visual_message_return_type=unseen&igd_request_log_tracking_id=7dd6e8e8-8f9e-4006-83c4-2897cc347448&no_pending_badge=true&thread_message_limit=5&persistentBadging=true&limit=15&push_disabled=true&is_prefetching=false&fetch_reason=initial_snapshot
        url = "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&igd_request_log_tracking_id=7dd6e8e8-8f9e-4006-83c4-2897cc347448&no_pending_badge=true&thread_message_limit=5&persistentBadging=true&limit=15&push_disabled=true&is_prefetching=false&fetch_reason=initial_snapshot"

        headers = {
            "accept-language": "ru-RU, en-US",
            "authorization": str(self._local_data.authorization),
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-ax-base-colors-enabled": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: direct_v2/inbox/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": str(self._local_data.android_id),
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "ru_RU",
            "x-ig-bandwidth-speed-kbps": "619.000",
            "x-ig-bandwidth-totalbytes-b": "252236",
            "x-ig-bandwidth-totaltime-ms": "407",
            "x-ig-client-endpoint": "feed_timeline",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-device-languages": '{"system_languages":"ru-RU","keyboard_language":"en-US"}',
            "x-ig-device-locale": "ru_RU",
            "x-ig-family-device-id": self._local_data.family_device_id,
            "x-ig-mapped-locale": "ru_RU",
            "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            "x-ig-timezone-offset": "10800",
            "x-ig-www-claim": "hmac.AR1RJENg5yBy3KaeiJJxOF4iF8xuVgf6DoNSrwUYRKi7APBL",
            "x-mid": str(self._local_data.mid),
            "x-pigeon-rawclienttime": "1755922785.086",
            "x-pigeon-session-id": "UFS-8e93b583-37f6-4c54-b740-92a39d02287e-0",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "76cd0ea4f0283cc0fe0aea08a1be9034",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        await self._request_handler(request)

    async def _60_graphql_www_CXPFbStoriesCurrentPrivacyQuery(self):
        # POST /graphql_www
        url = "https://i.instagram.com/graphql_www"

        headers = {
            "authorization": str(self._local_data.authorization),
            "content-type": "application/x-www-form-urlencoded",
            "ig-intended-user-id": str(self._local_data.user_id),
            "ig-u-ds-user-id": str(self._local_data.user_id),
            "ig-u-rur": str(self._local_data.rur),
            "priority": "u=3, i",
            "x-client-doc-id": "320625293115518493869044192773",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "CXPFbStoriesCurrentPrivacyQuery",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-app-id": "567067343352427",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-device-id": str(self._local_data.device_id),
            "x-ig-validate-null-in-legacy-dict": "true",
            "x-mid": str(self._local_data.mid),
            "x-root-field-name": "xcxp_fb_stories_current_privacy",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)",
            "x-fb-conn-uuid-client": "a4ff90dbde7f8fd2cc0ecf7278d30b7c",
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
            "x-graphql-client-library": "pando",
        }

        payload = {
            "method": "post",
            "pretty": "false",
            "format": "json",
            "server_timestamps": "true",
            "locale": "user",
            "fb_api_req_friendly_name": "CXPFbStoriesCurrentPrivacyQuery",
            "client_doc_id": "320625293115518493869044192773",
            "enable_canonical_naming": "true",
            "enable_canonical_variable_overrides": "true",
            "enable_canonical_naming_ambiguous_type_prefixing": "true",
            "variables": "{}",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
        )

        await self._request_handler(request)
