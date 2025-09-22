import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from transitions import MachineError

from src.domain.shared.exceptions import DomainError, InvalidStateTransitionError
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.working_group.entities.worker.entity import AccountWorker
from src.domain.working_group.entities.worker.work_state import AccountWorkerWorkState
from src.domain.working_group.entities.worker_task.base import AccountWorkerTask
from src.domain.working_group.entities.working_group.work_state import (
    WorkingGroupWorkState,
)
from src.domain.working_group.entities.working_group.work_state_statemachine import (
    working_group_work_state_machine,
)
from src.domain.working_group.exceptions import (
    WorkerAlreadyWorkedWithinLastWorkingGroupExecutionError,
    WorkingGroupAccountWorkerTaskIdDoesNotExistError,
    WorkingGroupProcessingAccountsCountExceededError,
)


@dataclass(kw_only=True)
class WorkingGroup:
    id: uuid.UUID
    name: str
    config: WorkingGroupConfig = field(default_factory=WorkingGroupConfig)
    worker_tasks: List[AccountWorkerTask] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    work_state: WorkingGroupWorkState = WorkingGroupWorkState.IDLE
    workers: List[AccountWorker] = field(default_factory=list)

    def get_enabled_worker_tasks(self, sort_by_index=False) -> list[AccountWorkerTask]:
        if sort_by_index:
            return sorted(
                [st for st in self.worker_tasks if st.enabled], key=lambda s: s.index
            )
        else:
            return [st for st in self.worker_tasks if st.enabled]

    def get_account_worker_task_by_id(self, task_id: uuid.UUID):
        for task in self.worker_tasks:
            if task.id == task_id:
                return task
        raise WorkingGroupAccountWorkerTaskIdDoesNotExistError(
            working_group_id=self.id,
            task_id=task_id,
        )

    def update_account_worker_task_name(self, task_id: uuid.UUID, name: str):
        task = self.get_account_worker_task_by_id(task_id)
        task.name = name

    def update_account_worker_task_index(self, task_id: uuid.UUID, index: int):
        task = self.get_account_worker_task_by_id(task_id)
        task.index = index

    def update_account_worker_task_config(self, task_id: uuid.UUID, config: dict):
        task = self.get_account_worker_task_by_id(task_id)
        task.config = config

    def update_account_worker_task_enabled(self, task_id: uuid.UUID, enabled: bool):
        task = self.get_account_worker_task_by_id(task_id)
        task.enabled = enabled

    def trigger(self, action: str) -> bool:
        try:
            return working_group_work_state_machine.events[action].trigger(self)
        except MachineError:
            raise InvalidStateTransitionError(
                action=action, state=self.work_state.value
            )

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
            working_group_work_state_machine.get_transitions(
                trigger="start", source=self.work_state
            )
        )

    def may_work(self) -> bool:
        return bool(
            working_group_work_state_machine.get_transitions(
                trigger="work", source=self.work_state
            )
        )

    def may_stop(self) -> bool:
        return bool(
            working_group_work_state_machine.get_transitions(
                trigger="stop", source=self.work_state
            )
        )

    def may_finish(self) -> bool:
        return bool(
            working_group_work_state_machine.get_transitions(
                trigger="finish", source=self.work_state
            )
        )

    def may_pause(self) -> bool:
        return bool(
            working_group_work_state_machine.get_transitions(
                trigger="pause", source=self.work_state
            )
        )

    def may_resume(self) -> bool:
        return bool(
            working_group_work_state_machine.get_transitions(
                trigger="resume", source=self.work_state
            )
        )

    def start_worker(
        self,
        worker: AccountWorker,
        last_run_started_account_ids: list[uuid.UUID],
    ) -> bool:
        if worker.working_group_id != self.id:
            raise DomainError()
        if (
            self.count_processing_workers
            >= self.config.general.max_parallel_processing_accounts_count
        ):
            raise WorkingGroupProcessingAccountsCountExceededError()

        worker.start()

        if worker.id not in last_run_started_account_ids:
            last_run_started_account_ids.append(worker.id)
            return True
        else:
            raise WorkerAlreadyWorkedWithinLastWorkingGroupExecutionError()

    def has_workers_that_may_start(self, last_run_started_account_ids) -> bool:
        for worker in self.workers:
            if worker.may_start() and worker.id not in last_run_started_account_ids:
                return True

    def get_workers_that_may_start(
        self, last_run_started_account_ids: list[uuid.UUID]
    ) -> list[AccountWorker]:
        workers_may_start = []
        for worker in self.workers:
            if worker.may_start() and worker.id not in last_run_started_account_ids:
                workers_may_start.append(worker)
        return workers_may_start

    def finish_worker(self, worker: AccountWorker) -> bool:
        if worker.working_group_id != self.id:
            raise DomainError()
        return worker.finish()

    @property
    def count_processing_workers(self) -> int:
        # Возвращает кол-во workers, которые находятся в обработке
        return sum(
            1 for ta in self.workers if not ta.work_state == AccountWorkerWorkState.IDLE
        )

    def is_all_assigned_workers_finished(
        self,
        last_run_started_account_ids: list[uuid.UUID],
    ) -> bool:
        """Все ли workers, которые привязаны к задаче в текущий момент , завершили работу"""
        for worker in self.workers:
            if (worker.id not in last_run_started_account_ids) or (
                worker.work_state != AccountWorkerWorkState.IDLE
            ):
                return False
        return True
