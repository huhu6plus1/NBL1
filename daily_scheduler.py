# 每日定时调度器（示意）
from datetime import datetime

def should_run_scan(current_time):
    # 示例：每天09:00触发一次
    return current_time.hour == 9 and current_time.minute == 0
