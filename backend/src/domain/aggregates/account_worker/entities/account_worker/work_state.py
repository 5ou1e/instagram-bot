from enum import Enum

from transitions import Machine


class AccountWorkerWorkState(Enum):
    IDLE = "IDLE"
    PENDING_START = "PENDING_START"
    STARTING = "STARTING"
    WORKING = "WORKING"
    STOPPING = "STOPPING"
    PAUSED = "PAUSED"

    @classmethod
    def to_list(cls) -> list["AccountWorkerWorkState"]:
        return [s for s in cls]


account_work_state_machine = Machine(
    states=AccountWorkerWorkState.to_list(),
    initial=AccountWorkerWorkState.IDLE,
    model_attribute="work_state",
)

# Транзиции
account_work_state_machine.add_transition(
    "wait_for_start",
    AccountWorkerWorkState.IDLE,
    AccountWorkerWorkState.PENDING_START,
)
account_work_state_machine.add_transition(
    "start", AccountWorkerWorkState.IDLE, AccountWorkerWorkState.STARTING
)
account_work_state_machine.add_transition(
    "work", AccountWorkerWorkState.STARTING, AccountWorkerWorkState.WORKING
)
account_work_state_machine.add_transition(
    "stop",
    [
        AccountWorkerWorkState.PENDING_START,
        AccountWorkerWorkState.WORKING,
        AccountWorkerWorkState.PAUSED,
    ],
    AccountWorkerWorkState.STOPPING,
)
account_work_state_machine.add_transition(
    "finish", AccountWorkerWorkState.STOPPING, AccountWorkerWorkState.IDLE
)
account_work_state_machine.add_transition(
    "pause", AccountWorkerWorkState.WORKING, AccountWorkerWorkState.PAUSED
)
account_work_state_machine.add_transition(
    "resume", AccountWorkerWorkState.PAUSED, AccountWorkerWorkState.WORKING
)
