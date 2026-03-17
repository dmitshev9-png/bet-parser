# ==========================================
# BETTINGTIPS PARSER API
# будет запускаться на Render
# ==========================================

from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def get_tips():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://bettingtips1x2.com", timeout=60000)
        page.wait_for_timeout(8000)

        tips = page.locator(".tipsDiv p strong").all_text_contents()

        browser.close()
        return tips

@app.route("/")
def home():
    return "Parser is working 🚀"

@app.route("/tips")
def tips():
    return jsonify(get_tips())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)