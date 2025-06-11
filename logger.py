import json
from datetime import datetime
import os

LOG_PATH = "logs/recommendations.jsonl"
os.makedirs("logs", exist_ok=True)

def log_recommendation(match, market, ev, pushed=True):
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "match": match,
        "market": market,
        "ev": ev,
        "pushed": pushed
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
    print("✅ 推荐记录已写入日志")
