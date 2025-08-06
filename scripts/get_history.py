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

lines = [f"## 📅 과거 {data['date']}\n에 일어난 일은?"]

for event in events[:5]:
    year = event["year"]
    text = event["text"]
    link = event["links"][0]["link"] if event["links"] else ""
    try:
        translated_text = translator.translate(text, dest='ko').text
    except Exception as e:
        print("번역 실패:", e)
        translated_text = text

    lines.append(f"**{year}년**")
    lines.append(f"- {translated_text}  [Wikipedia]({link})\n")

Path("data").mkdir(exist_ok=True)
Path(f"data/history_{date_str}.md").write_text("\n".join(lines), encoding="utf-8")
Path("README.md").write_text("\n".join(lines), encoding="utf-8")
