import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routing.api.v1.router import router as api_v1_router
from app.core.settings import get_settings
from app.core.redis import redis_client

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting application...")

    try:
        await redis_client.connect(settings.redis.build_url())
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise

    logger.info("Application startup complete")

    yield

    logger.info("Shutting down application...")

    try:
        await redis_client.disconnect()
        logger.info("Redis disconnected")
    except Exception as e:
        logger.error(f"Error disconnecting Redis: {e}")

    logger.info("Application shutdown complete")

app = FastAPI(
    title="DSUGrade API",
    version="1.0.0",
    docs_url=settings.fastapi.docs_url,
    openapi_url=settings.fastapi.openapi_url,
    redoc_url=settings.fastapi.redoc_url,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.fastapi.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='app.__main__:app', host=settings.uvicorn.host, port=settings.uvicorn.port
    )
