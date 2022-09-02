import logging
import os
from glob import glob
from pathlib import PurePosixPath
from typing import Optional

import pandas as pd
import pyarrow.parquet as pq

from .settings import get_settings

BASE_PATH: PurePosixPath = get_settings().DATA_PATH


def get_table_path(split: Optional[str] = None) -> PurePosixPath:
    path = BASE_PATH.joinpath(
        "processed",
        "dataset",
    )
    if split:
        path.joinpath(split)
    return path


def get_img_path(fname: Optional[str] = None) -> PurePosixPath:
    path = BASE_PATH.joinpath(
        "processed",
        "img",
    )
    if fname:
        path = path.joinpath(fname)
    return path


def get_dump_path(
    fname: Optional[str] = None,
    folder: str = "answers",
) -> PurePosixPath:
    path = BASE_PATH.joinpath(
        "experiment",
        folder,
    )
    os.makedirs(path, exist_ok=True)
    if fname is not None:
        path = path.joinpath(fname)
    return path


def get_latest_dump_path() -> PurePosixPath:
    path = BASE_PATH.joinpath(
        "experiment",
        "answers",
        "*",
    )
    fpath = max(glob(str(path)))
    return PurePosixPath(fpath)


def get_table(split: Optional[str] = None) -> pq.ParquetDataset:
    path = get_table_path()
    if split is None:
        logging.warning("Loading the full dataset (split argument set to None).")
    _filter = [("split", "=", split)] if split else None
    table = pq.read_table(path, filters=_filter)
    return table


def get_df(split: Optional[str] = None) -> pd.DataFrame:
    path = get_table_path()
    if split is None:
        logging.warning("Loading the full dataset (split argument set to None).")
    _filter = [("split", "=", split)] if split else None
    df = pd.read_parquet(path, filters=_filter)
    return df
