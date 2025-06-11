# ev_model.py
def generate_recommendation(match_data):
    '''
    简化版推荐模型（仅逻辑原型）
    输入: match_data = {
        'match': 'Team A vs Team B',
        'total_line': 186.5,
        'odds': 1.82,
        'home_full_strength': True,
        'away_injury': False
    }
    返回: match, market, ev, reason
    '''

    match = match_data["match"]
    total_line = match_data["total_line"]
    odds = match_data["odds"]
    home_full_strength = match_data["home_full_strength"]
    away_injury = match_data["away_injury"]

    # 简易逻辑：盘口高 & 阵容齐整 → 小分有EV
    if total_line >= 186 and home_full_strength:
        prediction_winrate = 0.6  # 假设60%胜率下注小分
        ev = (prediction_winrate * odds) - 1
        if ev >= 0.03:
            return match, f"小{total_line} @{odds}", round(ev, 4), "盘口高开，主力齐整"

    # 或者主力缺阵 → 推荐打穿主队（+受让盘）
    if away_injury:
        prediction_winrate = 0.58
        alt_odds = 1.90
        ev = (prediction_winrate * alt_odds) - 1
        if ev >= 0.03:
            return match, "主队 -4.5 @1.90", round(ev, 4), "客队核心缺阵，主队有穿盘优势"

    return None, None, 0.0, "暂无推荐"
