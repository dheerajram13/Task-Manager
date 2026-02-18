from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import get_task_service
from app.api.schemas.error_response import ErrorResponse
from app.api.schemas.task_request import TaskCreateRequest, TaskPatchRequest
from app.api.schemas.task_response import PaginatedTasksResponse, TaskResponse
from app.core.constants import DEFAULT_LIMIT, MAX_LIMIT
from app.domain.entities.task import TaskFilters
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _parse_csv_tags(tags: str | None) -> list[str]:
    if not tags:
        return []
    return [part.strip() for part in tags.split(",") if part.strip()]


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={422: {"model": ErrorResponse}},
)
def create_task(
    payload: TaskCreateRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = service.create_task(payload)
    return TaskResponse.from_model(task)


@router.get(
    "",
    response_model=PaginatedTasksResponse,
    responses={422: {"model": ErrorResponse}},
)
def list_tasks(
    completed: bool | None = Query(default=None),
    priority: int | None = Query(default=None, ge=1, le=5),
    tags: str | None = Query(default=None, description="CSV tags for any-match filtering"),
    limit: int = Query(default=DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    offset: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
) -> PaginatedTasksResponse:
    filters = TaskFilters(
        completed=completed,
        priority=priority,
        tags=_parse_csv_tags(tags),
        limit=limit,
        offset=offset,
    )
    total, items = service.list_tasks(filters)
    return PaginatedTasksResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[TaskResponse.from_model(item) for item in items],
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)) -> TaskResponse:
    task = service.get_task(task_id)
    return TaskResponse.from_model(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
def patch_task(
    task_id: int,
    payload: TaskPatchRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = service.patch_task(task_id, payload)
    return TaskResponse.from_model(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)) -> Response:
    service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
