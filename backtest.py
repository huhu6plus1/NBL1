# 推荐回查模块（简化版）
import json

def load_logs(path="logs/recommendations.jsonl"):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def match_result(recommendation, actual_score):
    # 比较推荐方向是否命中（需手动录入赛果）
    # 示例略，仅做框架用途
    return True if "小" in recommendation["content"] else False
