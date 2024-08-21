from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup as bs

def Get_Related_Post(url: str):
    '''
    Example Url

    1. https://www.flipkart.com/search?q=tv&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_8_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_8_0_na_na_na&as-pos=8&as-type=TRENDING&suggestionId=tv&requestId=cbf12b63-0b14-4eeb-b131-afc9e1695106

    2. https://www.flipkart.com/sports/cycling/electric-cycle/pr?sid=abc%2Culv%2Ctwp&hpid=IN6WQymhhksnM1l95t0Z6Kp7_Hsxr70nj65vMAAFKlc%3D&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJVcCB0byA0MCUgT2ZmIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwiaGVyb1BpZCI6eyJzaW5nbGVWYWx1ZUF0dHJpYnV0ZSI6eyJrZXkiOiJoZXJvUGlkIiwiaW5mZXJlbmNlVHlwZSI6IlBJRCIsInZhbHVlIjoiRUNZSDJYNjQyQ0hYRERDViIsInZhbHVlVHlwZSI6IlNJTkdMRV9WQUxVRUQifX0sInRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkVsZWN0cmljIEN5Y2xlIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D

    '''
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')
    elements = soup.find_all("div", class_="_75nlfW")[:10]
    results = []

    try:
        for element in elements:
            try:
                product_url = "https://www.flipkart.com" + element.find("a")['href']
                offer_percentage = element.find("span", string=lambda text: text and "% off" in text).text.replace('off', '').replace('%', '')
                curr_price = element.find("div", class_="Nx9bqj").text[1:].replace(',', '')
                mrp_price = element.find("div", class_="yRaY8j").text[1:].replace(',', '')

                try:
                    name = element.find("a", class_="WKTcLC")['title']
                except:
                    name = element.find("img", class_="DByuf4")['alt']

                try:
                    rating = element.find('div', attrs={'class':'hGSR34'})
                except:
                    rating = None

                results.append({
                    'Product_Name': name,
                    'Product_Rating': rating,
                    'Current_Price': curr_price,
                    'MRP_Price': mrp_price,
                    'Product_offer': offer_percentage,
                    'Product_URL':product_url
                })
                

            except Exception as e:
                print(f"Error processing element: {e}")
                continue

    except:
        return results

    return results



def Get_Product_Details(url:str):
    '''
    Example url : https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4?pid=MOBGTAGPTB3VS24W&lid=LSTMOBGTAGPTB3VS24WVZNSC6&marketplace=FLIPKART&q=mobiles&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=s_1_2&otracker=AS_Query_TrendingAutoSuggest_2_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_2_0_na_na_na&fm=search-autosuggest&iid=25e70862-cf70-4e13-ac60-fe7660686dfc.MOBGTAGPTB3VS24W.SEARCH&ppt=sp&ppn=sp&ssid=mni1rvlby80000001724048231675&qH=eb4af0bf07c16429
    '''
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    product = soup.find('div', class_=['DOjaWF', 'YJG4Cf'])

    result = {}

    try:
        name = product.find("h1", class_="_6EBuvT").text
        current_price = product.find("div", class_="Nx9bqj CxhGGd").text.replace(',', '').replace('₹', '')
        original_price = product.find("div", class_="yRaY8j A6+E6v").text.replace(',', '').replace('₹', '')
        discount_percent = product.find("div", class_=re.compile(r'\bUkUFwK\b.*\bWW8yVX\b')).text.replace('off', '').replace('%', '')
        rating = product.find("div", class_="XQDdHH").text
        rating_count_span = product.find("span", class_="Wphh3N").find_all("span")
        matches = re.findall(r'(\d{1,3}(?:,\d{3})*)', rating_count_span[0].text)
        if matches and len(matches) == 2:
            no_of_rating = matches[0].replace(',', '')
            no_of_reviews = matches[1].replace(',', '')
        else:
            no_of_rating = rating_count_span[1].text.split(" ")[0].replace(',', '')
            no_of_reviews = rating_count_span[3].text.split(" ")[0].replace(',', '')

        All_offer_tags = product.find("div", class_="I+EQVr").find_all("span")
        offers = []
        for offer in All_offer_tags:
            try:
                all_span = offer.find("li").find_all('span')
                offer_type = all_span[0].text
                offer_description = all_span[1].text
                offers.append({
                    "Offer_type":offer_type,
                    "Offer_Description":offer_description
                })
            except Exception as e:
                continue

        highlights = []
        try:
            all_highlights_tag = product.find("div", class_="xFVion").find_all("li")
            for highlight in all_highlights_tag:
                highlights.append(highlight.text)
        except:
            highlights = []

        Payment_Options = []
        try:
            Payment_Options_tag = product.find("div", class_="HQijVm").find_all("li")
            for option in Payment_Options_tag:
                Payment_Options.append(option.text)
        except:
            Payment_Options = []

        try:
            product_description = product.find("div", class_="yN+eNk w9jEaj").text
        except:
            product_description = ""

        specs = []

        All_specs_tag = product.find("div",class_="_1OjC5I")
        if All_specs_tag:
            for spec in All_specs_tag.find_all("div"):
                try:
                    title = spec.find("div").text
                    details = []
                    table_rows = spec.find("table",class_="_0ZhAN9").find_all("tr")
                    for each_row in table_rows:
                        all_property = each_row.find_all("td")
                        pro = all_property[0].text
                        val = all_property[1].text
                        details.append({
                            "property": pro,
                            "value": val
                        })
                    
                    specs.append({
                        "title":title,
                        "details":details
                    })
                except:
                    continue
                
        result = {
            "name": name,
            "current_price": current_price,
            "original_price": original_price,
            "discount_percent": discount_percent,
            "rating": rating,
            "no_of_rating": no_of_rating,
            "no_of_reviews": no_of_reviews,
            "highlights": highlights,
            "offers": offers,
            "Payment_Options": Payment_Options,
            "product_description": product_description,
            "specs": specs
        }

    except:
        return result

    return result


def Get_Order_History(cookies):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': '_gid=GA1.2.376810832.1723973383; T=SD.8297445a-c3a7-454c-8db2-08c7f7f57a35.1723973442100; _fbp=fb.1.1723973445369.584970553217977911; _gac_UA-172010654-1=1.1723974918.Cj0KCQjwt4a2BhD6ARIsALgH7Dq71gYehZuxgpal5uXIRb3oCj9cy9uZBEoT3zG9JGgsb1X6iVtJVCEaAt5-EALw_wcB; _gcl_gs=2.1.k1$i1723975268; _gcl_aw=GCL.1723975304.Cj0KCQjwt4a2BhD6ARIsALgH7Dq71gYehZuxgpal5uXIRb3oCj9cy9uZBEoT3zG9JGgsb1X6iVtJVCEaAt5-EALw_wcB; _gcl_au=1.1.316233740.1723973445.2093527625.1723987793.1723987881; _ga_2P94RMW04V=GS1.2.1723987560.2.1.1723988664.0.0.0; vh=695; vw=1536; dpr=1.25; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C19954%7CMCMID%7C21476465616184877218592220524603309424%7CMCAAMLH-1724602689%7C12%7CMCAAMB-1724602689%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1724005090s%7CNONE%7CMCAID%7CNONE; mp_9ea3bc9a23c575907407cf80efd56524_mixpanel=%7B%22distinct_id%22%3A%20%22ACC1CA692790CD146EC9021F458F9DC60D3%22%2C%22%24device_id%22%3A%20%2219164d53f8d5d7-0e4475eac7b911-26001e51-144000-19164d53f8e13ab%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22ACC1CA692790CD146EC9021F458F9DC60D3%22%7D; _ga=GA1.1.1985921494.1723973383; AMCV_55CFEDA0570C3FA17F000101%40AdobeOrg=-227196251%7CMCIDTS%7C19954%7CMCMID%7C65944996142707664201684694952521642495%7CMCAAMLH-1724578251%7C12%7CMCAAMB-1724610805%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1724013205s%7CNONE%7CMCAID%7CNONE; _ga_TVF0VCMCT3=GS1.1.1724006004.3.0.1724006005.59.0.0; _ga_0SJLGHBL81=GS1.1.1724006004.3.1.1724006043.0.0.0; s_nr=1724006061720-Repeat; ULSN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjb29raWUiLCJhdWQiOiJmbGlwa2FydCIsImlzcyI6ImF1dGguZmxpcGthcnQuY29tIiwiY2xhaW1zIjp7ImdlbiI6IjEiLCJ1bmlxdWVJZCI6IlVVSTI0MDgxOTE3MjAzNTY0NkJRSE40M1ciLCJma0RldiI6bnVsbH0sImV4cCI6MTczOTg0ODIzNSwiaWF0IjoxNzI0MDY4MjM1LCJqdGkiOiI4N2Y1Mzc3Ny1iNGRjLTQyN2ItODZmNi0xMTU4YmM0YTEyNGIifQ.G4wok2LFh1UPXO2mNYhd6sPHxBLEYIO5QyfrtXrLqGo; ud=4.yLMB0bKfvQdG3yvxWxMfS-rYCYvI9X15on9Jpz-4oS7aNvHr_lZoqd39zDhtjUA-dg_CHVgGAdkIRYEebo8qRF_78VktRbNcWW5n8wG0gbf7zM4PP3cCoaPoMVMxLE-ldMk0OW-XcBTKdUC0VA7BFbvDyIxSlE2pIzv-KEqKFhZDsUk7nDM8_wjmHgETMML5; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3MjQwNzM4MzYsImlhdCI6MTcyNDA3MjAzNiwiaXNzIjoia2V2bGFyIiwianRpIjoiNTU1YjgxYmYtMjA4Yi00OWVhLWE5NWItYmM3NGQ2ODg5ZTUxIiwidHlwZSI6IkFUIiwiZElkIjoiU0QuODI5NzQ0NWEtYzNhNy00NTRjLThkYjItMDhjN2Y3ZjU3YTM1LjE3MjM5NzM0NDIxMDAiLCJiSWQiOiI0VUtaRlYiLCJrZXZJZCI6IlZJOUZGQkE5NjJERTRGNEU2NzkzQzFCRDE3ODNEQTc0OTkiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6ImFKSkRCcHRmTkFZYWhYWkpnSndVSGZfMEdYb05sN0I2MUlMWU1FR19JOHN6dV95bnZ3LVpHdz09IiwidnMiOiJMSSIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.DBCcNLNvFmFm12X_UhP9vNCgGnbPgr5RanUhavImEA0; rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3Mzk5Njk2MzYsImlhdCI6MTcyNDA3MjAzNiwiaXNzIjoia2V2bGFyIiwianRpIjoiMTM0YmU2MTQtYWNjOC00MDQ2LTk0MTQtYzBlYjgzNmQxYTNiIiwidHlwZSI6IlJUIiwiZElkIjoiU0QuODI5NzQ0NWEtYzNhNy00NTRjLThkYjItMDhjN2Y3ZjU3YTM1LjE3MjM5NzM0NDIxMDAiLCJiSWQiOiI0VUtaRlYiLCJrZXZJZCI6IlZJOUZGQkE5NjJERTRGNEU2NzkzQzFCRDE3ODNEQTc0OTkiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiQkxVTjBaIn0.GwXJZF9bmvyhzt_8Gc89-9hjWa2WSn3lCBIJ9MEOIrs; Network-Type=4g; gpv_pn=HomePage; gpv_pn_t=FLIPKART%3AHomePage; s_sq=flipkart-prd%3D%2526pid%253DHomePage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.flipkart.com%25252Faccount%25252Forders%25253Flink%25253Dhome_orders%2526ot%253DA; K-ACTION=null; S=d1t19EG41Pz8aCWg3NWwhPz88P04lmR/p+iIk8FB/7fKg+5vogftd/ASvcf87/12CHFZ52oJcPRxylLhURm/cwqCaJw==; vd=VI9FFBA962DE4F4E6793C1BD1783DA7499-1723997889278-5.1724072246.1724072036.157882264; SN=VI9FFBA962DE4F4E6793C1BD1783DA7499.TOK92737F6595C3415085C54EBF91F0CCD0.1724072252.LI',
        'Origin': 'https://www.flipkart.com',
        'Referer': 'https://www.flipkart.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 FKUA/website/42/website/Desktop',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'page': '1',
        'filterType': 'PREORDER_UNITS',
    }

    response = requests.get(
        'https://2.rome.api.flipkart.com/api/5/self-serve/orders/',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    Order_History = []

    if(response.status_code == 200):
        data = response.json().get("RESPONSE").get("multipleOrderDetailsView").get("orders")
        for json_response in data:
            order_meta = json_response.get('orderMetaData', {})
            order_id = order_meta.get('orderId')
            # order_date = order_meta.get('orderDate')
            order_date = datetime.fromtimestamp(order_meta.get('orderDate') / 1000.0).strftime('%Y-%m-%d')
            marketplace = order_meta.get('orderMarketPlaceMeta')
            number_of_items = order_meta.get('numberOfItems')

            # Extract product details
            product_data = json_response.get('productDataBag', {})
            product_key = next(iter(product_data))  # Get the first product key
            product_info = product_data.get(product_key, {}).get('productBasicData', {})
            product_title = product_info.get('title')
            product_category = product_info.get('category')
            product_image_url = product_info.get('imageLocation', {}).get('1000x1000')
            product_price = json_response.get('orderMoneyDataBag', {}).get('amount')
            product_quantity = json_response.get('units', {}).get(product_key + "00000", {}).get('deliveryDataBag', {}).get('quantity')

            # Extract delivery details
            delivery_data = json_response.get('units', {}).get(product_key + "00000", {}).get('deliveryDataBag', {})
            delivery_status = delivery_data.get('status', {}).get('text')
            delivered_date = delivery_data.get('promiseDataBag', {}).get('actualDeliveredDate')



            # Create a dictionary with the extracted details
            parsed_details = {
                'order_id': order_id,
                'order_date': order_date,
                'marketplace': marketplace,
                'number_of_items': number_of_items,
                'product_title': product_title,
                'product_image_url': product_image_url,
                'product_price': product_price,
                'product_category':product_category,
            }

            Order_History.append(parsed_details)
    else:
        print("Bad request",response.status_code)    

    return Order_History