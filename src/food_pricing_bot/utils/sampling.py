from random import choice

from .db import get_answers
from .storage import get_df

DF = get_df(split="test")


def sample_new_item(chat_id: str) -> str:
    previous_items = set(get_answers(chat_id).keys())
    all_items = set(DF.index)
    available_items = set.difference(all_items, previous_items)
    return choice(available_items)
