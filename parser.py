# ==========================================
# BETTINGTIPS PARSER API (STABLE REQUESTS VERSION)
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
            "User-Agent": "Mozilla/5.0",
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            return [f"HTTP ERROR: {response.status_code}"]

        soup = BeautifulSoup(response.text, "html.parser")

        tips = []

        # 🔥 ищем все блоки Today's Predictions
        prediction_blocks = soup.find_all("strong", string="Today's Predictions:")

        if not prediction_blocks:
            return ["ERROR: Predictions not found"]

        for block in prediction_blocks:
            # берём следующий элемент после strong
            current = block.next_sibling

            # проходим по следующим элементам
            while current:
                if current.name == "br":
                    current = current.next_sibling
                    continue

                # если дошли до следующего блока — стоп
                if current.name == "div":
                    break

                if isinstance(current, str):
                    text = current.strip()

                    # фильтр матчей
                    if text and ":" in text and "-" in text:
                        tips.append(text)

                current = current.next_sibling

        return tips if tips else ["ERROR: No matches found"]

    except Exception as e:
        return [f"ERROR: {str(e)}"]