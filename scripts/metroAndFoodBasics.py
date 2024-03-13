import requests
from bs4 import BeautifulSoup
import csv
import time
foodBasicsURL = "https://www.foodbasics.ca/search-page-{page}?sortOrder=popularity&filter=%3Apopularity%3Adeal%3AFlyer+%26+Deals%2F%3Adeal%3AFlyer+%26+Deals&fromEcomFlyer=true"
metroURL = "https://www.metro.ca/en/online-grocery/search-page-{page}?sortOrder=relevance&filter=%3Arelevance%3Adeal%3AFlyer+%26+Deals"


def scrape_products(base_url, csv_file_path):
    product_data = []

    # Get the first page to find the last page number
    response = requests.get(base_url.format(page=1))
    soup = BeautifulSoup(response.content, 'html.parser')
    pagination = soup.find('div', class_='ppn--pagination')
    if pagination is None:
        print("Pagination element not found. Please check the URL or the structure of the webpage.")
        return
    else:
        last_page_number = int(pagination.find_all('a', class_='ppn--element')[-2].text)
        print(f"Found {last_page_number} pages of products.")
    # Loop through each page until the last page
    for page_number in range(1, last_page_number + 1):
        url = base_url.format(page=page_number)
        response = requests.get(url,)
        if response.status_code == 403:
            print("Error 403: Forbidden")
        elif response.status_code != 200:
            print(f"Error accessing page {page_number}. Continuing to next page.")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        product_tiles = soup.find_all('div', class_='default-product-tile')

        if not product_tiles:
            print(f"No more products found on page {page_number}. Continuing to next page.")
            continue

        for product_tile in product_tiles:
            product_name = product_tile.find('div', class_='head__title')
            product_name = product_name.text.strip() if product_name else None

            # Check if the element is present before accessing its text attribute
            product_amount_elem = product_tile.find('span', class_='head__unit-details')
            product_amount = product_amount_elem.text.strip() if product_amount_elem else None

            price_div = product_tile.find('div', {'data-main-price': True})
            price = price_div['data-main-price'] if price_div else None
            product_data.append({"Product": product_name, "Amount": product_amount, "Price": price})

        time.sleep(5)  # Add a delay of 5 seconds

    # Write the data to a CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Product", "Amount", "Price"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for product in product_data:
            writer.writerow(product)

    print(f"Data has been successfully written to {csv_file_path}.")

# Call the function with the URLs and output files
print("Scraping Food Basics...")
scrape_products(foodBasicsURL, "foodbasics.csv")
print("Scraping Metro...")
scrape_products(metroURL, "metro.csv")
