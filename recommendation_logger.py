import json
from datetime import datetime

def log_recommendation(rec, file_path="logs/recommendations.jsonl"):
    rec["timestamp"] = datetime.utcnow().isoformat()
    with open(file_path, "a") as f:
        f.write(json.dumps(rec) + "\n")
