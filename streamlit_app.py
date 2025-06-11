import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from wechat_push import send_push
from logger import log_recommendation
from ev_model import generate_recommendation

st.set_page_config(page_title="NBL 自动EV监听系统", layout="wide")
st.title("🏀 NBL1 + NZ NBL 自动EV监听系统 v2.2")

# ========== 1. 使用模型生成真实推荐 & 推送 & 写入日志 ==========
st.header("🟢 生成真实推荐 + 推送 + 写入记录")

# 示例输入数据（后续将来自比赛爬虫）
match_data = {
    "match": "Waverley vs Diamond Valley",
    "total_line": 186.5,
    "odds": 1.82,
    "home_full_strength": True,
    "away_injury": False
}

if st.button("🔔 运行推荐模型"):
    match, market, ev, reason = generate_recommendation(match_data)
    if market:
        st.success(f"✅ 推荐方向：{market}，EV={round(ev*100, 2)}%\n理由：{reason}")
        content = f"推荐方向：{market}\n理由：{reason}"
        success = send_push(f"NBL推荐 - {match}", content, ev, method="serverchan")
        log_recommendation(match, market, ev, pushed=success)
        if success:
            st.success("📤 推送成功 + 推荐记录已写入")
        else:
            st.error("⚠️ 推送失败，但记录已保存")
    else:
        st.warning("暂无推荐符合EV阈值（≥3%）")

# ========== 2. 最近推荐记录 ==========
st.header("📋 最近推荐记录")
log_path = "logs/recommendations.jsonl"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-10:]
        records = [json.loads(l) for l in lines]
        df = pd.DataFrame(records)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp", ascending=False)
        st.dataframe(df[["timestamp", "match", "market", "ev", "pushed"]])
else:
    st.warning("暂无推荐记录")

# ========== 3. 上传赛果，计算命中 ==========
st.header("✅ 上传赛果 → 判断推荐是否命中")
uploaded = st.file_uploader("上传赛果CSV（需包含 match, final_score 字段）", type=["csv"])
if uploaded:
    results_df = pd.read_csv(uploaded)
    if "match" in results_df.columns and "final_score" in results_df.columns:
        st.success("✅ 成功读取赛果数据")
        st.write(results_df.head())

        if os.path.exists(log_path):
            logs = [json.loads(l) for l in open(log_path)]
            for log in logs:
                row = results_df[results_df["match"] == log["match"]]
                if not row.empty:
                    hit = "小" in log["market"] and int(row.iloc[0]["final_score"]) < 186.5
                    log["hit"] = hit
            st.success("🏁 命中判断完成")
        else:
            st.warning("找不到推荐记录")
    else:
        st.error("❌ 缺少必要字段：match 和 final_score")

# ========== 4. ROI 趋势图 ==========
st.header("📈 ROI趋势图（占位）")
st.markdown("📊 即将支持：单位时间 ROI 走势、联赛分布、推荐类型ROI图表")
