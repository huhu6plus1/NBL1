# daily_runner.py
import datetime
from ev_model import generate_recommendation
from logger import log_recommendation
from wechat_push import send_push

# 示例：今日比赛列表（后续由 match_fetcher 自动生成）
today_matches = [
    {
        "match": "Waverley vs Diamond Valley",
        "total_line": 186.5,
        "odds": 1.82,
        "home_full_strength": True,
        "away_injury": False
    },
    {
        "match": "Auckland vs Taranaki",
        "total_line": 181.5,
        "odds": 1.85,
        "home_full_strength": False,
        "away_injury": True
    }
]

def daily_run():
    print(f"📅 开始每日推荐扫描任务 @ {datetime.datetime.now()}")
    for game in today_matches:
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
