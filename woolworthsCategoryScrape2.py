from playwright.sync_api import sync_playwright, Playwright, TimeoutError
import pandas as pd
import requests
import json

def extract_product_fields(product):
    """Return only the desired fields for each product"""
    return {
        "Name": product.get("Name"),
        "Price": product.get("Price"),
        "WasPrice": product.get("WasPrice"),
        "Description": product.get("Description"),
        "Unit": product.get("Unit"),
        "PackageSize": product.get("PackageSize")
    }

def scrape(data):
    for i in range(len(data.index)):
        current = data.values[i]
        category = current[0]
        format_object = current[1]
        category_id = current[2]
        print(i)
        print(category, format_object, category_id)
           
        page_number = 1
        while True:
            
            url = "https://www.woolworths.com.au/apis/ui/browse/category"
            category_path = f"/shop/browse/{category}?pageNumber={page_number}"
            payload = {
                "categoryId": category_id,
                "categoryVersion": "v2",
                "enableAdReRanking": False,
                "filters": [],
                "formatObject": format_object,
                "gpBoost": 0,
                "groupEdmVariants": False,
                "isBundle": False,
                "isHideUnavailableProducts": False,
                "isMobile": False,
                "isRegisteredRewardCardPromotion": False,
                "isSpecial": False,
                "location": category_path,
                "pageNumber": page_number,
                "pageSize": 36,
                "sortType": "TraderRelevance",
                "token": "",
                "url": category_path
            }
            headers = {
            'Content-Type': 'application/json',
            'Cookie': '_abck=3E4D6C62D955C22601E20412A2F5C058~-1~YAAQr244F3X030uZAQAAo1J2TQ5QwVKM9vpaelkq8YB1EGtpQ99ChUnD+YY4EaMRGtJLIrek163A6goo5S5/TZxqQi9HbNpXJn/oagACFciDm3sue9wN+aIwYJZ3pRZd9ASyVmUd+H9xyptFtXoBqmwh6CSeW8tpqgHbesEaxrte2t38sA4zv3xiIamKPrxZjwOXUAFF23BP6G2HS3W8tW00WbdRtJD4cK3z38Ee1a5j7zydFneh83tjMEwHm5NWbafbGPxSa1DTOaeJa9zcDWTLMVwr2h1FTMeXjUiPs4DNzqjqp+PWeLLl+fB4dZA2kjPS+c3nF1pt/JVhtsMskiwwtOgIIpH8nA6X3mAvzOoAkEFDBgMbGz0io/IHQjpkhM0PirD7RHPX319iFcKGWcqK++B7npEcFFSnUc9BH/DL7kp5/TQh7uLJH4r8tKufgPRdwaKWquES3tOZXrIuG2DmHsp2r4wN3zuRsGcpR8sH94ZmT6hkd8dEIGyMLWQqsZ50YPI41FmeNl5/kDSxZrol5OZgz57CuqlVotJPoZF3cGbF4W62KOvPwr6TdFQxl4hmtr1WCV9h688m+hLFZRS+xqEgL9v8666lPTJiJKJApd/TmNh9SSQJt28htFmNqrhN9kO5hNP3R0PzgfVgLQRfW5gpImMNTm9qXrAfQzpuyk2kn7mjy0WiJoENgXJq9yhtaQ31uVIWdX4xc6RiUDorG/snVU+SWWBbF59+Gv54wad43UuTmqdMEatH9GHSgRhaNHpTvQsjgHxfzYfFmLf6CYlyJe0lIffpIpgBXNJwytE40JkYUuBD5ktgM+DqBpyTgIE0iEXU5m6ExCJZPQy6zJ3dSD262wCjPHD6P4S175fNXxWwIDh93enm3bO2KltoYMQ4e1gDzfXCyv0owSQ1bQpkuATj98z/g6wXgCT4kGsZb12+fPOMbUIpvu0H4SeN4bQBaBZXtIU3tLOVhD2r/Fj9E03Z3jKti9QbuIrBwOqDvF4wUvxkH9fI1tTuAOq/FEGaEp2oNiDOm9ArAQ3A/C6jIsiPEEX/WIqvQyPhZA==~-1~-1~-1~-1~-1; ak_bmsc=F1EE4BC425DE99A5F95FAC47F049F281~000000000000000000000000000000~YAAQrW44F3LMCTeZAQAAGe91TR3gznWOHhDaQnTv49/FPNqUOG2MaXv92RThTggC+iVil9OXG2q/574C5jBqgbMPbFb9QdSG0y4M0S4QxZcTKMrVFKyXF+M57WNZFxYj9dtExkkfXr9516TBzxhI0NHBUYv2/vrq7gbF455nsS8a0m8/rB7KJj7pIOoAkDPJTfBYFls/eo/BumgAMxwhLudZjwyyi7FwBoMGMDsjWuMP23Nw55NgNruar+9y3TCRCbtACclqP7sVnbx7MMD+X67eEepqyMJSDFvIpBh+OYE6TxBsQcVis90JKag/xffOra1tZe4IMG9HDsIEh5ecwkllXQsI11YXM6BYl8fgnn1/qccLP29D7Frm8YFuBprWnk8bvTPS7+7ortP7gOez2QUhj093IIWA2SI50Q591TlXcxPPaN4zTyzA; bm_mi=21A5B554682226FE94CD1026D7B32DF6~YAAQtW44FwFBGhqZAQAAYe90TR09quSNdVDhPr6n6PRj/1RY5zJtLy8RN3hq7dyyMLeDrZ7xXhn7qODYI+xsV5N9Cp5PUcvyICtCgBECSK/vxXLXWt0AGqsRpIbMP7MBoSE8VyvfaroXgedVAM8WxBqL7xlHcwfJ1AEQTJtJ4WdIxV7BvLtXuZZpQjnQcFebi8SH24tV9fTD5m5ezKIEIk7EteGpxq8rfFRucADBd1e0tWkNkY1Xcohj00TUqy7modlysAbovGqKTj+jhT05OUiVCEyPC5kvEE3TMOQf1Xi4FAlAA0pmUfmiERZzcUc2CPFMkZQEyS2tQ9s9+ZuQuuSaAawO3ZuDRUerYA==~1; bm_sv=4F0B8E78BC944CC2B0608A045D25AB53~YAAQrW44F0a7CTeZAQAAGxp1TR1S+Q9RtfBlrph3LrMF+ceRPesKqT3eKOcY7hRK4hwrKtLY2jgoUU3mlz6k68Zoo72R9zKVqMQS4KptW65Z70rM7pP7wFB/lsa93PHBw6Vomo3pXB3UPsFfCgNhUvZUGKwOpswWdu9gMHEcMVPTBf08kE7/qoknqXlxRNLoQ68a1nhU6n+D4qaypiZ4RiemqXP3E7WPWyRvtrhtvxqQ1zD03D0HaIhssLUuthcnH9Cj0eLXzYQ=~1; bm_sz=DC9D2DD268AC059D4FC6BA03D7EBF9BD~YAAQr244F3b030uZAQAAo1J2TR0w0rTvrZWovbymBmfu+smS6utkZxERtn8uLufLCvI1Ymedk5PtlxVWHOXZUFB+ULALGvTUBlS0E9iItnw0VzZEzG7DWPAHPMmVjeYDjHKuoTr05JLcbJaeYP6v46/bmUGFuYhiIiT42udkh0iOYDJEjODJJHPtQxDk67vRVrbQzKxwQ1jc/F4Lzz9uyBob8VXFf7nMD+CNYo3paDoe/w9759X2apVFmOS6DRZgu8dnghfZ/qDG06TO+RULHba/3uNUBukmuKcpXBJnpxKt/iUi4E+h91cIacPknFpZIwCHAauBnnBwxOK4rjPdfWg+VkZhGXVhmk0Qed4ic0Wc2NSKPpOwXcIM9c9XHYmqQDuC8X9wXZVe6BIWISc27+Q0gzeBNaw8gABmMnQ/7mkEw9cJQYRc634aRyafAa62h2UsvTz0wu2N6kq9brUE~4342584~3552054; dtCookie=v_4_srv_2_sn_D7C44AA4435A7CE7124EEFF7FB3BF6A4_perc_100000_ol_0_mul_1_app-3Af908d76079915f06_0_rcs-3Acss_0; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NTc5MzkxNTEsImV4cCI6MTc1Nzk0Mjc1MSwiaWF0IjoxNzU3OTM5MTUxLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImQ1OWIyY2UxLTc5YTktNDZhOS04MDI5LWY0OGFlMTJmMWFmOCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.UyhoWF_IzXGeyGwMxCAuN6swSfEJvl083qLUtBasq2uQdSmok_h1dvfqbvYSHyhOLvQ_2DXbc77pTyZ6sCrjF0L5361iw-YjFYM0yWFELnsar37GJ1-NiZY_F1VOnIPOMKs16nyTmRvEhEj9_HIivtTzXOZ4kDM8EUZJWcd4L7TqZAXARQWPebfJDXURkfIbxeGV3j5XCFEvKksYannc6Z-e_6yeuZUptogG1bei04xPsY5bkumaM7fiVfbyQiF2Q7DKS_0MHGxhvfRUuDFK-uMxrFU-oFGcweHGwug2pIjFr24m8HktDAjJQYSEP9ZH6odLFx050o0QTd7InHsslg; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NTc5MzkxNTEsImV4cCI6MTc1Nzk0Mjc1MSwiaWF0IjoxNzU3OTM5MTUxLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImQ1OWIyY2UxLTc5YTktNDZhOS04MDI5LWY0OGFlMTJmMWFmOCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.UyhoWF_IzXGeyGwMxCAuN6swSfEJvl083qLUtBasq2uQdSmok_h1dvfqbvYSHyhOLvQ_2DXbc77pTyZ6sCrjF0L5361iw-YjFYM0yWFELnsar37GJ1-NiZY_F1VOnIPOMKs16nyTmRvEhEj9_HIivtTzXOZ4kDM8EUZJWcd4L7TqZAXARQWPebfJDXURkfIbxeGV3j5XCFEvKksYannc6Z-e_6yeuZUptogG1bei04xPsY5bkumaM7fiVfbyQiF2Q7DKS_0MHGxhvfRUuDFK-uMxrFU-oFGcweHGwug2pIjFr24m8HktDAjJQYSEP9ZH6odLFx050o0QTd7InHsslg; INGRESSCOOKIE=1757918865.706.67.378285|37206e05370eb151ee9f1b6a1c80a538; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneAandC:PROD-ZoneC|~rv=72~m=PROD-ZoneC:0|~os=43eb3391333cc20efbd7f812851447e6~id=ae2cf212a91e49f6f59f62ae26168361; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NTc5MzkxNTEsImV4cCI6MTc1Nzk0Mjc1MSwiaWF0IjoxNzU3OTM5MTUxLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImQ1OWIyY2UxLTc5YTktNDZhOS04MDI5LWY0OGFlMTJmMWFmOCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.UyhoWF_IzXGeyGwMxCAuN6swSfEJvl083qLUtBasq2uQdSmok_h1dvfqbvYSHyhOLvQ_2DXbc77pTyZ6sCrjF0L5361iw-YjFYM0yWFELnsar37GJ1-NiZY_F1VOnIPOMKs16nyTmRvEhEj9_HIivtTzXOZ4kDM8EUZJWcd4L7TqZAXARQWPebfJDXURkfIbxeGV3j5XCFEvKksYannc6Z-e_6yeuZUptogG1bei04xPsY5bkumaM7fiVfbyQiF2Q7DKS_0MHGxhvfRUuDFK-uMxrFU-oFGcweHGwug2pIjFr24m8HktDAjJQYSEP9ZH6odLFx050o0QTd7InHsslg'
            }

            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                print("No resposne")
data = pd.read_csv('woolworthsCategories.csv', delimiter="|")
scrape(data)