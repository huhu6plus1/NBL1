import json
from datetime import datetime
import os

LOG_PATH = "logs/recommendations.jsonl"

# 更安全地创建 logs 文件夹（避免 FileExistsError）
if not os.path.exists("logs"):
    os.mkdir("logs")
elif not os.path.isdir("logs"):
    raise RuntimeError("🚫 'logs' 已存在但不是文件夹，请手动删除该文件后重试")

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
