import logging
import json

from fastapi import APIRouter

from app.core.dependencies import RedisDep
from app.domains.minecraft.schemas import User

router = APIRouter(prefix='/minecraft')

logger = logging.getLogger(__name__)


@router.get('/auth/status')
async def check_minecraft_player_auth_status(nickname: str, redis: RedisDep):
    user_data: dict
    logger.info(f'Checking Minecraft auth status for nickname: {nickname}')
    user_data_json_str = await redis.getdel(nickname)

    if user_data_json_str:
        user_data = json.loads(user_data_json_str)
        logger.info(f'User authenticated: nickname={nickname}, name={user_data.get("name")}')
        return {"status": True, "name": user_data.get("name"), "nickname": nickname, "course": user_data.get("course"), "faculty": user_data.get("faculty")}

    logger.info(f'User not authenticated: nickname={nickname}')
    return {"status": False, "nickname": nickname}


@router.post('/auth/set')
async def set_student_auth_status(user: User, redis: RedisDep):
    logger.info(f'Setting Minecraft auth status for nickname: {user.nickname}, name: {user.name}')
    data = {'name': user.name, 'course': user.course, 'faculty': user.faculty}
    user_data_json_str = json.dumps(data, ensure_ascii=False)
    await redis.set(name=user.nickname, value=user_data_json_str, ex=3600)
