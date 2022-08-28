from .storage import get_df

DF = get_df(split="test")


async def get_correct_price(item_id: str) -> int:
    fractional_price = DF.loc[item_id, "fractional_price"]
    return fractional_price
