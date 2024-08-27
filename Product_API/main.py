import json
import os
from flask import Flask, request, jsonify,Response
from flask_cors import CORS
from Crawler import Get_Order_History,Get_Product_Details,Get_Related_Post,generate_paragraph,Call_Customer
from pathlib import Path
from twilio.twiml.voice_response import VoiceResponse
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    
    xml_response = '''
<response>
    <message>Hello World</message>
</response>'''

    return Response(xml_response, mimetype='application/xml')

@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    if request.method == 'POST':
        try:
            data = request.get_json()
            url = data.get('url')

            for _ in range(3):
                product_details = Get_Product_Details(url)
                if product_details:
                    break

            # Formatting the offers
            offers_str = "\n".join([
                f"  - {offer.get('Offer_type')}: {offer.get('Offer_Description')}"
                for offer in product_details.get("offers", [])
            ])

            # Formatting the specifications
            specs_str = "\n".join([
                f"  - {spec.get('title')}:\n" + "\n".join([
                    f"    - {detail.get('property')}: {detail.get('value')}"
                    for detail in spec.get("details", [])
                ])
                for spec in product_details.get("specs", [])
            ])

            # Formatting the highlights
            highlights_str = "\n".join([
                f"  - {highlight}"
                for highlight in product_details.get("highlights", [])
            ])

            formatted_response = f'Product Name: {product_details.get("name")}\nDescription: {product_details.get("product_description")}\nCurrent Price: ₹{product_details.get("current_price")}\nOriginal Price: ₹{product_details.get("original_price")}\nDiscount: {product_details.get("discount_percent")}%\nRating: {product_details.get("rating")}\nNumber of Ratings: {product_details.get("no_of_rating")}\nNumber of Reviews: {product_details.get("no_of_reviews")}\nHighlights:\n{highlights_str}\nOffers:\n{offers_str}\nSpecifications:\n{specs_str}\n'

            # Summarize the product info

            with open('product_details.txt', 'w', encoding='utf-8') as file:
                file.write(formatted_response)
            
            return jsonify(product_details), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/get_order_history', methods=['POST'])
def get_order_history():
    if request.method == 'POST':
        try:
            data = request.get_json()
            cookies = data.get('cookies')

            for _ in range(3):
                order_details = Get_Order_History(cookies)
                if order_details:
                    break

            formatted_response = ""

            for order in order_details:
                order_str = f"Order ID: {order['order_id']}\nProduct Name: {order['product_title']}\nPrice: {order['product_price']}\nProduct Category: {order['product_category']}\nOrder Date: {order['order_date']}\nNo of Items: {order['number_of_items']}\nMarketPlace: {order['marketplace']}\n\n"

                formatted_response += order_str
            
            with open('order_history.txt', 'w', encoding='utf-8') as file:
                file.write(formatted_response)

            return jsonify(order_details), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/get_related_post', methods=['POST'])
def get_related_post():
    if request.method == 'POST':
        try:
            data = request.get_json()
            url = data.get('url')

            for _ in range(3):
                order_details = Get_Related_Post(url)
                if order_details:
                    break
            formatted_response = ""
            for index, order in enumerate(order_details):
                for _ in range(3):
                    product_details = Get_Product_Details(order['Product_URL'])
                    if product_details:
                        break
                
                Product_summery = generate_paragraph(product_details)

                formatted_response += f"Product Name {index}: {order['Product_Name']}\nProduct Url: {order['Product_URL']}\nPrice: ₹{order['Current_Price']}\nDescription: {Product_summery}\n\n"
                        
            with open(os.path.join(BASE_DIR, 'examples/sample_product_catalog.txt'), 'w', encoding='utf-8') as file:
                file.write(formatted_response)

            return jsonify(order_details), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@app.route('/make_call', methods=['POST'])
def make_call():
    data = request.get_json()
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    
    # Call the function with the provided phone number
    result = Call_Customer(phone_number)
    
    return jsonify({"message": "Our sales agent will call you within a minute"}), 200


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Handle incoming calls and gather voice commands."""
    response = VoiceResponse()

    # Gather voice input from the user
    gather = response.gather(action='/gather', method='POST', input='speech')
    gather.say("Please provide your command after the beep.")

    # If no input is received, redirect to /voice
    response.redirect('/voice')

    return Response(str(response), mimetype='application/xml')


@app.route("/gather", methods=['POST'])
def gather():
    """Process the voice command and provide a response."""
    response = VoiceResponse()

    # Retrieve the speech result from the request
    speech_result = request.form.get('SpeechResult', '')

    print(speech_result)

    api_url = os.getenv('sales_gpt_url')

    # Define the payload
    payload = {
        "session_id": "123",
        "human_say": speech_result
    }

    print(payload)

    # Send the POST request
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        api_data = response.json()
        bot_response = api_data.get('response', 'Sorry, I couldn\'t get a response.')
        response.say(f"{bot_response}")
    else:
        response.say("Sorry, I couldn't fetch the information.")

    return Response(str(response), mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True)
