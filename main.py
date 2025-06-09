
# app/main.py

import streamlit as st
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import threading
from config import SENDKEY

st.set_page_config(page_title="NBL1/NZNBL 自动EV监听系统", layout="wide")
st.title("🏀 NBL1 + NZNBL 自动盘口EV监听系统")

st.markdown("系统正在监听每日比赛出场名单，一旦发现正EV将自动推送微信提醒。")

# 示例比赛（真实项目中应由调度器动态加载）
example_games = [
    {
        "teams": "Mt Gambier vs Bendigo",
        "start_time": datetime.now() + timedelta(minutes=10),
        "url": "https://nbl1.com.au/game/mt-gambier-vs-bendigo",
        "last_lineup": []
    },
]

def check_lineup(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        players = soup.select(".player-name")
        return [p.text.strip() for p in players]
    except Exception:
        return []

def calculate_ev(prob, odds):
    implied = 1 / odds
    return prob - implied

def send_wechat_push(game_name, ev):
    title = f"【正EV提醒】{game_name}"
    content = f"比赛：{game_name}\nEV={ev:.2%}，立即关注投注时机"
    push_url = f"https://sctapi.ftqq.com/" + SENDKEY + ".send"
    requests.post(push_url, data={"title": title, "desp": content})

def monitor_game(game):
    game_start = game["start_time"]
    while datetime.now() < game_start:
        time_to_start = (game_start - datetime.now()).total_seconds()
        interval = 20 if time_to_start <= 900 else 300
        lineup = check_lineup(game["url"])
        if lineup and lineup != game["last_lineup"] and len(lineup) >= 5:
            ev = calculate_ev(0.55, 1.90)
            if ev > 0.03:
                send_wechat_push(game["teams"], ev)
                st.success(f"✅ 正EV推送：{game['teams']} EV={ev:.2%}")
            game["last_lineup"] = lineup
        time.sleep(interval)

# 启动监听线程（真实项目中为调度器动态加载所有比赛）
for g in example_games:
    threading.Thread(target=monitor_game, args=(g,), daemon=True).start()
