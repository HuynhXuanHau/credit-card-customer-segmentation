from __future__ import annotations
from typing import Dict, Any

import numpy as np
import pandas as pd
import streamlit as st

from core.model_io import load_all
from core.features import feature_engineering_B
from core.explain import explain_rules
from core.constants import (
    RAW_NEEDED,
    CLUSTER_LABELS_VI,
    ADVANCED_HELP,
    SAMPLE_HEADER,
)


# =========================================================
# PAGE
# =========================================================
st.set_page_config(page_title="Phân khúc khách hàng thẻ tín dụng", layout="wide")

st.title("PHÂN KHÚC KHÁCH HÀNG THẺ TÍN DỤNG")
st.markdown("SV:Nguyễn Đình Trường & Huỳnh Xuân Hậu — **GVHD:** TS Nguyễn Sĩ Thìn")

model = load_all()

st.sidebar.header("Nhập dữ liệu khách hàng")

input_mode = st.sidebar.radio(
    "Chọn cách nhập:",
    ["Nhập tay", "Dán từ Excel"]
)


# =========================================================
# 1) INPUT
# =========================================================
if input_mode == "Nhập tay":
    st.sidebar.subheader("Thông tin chính")

    BALANCE = st.sidebar.number_input("BALANCE (Dư nợ)", min_value=0.0, value=3000.0, step=100.0)
    CREDIT_LIMIT = st.sidebar.number_input("CREDIT_LIMIT (Hạn mức)", min_value=1.0, value=10000.0, step=500.0)
    PAYMENTS = st.sidebar.number_input("PAYMENTS (Tổng thanh toán)", min_value=0.0, value=3000.0, step=100.0)

    PURCHASES = st.sidebar.number_input("PURCHASES (Tổng mua sắm)", min_value=0.0, value=5000.0, step=100.0)
    CASH_ADVANCE = st.sidebar.number_input("CASH_ADVANCE (Rút tiền)", min_value=0.0, value=500.0, step=100.0)

    ONEOFF_PURCHASES = st.sidebar.number_input("ONEOFF_PURCHASES (Mua 1 lần)", min_value=0.0, value=2000.0, step=100.0)
    INSTALLMENTS_PURCHASES = st.sidebar.number_input("INSTALLMENTS_PURCHASES (Trả góp)", min_value=0.0, value=1000.0, step=100.0)

    MINIMUM_PAYMENTS = st.sidebar.number_input("MINIMUM_PAYMENTS (Trả tối thiểu)", min_value=0.0, value=500.0, step=50.0)
    TENURE = st.sidebar.number_input("TENURE (Số tháng dùng thẻ)", min_value=1, value=12, step=1)

    with st.sidebar.expander("Hành vi (nâng cao)"):
        BALANCE_FREQUENCY = st.slider(
            "BALANCE_FREQUENCY", 0.0, 1.0, 0.5, 0.05,
            help=ADVANCED_HELP["BALANCE_FREQUENCY"]
        )
        PURCHASES_FREQUENCY = st.slider(
            "PURCHASES_FREQUENCY", 0.0, 1.0, 0.5, 0.05,
            help=ADVANCED_HELP["PURCHASES_FREQUENCY"]
        )
        ONEOFF_PURCHASES_FREQUENCY = st.slider(
            "ONEOFF_PURCHASES_FREQUENCY", 0.0, 1.0, 0.3, 0.05,
            help=ADVANCED_HELP["ONEOFF_PURCHASES_FREQUENCY"]
        )
        PURCHASES_INSTALLMENTS_FREQUENCY = st.slider(
            "PURCHASES_INSTALLMENTS_FREQUENCY", 0.0, 1.0, 0.3, 0.05,
            help=ADVANCED_HELP["PURCHASES_INSTALLMENTS_FREQUENCY"]
        )
        CASH_ADVANCE_FREQUENCY = st.slider(
            "CASH_ADVANCE_FREQUENCY", 0.0, 1.0, 0.1, 0.05,
            help=ADVANCED_HELP["CASH_ADVANCE_FREQUENCY"]
        )

        CASH_ADVANCE_TRX = st.number_input(
            "CASH_ADVANCE_TRX", min_value=0, value=1, step=1,
            help=ADVANCED_HELP["CASH_ADVANCE_TRX"]
        )
        PURCHASES_TRX = st.number_input(
            "PURCHASES_TRX", min_value=0, value=10, step=1,
            help=ADVANCED_HELP["PURCHASES_TRX"]
        )
        PRC_FULL_PAYMENT = st.slider(
            "PRC_FULL_PAYMENT", 0.0, 1.0, 0.4, 0.05,
            help=ADVANCED_HELP["PRC_FULL_PAYMENT"]
        )

    df_input = pd.DataFrame([{
        "BALANCE": BALANCE,
        "CREDIT_LIMIT": CREDIT_LIMIT,
        "PAYMENTS": PAYMENTS,
        "MINIMUM_PAYMENTS": MINIMUM_PAYMENTS,
        "TENURE": TENURE,
        "PURCHASES": PURCHASES,
        "CASH_ADVANCE": CASH_ADVANCE,
        "ONEOFF_PURCHASES": ONEOFF_PURCHASES,
        "INSTALLMENTS_PURCHASES": INSTALLMENTS_PURCHASES,

        "BALANCE_FREQUENCY": BALANCE_FREQUENCY,
        "PURCHASES_FREQUENCY": PURCHASES_FREQUENCY,
        "ONEOFF_PURCHASES_FREQUENCY": ONEOFF_PURCHASES_FREQUENCY,
        "PURCHASES_INSTALLMENTS_FREQUENCY": PURCHASES_INSTALLMENTS_FREQUENCY,
        "CASH_ADVANCE_FREQUENCY": CASH_ADVANCE_FREQUENCY,
        "CASH_ADVANCE_TRX": CASH_ADVANCE_TRX,
        "PURCHASES_TRX": PURCHASES_TRX,
        "PRC_FULL_PAYMENT": PRC_FULL_PAYMENT,
    }])

else:
    st.sidebar.subheader("Dán 1 dòng từ Excel (có header)")
    st.sidebar.caption("Copy từ Excel rồi paste vào ô dưới (tab-separated).")

    st.sidebar.code(SAMPLE_HEADER, language="text")
    pasted = st.sidebar.text_area("Dán vào đây (1 dòng header + 1 dòng value)", height=140)

    df_input = None
    if pasted.strip():
        try:
            from io import StringIO
            df_tmp = pd.read_csv(StringIO(pasted), sep="\t")
            if len(df_tmp) < 1:
                raise ValueError("Không đọc được dữ liệu.")
            df_input = df_tmp.iloc[[0]].copy()

            # chỉ giữ các cột cần thiết cho bài toán
            for c in RAW_NEEDED:
                if c not in df_input.columns:
                    df_input[c] = 0.0
            df_input = df_input[RAW_NEEDED].copy()

        except Exception as e:
            st.sidebar.error(f"Lỗi parse dữ liệu Excel: {e}")

    if df_input is None:
        st.info("Hãy dán dữ liệu theo format: 1 dòng header + 1 dòng giá trị.")
        st.stop()


# =========================================================
# 2) PREDICT
# =========================================================
do_predict = st.sidebar.button("Dự đoán", type="primary")
left, right = st.columns([1, 1])

if not do_predict:
    st.info("Chọn cách nhập ở sidebar, nhập dữ liệu rồi bấm **Dự đoán**.")
    st.stop()

try:
    df_all = feature_engineering_B(df_input)

    fe_cols = model["fe_cols"]
    for c in fe_cols:
        if c not in df_all.columns:
            df_all[c] = 0.0
    df_fe = df_all[fe_cols].copy()

    scaler = model["scaler"]
    kmeans = model["kmeans"]

    # FIX mismatch feature names (kể cả trường hợp scaler fit có 'Cluster')
    if hasattr(scaler, "feature_names_in_"):
        expected_cols = list(scaler.feature_names_in_)
        for c in expected_cols:
            if c not in df_fe.columns:
                df_fe[c] = 0.0
        df_fe = df_fe.reindex(columns=expected_cols, fill_value=0.0)
    else:
        df_fe = df_fe.reindex(columns=fe_cols, fill_value=0.0)

    X = scaler.transform(df_fe)
    distances = kmeans.transform(X)[0]
    cluster_id = int(np.argmin(distances))

    # confidence
    logits = -distances
    logits = logits - np.max(logits)
    probs = np.exp(logits) / (np.sum(np.exp(logits)) + 1e-12)
    confidence = float(probs[cluster_id])

except Exception as e:
    st.error(f"Lỗi dự đoán: {e}")
    st.stop()


# =========================================================
# 3) OUTPUT
# =========================================================
with left:
    st.subheader("Kết quả dự đoán")
    st.success(f"Phân khúc: **{CLUSTER_LABELS_VI.get(cluster_id, f'Cụm {cluster_id}')}**")
    st.info(f"Độ tin cậy (distance-based): **{confidence * 100:.2f}%**")

    with st.expander("Khoảng cách tới các centroid"):
        ddf = pd.DataFrame({
            "Cluster": np.arange(len(distances)),
            "Distance": distances
        }).sort_values("Distance")
        st.dataframe(ddf, use_container_width=True)

    st.markdown("### Input (cột dùng để tính feature)")
    keep_in = [c for c in RAW_NEEDED if c in df_input.columns]
    st.dataframe(df_input[keep_in], use_container_width=True)


with right:
    st.subheader("Phân tích")

    st.markdown("### Feature sau xử lý (cột model dùng)")
    show_cols = model["fe_cols"]
    st.dataframe(df_all[show_cols], use_container_width=True)

    st.markdown("### So sánh Input vs Hồ sơ cụm (cluster mean)")
    profile = model.get("cluster_profile")
    cluster_mean_row = None

    if profile is not None and "Cluster" in profile.columns:
        row_c = profile[profile["Cluster"] == cluster_id]
        if len(row_c) == 1:
            row_c = row_c.drop(columns=["Cluster"])
            compare_cols = [c for c in show_cols if c in row_c.columns]
            cluster_mean_row = row_c.iloc[0]

            cmp = pd.DataFrame({
                "Input": df_all[compare_cols].iloc[0].values,
                "Trung bình cụm": row_c[compare_cols].iloc[0].values
            }, index=compare_cols)
            st.bar_chart(cmp)
        else:
            st.warning("Không tìm thấy dòng cụm tương ứng trong cluster_profile.csv.")
    else:
        st.caption("Chưa có cluster_profile.csv (không bắt buộc).")

    st.markdown("### Lý giải vì sao vào cụm này")
    reasons = explain_rules(df_all, cluster_mean_row)
    if reasons:
        for r in reasons:
            st.write(f"- {r}")
    else:
        st.write("- Các chỉ số ở mức trung bình; mô hình quyết định dựa trên tổng hợp nhiều feature.")

st.divider()
