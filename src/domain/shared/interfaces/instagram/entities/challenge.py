from pydantic import BaseModel


class ChallengeData(BaseModel):
    url: str
    api_path: str
    hide_webview_header: bool
    lock: bool
    logout: bool
    native_flow: bool
    flow_render_type: bool
    challenge_context: str | None = None
