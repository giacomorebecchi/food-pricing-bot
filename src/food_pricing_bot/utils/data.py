from telegram import InputFile

from .storage import get_df, get_img_path

DF = get_df(split="test")


def get_correct_price(item_id: str) -> int:
    fractional_price = DF.loc[item_id, "price_fractional"]
    return fractional_price


def get_img(item_id: str) -> InputFile:
    fname = f"{item_id}.jpg"
    img_bytes = open(get_img_path(fname), mode="rb").read()
    return InputFile(img_bytes)


def get_txt(item_id: str) -> str:
    txt = DF.loc[item_id, "txt"]
    return txt
