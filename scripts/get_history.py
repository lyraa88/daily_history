from googletrans import Translator
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://history.muffinlabs.com/date")

today = datetime.date.today()
month, day = today.month, today.day
date_str = today.isoformat()

url = f"{BASE_URL}/{month}/{day}"
response = requests.get(url)
data = response.json()
events = data["data"]["Events"]

translator = Translator()

# README 상단 소개글 (고정 설명)
header = f"""

이 레포지토리는 [MuffinLabs의 History API](https://history.muffinlabs.com/date)로부터  
**매일 00:00(KST)** 기준으로 데이터를 가져와 자동으로 업데이트됩니다.

5개의 주요 역사적 사건이 한국어로 번역되어 요약되며, 원본 출처는 Wikipedia입니다.

---

## 📅 과거 **{data['date']}**에 일어난 주요 사건들

---
"""

# 본문 내용
body_lines = []
for event in events[:5]:
    year = event["year"]
    text = event["text"]
    link = event["links"][0]["link"] if event["links"] else ""
    try:
        translated_text = translator.translate(text, dest='ko').text
    except Exception as e:
        print("번역 실패:", e)
        translated_text = text

    body_lines.append(f"**{year}년**")
    body_lines.append(f"- {translated_text}  [Wikipedia]({link})\n")

#  파일로 저장
output_text = header + "\n".join(body_lines)

Path("data").mkdir(exist_ok=True)
Path(f"data/history_{date_str}.md").write_text(output_text, encoding="utf-8")
Path("README.md").write_text(output_text, encoding="utf-8")
