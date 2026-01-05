# core/model_io.py

from __future__ import annotations
from typing import Dict, Any
import pandas as pd
import streamlit as st
import joblib


@st.cache_resource
def load_all() -> Dict[str, Any]:
    scaler = joblib.load("scaler.pkl")
    kmeans = joblib.load("kmeans.pkl")
    fe_cols = joblib.load("fe_cols.pkl")
    cluster_profile = None
    try:
        cluster_profile = pd.read_csv("cluster_profile.csv")
    except Exception:
        cluster_profile = None

    return {
        "scaler": scaler,
        "kmeans": kmeans,
        "fe_cols": list(fe_cols),
        "cluster_profile": cluster_profile
    }
