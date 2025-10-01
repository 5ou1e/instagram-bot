import json

from pydantic import BaseModel

from src.infrastructure.instagram.bloks_utils.utils import find_action
from tests.bloks_tools import BloksResponseParser
from tests.bloks_tools import GetArgResolver


class ChallengeRequiredData(BaseModel):
    url: str
    api_path: str
    hide_webview_header: bool
    lock: bool
    logout: bool
    native_flow: bool
    flow_render_type: bool
    challenge_context: str


with open(r"/tests/resolve_challenge/response_with_challenge.json", "r",
          encoding="utf-8") as file:
    response = json.loads(file.read())


parser = BloksResponseParser(response)

action = parser.parse_complete_action()
resolver = GetArgResolver()
action = resolver.resolve_getarg_references(action)
print(action)


needed_action = find_action(action, "bk.action.caa.PresentCheckpointsFlow")

print(needed_action)

error_data = json.loads(needed_action[1])["error"]["error_data"]
print(error_data)

converted = ChallengeRequiredData(**error_data)
print(converted)


