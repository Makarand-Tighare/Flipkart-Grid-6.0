import asyncio
import json
import re
from langchain_community.chat_models import BedrockChat, ChatLiteLLM
from langchain_openai import ChatOpenAI

import requests
from salesgpt.agents import SalesGPT
from salesgpt.models import BedrockCustomModel


class SalesGPTAPI:
    def __init__(
        self,
        config_path: str,
        verbose: bool = True,
        max_num_turns: int = 20,
        model_name: str = "gpt-4o-mini",
        product_catalog_path: str = "examples/sample_product_catalog.txt",
        use_tools=True,
    ):
        self.config_path = config_path
        self.verbose = verbose
        self.max_num_turns = max_num_turns
        self.model_name = model_name
        self.use_tools = use_tools
        self.product_catalog_path = product_catalog_path
        self.product_catalog = self.load_product_catalog()
        self.conversation_history = []
        self.current_turn = 0

        # Initialize the LLM based on the model name
        if "anthropic" in model_name:
            self.llm = BedrockCustomModel(
                type="bedrock-model",
                model=model_name,
                system_prompt="You are a helpful assistant.",
            )
        else:
            self.llm = ChatLiteLLM(temperature=0.2, model=model_name)

        # Initialize the sales agent
        self.sales_agent = self.initialize_agent()

    def load_product_catalog(self):
        # Load the product catalog into a dictionary
        product_catalog = {}
        with open(self.product_catalog_path, 'r') as f:
            current_product = None
            for line in f:
                try:
                    if line.startswith("Product Name"):
                        current_product = line.strip().split(": ", 1)[1]
                        product_catalog[current_product] = {"description": "", "url": "", "price": ""}
                    elif line.startswith("Product Url"):
                        product_catalog[current_product]["url"] = line.strip().split(": ", 1)[1]
                    elif line.startswith("Price"):
                        product_catalog[current_product]["price"] = line.strip().split(": ", 1)[1]
                    elif line.startswith("Description"):
                        product_catalog[current_product]["description"] += line.strip().split(": ", 1)[1]
                    else:
                        product_catalog[current_product]["description"] += line.strip()
                except Exception as e:
                    print(e)

        return product_catalog

    def initialize_agent(self):
        config = {"verbose": self.verbose}
        if self.config_path:
            try:
                with open(self.config_path, "r") as f:
                    config.update(json.load(f))
                if self.verbose:
                    print(f"Loaded agent config: {config}")
            except FileNotFoundError:
                print(f"Config file not found at {self.config_path}. Using default configuration.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from config file. Please check the file format.")
        else:
            print("Default agent config in use")

        if self.use_tools:
            print("USING TOOLS")
            config.update(
                {
                    "use_tools": True,
                    "product_catalog_path": self.product_catalog_path,
                    "salesperson_name": "Flippi"
                    if not self.config_path
                    else config.get("salesperson_name", "Flippi"),
                }
            )

        try:
            sales_agent = SalesGPT.from_llm(self.llm, **config)
        except AttributeError as e:
            print(f"Error initializing SalesGPT: {e}")
            raise

        print(f"SalesGPT use_tools: {sales_agent.use_tools}")
        sales_agent.seed_agent()
        return sales_agent

    async def do(self, human_input=None):
        self.current_turn += 1
        if self.current_turn >= self.max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            return [
                "BOT",
                "In case you'll have any questions - just text me one more time!",
            ]

        if human_input:
            product_name = self.is_product_query(human_input)
            if product_name:
                # Use RAG to generate response
                response = self.retrieve_and_generate(product_name)
                return response

            self.sales_agent.human_step(human_input)

        ai_log = await self.sales_agent.astep(stream=False)
        await self.sales_agent.adetermine_conversation_stage()

        if self.verbose:
            print("=" * 10)
            print(f"AI LOG {ai_log}")

        if (
            self.sales_agent.conversation_history
            and "<END_OF_CALL>" in self.sales_agent.conversation_history[-1]
        ):
            print("Sales Agent determined it is time to end the conversation.")
            self.sales_agent.conversation_history[
                -1
            ] = self.sales_agent.conversation_history[-1].replace("<END_OF_CALL>", "")

        reply = (
            self.sales_agent.conversation_history[-1]
            if self.sales_agent.conversation_history
            else ""
        )
        cleaned_reply = reply.replace('`', '')
        response = ": ".join(cleaned_reply.split(": ")[1:]).rstrip("<END_OF_TURN>")

        return response

    def is_product_query(self, query):
        product_keywords = ["find", "look for", "search for", "show me", "details about", "information on", "available", "options for", "suggest me"]
        if any(keyword in query.lower() for keyword in product_keywords):
            return self.extract_product_name(query)
        return None

    def extract_product_name(self, query):
        product_keywords = ["find", "look for", "search for", "show me", "details about", "information on", "available", "options for", "suggest me"]
        for keyword in product_keywords:
            if keyword in query.lower():
                parts = re.split(r'\b' + keyword + r'\b', query, flags=re.IGNORECASE)
                if len(parts) > 1:
                    return parts[1].strip()
        return query.strip()

    def retrieve_and_generate(self, product_name):
        # Search the product catalog
        matching_product = next(
            (product for product in self.product_catalog.keys() if product_name.lower() in product.lower()), 
            None
        )
        if matching_product:
            product_info = self.product_catalog[matching_product]
            # Combine retrieval and generation using the LLM
            response = f"Here is what I found about {matching_product}: {product_info['description']}. You can view more details [here]({product_info['url']}). The price is {product_info['price']}."
        else:
            response = "Sorry, I couldn't find information on that product. Please try another query."
        return ["BOT", response]

    async def do_stream(self, conversation_history: [str], human_input=None):
        # This method provides streaming responses (for real-time interactions)
        current_turns = len(conversation_history) + 1
        if current_turns >= self.max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            yield [
                "BOT",
                "In case you'll have any questions - just text me one more time!",
            ]
            raise StopAsyncIteration

        self.sales_agent.seed_agent()
        self.sales_agent.conversation_history = conversation_history

        if human_input is not None:
            self.sales_agent.human_step(human_input)

        stream_gen = self.sales_agent.astep(stream=True)
        async for model_response in stream_gen:
            for choice in model_response.choices:
                message = choice["delta"]["content"]
                if message is not None:
                    if "<END_OF_CALL>" in message:
                        print(
                            "Sales Agent determined it is time to end the conversation."
                        )
                        yield [
                            "BOT",
                            "In case you'll have any questions - just text me one more time!",
                        ]
                        return
                    yield message
                else:
                    continue
