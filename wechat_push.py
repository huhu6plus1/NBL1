import requests

def send_push(title, content, ev_value, method='serverchan'):
    if method == 'serverchan':
        key = 'SCT282237TA-4sseGxqm4WrkvefyZLDe53M0'
        url = f'https://sctapi.ftqq.com/{key}.send'
        data = {
            "title": title,
            "desp": f"{content}\n\nEV值：{ev_value:.2%}"
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Server酱推送成功")
                return True
            else:
                print(f"❌ 推送失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"❌ 推送异常：{e}")
    else:
        print("⚠️ 当前为非Server酱模式，未发送。")
    return False
