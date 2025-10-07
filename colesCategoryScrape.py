from playwright.sync_api import sync_playwright, Playwright, TimeoutError
import pandas as pd
import requests

def get_build_id(playwright: Playwright, url):

    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    page.wait_for_selector("body script#__NEXT_DATA__")
    script_content = page.locator("body script#__NEXT_DATA__").text_content()
    print(script_content)

    browser.close()



def extract_product_fields(product):
    brand = product.get("brand")
    name = product.get("name")
    size = product.get("size")
    id = product.get("id")
    pricing = product.get("pricing")
    

    if not pricing: 
        print("⚠️ Missing pricing field:", product)

    return {
        "Name": f"{brand} {name} {size}" ,
        "Price": pricing.get("now") if pricing else None,
        "Price / KG": pricing.get("comparable") if pricing else None,
        "URL": f"https://coles.com.au/product/{id}"
    }


def run():
    

    categories = pd.read_csv('colesCategories.csv')["Category"]
    all_products = []
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'X-Nextjs-Data': '1',
    }
    
    for category in categories:
        print(f"category: {category}")
        page_number = 1
        products = []

        while True:
            if page_number % 10 == 0:
                print(f"im on page {page_number}")
            endpoint_url = f"https://www.coles.com.au/_next/data/20250916.2-6e5279cb065214e15253b3ec472b8c75953deabd/en/browse/{category}.json?page={page_number}&slug={category}"
            
            try:
                response = requests.get(endpoint_url, headers=headers)
                data = response.json()
                results = data.get("pageProps", {}).get("searchResults", {}).get("results", [])
            except:
                print("request failed")
                break


            products = [
                extract_product_fields(result)
                for result in results
                if result.get("_type") == "PRODUCT" and not result.get("featured") and result.get("availability") is True
            ]

            all_products.extend(products)
    
            if len(products) > 0:
                
                page_number += 1
            else:
                print("skipping")
                break

    df = pd.DataFrame(all_products).drop_duplicates()
    df.to_csv("coles_products.csv", index=False)
    print(f"Saved {len(all_products)} products to coles_products.csv")
with sync_playwright() as playwright:
    get_build_id(playwright, 'https://www.coles.com.au/')
# run()