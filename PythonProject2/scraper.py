import os
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date

today = date.today()
headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}
url1="https://pokemoncardprices.io/top-100-pokemon-cards"
url2="https://pokemoncardprices.io/top-100-pokemon-cards?page=2"
url3="https://pokemoncardprices.io/top-100-pokemon-cards?page=3"
url4="https://pokemoncardprices.io/top-100-pokemon-cards?page=4"


def scraper(URL):
    driver = webdriver.Chrome()  #odpala wyszukiwarke
    driver.get(URL)
    time.sleep(3)
    html = driver.page_source

    #response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', {"data-slot": "card-content"})

    card_list = []

    for card in cards:

        label_name = card.find("span", string="NAME:")
        name = label_name.find_next("h3").text.strip() if label_name else None

        label_set = card.find("span", string="SET:")
        set= label_set.find_next("span").text.strip() if label_set else None

        label_number = card.find("span", string="NUMBER:")
        number = label_number.find_next("span").text.strip() if label_number else None

        label_rarity = card.find("span", string="RARITY:")
        rarity = label_rarity.find_next("span").text.strip() if label_rarity else None

        label_price1st = card.find("span", string="1st Edition Holofoil")
        if label_price1st:
            next_span = label_price1st.find_next("span")
            if next_span and "$" in next_span.text:
                price1st = next_span.text.strip("$")
        else :
            price1st = None

        label_priceUnHolo = card.find("span", string="Unlimited Holofoil")
        if label_priceUnHolo:
            next_span = label_priceUnHolo.find_next("span")
            if next_span and "$" in next_span.text:
                priceUnHolo = next_span.text.strip("$")
        else:
            priceUnHolo = None

        label_priceHolo = card.find("span", string="Holofoil")
        if label_priceHolo:
            next_span = label_priceHolo.find_next("span")
            if next_span and "$" in next_span.text:
                priceHolo = next_span.text.strip("$")
        else:
            priceHolo = None

        label_priceNor = card.find("span", string="Normal")
        if label_priceNor:
            next_span = label_priceNor.find_next("span")
            if next_span and "$" in next_span.text:
                priceNor = next_span.text.strip("$")
        else:
            priceNor = None

        label_priceRevHolo = card.find("span", string="Reverse Holofoil")
        if label_priceRevHolo:
            next_span = label_priceRevHolo.find_next("span")
            if next_span and "$" in next_span.text:
                priceRevHolo = next_span.text.strip("$")
        else:
            priceRevHolo = None

        card = {
            "name": name,
            "set": set,
            "number": number,
            "rarity": rarity,
            "prices" : {
                "1st Edition Holofoil ": price1st,
                "Unlimited Holofoil": priceUnHolo,
                "Holofoil": priceHolo,
                "Normal":priceNor,
                "Reverse Holofoil": priceRevHolo,
                "Date: ": today,
            }
        }
        card_list.append(card)
    driver.quit()
    return card_list

def all_website(fi,se,th,fo):
     l = fi + se + th + fo
     return l

cards_1 = scraper(url1)
cards_2 = scraper(url2)
cards_3 = scraper(url3)
cards_4 = scraper(url4)

all_cards=all_website(cards_1,cards_2,cards_3,cards_4)


df = pd.json_normalize(all_cards)
df.to_csv("pokemon_cards.csv",
          mode='a' if os.path.exists("pokemon_cards.csv")
          else 'w', index=False, encoding="utf-8", sep=";")


