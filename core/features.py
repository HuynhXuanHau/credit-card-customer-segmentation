# core/features.py

from __future__ import annotations
import numpy as np
import pandas as pd
from .constants import RAW_NEEDED, EPS


def feature_engineering_B(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo features theo notebook hướng B:
    TOTAL_PURCHASES, TOTAL_SPENDING, MONTHLY_PAYMENTS, MINIMUM_PAYMENTS_RATIO,
    LOG_BALANCE, LOG_CREDIT_LIMIT, LOG_TOTAL_PURCHASES, LOG_TOTAL_SPENDING, LOG_PAYMENTS,
    giữ các frequency/trx/prc_full_payment.
    """
    df = df_in.copy()

    for c in RAW_NEEDED:
        if c not in df.columns:
            df[c] = 0.0

    for c in RAW_NEEDED:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    df["TOTAL_PURCHASES"] = df["ONEOFF_PURCHASES"] + df["INSTALLMENTS_PURCHASES"]
    df["TOTAL_SPENDING"] = df["PURCHASES"] + df["CASH_ADVANCE"]
    df["MONTHLY_PAYMENTS"] = df["PAYMENTS"] / (df["TENURE"] + EPS)
    df["MINIMUM_PAYMENTS_RATIO"] = df["MINIMUM_PAYMENTS"] / (df["CREDIT_LIMIT"] + EPS)

    df["LOG_BALANCE"] = np.log1p(df["BALANCE"].clip(lower=0))
    df["LOG_CREDIT_LIMIT"] = np.log1p(df["CREDIT_LIMIT"].clip(lower=0))
    df["LOG_TOTAL_PURCHASES"] = np.log1p(df["TOTAL_PURCHASES"].clip(lower=0))
    df["LOG_TOTAL_SPENDING"] = np.log1p(df["TOTAL_SPENDING"].clip(lower=0))
    df["LOG_PAYMENTS"] = np.log1p(df["PAYMENTS"].clip(lower=0))

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    for c in df.columns:
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].median())

    return df
