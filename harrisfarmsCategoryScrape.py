from playwright.sync_api import sync_playwright, Playwright, TimeoutError
import pandas as pd

def get_categories(csv):
    return list(pd.read_csv(csv)['Category'])

def extract_product_fields(product):
    name = product.get_attribute("data-title")

    href = product.locator("a.full-link").get_attribute("href")
    link = f"https://www.harrisfarm.com.au{href}"

    price = product.locator("span.from_price").text_content()
    pricekg = product.locator("span.compare_at_price").text_content()

    if price:
        price = float(price.replace("$", ""))
    return {
        "Name": name,
        "Price": price,
        "Price/KG": pricekg,
        "URL": link
    }
            


def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()

    categories = get_categories("harrisfarmCategories.csv")

    all_products = []
    for category in categories:
        print(f"category: {category}")
        page_number = 1
        

        while True:
            products = []
            if page_number % 10 == 0:
                print(f"im on page {page_number}")

            url = f"https://www.harrisfarm.com.au/collections/{category}?page={page_number}"
            page.goto(url, wait_until="domcontentloaded")
            for item in page.locator('#product-grid').get_by_role('listitem').all():
                products.append(extract_product_fields(item))
            all_products.extend(products)

            

            if len(products) > 0:
                page_number += 1
            else:
                break
    browser.close()
    df = pd.DataFrame(all_products).drop_duplicates()
    df.to_csv("harrisfarm_products.csv", index=False)
    print(f"Saved {len(all_products)} products to harrisfarm_products.csv")       

with sync_playwright() as playwright:
    run(playwright)
