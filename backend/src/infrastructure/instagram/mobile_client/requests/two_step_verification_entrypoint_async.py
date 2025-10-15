from dataclasses import dataclass

from yarl import URL

from src.domain.aggregates.account_worker.entities.android_device import (
    AndroidDevice,
)
from src.domain.shared.entities.account import AccountIgAppSessionData
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.utils import dumps_orjson
from src.infrastructure.instagram.mobile_client.instagram_version_info import (
    InstagramAppVersionInfo,
)
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import (
    InstagramHttpRequest,
)


@dataclass(kw_only=True, slots=True)
class TwoStepVerificationEntrypointAsyncRequest(InstagramHttpRequest):
    """https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.ap.two_step_verification.entrypoint_async/

    Пример успешного ответа:
        "action": "(bk.action.core.TakeLast, (bk.action.core.TakeLast, (#he43lisfu, \"ig4a\", (#he43lisg5), null), (bk.action.logging.LogEvent, \"caa_aymh_client_events_ig\", \"\", (bk.action.map.Make, (bk.action.array.Make, \"aymh_params\", \"core\"), (bk.action.array.Make, (bk.action.mins.CallRuntime, 6), (bk.action.map.Make, (bk.action.array.Make, \"caa_core_data_encrypted\", \"event_category\", \"event_flow\", \"event_step\", \"event\", \"extra_client_data_bks_input\", \"is_dark_mode\", \"waterfall_id\", \"rl_client_session_id\", \"access_flow_version\", \"client_error_message\", \"contactpoint\"), (bk.action.array.Make, \"AXfsj3OcPXgF9Xjcbk1-6oCB2TH533BHtKKMmhQjVezapjXMq-34vzEzdqP5H2x_1tgRhHoRvI8khaco8fXIeij6_Tx4qU3KSRVfdhXJpmLyQZvesSwhd9YWpPp1cwfBp-O7zuIe5f0bj9wpoidlQTq8nAHUQqldQ3eWZKIHzkf3YcJHt1uQVw2FFZ8hJrOb3wd2VywVcWaRFPObSQIpwWsAuqiQvrx97LPm2o4JPDTUd12XWlrbZ6AGUQmEF7EBJv0A0N0BjlpJ5lq25gxPs-KdcUf5kriZoiXjrIDMFMLSrswl3tj2C94iVs6ICtcLLcOp8oKjJb9jCUQdHKiojJCkAzouPzkq7q6URQyyf5Vu_NAuGsdrAKW-F7_t9KBG7BFASj1BdCSp8ujMSUOElOlhx-NmediYFVBhvIlpKakdaD00bvFUicenwCcAiepjyn1XGu93ArGMXALa7v1CT4NkA8PkXMCD5d4JVwKjUiEMBpo9NLPP_62Fs9zRykbb5XlbFLxlD4_45dpCgV3Ox6didzye6hGvTYrMzFr_b_U\", \"aymh_home_page_init\", \"aymh\", \"home_page\", \"aymh_screen_skipped_no_profiles\", (bk.action.map.Merge, (bk.action.map.Merge, (bk.action.mins.CallRuntime, 6), (bk.action.mins.CallRuntime, 6, \"is_from_switcher\", \"0\")), (bk.action.mins.CallRuntime, 6, \"is_from_logged_out\", \"0\")), (ig.action.IsDarkModeEnabled), \"8fb70aeb-f5a1-4361-aff2-54846cd5f11c\", null, \"F2_FLOW\", null, null))))), (bk.action.logging.LogEvent, \"caa_aymh_client_events_ig\", \"\", (bk.action.map.Make, (bk.action.array.Make, \"aymh_params\", \"core\"), (bk.action.array.Make, (bk.action.mins.CallRuntime, 6), (bk.action.map.Make, (bk.action.array.Make, \"caa_core_data_encrypted\", \"event_category\", \"event_flow\", \"event_step\", \"event\", \"extra_client_data_bks_input\", \"is_dark_mode\", \"waterfall_id\", \"rl_client_session_id\", \"access_flow_version\", \"client_error_message\", \"contactpoint\"), (bk.action.array.Make, \"AXfTgyfXdxr5hE-HSRi1Q_1HC5h_xo7IL-ykf6N1LfzyvG9ksG2Mn2nfw-eGyZhyZcc7Fs-vAqCOM7iwpCCF4uFxfmQT_n4aOV-LZ4oeXhY2x10nMn2bBPk2aj8WN8ugAq5JC_1CYiEiWw_qAVV9_QaC8x_1jElR7IAwkKmJpt0-dZmRvXBGOLnZwLLVY0Ham96CfEc22MICCn-ozr7iT-vqKn2fLkhbYSK5cNdfedXFIGJCKm-nK5CwAwGQYQMxdoNefA2sv68cMjmH2t7GxFq1pRHh7JJFkAKqZkz1an_zll5hXUtifp2q2ZvMw38_Aoqnwq6t3kIGgmojZqccxT2NBNZlJ8znQwGcRLRz6tP3Uo1ghPCopy-7Rq2GwmlFMPhHxjzby0mA6jW-ZRoJ4EzwhBBNYr7MPesJgEU7snfJ2TcH5JAXgZaWWk_OybqvelQfxc8MboROhDfviQSuSshsK6-Woe5DR5eKfciC4P024P35K7jN-9B8n8bNE1Xw-e7H1wC4l9se__v7HEVDR_T9lUfmn5KUqbf0qLmRkEA\", \"prefill_login_signal\", \"aymh\", \"home_page\", \"aymh_profile_load_attempted\", (bk.action.map.Merge, (bk.action.map.Merge, (bk.action.map.Merge, (bk.action.mins.CallRuntime, 6), (bk.action.mins.CallRuntime, 6, \"credential_type\", \"google_oauth\")), (bk.action.mins.CallRuntime, 6, \"is_from_switcher\", \"0\")), (bk.action.mins.CallRuntime, 6, \"is_from_logged_out\", \"0\")), (ig.action.IsDarkModeEnabled), \"8fb70aeb-f5a1-4361-aff2-54846cd5f11c\", null, \"F2_FLOW\", null, null))))), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_REMOVE_PROFILE:consecutive_profile_removal:0\", 0), (bk.action.core.TakeLast, (bk.action.caa.reg.SaveCachedInfo, \"\", true), (bk.action.core.TakeLast, (bk.action.qpl.MarkerPoint, 516762113, 0, \"trigger_BloksCAARegYouthRegulationDeletePreRegEntAsyncControllerTypedQueryBuilder\", (bk.action.tree.Make, 13747)), (#he43lisg7, 36707139, 49064891400037, \"com.bloks.www.bloks.caa.reg.youthregulation.deletepregent.async\", (bk.action.map.Make, (bk.action.array.Make, \"device_id\", \"reg_info\", \"flow_info\", \"family_device_id\", \"waterfall_id\", \"offline_experiment_group\", \"layered_homepage_experiment_group\", \"is_platform_login\", \"is_from_logged_in_switcher\", \"is_from_logged_out\", \"qe_device_id\", \"access_flow_version\"), (bk.action.array.Make, \"android-dcf4b72e82a08913\", \"{\\\"first_name\\\":null,\\\"last_name\\\":null,\\\"full_name\\\":null,\\\"contactpoint\\\":null,\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":null,\\\"is_using_unified_cp\\\":null,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":null,\\\"birthday_derived_from_age\\\":null,\\\"did_use_age\\\":null,\\\"gender\\\":null,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":null,\\\"was_headers_prefill_available\\\":null,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"is_spectra_reg\\\":null,\\\"spectra_reg_token\\\":null,\\\"spectra_reg_guardian_id\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"msplit_creator_nonce\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"dismissed_login_upsell_with_cna\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"client_known_key_hash\\\":null,\\\"flash_call_provider\\\":null,\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false,\\\"fb_suma_combined_landing_candidate_variant\\\":\\\"control\\\",\\\"fb_suma_is_high_confidence\\\":null,\\\"screen_visited\\\":[],\\\"fb_email_login_upsell_skip_suma_post_tos\\\":false,\\\"fb_suma_is_from_email_login_upsell\\\":false,\\\"fb_suma_is_from_phone_login_upsell\\\":false,\\\"fb_suma_login_upsell_skipped_warmup\\\":false,\\\"fb_suma_login_upsell_show_list_cell_link\\\":false,\\\"should_prefill_cp_in_ar\\\":null,\\\"ig_partially_created_account_user_id\\\":null,\\\"ig_partially_created_account_nonce\\\":null,\\\"ig_partially_created_account_nonce_expiry\\\":null,\\\"has_seen_suma_landing_page_pre_conf\\\":false,\\\"has_seen_suma_candidate_page_pre_conf\\\":false,\\\"suma_on_conf_threshold\\\":-1,\\\"is_keyboard_autofocus\\\":null,\\\"pp_to_nux_eligible\\\":false,\\\"should_show_error_msg\\\":true,\\\"welcome_ar_entrypoint\\\":\\\"control\\\",\\\"th_profile_photo_token\\\":null,\\\"attempted_silent_auth_in_fb\\\":false}\", \"{\\\"flow_name\\\":\\\"new_to_family_ig_youth_reg\\\",\\\"flow_type\\\":\\\"ntf\\\"}\", \"1fc9267e-8da0-4a40-a5f2-0c1ff668c08f\", \"8fb70aeb-f5a1-4361-aff2-54846cd5f11c\", \"caa_iteration_v3_perf_ig_4\", null, false, false, false, \"9d139e7c-6663-468c-aa45-aa3cd89294a1\", \"F2_FLOW\")), (bk.action.mins.CallRuntime, 6, \"lois_settings\", (#he43lisgb)), \"current-screen\", (bk.action.mins.CallRuntime, 6), (bk.action.core.FuncConst, (bk.action.qpl.MarkerPoint, 516762113, 0, \"success_BloksCAARegYouthRegulationDeletePreRegEntAsyncControllerTypedQueryBuilder\", (bk.action.tree.Make, 13747))), (bk.action.core.FuncConst, (bk.action.qpl.MarkerPoint, 516762113, 0, \"failure_BloksCAARegYouthRegulationDeletePreRegEntAsyncControllerTypedQueryBuilder\", (bk.action.tree.Make, 13747))), (bk.action.array.Make)))), (bk.action.core.TakeLast, (bk.action.qpl.MarkerPoint, 896612552, 0, \"genOpenLoginHomePage_start\", (bk.action.tree.Make, 13747)), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_ACCOUNT_CENTER_PROFILES:account_centers:0\", (bk.action.array.Make)), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_ACCOUNT_CENTER_PROFILES:smartlock_shown_on_aymh:0\", false), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_ACCOUNT_CENTER_PROFILES:last_auto_login_time:0\", 0), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_ACCOUNT_CENTER_PROFILES:is_login_in_progress:0\", false), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_LOGIN_FORM:account_list:0\", (bk.action.array.Make)), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_LOGIN_FORM:sso_token_map_json_string:0\", \"\"), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_LOGIN_FORM:show_internal_settings:0\", false), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_LOGIN_FORM:launched_url:0\", \"\"), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_TEST_VALUES:is_redirect_to_caa_reg_enabled:0\", true), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_TEST_VALUES:enabled_login_with_fb_in_ar:0\", true), (bk.action.bloks.WriteGlobalConsistencyStore, \"CAA_TEST_VALUES:enabled_login_with_fb_in_lf:0\", false), (bk.action.fx.OpenSyncScreen, (bk.action.tree.Make, 16338, 35, (bk.action.core.FuncConst, (bk.action.mins.CallRuntime, 6, \"app_id\", \"com.bloks.www.caa.login.login_homepage\")), 40, 719983200, 36, (bk.action.array.Make, (bk.action.tree.Make, 15932, 38, \"adjust_resize\")), 38, \"CAA_LOGIN_HOME_PAGE\", 41, true, 43, \"com.bloks.www.caa.login.login_homepage\"), (bk.action.bloks.GetPayload, \"he43lismc\", (bk.action.map.Make, (bk.action.array.Make, \"he43lis8a\", \"he43lisa6\"), (bk.action.array.Make, (bk.action.ref.Make, null), (bk.action.ref.Make, null)))), (bk.action.tree.Make, 16085, 38, \"full_screen\", 40, (bk.action.core.FuncConst, 1), 45, \"none\")), (bk.action.qpl.MarkerPoint, 896612552, 0, \"genOpenLoginHomePage_end\", (bk.action.tree.Make, 13747)))), 1)"
    """

    @classmethod
    def create(
        cls,
        device: AndroidDevice,
        version_info: InstagramAppVersionInfo,
        ig_session_data: AccountIgAppSessionData,
        context_data: str,
        internal_latency_qpl_marker_id: int,
        internal_latency_qpl_instance_id: float,
        **kwargs,
    ) -> "TwoStepVerificationEntrypointAsyncRequest":
        uri = "bloks/async_action/com.bloks.www.ap.two_step_verification.entrypoint_async/"
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            device=device,
            version_info=version_info,
            ig_session_data=ig_session_data,
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

        # TODO context_data берется из предыдущего респонса send_login_request
        data = {
            "params": dumps_orjson(
                {
                    "client_input_params": {
                        "auth_secure_device_id": "",
                        "has_whatsapp_installed": 0,
                        "machine_id": ig_session_data.mid,
                        "family_device_id": device.profile.family_device_id,
                    },
                    "server_params": {
                        "context_data": "Admwu7_nn5T_gwXjCRBF-CM3naPmJgwqSj6fMezMHFePKZkZF6IbtH5P_aYt6PGDDxT4N_AovTKNq09rsZ1OYhZ8Adsys0F2oiOTcuvhAgEahqk9HVvpJQhUwJZkck2M6rUBCNv5RJj4JQ4CIpIDZy_4rO9JI5Jpgx4IirEEgZPQuHOJerixp_X45zoMkR5LTEsCsIV2k1XKYdhGrteEDUjAOlxdrfM-2wwcIxu-BmFHD_UpWXHCyUa9X8hYNZ1XlcTIIiwA-5XCSScSZNMcjzIkXbSC5yi3I_RzoeOqcjKuFp1B1qchk4kaxzqSL_d8ocHfRQZDVJTExZg2s0zRgYz4-s9GPqGHCwXHxqaaGeL-kPaA620Ri5qxqOjlBsk1uK0Fzpcw7nhlRSXeDBGSLc575qRTTG6eMqXamZS48Uj_7AoNT2eKpdat8Wrt7BYeK0uxAilVBgevYhoiAbqtGtmJ0F5JpPASuPYjyiX5CkmG3wvBDM7RhDeIZIHXldfMAgnPS_lJNydQGnhfeiA7YOsX8lC71PV6HOlcaLfn2QCsZvgbEX30MUcYxMjNr2xq1iRidz9UXrf3wK0Lexa82KMB9BHCBzqr4A1HdNMFeoKO4qV2b6FrDfQAdOTbFvj3sek7oQ7o4K1HRJYPye-amPl_AQPnKzupjOF2t6y1zihNbsiZUgnKKth8LAKBmwqdhTpd4r4rY1ZHRgiPH3Ilyc3J5bwwRH9p_l7EyEKWSTdYji99mDkX2TOyu_7jT6_CXD_pzB-LJjOm_zfhkqGU4L3yd63EKmJxbfvSNpH8Ptgm7k-FdYGvOZY5rxewZt1k8z1NSuaSVcbl6m_Ci6JlH4HjzgO9p4dqjIZKChf2Ek6ILAXPiCmtnoThDPIniTJqxQctvIxVDnCX-Xw7HcWQk355mpKjiMdcl6kzW1U4X-I9u462S4VTjAEAxZ00e6LUYZUko3nf-DfUJgqjNHWqdxenhjWfYBD_hDlhntDqzT-IsLgPRbO_vT0wLdykQ-4gzXo8QCpS5wc4_q2q9ps_KDgVs7FfgC4boPayc6bH9jzCT8Io5XfuXUmB0DRuqKTomimbMvDAIMNGHHXoaj9XLOTLMl1G3FXuxpe7ustMVMb3eE00d7pE5NemQjyumvS6g7QPrkXza2nRj8slug75cyjCcytrc9FclH-ipWvNbw|aplc",
                        "INTERNAL__latency_qpl_marker_id": 36707139,
                        "INTERNAL__latency_qpl_instance_id": 89502962000003.0,
                        "device_id": device.profile.device_id,
                    },
                }
            ),
            "bk_client_context": {
                "bloks_version": version_info.bloks_version_id,
                "styles_id": "instagram",
            },
            "bloks_versioning_id": version_info.bloks_version_id,
        }

        return cls(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )
