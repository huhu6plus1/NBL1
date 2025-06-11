# 推荐日志记录模块
import json
from datetime import datetime

LOG_FILE = "logs/recommendations.jsonl"

def log_recommendation(data):
    data["timestamp"] = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
