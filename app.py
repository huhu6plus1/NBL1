import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="NBL 自动EV系统", layout="wide")
st.title("🏀 NBL1 + NZNBL 自动EV监听系统 v2.2")

st.markdown("🟢 生成真实推荐 + 推送 + 写入记录")

LOG_FILE = "logs/recommendations.jsonl"

# 尝试读取推荐记录
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        records = [json.loads(line) for line in lines if line.strip()]
    if records:
        df = pd.DataFrame(records)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.subheader("📄 最近推荐记录")
        st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
    else:
        st.warning("暂无推荐记录")
else:
    st.error("未找到推荐记录文件 logs/recommendations.jsonl")
