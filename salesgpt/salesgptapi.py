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
        product_catalog: str = "examples/sample_product_catalog.txt",
        use_tools=True,
    ):
        self.config_path = config_path
        self.verbose = verbose
        self.max_num_turns = max_num_turns
        self.model_name = model_name
        if "anthropic" in model_name:
            self.llm = BedrockCustomModel(
                type="bedrock-model",
                model=model_name,
                system_prompt="You are a helpful assistant.",
            )
        else:
            self.llm = ChatLiteLLM(temperature=0.2, model=model_name)
        self.product_catalog = product_catalog
        self.conversation_history = []
        self.use_tools = use_tools
        self.sales_agent = self.initialize_agent()
        self.current_turn = 0

    def initialize_agent(self):
        config = {"verbose": self.verbose}
        if self.config_path:
            with open(self.config_path, "r") as f:
                config.update(json.load(f))
            if self.verbose:
                print(f"Loaded agent config: {config}")
        else:
            print("Default agent config in use")

        if self.use_tools:
            print("USING TOOLS")
            config.update(
                {
                    "use_tools": True,
                    "product_catalog": self.product_catalog,
                    "salesperson_name": "Flippi"
                    if not self.config_path
                    else config.get("salesperson_name", "Flippi"),
                }
            )

        sales_agent = SalesGPT.from_llm(self.llm, **config)

        print(f"SalesGPT use_tools: {sales_agent.use_tools}")
        sales_agent.seed_agent()
        return sales_agent

    async def do(self, human_input=None):
        self.current_turn += 1
        current_turns = self.current_turn
        if current_turns >= self.max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            return [
                "BOT",
                "In case you'll have any questions - just text me one more time!",
            ]
        
        # Check if the human input requires product information
        if human_input is not None:
            product_name = self.is_product_query(human_input)
            if product_name:
                # Example check: Assuming `self.product_catalog` contains a list or dict of known products
                if not self.is_product_available(human_input):
                    print(f"Product not found in catalog: {human_input}. Fetching from API...")
                    product_info = self.fetch_product_info_from_api(human_input)
                    if product_info:
                        self.update_product_catalog(human_input, product_info)
                    else:
                        print(f"Could not fetch product information for: {human_input}")
                        return ["BOT", "Sorry, I couldn't find information on that product."]
            else:    
                self.sales_agent.human_step(human_input)

        ai_log = await self.sales_agent.astep(stream=False)
        await self.sales_agent.adetermine_conversation_stage()

        # TODO - handle end of conversation in the API - send a special token to the client?
        if self.verbose:
            print("=" * 10)
            print(f"AI LOG {ai_log}")
            
        if (
            self.sales_agent.conversation_history
            and "<END_OF_CALL>" in self.sales_agent.conversation_history[-1]
        ):
            print("Sales Agent determined it is time to end the conversation.")
            # strip end of call for now
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
        #print("AI LOG INTERMEDIATE STEPS: ", ai_log["intermediate_steps"])

        if (
            self.use_tools and 
            "intermediate_steps" in ai_log and 
            len(ai_log["intermediate_steps"]) > 0
        ):
            
            try:
                res_str = ai_log["intermediate_steps"][0]
                print("RES STR: ", res_str)
                agent_action = res_str[0]
                tool, tool_input, log = (
                    agent_action.tool,
                    agent_action.tool_input,
                    agent_action.log,
                )
                actions = re.search(r"Action: (.*?)[\n]*Action Input: (.*)", log)
                action_input = actions.group(2)
                action_output =  res_str[1]
                if tool_input == action_input:
                    action_input=""
                    action_output = action_output.replace("<web_search>", "<a href='https://www.flipkart.com/search?q=")
                    action_output = action_output.replace("</web_search>", "' target='_blank' rel='noopener noreferrer'>")
            except Exception as e:
                print("ERROR: ", e)
                tool, tool_input, action, action_input, action_output = (
                    "",
                    "",
                    "",
                    "",
                    "",
                )
        else:
            tool, tool_input, action, action_input, action_output = "", "", "", "", ""

        print(reply)
        payload = {
            "bot_name": reply.split(": ")[0],
            "response": response,
            "conversational_stage": self.sales_agent.current_conversation_stage,
            "tool": tool,
            "tool_input": tool_input,
            "action_output": action_output,
            "action_input": action_input,
            "model_name": self.model_name,
        }
        return payload
    
    def is_product_available(self, product_name):
        # Example logic to check if product is in catalog
        with open(self.product_catalog, "r") as f:
            catalog = f.read()
        return product_name.lower() in catalog.lower()

    def fetch_product_info_from_api(self, product_name):
        # Replace with your API call logic
        base_url = "https://www.flipkart.com/search?q="
        full_url = base_url + product_name
        print(full_url)
        response = requests.post("http://127.0.0.1:5000/get_related_post", json={"url": full_url})
        if response.status_code == 200:
            return response.json()
        return None

    def update_product_catalog(self, product_name, product_info):
        # Example logic to update catalog
        with open(self.product_catalog, "a") as f:
            formatted_info = f"{product_name}: {json.dumps(product_info)}\n"
            f.write(formatted_info)
    
    def is_product_query(self, query):
        # Define a condition to determine if the query is related to a product
        product_keywords = ["find", "look for", "search for", "show me", "details about", "information on", "available", "options for","suggest me"]
        if any(keyword in query.lower() for keyword in product_keywords):
            return self.extract_product_name(query)
        return None
    
    def extract_product_name(self, query):
    # Example function to extract product name from the query
    # This can be enhanced with more sophisticated NLP techniques if needed
    # For simplicity, we assume the product name is the part of the query after certain keywords
    
    # Define keywords to determine where the product name starts
        product_keywords = ["find", "look for", "search for", "show me", "details about", "information on", "available", "options for","suggest me"]

    
    # Find where the product-related part starts
        for keyword in product_keywords:
            if keyword in query.lower():
             # Extract the part of the query after the keyword
                parts = re.split(r'\b' + keyword + r'\b', query, flags=re.IGNORECASE)
                if len(parts) > 1:
                    # Return the part of the query after the keyword, trimmed
                    return parts[1].strip()
    
    # If no keywords found, return the full query (or handle as needed)
        return query.strip()


    async def do_stream(self, conversation_history: [str], human_input=None):
        # TODO
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
        for model_response in stream_gen:
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
                    yield message
                else:
                    continue
