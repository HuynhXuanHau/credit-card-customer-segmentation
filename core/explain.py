# core/explain.py

from __future__ import annotations
from typing import List
import pandas as pd


def explain_rules(df_feat: pd.DataFrame, cluster_mean_row: pd.Series | None) -> List[str]:
    """
    Lý giải dựa trên feature chính của hướng B + so sánh mean cụm
    """
    r: List[str] = []

    x_spend = float(df_feat.get("LOG_TOTAL_SPENDING", pd.Series([0])).iloc[0])
    x_pay = float(df_feat.get("LOG_PAYMENTS", pd.Series([0])).iloc[0])
    x_minratio = float(df_feat.get("MINIMUM_PAYMENTS_RATIO", pd.Series([0])).iloc[0])
    x_freq = float(df_feat.get("PURCHASES_FREQUENCY", pd.Series([0])).iloc[0])

    if x_spend >= 8.0:
        r.append("Tổng chi tiêu (LOG_TOTAL_SPENDING) **cao** → khách chi tiêu lớn.")
    elif x_spend <= 6.0:
        r.append("Tổng chi tiêu (LOG_TOTAL_SPENDING) **thấp** → khách chi tiêu ít.")

    if x_pay >= 8.0:
        r.append("Thanh toán (LOG_PAYMENTS) **cao** → xu hướng trả nợ tốt.")
    elif x_pay <= 6.0:
        r.append("Thanh toán (LOG_PAYMENTS) **thấp** → xu hướng trả nợ yếu (rủi ro).")

    if x_minratio >= 0.3:
        r.append("Tỷ lệ trả tối thiểu (MINIMUM_PAYMENTS_RATIO) **cao** → áp lực trả nợ cao.")
    elif x_minratio <= 0.1:
        r.append("Tỷ lệ trả tối thiểu (MINIMUM_PAYMENTS_RATIO) **thấp** → áp lực trả nợ thấp.")

    if x_freq >= 0.7:
        r.append("Tần suất mua sắm (PURCHASES_FREQUENCY) **cao** → mua sắm thường xuyên.")
    elif x_freq <= 0.3:
        r.append("Tần suất mua sắm (PURCHASES_FREQUENCY) **thấp** → ít giao dịch mua sắm.")

    if cluster_mean_row is not None:
        def cmp(col: str, label: str):
            if col in df_feat.columns and col in cluster_mean_row.index:
                a = float(df_feat[col].iloc[0])
                b = float(cluster_mean_row[col])
                if a > b:
                    r.append(f"{label} **cao hơn** trung bình cụm.")
                elif a < b:
                    r.append(f"{label} **thấp hơn** trung bình cụm.")

        cmp("LOG_TOTAL_SPENDING", "Chi tiêu")
        cmp("LOG_PAYMENTS", "Thanh toán")
        cmp("LOG_CREDIT_LIMIT", "Hạn mức")
        cmp("MINIMUM_PAYMENTS_RATIO", "Tỷ lệ trả tối thiểu")
        cmp("PURCHASES_FREQUENCY", "Tần suất mua sắm")

    return r[:8]
