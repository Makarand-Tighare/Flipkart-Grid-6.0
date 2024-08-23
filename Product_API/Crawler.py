from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup as bs

def generate_paragraph(info):
    paragraph = []

    if info.get("product_description"):
        paragraph.append(f"{info['discount_percent']} ")

    if info.get("original_price") and info.get("discount_percent"):
        paragraph.append(f"**Product has a discount of {info['discount_percent']} from the original price of {info['original_price']}.**")

    if info.get("rating") and info.get("no_of_rating") and info.get("no_of_reviews"):
        paragraph.append(f"**The product has a rating of {info['rating']} based on {info['no_of_rating']} ratings and {info['no_of_reviews']} reviews.**")

    if info.get("highlights"):
        paragraph.append(f"**Some of the key highlights include: {', '.join(info['highlights'])}.**")

    if info.get("offers"):
        offers = [f"{offer['Offer_type']}: {offer['Offer_Description']}" for offer in info["offers"]]
        paragraph.append(f"**Current offers available are: {', '.join(offers)}.**")

    if info.get("specs"):
        specs = []
        for spec in info["specs"]:
            section_title = spec["title"]
            section_details = ', '.join([f"{item['property']}: {item['value']}" for item in spec["details"]])
            specs.append(f"{section_title} - {section_details}")
        paragraph.append(f"**Specifications include: {'. '.join(specs)}.**")

    return ' '.join(paragraph)


def Get_Related_Post(url: str):
    '''
    Example Url

    1. https://www.flipkart.com/search?q=tv&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_8_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_8_0_na_na_na&as-pos=8&as-type=TRENDING&suggestionId=tv&requestId=cbf12b63-0b14-4eeb-b131-afc9e1695106

    2. https://www.flipkart.com/sports/cycling/electric-cycle/pr?sid=abc%2Culv%2Ctwp&hpid=IN6WQymhhksnM1l95t0Z6Kp7_Hsxr70nj65vMAAFKlc%3D&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJVcCB0byA0MCUgT2ZmIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwiaGVyb1BpZCI6eyJzaW5nbGVWYWx1ZUF0dHJpYnV0ZSI6eyJrZXkiOiJoZXJvUGlkIiwiaW5mZXJlbmNlVHlwZSI6IlBJRCIsInZhbHVlIjoiRUNZSDJYNjQyQ0hYRERDViIsInZhbHVlVHlwZSI6IlNJTkdMRV9WQUxVRUQifX0sInRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkVsZWN0cmljIEN5Y2xlIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D

    '''
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    elements = soup.find_all("div", class_="_75nlfW")
    if len(elements) == 0:
        elements = soup.find_all("div", class_="slAVV4")

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

                if(len(results) >= 10):
                    break
                

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

    headers= {
        "Accept": "*/*",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "T=TI167691702105300117865288941532480409109681842272596976629217172849; dpr=1.25; _pxvid=a7fc4815-288b-11ef-8873-38fcb074a11b; ud=1.3RovXtHZlV6Ku4MnxYAGp12z9rswmi-Rm7GUyv5aizXCUI2_V6rn93V7V4ogfQ4fm36i3_Z-aKTDlXSoF8wff-Q5J7MMLR9utbckD-pUX1AuKf2V7ID2Mvgt-GqK0obnRPoz8bqk3INFmShTe_eIS9cCNFa1NHTnmCgl9pycz5IeO4LIPN__yoHFauwjrhNOShjS3S6zDlEYhWZNLPq5HYwavcfNzyJVZPZP7Jp0fn40rq1Q0Bxjutf4ioXUUJ9U1S1XDspLRa14r4sfIEkZ_dF-cx_vkm0ScTP3OCCNq8T8ATDaZo2Z-Q-pyyIdFmtgryhfvQce96qIRWg_pdpP5z4yq_rgToXUe36Ygxev8fB55U9NKbOkFNSBO_lXaKeQh9zfYnNdZvRW3KzyPVPOY5WD_yO9lVnt0dI-bjTncs5bq_MK7fv6xJfZqohdBelrZ4HMN3SLHKZXJnQu-TTh2AtpPbC4gVzAPwPo-1-0q5q48A6iAMy2v-HcMEs8MbbGoJseU8xrktTWaRWA3UjAlA22CIkDIbGMVC8Y-_kuy4ZAwbfc1toAJ09XUNR411uS0oPz_2aEuwP32ZqfV0Y4G8YofqONN3_TppZw1U3G1oQo3hYCLc4ZBhXbgLxzgIw6FE9X8BpEEzIASb-kcPAkfMR5rMpsqA9o4rvCfZxMyfhxGjYayWnISlRH57DhKOjW8HcXcY2lYvSpKwF9ClVta2Vb_KUJEBHnNbZRE4DPk-2QHswcT0fa4GYsDC7ZkNIp2kQ6cIn4hrv-Gh0Gcb0USRS7oH-IAJRO0afM1TrfY4qVtoLGYOtBycojNShq0y273jv4QcNrut7_Z2eken_McAK7Ofvo3Wx5R-J3p6doemo; vh=730; vw=1536; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3MjQzOTk2OTksImlhdCI6MTcyNDM5Nzg5OSwiaXNzIjoia2V2bGFyIiwianRpIjoiYzVhNTkzMDUtMjljNS00MjI5LWI5YTItNmYxZjhkY2Q4ODA3IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNjc2OTE3MDIxMDUzMDAxMTc4NjUyODg5NDE1MzI0ODA0MDkxMDk2ODE4NDIyNzI1OTY5NzY2MjkyMTcxNzI4NDkiLCJiSWQiOiJEWE1RT0IiLCJrZXZJZCI6IlZJNjQ1RTE0MTM2NDFGNDdDOEFBNDA3RTRFNTgwOEY2MkYiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6ImFBbHNIMUF0Y2RjdjZia29kVmR2cXlzYTZEcmN0UTNxNW80ZHFYb0hHQXhWOGdRU1NvMC0wdz09IiwidnMiOiJMSSIsInoiOiJDSCIsIm0iOnRydWUsImdlbiI6NH0.Z_Pkf9N4kSXn9PY13Iar5jEM0cuAIfzOVjEJBUUoH1Y; rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3NDAyOTU0OTksImlhdCI6MTcyNDM5Nzg5OSwiaXNzIjoia2V2bGFyIiwianRpIjoiY2RhYjBlZGUtN2U5My00N2FkLWIzYTAtY2ZjYjliODE5OTlmIiwidHlwZSI6IlJUIiwiZElkIjoiVEkxNjc2OTE3MDIxMDUzMDAxMTc4NjUyODg5NDE1MzI0ODA0MDkxMDk2ODE4NDIyNzI1OTY5NzY2MjkyMTcxNzI4NDkiLCJiSWQiOiJEWE1RT0IiLCJrZXZJZCI6IlZJNjQ1RTE0MTM2NDFGNDdDOEFBNDA3RTRFNTgwOEY2MkYiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiR0JOVkU3In0.CZ3xe59gmv8DF8ld8uGWZ6h_ms_lF1tP_yM7rLvXPf8; vd=VI645E1413641F47C8AA407E4E5808F62F-1709307194916-29.1724397899.1724397899.155871111; Network-Type=4g; K-ACTION=null; gpv_pn=HomePage; gpv_pn_t=FLIPKART%3AHomePage; AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg=1; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C19959%7CMCMID%7C55226863504053773221742399294611358139%7CMCAAMLH-1724612704%7C12%7CMCAAMB-1725002703%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1724405103s%7CNONE%7CMCAID%7CNONE; s_sq=flipkart-prd%3D%2526pid%253DHomePage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.flipkart.com%25252Faccount%25252Forders%25253Flink%25253Dhome_orders%2526ot%253DA; S=d1t18Pz9WcT8/NWk/P2YHaD9pP+e0rOZlBm4AnEneTHgXEvOFJVG2sp0Ijgm/+vLmt/Iq67dKB2jEdaxqYX2meucykQ==; SN=VI645E1413641F47C8AA407E4E5808F62F.TOK69262851B6C74A998F1A365C46D6ABA4.1724397929.LI",
        "Origin": "https://www.flipkart.com",
        "Referer": "https://www.flipkart.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "X-User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 FKUA/website/42/website/Desktop",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
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
    print(response)

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

