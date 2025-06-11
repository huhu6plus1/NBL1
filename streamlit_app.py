import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from wechat_push import send_push

st.set_page_config(page_title="NBL 自动EV监听系统", layout="wide")

st.title("🏀 NBL1 + NZ NBL 自动EV监听系统 v2.0")
st.caption("🔧 包含：监听+推送+推荐记录+赛果回查")

# ========== 1. 系统状态与推送测试 ==========
st.header("🟢 系统状态与测试推送")

st.markdown("✅ 当前监听运行中。点击下方按钮模拟生成推荐并进行真实推送（Server酱）")

if st.button("🔔 测试推荐并推送"):
    match = "Waverley vs Diamond Valley"
    market = "小186.5 @1.82"
    ev = 0.613
    reason = "盘口高开，主力在阵，构成强EV"
    content = f"推荐方向：{market}\n理由：{reason}"
    success = send_push(f"NBL推荐 - {match}", content, ev, method="serverchan")
    if success:
        st.success("✅ 推送已发送，请在微信中确认")
    else:
        st.error("❌ 推送失败，请检查配置")

# ========== 2. 最近推荐记录 ==========
st.header("📋 最近推荐记录")

log_path = "logs/recommendations.jsonl"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-10:]  # 显示最近10条
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

        # 模拟命中判断（仅展示结构）
        if os.path.exists(log_path):
            logs = [json.loads(l) for l in open(log_path)]
            for log in logs:
                row = results_df[results_df["match"] == log["match"]]
                if not row.empty:
                    # 简单判断命中（仅示例）
                    hit = "小" in log["market"] and int(row.iloc[0]["final_score"]) < 186.5
                    log["hit"] = hit
            st.success("🏁 命中判断完成，未来可扩展统计 ROI")
        else:
            st.warning("找不到推荐记录，无法对比")
    else:
        st.error("❌ 缺少必要字段：match 和 final_score")

# ========== 4. ROI 图表（占位） ==========
st.header("📈 ROI趋势图（开发中）")
st.markdown("📊 即将支持：单位时间 ROI 走势、联赛分布、推荐类型效率对比图")
