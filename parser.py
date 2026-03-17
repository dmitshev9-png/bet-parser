# ==========================================
# BETTINGTIPS PARSER API
# ==========================================

from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

def get_tips():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-setuid-sandbox"
                ]
            )

            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            # 🔥 правильный goto
            page.goto(
                "https://bettingtips1x2.com",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # даём странице прогрузиться
            page.wait_for_timeout(5000)

            # 🔥 правильный селектор
            tips = page.locator(".tipsDiv strong").all_text_contents()

            browser.close()
            return tips

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