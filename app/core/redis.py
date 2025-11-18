from typing import Optional
from redis.asyncio import Redis, ConnectionPool
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self._redis: Optional[Redis] = None
        self._pool: Optional[ConnectionPool] = None

    async def connect(self, url: str) -> None:
        self._pool = ConnectionPool.from_url(
            url=url,
            decode_responses=True,
            max_connections=10,
        )
        self._redis = Redis(connection_pool=self._pool)
        await self._redis.ping()
        logger.info("Redis connected")

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.aclose()
        if self._pool:
            await self._pool.disconnect()
        logger.info("Redis disconnected")

    @property
    def client(self) -> Redis:
        if not self._redis:
            raise RuntimeError("Redis not initialized")
        return self._redis

    async def health_check(self) -> bool:
        """Проверка здоровья Redis для /health endpoint."""
        try:
            await self._redis.ping()
            return True
        except Exception:
            return False


# Singleton
redis_client = RedisClient()


def get_redis_client() -> Redis:
    return redis_client.client
