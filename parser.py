# ==========================================
# BETTINGTIPS PARSER API
# будет запускаться на Render
# ==========================================

from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def get_tips():
    import subprocess
    subprocess.run(["playwright", "install", "chromium"])

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

page.goto("https://bettingtips1x2.com", timeout=60000)
page.wait_for_load_state("networkidle")

        tips = page.locator("strong").all_text_contents()

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