import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time


headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}
URL="https://pokemoncardprices.io/top-100-pokemon-cards"

driver = webdriver.Chrome()
driver.get(URL)
time.sleep(3)
html = driver.page_source

#response = requests.get(URL, headers=headers)
soup = BeautifulSoup(html, 'html.parser')
cards = soup.find_all('div', {"data-slot": "card-content"})

card_list = []

#for div in card_div:
    # Przykładowe pola: ranking, nazwa, cena, rzadkość
    #name = div.find("h3", class_="text-sm")
   # price = div.find("div", class_="card-list-item__price")
   # rarity = div.find("div", class_="card-list-item__rarity")
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
            price1st = next_span.text.strip()
    else :
        price1st = None

    label_priceUnHolo = card.find("span", string="Unlimited Holofoil")
    if label_priceUnHolo:
        next_span = label_priceUnHolo.find_next("span")
        if next_span and "$" in next_span.text:
            priceUnHolo = next_span.text.strip()
    else:
        priceUnHolo = None

    label_priceHolo = card.find("span", string="Holofoil")
    if label_priceHolo:
        next_span = label_priceHolo.find_next("span")
        if next_span and "$" in next_span.text:
            priceHolo = next_span.text.strip()
    else:
        priceHolo = None

    label_priceNor = card.find("span", string="Normal")
    if label_priceNor:
        next_span = label_priceNor.find_next("span")
        if next_span and "$" in next_span.text:
            priceNor = next_span.text.strip()
    else:
        priceNor = None

    label_priceRevHolo = card.find("span", string="Reverse Holofoil")
    if label_priceRevHolo:
        next_span = label_priceRevHolo.find_next("span")
        if next_span and "$" in next_span.text:
            priceRevHolo = next_span.text.strip()
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
            "Reverse Holofoil": priceRevHolo
        }
    }
    card_list.append(card)

print(card_list)
driver.quit()

df = pd.DataFrame([card_list])
df.to_csv("pokemon_cards.csv", index=False, encoding="utf-8")

'''
if cards:
    print("hi")
    #for para in content_div.find_all('p'):
    #   print(para.text.strip())
else:
    print("No article content found.")


# 1. Zdefiniuj cel
karta = "top-100-pokemon-cards" # Część URL-a
url = f"https://pokemoncardprices.io/{karta}"
dane_karty = {}

# 2. Pobierz zawartość strony
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Sprawdza, czy zapytanie zakończyło się błędem
except requests.exceptions.RequestException as e:
    print(f"Błąd podczas pobierania strony: {e}")
    # Możesz tu dodać obsługę błędu i przejść do następnej osoby
    # return

# 3. Parsuj treść HTML
soup = BeautifulSoup(response.content, 'html.parser')

# 4. Znajdź ramkę informacyjną (infobox)
# Ramki informacyjne często są w tabeli z klasą 'infobox'
infobox = soup.find('info',
                    {'class': 'p-0 space-y-2 h-full contents'})

if infobox:
    # 5. Iteruj po wierszach infoboksu (tr)
    for row in infobox.find_all('tr'):
        # Szukaj nagłówka i wartości
        header = row.find('th')
        value = row.find('td')

        if header and value:
            naglowek = header.get_text(strip=True)
            wartosc = value.get_text(strip=True)

            # Konkretne filtrowanie, które Cię interesuje
            #if "Born" in naglowek:
            #    dane_karty['urodzenie'] = wartosc
            #elif "Died" in naglowek:
            #    dane_karty['smierc'] = wartosc

# 6. Dodaj wynik do DataFrame lub listy
if dane_karty:
    dane_karty['Osoba'] = karta.replace('_', ' ')
    print(f"Pobrane dane dla {karta}: {dane_karty}")
else:
    print(f"Nie znaleziono infoboxu lub danych dla {karta}")

# 7. Wynik możesz następnie umieścić w DataFrame Pandas:
df_nowe_dane = pd.DataFrame([dane_karty])
df_nowe_dane.to_csv()
'''