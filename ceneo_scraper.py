import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

product_code = "133893145"
page = 1
all_opinions = []

while True:
    url = f"https://www.ceneo.pl/{product_code}/opinie-{page}"
    response = requests.get(url)

    if response.status_code != 200:
        break

    page_dom = BeautifulSoup(response.text, "html.parser")

    opinions = page_dom.select("div.js_product-review:not(.user-post--highlight)")

    if not opinions:
        break

    for opinion in opinions:
        opinion_id = opinion["data-entry-id"]

        author = opinion.select_one("span.user-post__author-name").get_text(strip=True)

        recommendation_tag = opinion.select_one("span.user-post__author-recommendation > em")
        recommendation = recommendation_tag.get_text(strip=True) if recommendation_tag else "Brak"

        stars = opinion.select_one("span.user-post__score-count").get_text(strip=True)

        content = opinion.select_one("div.user-post__text").get_text(strip=True)

        features = opinion.select("div.review-feature__title")
        advantages = []
        disadvantages = []

        for feature in features:
            label = feature.get_text(strip=True)
            items = [
                item.get_text(strip=True)
                for item in feature.find_next_sibling("div").select("div.review-feature__item")
            ]

            if "Zalety" in label:
                advantages = items
            elif "Wady" in label:
                disadvantages = items

        useful = opinion.select_one("button.vote-yes")["data-total-vote"]
        unuseful = opinion.select_one("button.vote-no")["data-total-vote"]

        dates = opinion.select("span.user-post__published time")
        pub_date = dates[0]["datetime"] if len(dates) > 0 else None
        pur_date = dates[1]["datetime"] if len(dates) > 1 else None

        all_opinions.append({
            "id": opinion_id,
            "author": author,
            "recommendation": recommendation,
            "stars": stars,
            "content": content,
            "advantages": advantages,
            "disadvantages": disadvantages,
            "useful_count": useful,
            "unuseful_count": unuseful,
            "pub_date": pub_date,
            "pur_date": pur_date
        })

    # sprawdzamy czy jest next page
    next_page = page_dom.select_one("button.pagination__next")
    if not next_page:
        break

    page += 1


# zapis do pliku
if not os.path.exists("./opinions"):
    os.mkdir("./opinions")

with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
