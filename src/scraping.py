import requests
from bs4 import BeautifulSoup
import csv
import random
import time
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed

# Liste des user agents pour rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/91.0.864.64"
]

def random_delay(min_sec=1, max_sec=2):
    time.sleep(random.uniform(min_sec, max_sec))

def get_car_urls(page_number):
    base_url = f"https://www.avito.ma/fr/maroc/voitures_d_occasion-%C3%A0_vendre?o={page_number}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        car_urls = set()

        for link in soup.find_all("a", class_="sc-1jge648-0 jZXrfL"):
            car_url = link.get("href")
            if car_url:
                full_url = "https://www.avito.ma" + car_url if car_url.startswith("/") else car_url
                car_urls.add(full_url)

        print(f"✅ Page {page_number}: {len(car_urls)} URLs found.")
        random_delay()
        return list(car_urls)

    except RequestException as e:
        print(f"❌ Error fetching page {page_number}: {e}")
        return []

def get_car_details(car_url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(car_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        details = {
            "Marque": None, "Modèle": None, "Année": None,
            "Type de carburant": None, "Puissance fiscale": None,
            "Kilométrage": None, "Nombre de portes": None,
            "Première main": None, "État": None,
            "Boîte à vitesses": None, "Origine": None, "Prix": None
        }

        items = soup.find_all("div", class_="sc-19cngu6-1 doRGIC")
        for item in items:
            label_tag = item.find("span", class_="sc-1x0vz2r-0 bXFCIH")
            value_tag = item.find("span", class_="sc-1x0vz2r-0 fjZBup")
            if label_tag and value_tag:
                label = label_tag.get_text(strip=True)
                value = value_tag.get_text(strip=True) or None

                mapping = {
                    "Année-Modèle": "Année",
                    "Boite de vitesses": "Boîte à vitesses",
                    "Type de carburant": "Type de carburant",
                    "Kilométrage": "Kilométrage",
                    "Marque": "Marque",
                    "Modèle": "Modèle",
                    "Nombre de portes": "Nombre de portes",
                    "Origine": "Origine",
                    "Première main": "Première main",
                    "Puissance fiscale": "Puissance fiscale",
                    "État": "État"
                }
                if label in mapping:
                    details[mapping[label]] = value

        price = soup.find("p", class_="sc-1x0vz2r-0 lnEFFR sc-1veij0r-10 jdRkSM")
        if price:
            details["Prix"] = price.get_text(strip=True)

        random_delay()
        return details

    except RequestException as e:
        print(f"❌ Error fetching car details for {car_url}: {e}")
        return None

def write_to_csv(car_details, filename="car_details.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Marque", "Modèle", "Année", "Type de carburant", "Puissance fiscale",
            "Kilométrage", "Nombre de portes", "Première main", "État",
            "Boîte à vitesses", "Origine", "Prix"
        ])
        file.seek(0, 2)
        if file.tell() == 0:
            writer.writeheader()
        for car in car_details:
            writer.writerow(car)

# MAIN
all_car_urls = set()
for page in range(1, 401):
    print(f"🔄 Scraping page {page}...")
    urls = get_car_urls(page)
    if urls:
        all_car_urls.update(urls)
    else:
        print(f"⚠️ Skipping page {page}")

print(f"🔗 Total unique car URLs collected: {len(all_car_urls)}")

car_details_list = []
print("🚀 Starting threaded scraping of car details...")

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(get_car_details, url): url for url in all_car_urls}
    for i, future in enumerate(as_completed(future_to_url), start=1):
        car_url = future_to_url[future]
        try:
            car_details = future.result()
            if car_details:
                car_details_list.append(car_details)
                write_to_csv([car_details])
                print(f"✅ [{i}/{len(all_car_urls)}] Scraped: {car_url}")
        except Exception as exc:
            print(f"❌ [{i}] Failed to scrape {car_url}: {exc}")

print(f"🏁 Finished scraping {len(car_details_list)} cars.")
