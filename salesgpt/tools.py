import json
import os
import random
import threading
import boto3
import requests
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import BedrockChat
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from litellm import completion
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Product_API.Crawler import Get_Related_Post,Get_Product_Details,generate_paragraph, order_product

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def setup_knowledge_base(
    product_catalog: str = None, model_name: str = "gpt-4o-mini"
):
    """
    We assume that the product catalog is simply a text string.
    """
    if not product_catalog:
        raise ValueError("Product catalog path must be provided and cannot be None.")

    # load product catalog
    with open(product_catalog, "r") as f:
        product_catalog = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=200)
    texts = text_splitter.split_text(product_catalog)

    llm = ChatOpenAI(model_name=model_name, temperature=0)

    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_texts(
        texts, embeddings, collection_name="product-knowledge-base"
    )

    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
    )
    return knowledge_base


def completion_bedrock(model_id, system_prompt, messages, max_tokens=1000):
    """
    High-level API call to generate a message with Anthropic Claude.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name=os.environ.get("AWS_REGION_NAME")
    )

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": messages,
        }
    )

    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())

    return response_body


def get_product_id_from_query(query, product_price_id_mapping_path):
    # Load product_price_id_mapping from a JSON file
    with open(product_price_id_mapping_path, "r") as f:
        product_price_id_mapping = json.load(f)

    # Serialize the product_price_id_mapping to a JSON string for inclusion in the prompt
    product_price_id_mapping_json_str = json.dumps(product_price_id_mapping)

    # Dynamically create the enum list from product_price_id_mapping keys
    enum_list = list(product_price_id_mapping.values()) + [
        "No relevant product id found"
    ]
    enum_list_str = json.dumps(enum_list)

    prompt = f"""
    You are an expert data scientist and you are working on a project to recommend products to customers based on their needs.
    Given the following query:
    {query}
    and the following product price id mapping:
    {product_price_id_mapping_json_str}
    return the price id that is most relevant to the query.
    ONLY return the price id, no other text. If no relevant price id is found, return 'No relevant price id found'.
    Your output will follow this schema:
    {{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Price ID Response",
    "type": "object",
    "properties": {{
        "price_id": {{
        "type": "string",
        "enum": {enum_list_str}
        }}
    }},
    "required": ["price_id"]
    }}
    Return a valid directly parsable json, dont return in it within a code snippet or add any kind of explanation!!
    """
    prompt += "{"
    model_name = os.getenv("GPT_MODEL", "gpt-4o-mini-1106")

    if "anthropic" in model_name:
        response = completion_bedrock(
            model_id=model_name,
            system_prompt="You are a helpful assistant.",
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=1000,
        )

        product_id = response["content"][0]["text"]

    else:
        response = completion(
            model=model_name,
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=1000,
            temperature=0,
        )
        product_id = response.choices[0].message.content.strip()
    return product_id


def generate_stripe_payment_link(query: str) -> str:
    """Generate a stripe payment link for a customer based on a single query string."""

    # example testing payment gateway url
    PAYMENT_GATEWAY_URL = os.getenv(
        "PAYMENT_GATEWAY_URL", "https://agent-payments-gateway.vercel.app/payment"
    )
    PRODUCT_PRICE_MAPPING = os.getenv(
        "PRODUCT_PRICE_MAPPING", "example_product_price_id_mapping.json"
    )

    # use LLM to get the price_id from query
    price_id = get_product_id_from_query(query, PRODUCT_PRICE_MAPPING)
    price_id = json.loads(price_id)
    payload = json.dumps(
        {"prompt": query, **price_id, "stripe_key": os.getenv("STRIPE_API_KEY")}
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", PAYMENT_GATEWAY_URL, headers=headers, data=payload
    )
    return response.text

def get_mail_body_subject_from_query(query):
    prompt = f"""
    Given the query: "{query}", analyze the content and extract the necessary information to send an email. The information needed includes the recipient's email address, the subject of the email, and the body content of the email. 
    Based on the analysis, return a dictionary in Python format where the keys are 'recipient', 'subject', and 'body', and the values are the corresponding pieces of information extracted from the query. 
    For example, if the query was about sending an email to notify someone of an upcoming event, the output should look like this:
    {{
        "recipient": "example@example.com",
        "subject": "Upcoming Event Notification",
        "body": "Dear [Name], we would like to remind you of the upcoming event happening next week. We look forward to seeing you there."
    }}
    Now, based on the provided query, return the structured information as described.
    Return a valid directly parsable json, dont return in it within a code snippet or add any kind of explanation!!
    """
    model_name = os.getenv("GPT_MODEL", "gpt-4o-mini-1106")

    if "anthropic" in model_name:
        response = completion_bedrock(
            model_id=model_name,
            system_prompt="You are a helpful assistant.",
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=1000,
        )

        mail_body_subject = response["content"][0]["text"]

    else:
        response = completion(
            model=model_name,
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=1000,
            temperature=0.2,
        )
        mail_body_subject = response.choices[0].message.content.strip()
    print(mail_body_subject)
    return mail_body_subject

def send_email_with_gmail(email_details):
    '''.env should include GMAIL_MAIL and GMAIL_APP_PASSWORD to work correctly'''
    try:
        sender_email = os.getenv("GMAIL_MAIL")
        app_password = os.getenv("GMAIL_APP_PASSWORD")
        recipient_email = email_details["recipient"]
        subject = email_details["subject"]
        body = email_details["body"]
        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Email was not sent successfully, error: {e}"

def send_email_tool(query):
    '''Sends an email based on the single query string'''
    email_details = get_mail_body_subject_from_query(query)
    if isinstance(email_details, str):
        email_details = json.loads(email_details)  # Ensure it's a dictionary
    print("EMAIL DETAILS")
    print(email_details)
    result = send_email_with_gmail(email_details)
    return result


def generate_calendly_invitation_link(query):
    '''Generate a calendly invitation link based on the single query string'''
    event_type_uuid = os.getenv("CALENDLY_EVENT_UUID")
    api_key = os.getenv('CALENDLY_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.calendly.com/scheduling_links'
    payload = {
    "max_event_count": 1,
    "owner": f"https://api.calendly.com/event_types/{event_type_uuid}",
    "owner_type": "EventType"
    }
    
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        data = response.json()
        return f"url: {data['resource']['booking_url']}"
    else:
        return "Failed to create Calendly link: "
    
def get_related_products(query) :
    
    url = "https://www.flipkart.com/search?q=" + query

    for _ in range(3):
        order_details = Get_Related_Post(url)
        if order_details:
            break

    found_products = ""

    formatted_response = ""
    for index, order in enumerate(order_details):
        found_products += order['Product_Name'] + "\n"
        for _ in range(3):
            product_details = Get_Product_Details(order['Product_URL'])
            if product_details:
                break
        
        Product_summery = generate_paragraph(product_details)

        formatted_response += f"Product Name {index}: {order['Product_Name']}\nProduct Url: {order['Product_URL']}\nPrice: ₹{order['Current_Price']}\nDescription: {Product_summery}\n\n"

    with open(os.path.join(BASE_DIR, 'examples/sample_product_catalog.txt'), 'w', encoding='utf-8') as file:
        file.write(formatted_response)

    if len(formatted_response) > 0:
        return f"we found some amezing products for you\n{found_products}\n\nplease specify the product name to get more details"
    else:
        return f"We don't find any relevent products for {query} You can ask something else"
    
def OrderProduct(query):
    details = query.split(",")
    print(details)
    print("\n\n\n\n\n\n")
    try:
        upi_id = details[1].replace(" ","")
        postal_code = details[2].replace(" ","")
        if(len(postal_code) == 6):
            thread = threading.Thread(target=order_product, args=(details[1], details[2], details[0]))
            thread.start()
            return f"Your order has been placed succesfully"
        else : 
            return f"Please provide valid UPI id and postal code"
    except:
        return f"Error occured during product order please try later"

def product_search_with_fallback(query, knowledge_base):
    """
    Searches for products using the knowledge base.
    If no products are found, it calls the get_related_products function.
    """
    response = knowledge_base.run(query)
    if "couldn't find specific" in response or not response.strip():
        # Fallback to get_related_products if no results found
        response = get_related_products(query)
        if "amezing products" in response:
            # Update the product catalog file if related products are found
            with open(os.path.join(BASE_DIR, 'examples/sample_product_catalog.txt'), 'a', encoding='utf-8') as file:
                file.write(response)
    return response



def get_tools(product_catalog):
    knowledge_base = setup_knowledge_base(product_catalog)

    tools = [
        Tool(
            name="ProductSearch",
            func=lambda query: product_search_with_fallback(query, knowledge_base),
            description=(
                "Use this tool to search for product information, including features, availability, and pricing details "
                "based on the user's query. If the specific product is not found in the existing catalog, "
                "this tool will automatically fetch related products from external sources. This ensures that the user receives information "
                "even when the desired product is not in the catalog. Use this tool for queries like 'Find a laptop with 16GB RAM' or 'Show me options for ergonomic chairs'."
            ),
        ),
        Tool(
            name="GeneratePaymentLink",
            func=generate_stripe_payment_link,
            description="Generates a payment link for a transaction. Include product name, quantity, and customer name.",
        ),
        Tool(
            name="SendEmail",
            func=send_email_tool,
            description="Sends an email. Query must specify the recipient, subject, and body.",
        ),
        Tool(
            name="SendCalendlyInvitation",
            func=generate_calendly_invitation_link,
            description="Creates a Calendly invitation for scheduling meetings based on user input.",
        ),
        Tool(
            name="GetRelatedProducts",
            func=get_related_products,
            description=(
                "Use this tool to find related products from external sources when the specific product the user is looking for is not available in the catalog. "
                "This tool scrapes external sources to find similar products based on the user's preferences. "
                "This is useful for queries such as 'Find more options for wireless headphones' or 'Show me some alternatives to gaming laptops' or 'recommend me some laptops' etc...."
            ),
        ),
        Tool(
            name="OrderProduct",
            func=OrderProduct,
            description=(
                "Use this tool to place an order for a product. The input must include the product URL, UPI ID, and postal code, "
                "all separated by commas. This is specifically for completing a purchase when the user provides all the required "
                "details. If any detail is missing, ask the user for the necessary information. Example input: "
                "'Place an order for https://example.com/product, 1234567890@upi, 123456'."
            ),
        )
    ]

    return tools
