from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.tasks import router as tasks_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logger import configure_logging
from app.infrastructure.db.base import Base, import_models
from app.infrastructure.db.session import get_engine


def create_app(*, initialize_db: bool = True) -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        if initialize_db:
            import_models()
            Base.metadata.create_all(bind=get_engine())
        yield

    app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(tasks_router)

    return app


app = create_app()
