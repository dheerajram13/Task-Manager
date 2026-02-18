from dataclasses import dataclass, field


@dataclass(slots=True)
class TaskFilters:
    completed: bool | None = None
    priority: int | None = None
    tags: list[str] = field(default_factory=list)
    limit: int = 20
    offset: int = 0
