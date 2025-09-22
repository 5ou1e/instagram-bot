import json

from src.infrastructure.instagram.bloks_utils.utils import find_action
from tests.bloks_tools import BloksResponseParser
from tests.bloks_tools import GetArgResolver


with open(r"/tests/resolve_process_client_data/process_client_data_response.json", "r",
          encoding="utf-8") as file:
    response = json.loads(file.read())


need = response["layout"]["bloks_payload"]["embedded_payloads"]


for item in need:
    # print(item)
    inner_payload = item["payload"]["layout"]["bloks_payload"]
    # print(inner_payload)
    if "ft" in inner_payload:
        for func, val in inner_payload["ft"].items():
            # print(func, val)
            if "Calling genOnClickLoginButton" in val:
                print(item["id"])
                print(val)
            # if func == "zphqfwmzo":
            #     print(val)
    # print("-" * 200)
    # print("-" * 200)

parser = BloksResponseParser(response)

needed_action = parser.get_ft_action("zphqfwmzo", "zphqfwn2w")
print(needed_action)

resolver = GetArgResolver()
action = resolver.resolve_getarg_references(needed_action)

print(action)

async_manifest_action = find_action(action, "bk.action.bloks.AsyncActionWithDataManifestV2")

print(async_manifest_action)
