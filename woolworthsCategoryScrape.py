from playwright.sync_api import sync_playwright, Playwright, TimeoutError
import pandas as pd


def extract_product_fields(product):
    name = product.get("DisplayName")
    id = product.get("Stockcode")
    return {
        "Name": name,
        "Price": product.get("Price"),
        "Price / KG": product.get("CupString"),
        "URL": f"https://www.woolworths.com.au/shop/productdetails/{id}"
    }

def get_categories(csv):
    return list(pd.read_csv(csv)['Category'])

def get_products(categories=get_categories("woolworthsCategories.csv")):
    for category in categories:
        page_number = 1

    return 
def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=True)
    page = browser.new_page()

    #Extracting Categories 
    categories = get_categories("woolworthsCategories.csv")
    #Extracting Items from Categories
    

    all_products = []
    for category in categories:
        print(f"category: {category}")
        page_number = 1
        products = []

        while True:
            if page_number % 10 == 0:
                print(f"im on page {page_number}")
            url = f"https://www.woolworths.com.au/shop/browse/{category}?pageNumber={str(page_number)}"
            
            with page.expect_response("https://www.woolworths.com.au/apis/ui/browse/category") as response:
                page.goto(url)
            
            data = response.value.json()
            products = [
                extract_product_fields(product)
                for bundle in data.get("Bundles", [])
                for product in bundle.get("Products", [])
                if product.get("IsSponsoredAd") is False
            ]
            all_products.extend(products)

            if len(products) > 0:
                page_number += 1
            else:
                break

        
            
    browser.close()
    df = pd.DataFrame(all_products).drop_duplicates()
    df.to_csv("woolworths_products.csv", index=False)
    print(f"Saved {len(all_products)} products to woolworths_products.csv")

with sync_playwright() as playwright:
    run(playwright)
