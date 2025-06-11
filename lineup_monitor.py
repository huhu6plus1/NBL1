# lineup_monitor.py
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from ev_model import generate_recommendation
from wechat_push import send_push
from logger import log_recommendation

# 示例主力名单（实际可替换为球员数据库或动态列表）
KEY_PLAYERS = {
    "Waverley": ["Khalil Shabazz", "Michael Harper", "Mason Forbes"],
    "Diamond Valley": ["Jock Perry", "Adam Thoseby", "Noah Todd"]
}

def fetch_lineup(game_url):
    try:
        r = requests.get(game_url, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        names = [td.get_text(strip=True) for td in soup.select("table td") if td.get_text()]
        return names
    except Exception as e:
        print("名单抓取失败:", e)
        return []

def monitor_game_lineup(game_info):
    match = game_info["match"]
    game_url = game_info.get("game_url")
    start_time = datetime.strptime(game_info["start_time"], "%Y-%m-%d %H:%M")
    print(f"🎯 开始监听：{match} @ {start_time}")

    detected = False
    while True:
        now = datetime.utcnow() + timedelta(hours=10)  # AEST时间
        seconds_left = (start_time - now).total_seconds()

        if seconds_left <= 0:
            print("⛔ 比赛已开始，停止监听")
            break
        elif seconds_left <= 900:
            freq = 20
        elif seconds_left <= 1800:
            freq = 60
        else:
            break  # 未到监听窗口

        lineup = fetch_lineup(game_url)
        print(f"👀 抓到 {len(lineup)} 人名单")

        for team, players in KEY_PLAYERS.items():
            for p in players:
                if not any(p in name for name in lineup):
                    print(f"⚠️ 检测到主力缺阵: {team} - {p}")
                    game_info["home_full_strength"] = team not in match
                    game_info["away_injury"] = team in match
                    match, market, ev, reason = generate_recommendation(game_info)
                    if ev >= 0.03:
                        content = f"名单更新后推荐：{market}\n理由：{reason}"
                        pushed = send_push(f"名单变动推荐 - {match}", content, ev)
                        log_recommendation(match, market, ev, pushed)
                    detected = True
                    break
            if detected:
                break

        if detected:
            break

        time.sleep(freq)
