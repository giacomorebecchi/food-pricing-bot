from random import choice

from .db import get_answers
from .storage import get_df

DF = get_df(split="test")


async def sample_new_item(chat_id: str) -> str:
    answers = await get_answers(chat_id)
    previous_items = set(answers.keys())
    all_items = set(DF.index)
    available_items = set.difference(all_items, previous_items)
    return choice(available_items)
