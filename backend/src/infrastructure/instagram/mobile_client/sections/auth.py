from uuid import uuid4

from yarl import URL

from src.domain.shared.interfaces.instagram.entities.challenge import ChallengeData
from src.domain.shared.interfaces.instagram.exceptions import (
    AuthorizationError,
    ChallengeRequired,
    InstagramError,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.utils import generate_waterfall_id
from src.infrastructure.instagram.bloks_utils.response_parsers import (
    ChallengeRequiredLoginResult,
    SuccessLoginResult,
    TwoStepVerificationRequiredLoginResult,
    UnknownLoginResult,
    parse_bloks_login_response,
)
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.password_encrypter import PasswordEncrypter
from src.infrastructure.instagram.common.utils import dumps_orjson
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState
from src.infrastructure.instagram.mobile_client.utils.extractors import (
    extract_data_from_authorization,
)


class AuthSection:

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

    async def login(self, username: str, password: str):
        self._state.local_data.clear_authorization_data()
        self._state.local_data.set_rur(None)
        self._state.local_data.set_www_claim(None)
        self._state.local_data.set_waterfall_id(generate_waterfall_id())

        await self.send_requests_before_login()

        await self._login(username, password)

        await self.send_requests_after_success_login()

    async def _login(self, username: str, password: str):
        if self._state.local_data.public_key and self._state.local_data.public_key_id:
            enc_password = PasswordEncrypter.encrypt_v4(
                password,
                self._state.local_data.public_key_id,
                self._state.local_data.public_key,
            )
        else:
            enc_password = PasswordEncrypter.encrypt_v0(
                password,
            )

        login_attempt_count = 0
        params = {
            "client_input_params": {
                "sim_phones": [],
                "aymh_accounts": [],
                "secure_family_device_id": "",
                "has_granted_read_contacts_permissions": 0,
                "auth_secure_device_id": "",
                "has_whatsapp_installed": 0,
                "password": enc_password,
                "sso_token_map_json_string": "",
                "block_store_machine_id": "",
                "ig_vetted_device_nonces": "",
                "cloud_trust_token": None,
                "event_flow": "login_manual",
                "password_contains_non_ascii": "false",
                "client_known_key_hash": "",
                "encrypted_msisdn": "",
                "has_granted_read_phone_permissions": 0,
                "app_manager_id": "",
                "should_show_nested_nta_from_aymh": 1,
                "device_id": self._local_data.android_id,
                "login_attempt_count": login_attempt_count,
                "machine_id": self._local_data.mid,
                "flash_call_permission_status": {
                    "READ_PHONE_STATE": "DENIED",
                    "READ_CALL_LOG": "DENIED",
                    "ANSWER_PHONE_CALLS": "DENIED",
                },
                "accounts_list": [],
                "family_device_id": self._local_data.family_device_id,
                "fb_ig_device_id": [],
                "device_emails": [],
                "try_num": 1,
                "lois_settings": {"lois_token": ""},
                "event_step": "home_page",
                "headers_infra_flow_id": "",
                "openid_tokens": {},
                "contact_point": username,
            },
            "server_params": {
                "should_trigger_override_login_2fa_action": 0,
                "is_vanilla_password_page_empty_password": 0,
                "is_from_logged_out": 0,
                "should_trigger_override_login_success_action": 0,
                "login_credential_type": "none",
                "server_login_source": "login",
                "waterfall_id": self._local_data.waterfall_id,
                "two_step_login_type": "one_step_login",
                "login_source": "Login",
                "is_platform_login": 0,
                "INTERNAL__latency_qpl_marker_id": 36707139,
                "is_from_aymh": 0,
                "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
                "is_from_landing_page": 0,
                "password_text_input_id": "hqg4g8:68",
                # // came from last request https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.caa.login.login_homepage/ HTTP/2.0
                "is_from_empty_password": 0,
                "is_from_msplit_fallback": 0,
                "ar_event_source": "login_home_page",
                "qe_device_id": self._local_data.device_id,
                "username_text_input_id": "hqg4g8:67",
                # // came from last request https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.caa.login.login_homepage/
                "layered_homepage_experiment_group": "Deploy: Not in Experiment",
                "device_id": self._local_data.android_id,
                "INTERNAL__latency_qpl_instance_id": 107234727200302.0,
                # // came from last request (#1xxbjgdl96, 36707139, 197267722000072, \"com.bloks.www.caa.login.cp_text_input_t
                "reg_flow_source": "aymh_single_profile_native_integration_point",
                "is_caa_perf_enabled": 1,
                "credential_type": "password",
                "is_from_password_entry_page": 0,
                "caller": "gslr",
                "family_device_id": self._local_data.family_device_id,
                "is_from_assistive_id": 0,
                "access_flow_version": "pre_mt_behavior",
                "is_from_logged_in_switcher": 0,
            },
        }
        bk_client_context = {
            "bloks_version": self._version_info.bloks_version_id,
            "styles_id": "instagram",
        }

        data = {
            "params": dumps_orjson(params),
            "bk_client_context": dumps_orjson(bk_client_context),
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        uri = constants.BLOKS_SEND_LOGIN_REQUEST_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                # "X-Ig-Nav-Chain": f"com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:{timestamp_with_ms_str()}::",  # FIXME строится на группы запросов, а не на 1 запрос
                "Priority": "u=3",
                "X-Bloks-Prism-Button-Version": "CONTROL",
            }
        )

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        response = await self._request_handler(request)
        if not response.get("status") == "ok":
            raise AuthorizationError(message=str(response))

        login_result = parse_bloks_login_response(response)
        if isinstance(login_result, SuccessLoginResult):
            login_response_data = login_result.login_response_data
            self._update_local_data_from_login_response_data(login_response_data)
            await self.logger.info(f"Сессия после авторизации: {self._local_data}")
            return True

        elif isinstance(login_result, ChallengeRequiredLoginResult):
            raise ChallengeRequired(challenge_data=login_result.challenge_data)
        elif isinstance(login_result, TwoStepVerificationRequiredLoginResult):
            raise InstagramError(message=f"Инстаграм требует принять код с почты")
        elif isinstance(login_result, UnknownLoginResult):
            raise InstagramError(message=f"Неизвестная ошибка авторизации:  {login_result.response}")

    async def _zr_dual_tokens(self):
        uri = constants.ZR_DUAL_TOKENS_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
            }
        )

        data = {
            "normal_token_hash": "",
            "device_id": self._local_data.android_id,
            "custom_device_id": self._local_data.device_id,
            "fetch_reason": "token_expired",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        await self._request_handler(request)

    async def _create_android_keystore(self, key_hash: str | None = None):
        uri = constants.ATTESTATION_CREATE_ANDROID_KEYSTORE_URI
        url = URL(constants.INSTAGRAM_API_B_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
            }
        )

        data = {
            "app_scoped_device_id": self._local_data.device_id,
            "key_hash": key_hash
            or "",  # В оригинале тут либо пустая строка либо хеш "6c2539295e19c116959b66e0ed14c2901767f4fcac4a788dfe2f6f182138065c"
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        return await self._request_handler(request)

    async def _process_client_data_and_redirect(self):
        uri = constants.BLOKS_PROCESS_CLIENT_DATA_AND_REDIRECT_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                "Priority": "u=3",
            }
        )

        data = {
            "params": dumps_orjson(
                {
                    "is_from_logged_out": False,
                    "logged_out_user": "",
                    "qpl_join_id": str(uuid4()),
                    "family_device_id": False,
                    "device_id": self._local_data.android_id,
                    "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
                    "waterfall_id": self._local_data.waterfall_id,
                    "logout_source": "",
                    "show_internal_settings": False,
                    "last_auto_login_time": 0,
                    "disable_auto_login": False,
                    "qe_device_id": self._local_data.device_id,
                    "is_from_logged_in_switcher": False,
                    "switcher_logged_in_uid": "",
                    "account_list": [],
                    "blocked_uid": [],
                    "INTERNAL_INFRA_THEME": "THREE_C",
                    "launched_url": "",
                    "sim_phone_numbers": [],
                    "is_from_registration_reminder": False,
                }
            ),
            "bk_client_context": dumps_orjson(
                {
                    "bloks_version": self._version_info.bloks_version_id,
                    "styles_id": "instagram",
                }
            ),
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        await self._request_handler(request)

    async def _youth_regulation_delete_pregent(self):
        uri = constants.BLOKS_YOUTH_REGULATION_DELETE_PREGENT_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                "Priority": "u=3",
            }
        )

        data = {
            "params": dumps_orjson(
                {
                    "client_input_params": {"lois_settings": {"lois_token": ""}},
                    "server_params": {
                        "is_from_logged_out": 0,
                        "layered_homepage_experiment_group": None,
                        "device_id": self._local_data.android_id,
                        "waterfall_id": self._local_data.waterfall_id,
                        "INTERNAL__latency_qpl_instance_id": 105559132700037.0,  # TODO понять откуда его брать или просто генерить и поменять везде
                        "flow_info": dumps_orjson(
                            {
                                "flow_name": "new_to_family_ig_youth_reg",
                                "flow_type": "ntf",
                            }
                        ),
                        "is_platform_login": 0,
                        "INTERNAL__latency_qpl_marker_id": self._version_info.qpl_marker_id,
                        "reg_info": dumps_orjson(
                            {
                                "first_name": None,
                                "last_name": None,
                                "full_name": None,
                                "contactpoint": None,
                                "ar_contactpoint": None,
                                "contactpoint_type": None,
                                "is_using_unified_cp": None,
                                "unified_cp_screen_variant": None,
                                "is_cp_auto_confirmed": False,
                                "is_cp_auto_confirmable": False,
                                "confirmation_code": None,
                                "birthday": None,
                                "birthday_derived_from_age": None,
                                "did_use_age": None,
                                "gender": None,
                                "use_custom_gender": None,
                                "custom_gender": None,
                                "encrypted_password": None,
                                "username": None,
                                "username_prefill": None,
                                "fb_conf_source": None,
                                "device_id": None,
                                "ig4a_qe_device_id": None,
                                "family_device_id": None,
                                "user_id": None,
                                "safetynet_token": None,
                                "safetynet_response": None,
                                "machine_id": None,
                                "profile_photo": None,
                                "profile_photo_id": None,
                                "profile_photo_upload_id": None,
                                "avatar": None,
                                "email_oauth_token_no_contact_perm": None,
                                "email_oauth_token": None,
                                "email_oauth_tokens": None,
                                "should_skip_two_step_conf": None,
                                "openid_tokens_for_testing": None,
                                "encrypted_msisdn": None,
                                "encrypted_msisdn_for_safetynet": None,
                                "cached_headers_safetynet_info": None,
                                "should_skip_headers_safetynet": None,
                                "headers_last_infra_flow_id": None,
                                "headers_last_infra_flow_id_safetynet": None,
                                "headers_flow_id": None,
                                "was_headers_prefill_available": None,
                                "sso_enabled": None,
                                "existing_accounts": None,
                                "used_ig_birthday": None,
                                "sync_info": None,
                                "create_new_to_app_account": None,
                                "skip_session_info": None,
                                "ck_error": None,
                                "ck_id": None,
                                "ck_nonce": None,
                                "should_save_password": None,
                                "horizon_synced_username": None,
                                "fb_access_token": None,
                                "horizon_synced_profile_pic": None,
                                "is_identity_synced": False,
                                "is_msplit_reg": None,
                                "is_spectra_reg": None,
                                "spectra_reg_token": None,
                                "spectra_reg_guardian_id": None,
                                "user_id_of_msplit_creator": None,
                                "msplit_creator_nonce": None,
                                "dma_data_combination_consent_given": None,
                                "xapp_accounts": None,
                                "fb_device_id": None,
                                "fb_machine_id": None,
                                "ig_device_id": None,
                                "ig_machine_id": None,
                                "should_skip_nta_upsell": None,
                                "big_blue_token": None,
                                "skip_sync_step_nta": None,
                                "caa_reg_flow_source": None,
                                "ig_authorization_token": None,
                                "full_sheet_flow": False,
                                "crypted_user_id": None,
                                "is_caa_perf_enabled": False,
                                "is_preform": True,
                                "ignore_suma_check": False,
                                "dismissed_login_upsell_with_cna": False,
                                "ignore_existing_login": False,
                                "ignore_existing_login_from_suma": False,
                                "ignore_existing_login_after_errors": False,
                                "suggested_first_name": None,
                                "suggested_last_name": None,
                                "suggested_full_name": None,
                                "frl_authorization_token": None,
                                "post_form_errors": None,
                                "skip_step_without_errors": False,
                                "existing_account_exact_match_checked": False,
                                "existing_account_fuzzy_match_checked": False,
                                "email_oauth_exists": False,
                                "confirmation_code_send_error": None,
                                "is_too_young": False,
                                "source_account_type": None,
                                "whatsapp_installed_on_client": False,
                                "confirmation_medium": None,
                                "source_credentials_type": None,
                                "source_cuid": None,
                                "source_account_reg_info": None,
                                "soap_creation_source": None,
                                "source_account_type_to_reg_info": None,
                                "registration_flow_id": "",
                                "should_skip_youth_tos": False,
                                "is_youth_regulation_flow_complete": False,
                                "is_on_cold_start": False,
                                "email_prefilled": False,
                                "cp_confirmed_by_auto_conf": False,
                                "auto_conf_info": None,
                                "in_sowa_experiment": False,
                                "youth_regulation_config": None,
                                "conf_allow_back_nav_after_change_cp": None,
                                "conf_bouncing_cliff_screen_type": None,
                                "conf_show_bouncing_cliff": None,
                                "eligible_to_flash_call_in_ig4a": False,
                                "flash_call_permissions_status": None,
                                "attestation_result": None,
                                "request_data_and_challenge_nonce_string": None,
                                "confirmed_cp_and_code": None,
                                "notification_callback_id": None,
                                "reg_suma_state": 0,
                                "is_msplit_neutral_choice": False,
                                "msg_previous_cp": None,
                                "ntp_import_source_info": None,
                                "youth_consent_decision_time": None,
                                "should_show_spi_before_conf": True,
                                "google_oauth_account": None,
                                "is_reg_request_from_ig_suma": False,
                                "device_emails": None,
                                "is_toa_reg": False,
                                "is_threads_public": False,
                                "spc_import_flow": False,
                                "caa_play_integrity_attestation_result": None,
                                "client_known_key_hash": None,
                                "flash_call_provider": None,
                                "spc_birthday_input": False,
                                "failed_birthday_year_count": None,
                                "user_presented_medium_source": None,
                                "user_opted_out_of_ntp": None,
                                "is_from_registration_reminder": False,
                                "show_youth_reg_in_ig_spc": False,
                                "fb_suma_combined_landing_candidate_variant": "control",
                                "fb_suma_is_high_confidence": None,
                                "screen_visited": [],
                                "fb_email_login_upsell_skip_suma_post_tos": False,
                                "fb_suma_is_from_email_login_upsell": False,
                                "fb_suma_is_from_phone_login_upsell": False,
                                "fb_suma_login_upsell_skipped_warmup": False,
                                "fb_suma_login_upsell_show_list_cell_link": False,
                                "should_prefill_cp_in_ar": None,
                                "ig_partially_created_account_user_id": None,
                                "ig_partially_created_account_nonce": None,
                                "ig_partially_created_account_nonce_expiry": None,
                                "has_seen_suma_landing_page_pre_conf": False,
                                "has_seen_suma_candidate_page_pre_conf": False,
                                "suma_on_conf_threshold": -1,
                                "is_keyboard_autofocus": None,
                                "pp_to_nux_eligible": False,
                                "should_show_error_msg": True,
                                "welcome_ar_entrypoint": "control",
                                "th_profile_photo_token": None,
                                "attempted_silent_auth_in_fb": False,
                            }
                        ),
                        "family_device_id": self._local_data.family_device_id,
                        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
                        "access_flow_version": "F2_FLOW",
                        "is_from_logged_in_switcher": 0,
                        "qe_device_id": self._local_data.device_id,
                    },
                }
            ),
            "bk_client_context": dumps_orjson(
                {
                    "bloks_version": self._version_info.bloks_version_id,
                    "styles_id": "instagram",
                }
            ),
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        await self._request_handler(request)

    async def _phone_number_prefill_async(self):
        uri = constants.BLOKS_PHONE_NUMBER_PREFILL_ASYNC_URI

        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                "Priority": "u=3",
            }
        )

        data = {
            "params": dumps_orjson(
                {
                    "client_input_params": {
                        "user_name_field_text": "",
                        "lois_settings": {"lois_token": ""},
                        "phone_number": None,
                    },
                    "server_params": {
                        "is_from_logged_out": 0,
                        "layered_homepage_experiment_group": None,
                        "device_id": self._local_data.android_id,
                        "waterfall_id": self._local_data.waterfall_id,
                        "INTERNAL__latency_qpl_instance_id": 111393086300282.0,  # Лежит внутри ответа bloks  /process_client_data_and_redirect
                        "source": "prefill_login_form",
                        "is_platform_login": 0,
                        "INTERNAL__latency_qpl_marker_id": self._version_info.qpl_marker_id,
                        "family_device_id": self._local_data.family_device_id,
                        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
                        "access_flow_version": "pre_mt_behavior",
                        "is_from_logged_in_switcher": 0,
                        "qe_device_id": self._local_data.device_id,
                    },
                }
            ),
            "bk_client_context": dumps_orjson(
                {
                    "bloks_version": self._version_info.bloks_version_id,
                    "styles_id": "instagram",
                }
            ),
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        await self._request_handler(request)

    async def _multiple_accounts_get_account_family(self):
        uri = constants.MULTIPLE_ACCOUNTS_GET_ACCOUNT_FAMILY_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                # Специфичные для эндпоинтов ( отправляются почти всегда )
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
            }
        )

        params = {
            "request_source": "com.bloks.www.caa.login.login_homepage",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        await self._request_handler(request)

    async def _login_save_credentials(self):
        uri = constants.BLOKS_LOGIN_SAVE_CREDENTIALS_URI
        url = URL(constants.INSTAGRAM_API_B_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
            }
        )

        data = {
            "qe_device_id": self._local_data.device_id,
            "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
            "_uuid": self._local_data.device_id,
            "family_device_id": self._local_data.family_device_id,
            "bk_client_context": dumps_orjson(
                {
                    "bloks_version": self._version_info.bloks_version_id,
                    "styles_id": "instagram",
                }
            ),
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        await self._request_handler(request)

    async def send_requests_before_login(self):
        """Выполняет запросы как в моб. приложении при переходе на экран авторизации"""

        await self._zr_dual_tokens()
        await self._create_android_keystore()
        await self._process_client_data_and_redirect()
        await self._youth_regulation_delete_pregent()
        await self._phone_number_prefill_async()

    async def send_requests_after_success_login(self):
        """Выполняет запросы как в моб. приложении после успешной авторизации"""

        await self._multiple_accounts_get_account_family()
        await self._zr_dual_tokens()
        await self._login_save_credentials()

    def _update_local_data_from_login_response_data(self, login_response_data: dict):
        headers_raw = login_response_data.get("headers", {})
        headers = {k.lower(): v for k, v in headers_raw.items()}

        authorization = headers.get("ig-set-authorization", "")
        self._local_data.set_authorization_data(
            extract_data_from_authorization(authorization)
        )
        self._local_data.user_id = self._local_data.authorization_data["ds_user_id"]

        www_claim = headers.get("x-ig-set-www-claim")
        if www_claim:
            self._local_data.set_www_claim(www_claim)
        rur = headers.get("ig-set-ig-u-rur")
        if rur:
            self._local_data.set_rur(rur)

        password_key_id = headers.get("ig-set-password-encryption-key-id")
        if password_key_id:
            self._local_data.set_public_key_id(int(password_key_id))

        password_pub_key = headers.get("ig-set-password-encryption-pub-key")
        if password_pub_key:
            self._local_data.set_public_key(password_pub_key)

        logged_in_user = login_response_data.get("login_response", {}).get(
            "logged_in_user", {}
        )
        session_flush_nonce = logged_in_user.get("session_flush_nonce")
        if session_flush_nonce:
            self._local_data.set_session_flush_nonce(session_flush_nonce)

    async def get_challenge_required_info(self, challenge_data: ChallengeData):

        path = challenge_data.api_path
        if path.startswith("/"):
            path = path[1:]
        uri = path
        url = URL(constants.INSTAGRAM_API_B_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )
        headers.update(
            {
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
            }
        )

        params = {
            "guid": self._local_data.device_id,
            "device_id": self._local_data.android_id,
            "challenge_context": challenge_data.challenge_context,
        }

        request = HttpRequest(method="GET", url=url, headers=headers, params=params)

        result = await self._request_handler(request)

        return result
