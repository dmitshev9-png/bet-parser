# ==========================================
# BETTINGTIPS PARSER API (LIGHT VERSION)
# ==========================================

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def get_tips():
    try:
        url = "https://bettingtips1x2.com"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        tips = []

        # ищем блоки с прогнозами
        tip_blocks = soup.select(".tipsDiv")

        for block in tip_blocks:
            matches = block.find_all("strong")
            for m in matches:
                text = m.get_text(strip=True)
                if text:
                    tips.append(text)

        return tips if tips else ["No tips found"]

    except Exception as e:
        return [f"ERROR: {str(e)}"]


@app.route("/")
def home():
    return "Parser is working 🚀"


@app.route("/tips")
def tips():
    return jsonify(get_tips())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)