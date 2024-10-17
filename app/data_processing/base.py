import numpy as np
import pandas as pd
from database.external import get_invoice_move_lines_data
from utils.constants import PRODUCT_FAMILY_OTHERS


def handle_empty_families(df):
    df["product_family"] = df["product_family"].replace("", np.nan)
    df["product_family"] = df["product_family"].fillna(PRODUCT_FAMILY_OTHERS)
    return df


def get_invoice_move_lines_df():
    data = get_invoice_move_lines_data()

    df = pd.DataFrame()

    if data:
        df = pd.DataFrame(data)

        df["confirm_date"] = pd.to_datetime(df["confirm_date"], errors="coerce")
        df = handle_empty_families(df)

    return df
