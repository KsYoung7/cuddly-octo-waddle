import requests
import json
import time
import random
import pandas as pd
from tqdm import tqdm
import os
import sys

# 将项目根目录添加到sys.path（假设weibo_spider.py位于crawler目录下）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from config import RAW_DATA_DIR, COOKIES_PATH

class WeiboSpider:
    def __init__(self, keywords, max_pages=50, sleep=2):
        self.keywords = keywords
        self.max_pages = max_pages
        self.sleep = sleep
        if not os.path.exists(RAW_DATA_DIR):
            os.makedirs(RAW_DATA_DIR)
        self.session = requests.Session()
        self.cookies = self.load_cookies()

    def load_cookies(self):
        with open(COOKIES_PATH, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        if isinstance(cookies, dict):
            return cookies
        return {c['name']: c['value'] for c in cookies}

    def search(self):
        all_results = []
        for keyword in self.keywords:
            print(f"正在爬取关键词: {keyword}")
            for page in tqdm(range(1, self.max_pages + 1)):
                url = (f"https://weibo.com/ajax/statuses/search?containerid=100103type=1&q={keyword}&page={page}")
                headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "https://weibo.com/"
                }
                try:
                    resp = self.session.get(url, headers=headers, cookies=self.cookies, timeout=10)
                    print(f"[DEBUG] 第{page}页返回内容前200字：{resp.text[:200]}")
                    data = resp.json()
                    # v4接口：statuses为主内容列表
                    statuses = data.get("statuses", [])
                    if not statuses:
                        print(f"[INFO] 未获取到数据，提前结束 {keyword} 的抓取。")
                        break
                    else:
                        print(f"[INFO] 本页共获取到 {len(statuses)} 条微博。")
                    for status in statuses:
                        user = status.get("user", {})
                        all_results.append({
                            "id": status.get("idstr", ""),
                            "text": status.get("text", ""),
                            "created_at": status.get("created_at", ""),
                            "user_id": user.get("id", ""),
                            "user_name": user.get("screen_name", ""),
                            "attitudes_count": status.get("attitudes_count", 0),
                            "comments_count": status.get("comments_count", 0),
                            "reposts_count": status.get("reposts_count", 0),
                            "source": status.get("source", ""),
                        })
                    time.sleep(self.sleep + random.random())
                except Exception as e:
                    print(f"抓取失败: {e}")
                    break
        if all_results:
            df = pd.DataFrame(all_results)
            out_path = os.path.join(RAW_DATA_DIR, "weibo_gaokao_english_2025.csv")
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
            print(f"数据已保存到 {out_path}")
        else:
            print("未抓取到任何数据，请检查Cookie、接口或关键词。")

if __name__ == "__main__":
    keywords = ["高考 英语", "2025高考 英语", "高考英语作文", "高考英语难度", "高考英语评论"]
    spider = WeiboSpider(keywords, max_pages=30, sleep=1.5)
    spider.search()