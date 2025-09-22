import json

from pydantic import BaseModel

from src.infrastructure.instagram.bloks_utils.utils import find_action, deserialize_bloks_action


action = """
(bk.action.core.TakeLast, (bk.action.core.FuncConst, 1), (bk.action.core.If, (bk.action.bloks.GetVariable2, "1zo7tafvj6"), (#1zo7tafvjj, 2293785, 0, (bk.action.mins.CallRuntime, 6, "fallback_triggered", true)), null), (bk.action.core.TakeLast, (bk.action.core.TakeLast, (bk.action.core.TakeLast, (bk.action.core.If, (bk.action.core.If, (bk.action.bloks.IsAppInstalled, "https:\/\/whatsapp:\/\/", (bk.action.array.Make, "com.whatsapp")), true, (bk.action.bloks.IsAppInstalled, "https:\/\/whatsapp:\/\/", (bk.action.array.Make, "com.whatsapp.w4b"))), (bk.action.core.TakeLast, (bk.action.caa.reg.ClearWACode), (bk.action.core.FuncConst, 1), (bk.action.caa.reg.SendIntentToWA)), null), (bk.action.qpl.MarkerPoint, 516765874, 0, "send_intend_to_wa", (bk.action.tree.Make, 13747))), (bk.action.core.TakeLast, (bk.action.qpl.MarkerAnnotate, 2293785, 0, (bk.action.map.Make, (bk.action.array.Make, "login_type", "login_source"), (bk.action.array.Make, "Password", "Login"))), (bk.action.qpl.MarkerAnnotate, 2293785, 0, (bk.action.mins.CallRuntime, 6, "end_point", "redirect_login_challenges")), (bk.action.qpl.MarkerEndV2, 2293785, 0, 87, (bk.action.tree.Make, 13704))), (#1zo7tafvjl, 36707139, 202196551900003, "com.bloks.www.ap.two_step_verification.entrypoint_async", (bk.action.map.Make, (bk.action.array.Make, "context_data", "device_id"), (bk.action.array.Make, "AdlZg30wIiJO6TDFhAPlMDJ0Rwk0d5lihWpz2AHN8YK3_pBqs9vOKYBt1PETDttA4YUuifehEGslTJLvQa58EaDRWAuGysSOq0_bJbEC0E1ot7vNQqD_Ro4C4I-MIiO_ezvJ9DlqxT3RsKvwZ7b_NFcn8S4Vd3BAtYPGc7JQHUVROmX1G6pcMgpE6rDSUYU-mlEINWFREEP5vnSeOnyAme7Np6uqDbi97h3Jde1FxoGF2_KWVtZ8pmEczDJOPSsypRxmcHFFOeeKMUI5pSPuEBJ7HudaKnWkA1hMAbTe-hvN6RUsYp2WjmeKMX6kUhTPWk-i2ML3dMON16I94hfKy2h6vbzNlRBVbtEuoQxTzkLGsRRlgTasmncobktIMXSfGJHya0Vb16SrUixnW8kL4tuUX3yl66mSHsBiGld7SwvUFU_Y_o-740piakZx84SmXpFsGcjlmIE_KsngymdCCOqLaQn1Y8U132Tivq9Dj27RUBaL1nGs7EZoAbEfXS1cf-GwCpPlirGmsotIG1vtckYwbUiF2LtK6LNwoZyRifLLVyi3FMT2J8bhIDjkM6AVSMjagFTZ8-h8Q9ln8bMNDCJBybQfBntp6RkJRMa8YhpgncqMwCSKDgT-rd_OxEu8ZKKp9spXo0oW7KyuFr2Ln2Qm_BKSg5FTo9BnpB5LavitENNNB590FRbmHpWgIbYzJLCSKfmaG3dzNPgb2s9B3izbBYiHgss602G4KUYMyLgEiPtCnKk89CBJOf2TnKPmYXTX2bRquk8uuI2TCTQQ2j4_tdtH1uVQP2FAeqVki-1qgItT145rOeWTlfxpTpRVeOd5TQdFcfpH9JQNGSrJM7Vfvdd0yIPEVfBaLOLTo25T8An51g3pVFFspe-J6dqFxSfMo7hI88116zg25XCbsKoDEhKPhI551t2uNADwViRENzlt5LkGYQtEYACB4EROPPvoWYcEatG_bTxtMmae_z6TBM40aCFEMNc374j_8Yu8mtp1jtRwoz0_Z5w_7PHdAV5xp169yUDrX8hREMIOcGz3I9MYIutzwX7hWk2QQOk1KGPCaCtAbfX5oF_GVmI6sMuV-8MCatRLJC0j0S-_jaD_MTfjoM4O95mvr42BHvRmms2NL55oK-rpphq53Y4SbQDS-Bb3-2YG6uASZ_UapImTmFHa5fU4ffdLQ37rCtA|aplc", "3a6040e9-245e-451b-9b53-440777b0ed49")), (bk.action.map.Make, (bk.action.array.Make, "has_whatsapp_installed", "machine_id", "family_device_id", "auth_secure_device_id"), (bk.action.array.Make, (bk.action.core.If, (bk.action.bloks.IsAppInstalled, "https:\/\/whatsapp:\/\/", (bk.action.array.Make, "com.whatsapp")), true, (bk.action.bloks.IsAppInstalled, "https:\/\/whatsapp:\/\/", (bk.action.array.Make, "com.whatsapp.w4b"))), (bk.action.caa.FetchMachineID), (bk.fx.action.GetFamilyDeviceId), "")), "current-screen", (bk.action.mins.CallRuntime, 6), (bk.action.core.FuncConst, 1), (bk.action.core.FuncConst, 1), (bk.action.array.Make))), (bk.action.map.Make, (bk.action.array.Make, "should_dismiss_loading", "has_identification_error"), (bk.action.array.Make, false, false))))
"""

action = deserialize_bloks_action(action)
print(action)
needed_action = find_action(action, arg_value="com.bloks.www.ap.two_step_verification.entrypoint_async")

print(needed_action)


print(needed_action[5])

print([val for val in needed_action[5][1][1:]])

#
# map_make = find_action(needed_action, action_name="bk.action.map.Make")
#
# print(map_make)
#
# array_make_names = find_action(map_make, "bk.action.array.Make")
# names = [val for val in map_make[1][1:]]
# values = [val for val in map_make[2][1:]]
# print({k: v for k, v in zip(names, values)})
# print(names)

action = """
(bk.action.core.TakeLast, (bk.action.cds.PushScreen, (bk.action.tree.Make, 13784, 38, (bk.action.tree.Make, 13901, 35, (bk.action.bloks.GetScript, \"aazfyrxno\")), 35, \"com.bloks.www.ap.two_step_verification.code_entry\", 49, 719983200, 45, \"generic_code_entry\", 46, 0, 42, (bk.action.array.Make, (bk.action.tree.Make, 15932)), 56, (bk.action.core.FuncConst, (bk.action.mins.CallRuntime, 6))), (bk.action.tree.Make, 16087, 38, (bk.action.core.FuncConst, (bk.action.mins.CallRuntime, 6))), (bk.action.mins.CallRuntime, 6, \"params\", (bk.action.string.JsonEncode, (bk.action.mins.CallRuntime, 6, \"server_params\", (bk.action.map.Make, (bk.action.array.Make, \"context_data\", \"device_id\", \"INTERNAL_INFRA_screen_id\"), (bk.action.array.Make, \"AdlDW8yHXhBiVmS_lrqzq-FyTrraxiD-fG9aZRT4P-N35oPPoTVkPd-QWFPBRC497CG7Qd8zpFPf--axMJW_mbn3sPw2qeDoeDFsvdp2G7dFqq2X9XUSOFMjE23aVPJK2ue1Uu0ITAzx-RWBHx3rgv0e43f9FPlG9aLqgd4pdVNiQCQ3BEbKh3ZoUNhFgEZope8SOJGl6V1rrPcykexrfGaHVV7vphWTgOTCdKoMOQXAY3DF5VqR1mz-6BjNHV8ZugJ0UVkPn2ed4hJysYWMgFzNwvY1P9ppAuikAhehdzn4AA1BvbzhNy_MV7tBvsghnW80PcYtEu_mQI5snuwhoWZU8j6FWPSdn5H85RrTu-PmBLDwuKnl9PEICRJV41eo1tc0VM0wDrQYwuBFLE-NgDhMOmK-jHWIF2547B2MQUs89rEpYQYkS2tYcnjRYzgXzmirKDadPdvYCVnIpRKZi1ATdsLhrbv0roG1GqPnf8CzU6bIGEEdL79_7XUoEyrDXaWRdgO-ZdhDur2Oc7jcsTImOquTy3EmZjEb_T1c-uYbYP21y0RId_VPVrAfBvhhvplUCDWUX45CHFt7XZOxsTvS3YXXUPbcYLVDGbus3oLtpJAMU1Wze34KDduxL8lgqun5Bbi2oXuVswR_l8cKTMaZUpKa8d7DyvwaH30ykPuir9i2pxI8byKnItx1BAUd-240AjYjsUn52WquwG0XvNRrPIUjEnQKXPsYDJogSvHkoNH_60DxHFpLLCj3H1zwbswkXJ2pdA3bBwf5--joYA0lcWYoHlcryLas6Qeockjw0UQWq8izqaXVGkaRtSVMQspD2QmsGl_NhpIMROw3iMN731NWJAynZhkYZ8ZJ0FSEwwTUsoqeMPTAZmzTDGxk4_4WWqU3E7Ev0GGHZ352oi0hIk6FdnbcIypgdVLV7Af9KtXPAXBK67hO-8OWttkTLGIF7yevQpxYr0VXPzZ_e0fZJ_3P3zdgPrFBMXHwOMa7Z_q2yKIHKsXFWc4Mfiatgtcgkx8-0HnmXAoHJfQnC-esZQpp01QBldEVtCeAyUA9pQ0Kuf9f0R7LPxKomVvJy2Eq7eaAM5jY-90-J6M4ifMHryIOpESxd9c693veTWGemS1LNb7_KafZFWe_XuOWfYY-sg8PQ_SpbN6H11qr60LiPJ7vE3Rl4t-9oTuCefUiyI-b4RO9dgu6FGe6OmDlBme9S37gsEroCNEi1fTFGr7TPOdc4QLuln1UZsWnSjO-GkHYnsyXvtFqnG2q2fAwRiYqvfoTN-OMeDOHYjv0zPDwh9CYuN1mktYYRFMsWaiTXG2F7bieXPg__8XVi5nH3vpAHO-ERkwRviKxTXAuBwJn-VBAOdLg9_DYx3k493qAQkNOK9Q2i1nvbmyICrLLs0d46Oz4SNRw4f1ZTI8nGLghTky8QcJgEnZPPpicbq5KyOhrd37uCMOiSkjJ8sv9hNTwhmYZvgJN2GrSlF2RuyIATyzMvIQ8pAlttvmUKQDmeMUXlkMrgrivpI69bU95niiFzTiWTUGpTSt3c9gjOJz6eaw_w8Bw6uNVGqswev_DfJtR8r9Btxlr7dVPi2v15xC1JICRIG0mSnbBeV4SgHc5uCAPmW0i1utdz3MtdO63kwM2VuUQBbcdbq-_-IyF4zXszjJmT_X2t0mM-dsFu4Pb_B7oQDJbc1TIwI6RGK0Ii1Dh8fxRHCBZZX2NQJI1G20yQ4W-xsYlX8o8gxXQjAVrfY_9jdh_UGeVOh0pEaaVK2b7mYazP7TD7i99VOBAjG0GZ0gZvUyn2PVT0A9JW8sf1b43w1ypqieTORppnb-UBF9ZQxr9Ru8H7qjRj7twvo3yNakGKtLaZdDmvm_IwlzGmbCIz_A_jYfHZD8H3g_r3BFAg103Bha5dAhkKtrlqWu-gZckqTkukZv0ZGAV3WzJWGu3DzUYbhX5ALnXVWE0jcKFGuP61aohJwM_XiCfUGk6ekhaeJxfJa94JMHuI9mSrmGaqYiOsyj5035Ek_-sm0ojSAkHiLxFtAoHu63Ny67kfJq1Y-If--C8nfhNBoXT3aNglIBhDxCNzJpeDiQATTUa5RbAu_N2Go9B60byOODFVd5cprEL-gNDoVox0IErnafY7rV3NuMjXjuhffURKSuR4w2GkvmZ_C6Wrzd18QcmjqMvX3sXLg6P9lcqRyOG2lZ0NjUNe6hxouX_|aplc\", \"715f205a-a663-4c36-b077-e10a093c90b1\", \"generic_code_entry\"))))), (bk.action.core.GetArg, 0)), 1)
"""

action = deserialize_bloks_action(action)

print(json.dumps(action, indent=3))