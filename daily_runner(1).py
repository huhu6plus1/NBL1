# daily_runner.py
import datetime
from match_fetcher import fetch_today_matches
from ev_model import generate_recommendation
from logger import log_recommendation
from wechat_push import send_push

def daily_run():
    print(f"📅 开始每日推荐扫描任务 @ {datetime.datetime.now()}")
    matches = fetch_today_matches()
    for game in matches:
        match, market, ev, reason = generate_recommendation(game)
        if match and ev >= 0.03:
            content = f"推荐方向：{market}\n理由：{reason}"
            pushed = send_push(f"NBL推荐 - {match}", content, ev, method="serverchan")
            log_recommendation(match, market, ev, pushed=pushed)
            print(f"✅ 推送完成：{match} - {market} (EV={ev:.2%})")
        else:
            print(f"❌ 无推荐：{game['match']}")
    print("📤 全部比赛扫描完成")

if __name__ == "__main__":
    daily_run()
