"""
Three active Databases:
    - db = 0:
        - key = chat_id
        - value = item_id
        - rationale = id of last item sent to chat (with no answer yet)
    - db = 1:
        - key = chat_id
        - value = {item_id: answer}
        - rationale = store answer for every item, for every chat
    - db = 2:
        - key = chat_id
        - value = {"full_name": full_name, "datetime": [datetime]}  # dict
"""
import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict

from aioredis import Redis

from .settings import get_settings

if TYPE_CHECKING:
    from telegram import Update

REDIS_HOST = get_settings().REDIS_HOST
REDIS_PORT = get_settings().REDIS_PORT


async def get_redis(db: int) -> Redis:
    r = await Redis(host=REDIS_HOST, port=REDIS_PORT, db=db)
    return r


async def set_new_user(update: "Update") -> None:
    r = await get_redis(2)  # USERS_DB
    dt = datetime.now(timezone.utc).isoformat()
    chat_id = update.message.chat_id
    full_name = update.message.from_user.full_name
    data = await r.get(chat_id)
    if data is None:
        data = {
            "full_name": full_name,
            "datetime": [dt],
        }
    else:
        data = json.loads(data)
        data["datetime"].append(dt)
    await r.set(chat_id, json.dumps(data))


async def set_new_question(chat_id: str, item_id: str) -> None:
    r = await get_redis(0)
    await r.set(chat_id, item_id)


async def get_last_question(chat_id: str) -> str:
    r = await get_redis(0)
    item_id = await r.get(chat_id)
    return item_id.decode()


async def set_new_answer(
    chat_id: str,
    item_id: str,
    answer: str,
) -> None:
    r_q = await get_redis(0)
    r_a = await get_redis(1)
    item_id = await r_q.get(chat_id)
    answers = await r_a.get(chat_id)
    if answers is None:
        answers = {}
    else:
        answers = json.loads(answers)
    answers[item_id] = answer
    await r_a.set(chat_id, json.dumps(answers))


async def get_answers(chat_id: str) -> Dict:
    r = await get_redis(1)
    answers = await r.get(chat_id)
    if answers is None:
        return {}
    else:
        return json.loads(answers)
