import streamlit as st
from wechat_push import send_push

st.set_page_config(page_title="NBL1 + NZ NBL 自动EV监听系统", layout="wide")

st.title("🏀 NBL1 + NZ NBL 自动EV监听系统")
st.markdown("✅ 系统已启动，监听开启，推送方式：Server酱")

st.subheader("📅 今日比赛监控任务状态")
st.info("系统会根据设定频率监听名单与盘口，一旦 EV ≥ 3% 则立即推送推荐。")

# 模拟推荐内容（后续可接入真实模型）
match = "Waverley vs Diamond Valley"
market = "小186.5 @1.82"
ev = 0.613
reason = "盘口高开，主力在阵，构成强EV"

if st.button("🔔 立即手动测试一次真实推送"):
    st.success("✅ 模拟推荐已生成，准备推送...")
    content = f"推荐方向：{market}\n理由：{reason}"
    success = send_push(f"NBL推荐 - {match}", content, ev, method="serverchan")
    if success:
        st.success("📤 推送已发送（Server酱）")
    else:
        st.error("❌ 推送失败，请检查日志")
