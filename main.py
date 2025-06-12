from ev_calculator import calculate_ev
from recommendation_logger import log_recommendation
from lineup_monitor import check_lineups

# 示例调度流程（用于计划任务或手动执行）
if __name__ == "__main__":
    print("🎯 正在扫描今日比赛并生成推荐...")
    matches = check_lineups()
    for match in matches:
        ev_info = calculate_ev(match)
        if ev_info["ev"] >= 3.0:
            log_recommendation(ev_info)
            print(f"✅ 推荐生成: {ev_info['match']} -> {ev_info['recommendation']} (EV: {ev_info['ev']}%)")
