from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def get_tips():
    try:
        url = "https://bettingtips1x2.com/tipsters.html"

        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://bettingtips1x2.com/",
        }

        session = requests.Session()
        session.headers.update(headers)

        # 🔥 ШАГ 1 — заходим на главную (получаем cookies)
        session.get("https://bettingtips1x2.com")

        # 🔥 ШАГ 2 — идём на нужную страницу
        response = session.get(url, timeout=30)

        if response.status_code != 200:
            return [f"HTTP ERROR: {response.status_code}"]

        soup = BeautifulSoup(response.text, "html.parser")

        tips = []

        prediction_blocks = soup.find_all("strong", string="Today's Predictions:")

        if not prediction_blocks:
            return ["ERROR: Predictions not found"]

        for block in prediction_blocks:
            current = block.next_sibling

            while current:
                if current.name == "br":
                    current = current.next_sibling
                    continue

                if current.name == "div":
                    break

                if isinstance(current, str):
                    text = current.strip()

                    if text and ":" in text and "-" in text:
                        tips.append(text)

                current = current.next_sibling

        return tips if tips else ["ERROR: No matches found"]

    except Exception as e:
        return [f"ERROR: {str(e)}"]


@app.route("/")
def home():
    return "Parser is working 🚀"


@app.route("/tips")
def get_tips_api():
    return jsonify(get_tips())