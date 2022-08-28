import json
from datetime import datetime, timezone

from redis import Redis

from food_pricing_bot.utils.settings import get_settings
from food_pricing_bot.utils.storage import get_dump_path

REDIS_HOST = get_settings().REDIS_HOST
REDIS_PORT = get_settings().REDIS_PORT


def get_redis(db: int) -> Redis:
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=db)
    return r


def dump_answers() -> None:
    r = get_redis(1)
    fname = datetime.now(timezone.utc).isoformat() + ".jsonl"
    fpath = get_dump_path(fname)
    with open(fpath, mode="a") as f:
        for key in r.scan_iter():
            data = r.get(key)
            line = json.dumps({"chat_id": key.decode(), "data": json.loads(data)})
            f.write(line)


def delete_answers() -> None:
    r = get_redis(1)
    for key in r.scan_iter():
        r.delete(key)


if __name__ == "__main__":
    dump_answers()
