import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatLiteLLM
from salesgpt.agents import SalesGPT

# Load environment variables
load_dotenv()

llm = ChatLiteLLM(temperature=0.9, model_name="gpt-4o-mini-0613")

# Create the SalesGPT agent with Flipkart-specific information
sales_agent = SalesGPT.from_llm(
    llm,
    verbose=False,
    salesperson_name="Ted Lasso",
    salesperson_role="Business Development Representative",
    company_name="Flipkart",
    company_business="""Flipkart is a leading e-commerce platform in India, 
                        offering a wide range of products including electronics, 
                        fashion, home essentials, groceries, and lifestyle products. 
                        We are committed to providing our customers with the best 
                        online shopping experience by offering high-quality products, 
                        competitive prices, and exceptional customer service.""",
)

# Initialize the agent
sales_agent.seed_agent()

# Get a generator for the LLM output, streaming responses
generator = sales_agent.step(stream=True)

# Process the streaming LLM output in near-real time
for chunk in generator:
    print(chunk)
