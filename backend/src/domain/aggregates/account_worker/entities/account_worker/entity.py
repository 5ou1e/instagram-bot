import uuid
from dataclasses import dataclass, field
from datetime import datetime

from transitions import MachineError

from src.domain.aggregates.account_worker.entities.account_worker.work_state import (
    AccountWorkerWorkState,
    account_work_state_machine,
)
from src.domain.aggregates.account_worker.entities.android_device import AndroidDevice
from src.domain.aggregates.android_device_hardware.entities.android_device_hardware import (
    AndroidDeviceHardware,
)
from src.domain.aggregates.proxy.entities import Proxy
from src.domain.shared.exceptions import InvalidStateTransitionError

AccountWorkerID = type(uuid.UUID)


@dataclass(kw_only=True, slots=True)
class AccountWorker:
    id: AccountWorkerID
    working_group_id: uuid.UUID
    account_id: uuid.UUID
    proxy: Proxy | None = None
    android_device: AndroidDevice | None = None

    work_state: AccountWorkerWorkState = field(default=AccountWorkerWorkState.IDLE)
    status: str | None = None
    last_action_time: datetime | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    def set_android_device(self, android_device: AndroidDevice):
        self.android_device = android_device

    def set_android_device_hardware(
        self, android_device_hardware: AndroidDeviceHardware
    ):
        self.android_device.set_hardware(android_device_hardware)

    def set_proxy(self, proxy: Proxy | None):
        self.proxy = proxy

    def change_status(self, new_status: str | None):
        self.status = new_status

    def trigger(self, action: str) -> bool:
        try:
            return account_work_state_machine.events[action].trigger(self)
        except MachineError:
            raise InvalidStateTransitionError(
                action=action, state=self.work_state.value
            )

    def may_delete(self) -> bool:
        if self.work_state == AccountWorkerWorkState.IDLE:
            return True
        return False

    def wait_for_start(self) -> bool:
        return self.trigger("pending_start")

    def start(self) -> bool:
        return self.trigger("start")

    def work(self) -> bool:
        return self.trigger("work")

    def stop(self) -> bool:
        return self.trigger("stop")

    def pause(self) -> bool:
        return self.trigger("pause")

    def resume(self) -> bool:
        return self.trigger("resume")

    def finish(self) -> bool:
        return self.trigger("finish")

    def may_start(self) -> bool:
        return bool(
            account_work_state_machine.get_transitions(
                trigger="start", source=self.work_state
            )
        )

    def may_work(self) -> bool:
        return bool(
            account_work_state_machine.get_transitions(
                trigger="work", source=self.work_state
            )
        )

    def may_stop(self) -> bool:
        return bool(
            account_work_state_machine.get_transitions(
                trigger="stop", source=self.work_state
            )
        )

    def may_finish(self) -> bool:
        return bool(
            account_work_state_machine.get_transitions(
                trigger="finish", source=self.work_state
            )
        )

    def may_pause(self) -> bool:
        return bool(
            account_work_state_machine.get_transitions(
                trigger="pause", source=self.work_state
            )
        )

    def may_resume(self) -> bool:
        return bool(
            account_work_state_machine.get_transitions(
                trigger="resume", source=self.work_state
            )
        )
