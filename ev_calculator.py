# 简化版 EV 计算器（真实项目中应基于预测模型 + 盘口）
def calculate_ev(match):
    # 模拟EV计算结果
    return {
        "timestamp": "2025-06-12T14:00:00",
        "league": match.get("league", "NZNBL"),
        "match": match["match"],
        "bet_type": "小分",
        "line": 182.5,
        "odds": 1.85,
        "ev": 6.3,
        "confidence": "⭐⭐⭐",
        "recommendation": "小182.5@1.85",
        "status": "pending"
    }
