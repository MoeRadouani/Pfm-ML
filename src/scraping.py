import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from requests.exceptions import RequestException

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/91.0.864.64"
]

# Function to get URLs of cars from a listing page
def get_car_urls(page_number):
    base_url = f"https://www.avito.ma/fr/maroc/voitures_d_occasion-%C3%A0_vendre?page={page_number}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        car_urls = []

        for link in soup.find_all("a", class_="sc-1jge648-0 jZXrfL"):
            car_url = link.get("href")
            if car_url:
                full_url = "https://www.avito.ma" + car_url if car_url.startswith("/") else car_url
                car_urls.append(full_url)
                print(f"Found car URL: {full_url}")

        return car_urls

    except RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return []

# Function to get details from a single car page
def get_car_details(car_url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    try:
        response = requests.get(car_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        details = {
            "Marque": None,
            "Modèle": None,
            "Année": None,
            "Type de carburant": None,
            "Puissance fiscale": None,
            "Kilométrage": None,
            "Nombre de portes": None,
            "Première main": None,
            "État": None,
            "Boîte à vitesses": None,
            "Origine": None,
            "Prix": None
        }

        detail_items = soup.find_all("div", class_="sc-19cngu6-1 doRGIC")
        for item in detail_items:
            label_tag = item.find("span", class_="sc-1x0vz2r-0 bXFCIH")
            value_tag = item.find("span", class_="sc-1x0vz2r-0 fjZBup")

            if label_tag and value_tag:
                label = label_tag.get_text(strip=True)
                value = value_tag.get_text(strip=True) or None

                if label == "Année-Modèle":
                    details["Année"] = value
                elif label == "Boite de vitesses":
                    details["Boîte à vitesses"] = value
                elif label == "Type de carburant":
                    details["Type de carburant"] = value
                elif label == "Kilométrage":
                    details["Kilométrage"] = value
                elif label == "Marque":
                    details["Marque"] = value
                elif label == "Modèle":
                    details["Modèle"] = value
                elif label == "Nombre de portes":
                    details["Nombre de portes"] = value
                elif label == "Origine":
                    details["Origine"] = value
                elif label == "Première main":
                    details["Première main"] = value
                elif label == "Puissance fiscale":
                    details["Puissance fiscale"] = value
                elif label == "État":
                    details["État"] = value

        # Get price
        price = soup.find("p", class_="sc-1x0vz2r-0 lnEFFR sc-1veij0r-10 jdRkSM")
        if price:
            details["Prix"] = price.get_text(strip=True)

        return details

    except RequestException as e:
        print(f"Error fetching car details for {car_url}: {e}")
        return None

# Write car data to CSV (append mode)
def write_to_csv(car_details, filename="car_details.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[  
            "Marque", "Modèle", "Année", "Type de carburant", "Puissance fiscale", 
            "Kilométrage", "Nombre de portes", "Première main", "État", 
            "Boîte à vitesses", "Origine", "Prix"
        ])
        # Check if file is empty and write header only once
        file.seek(0, 2)
        if file.tell() == 0:
            writer.writeheader()
        for car in car_details:
            writer.writerow(car)

# MAIN CODE

all_car_urls = []
for page in range(1, 301):  # Scraping pages 1 and 2
    print(f"🔄 Scraping page {page}...")
    urls = get_car_urls(page)
    if urls:
        all_car_urls.extend(urls)
    else:
        print(f"⚠️ Skipping page {page}")
    time.sleep(random.uniform(2, 6))


# Scrape car details
car_details_list = []
for i, car_url in enumerate(all_car_urls):
    print(f"🚗 [{i+1}/{len(all_car_urls)}] Getting details for: {car_url}")
    car_details = get_car_details(car_url)
    if car_details:
        car_details_list.append(car_details)
        # Save after each car
        write_to_csv([car_details])  # Save the data of the current car
    time.sleep(random.uniform(3, 7))

print(f"✅ Finished scraping {len(car_details_list)} cars.")
