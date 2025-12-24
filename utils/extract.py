import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def scrape_main(base_url="https://fashion-studio.dicoding.dev", max_pages=50):
    data = []
    timestamp = datetime.now().isoformat()

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}/page{page}"
        print(f"Scraping {url} ...")

        try:
            res = requests.get(url, timeout=10)

            if res.status_code == 404:
                print(f"Page {page} returned 404. Stopping pagination.")
                break

            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            # Cari div dengan class product-details
            products = soup.find_all("div", class_="product-details")

            if not products:
                print(f"No products found on page {page}. Stopping.")
                break

            for product in products:
                try:
                    title_tag = product.find("h3", class_="product-title")
                    price_tag = product.find("span", class_="price")
                    rating_tag = product.find("p", string=lambda text: text and "Rating:" in text)
                    colors_tag = product.find("p", string=lambda text: text and "Colors" in text)
                    size_tag = product.find("p", string=lambda text: text and "Size:" in text)
                    gender_tag = product.find("p", string=lambda text: text and "Gender:" in text)

                    title = title_tag.get_text(strip=True) if title_tag else None
                    price = price_tag.get_text(strip=True) if price_tag else None
                    rating = rating_tag.get_text(strip=True).replace("Rating: ", "") if rating_tag else None
                    colors = colors_tag.get_text(strip=True) if colors_tag else None
                    size = size_tag.get_text(strip=True) if size_tag else None
                    gender = gender_tag.get_text(strip=True) if gender_tag else None

                    data.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "timestamp": timestamp
                    })
                except Exception as e:
                    print(f"Error parsing product on page {page}: {e}")

        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break  # Stop scraping jika gagal fetch halaman

    df = pd.DataFrame(data)
    if df.empty:
        print("Warning: No data scraped. DataFrame is empty.")
    return df
