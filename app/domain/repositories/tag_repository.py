from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.db.models.tag_model import TagModel


class TagRepository(ABC):
    @abstractmethod
    def get_or_create_many(self, names: list[str]) -> list["TagModel"]:
        raise NotImplementedError
