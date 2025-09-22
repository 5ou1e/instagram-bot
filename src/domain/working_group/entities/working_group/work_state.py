from enum import Enum
from typing import List


class WorkingGroupWorkState(Enum):
    IDLE = "idle"
    STARTING = "starting"
    WORKING = "working"
    STOPPING = "stopping"
    PAUSED = "paused"

    @classmethod
    def to_list(cls) -> List["WorkingGroupWorkState"]:
        return [s for s in cls]
