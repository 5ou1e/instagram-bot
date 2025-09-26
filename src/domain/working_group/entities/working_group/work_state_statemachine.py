from transitions import Machine

from src.domain.working_group.entities.working_group.work_state import (
    WorkingGroupWorkState,
)

working_group_work_state_machine = Machine(
    states=WorkingGroupWorkState.to_list(),
    initial=WorkingGroupWorkState.IDLE,
    model_attribute="work_state",
)

# Переходы
working_group_work_state_machine.add_transition(
    "start", WorkingGroupWorkState.IDLE, WorkingGroupWorkState.STARTING
)
working_group_work_state_machine.add_transition(
    "work", WorkingGroupWorkState.STARTING, WorkingGroupWorkState.WORKING
)
working_group_work_state_machine.add_transition(
    "stop",
    [WorkingGroupWorkState.WORKING, WorkingGroupWorkState.PAUSED],
    WorkingGroupWorkState.STOPPING,
)
working_group_work_state_machine.add_transition(
    "finish", WorkingGroupWorkState.STOPPING, WorkingGroupWorkState.IDLE
)
working_group_work_state_machine.add_transition(
    "pause", WorkingGroupWorkState.WORKING, WorkingGroupWorkState.PAUSED
)
working_group_work_state_machine.add_transition(
    "resume", WorkingGroupWorkState.PAUSED, WorkingGroupWorkState.WORKING
)
