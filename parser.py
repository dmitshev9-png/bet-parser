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
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        tips = []

        blocks = soup.select(".tipsDiv")

        for block in blocks:
            text = block.get_text(separator="\n", strip=True)

            if "Today's Predictions" in text:
                lines = text.split("\n")

                for line in lines:
                    if ":" in line and "-" in line:
                        tips.append(line)

        return tips if tips else ["No tips found"]

    except Exception as e:
        return [f"ERROR: {str(e)}"]