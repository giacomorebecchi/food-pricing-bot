"""
Two active Databases:
    - db = 0:
        - key = chat_id
        - value = item_id
        - rationale = id of last item sent to chat (with no answer yet)
    - db = 1:
        - key = chat_id
        - value = {item_id: answer}
        - rationale = store answer for every item, for every chat
"""

from redis import Redis

from food_pricing_bot.utils.settings import get_settings

REDIS_HOST = get_settings().REDIS_HOST
REDIS_PORT = get_settings().REDIS_PORT


def get_redis(db: int) -> Redis:
    return Redis(host=REDIS_HOST, port=REDIS_PORT, db=db)
