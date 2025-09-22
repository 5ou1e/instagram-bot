from uuid import UUID

from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.repositories.account_worker import AccountWorkerRepository
from src.domain.working_group.repositories.working_group import WorkingGroupRepository

DeleteWorkingGroupWorkersCommandResult = type(None)


class DeleteWorkingGroupWorkersCommandHandler:
    """Удалить воркеров рабочей группы"""

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
        account_worker_repository: AccountWorkerRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository
        self._account_worker_repository = account_worker_repository

    async def __call__(
        self,
        working_group_id: UUID,
        worker_ids: list[UUID] | None = None,
    ) -> DeleteWorkingGroupWorkersCommandResult:
        workers = []

        if worker_ids is None:
            workers = (
                await self._account_worker_repository.acquire_all_by_working_group(
                    working_group_id
                )
            )
        else:
            for worker_id in worker_ids:
                worker = await self._account_worker_repository.acquire_by_working_group_id_and_worker_id(
                    working_group_id=working_group_id,
                    worker_id=worker_id,
                    skip_locked=False,
                )
                workers.append(worker)

        can_be_deleted_ids = [worker.id for worker in workers if worker.may_delete()]

        await self._account_worker_repository.bulk_delete_by_working_group_id(
            working_group_id,
            worker_ids=can_be_deleted_ids,
        )

        await self._uow.commit()
