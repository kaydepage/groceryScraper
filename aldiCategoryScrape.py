import pandas as pd
import requests
def extract_product_fields(product):
    price = product.get("price").get("amountRelevantDisplay")
    brand = product.get("brandName")
    if brand:
        brand = brand.strip('"').strip()
        name = f'{brand} {product.get('name')}'
    else:
        name = product.get("name")
    id = product.get("sku")
    if price:
        price = float(price.replace("$", ""))
    return {
        "Name": name,
        "Price": price,
        "Price/KG": product.get("price").get("comparisonDisplay"),
        "URL": f"https://www.aldi.com.au/product/{id}"
    }
def run():
    categories = {
        "fruit_veg": 950000000,
        "meat_seafood": 940000000,
        "deli_chilled_meats": 930000000,
        "dairy_eggs": 960000000,
        "pantry": 970000000,
        "bakery": 920000000,
        "freezer": 980000000,
        "drinks": 1000000000,
        "snacks": 1588161408332087,
    }   
    print(categories)
    all_products = []
    headers = {
        "accept": "application/json, text/plain */*",
        "referer": "https://www.aldi.com.au/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }


    for category, code in categories.items():
        print(f"category: {category}")
        offset = 0
        products = []

        while True:
            
            url = f"https://api.aldi.com.au/v3/product-search?currency=AUD&serviceType=walk-in&categoryKey={code}&limit=30&offset={offset}"
            try:
                response = requests.get(url, headers=headers)
                data = response.json()
                results = data.get("data")
                
            except:
                print("request failed")
                break
            if results is None:
                break
            products = [
                extract_product_fields(result)
                for result in results
            ]
            all_products.extend(products)
            if len(products) > 0:
                offset += 30
            else:
                break

    df = pd.DataFrame(all_products).drop_duplicates()
    df.to_csv("aldi_products.csv", index=False)
    print(f"Saved {len(all_products)} products to aldi_products.csv")
run()