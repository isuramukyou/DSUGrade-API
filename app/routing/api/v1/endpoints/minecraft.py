import logging

from fastapi import APIRouter

from app.core.dependencies import RedisDep
from app.domains.minecraft.schemas import User

router = APIRouter(prefix='/minecraft')

logger = logging.getLogger(__name__)


@router.get('/auth/status')
async def check_minecraft_player_auth_status(nickname: str, redis: RedisDep):
    logger.info(f'Checking Minecraft auth status for nickname: {nickname}')
    name = await redis.getdel(nickname)

    if name:
        logger.info(f'User authenticated: nickname={nickname}, name={name}')
        return {"status": True, "name": name, "nickname": nickname}

    logger.info(f'User not authenticated: nickname={nickname}')
    return {"status": False, "name": None, "nickname": nickname}


@router.post('/auth/set')
async def set_student_auth_status(user: User, redis: RedisDep):
    logger.info(f'Setting Minecraft auth status for nickname: {user.nickname}, name: {user.name}')
    await redis.set(name=user.nickname, value=user.name, ex=3600)
