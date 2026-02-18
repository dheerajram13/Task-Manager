from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.repositories.tag_repository import TagRepository
from app.infrastructure.db.models.tag_model import TagModel


class SQLTagRepository(TagRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_or_create_many(self, names: list[str]) -> list[TagModel]:
        if not names:
            return []

        unique_names = list(dict.fromkeys(names))
        existing_stmt = select(TagModel).where(TagModel.name.in_(unique_names))
        existing = self._session.execute(existing_stmt).scalars().all()
        existing_by_name = {tag.name: tag for tag in existing}

        for name in unique_names:
            if name not in existing_by_name:
                tag = TagModel(name=name)
                self._session.add(tag)
                existing_by_name[name] = tag

        self._session.flush()
        return [existing_by_name[name] for name in unique_names]
