import requests
import os

def send_push(title, content, ev=None, method="serverchan"):
    if method == "serverchan":
        key = os.getenv("serverchan_key")  # 从 GitHub Secret 环境变量读取
        if not key:
            print("❌ [推送失败] Server酱 Key 未配置 (环境变量 serverchan_key)")
            return False
        url = f"https://sctapi.ftqq.com/{key}.send"
        data = {
            "title": title,
            "desp": content
        }
        try:
            res = requests.post(url, data=data)
            if res.status_code == 200:
                print("✅ 推送成功")
                return True
            else:
                print("❌ 推送失败，状态码:", res.status_code)
                return False
        except Exception as e:
            print("❌ 推送异常:", str(e))
            return False
