# match_fetcher.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_today_matches():
    today = datetime.utcnow() + timedelta(hours=12)  # UTC+12 新西兰时间
    today_str = today.strftime("%Y-%m-%d")
    matches = []

    # --- NZ NBL ---
    try:
        nznbl_url = "https://nznbl.basketball"
        r = requests.get(nznbl_url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for div in soup.find_all("div", class_="elementor-heading-title"):
            text = div.get_text(strip=True)
            if "vs" in text:
                parent = div.find_parent("div", class_="elementor-widget-wrap")
                time_text = parent.find_next("div", class_="elementor-heading-title").get_text(strip=True)
                match_time = f"{today_str} {time_text}"
                matches.append({
                    "match": text,
                    "total_line": 182.5,
                    "odds": 1.85,
                    "home_full_strength": True,
                    "away_injury": False,
                    "start_time": match_time
                })
    except Exception as e:
        print("NZ NBL 抓取失败:", e)

    # --- NBL1 South 示例，仅结构占位 ---
    try:
        nbl1_url = "https://nbl1.com.au/fixtures"
        r = requests.get(nbl1_url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.find_all("a", href=True):
            if "/game?" in item["href"]:
                text = item.get_text(strip=True)
                if "vs" in text and today_str in item["href"]:
                    matches.append({
                        "match": text,
                        "total_line": 186.5,
                        "odds": 1.82,
                        "home_full_strength": True,
                        "away_injury": False,
                        "start_time": today_str + " 19:00"
                    })
    except Exception as e:
        print("NBL1 抓取失败:", e)

    return matches
