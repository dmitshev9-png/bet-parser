# ==========================================
# BETTINGTIPS PARSER API
# будет запускаться на Render
# ==========================================

from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_tipsters():

    url = "https://www.bettingtips1x2.com/tipsters.html"

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, timeout=60000)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    matches = []

    lines = soup.get_text().split("\n")

    for line in lines:

        if ":" in line and "-" in line:

            matches.append(line.strip())

    return matches


@app.route("/tipsters")
def tipsters():

    data = get_tipsters()

    return jsonify(data)


@app.route("/")
def home():

    return "Bet Parser running"


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)