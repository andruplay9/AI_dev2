from io import StringIO
import aidevmethods
import NotToCommit
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import json
import random
import openai as OpenAIAPI
import pandas as pd
import whisper
import requests
import time
import embenidngsUtils

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'knowledge')

messages = [{"role": "user", "content": connector.question['question']}]
print(messages)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_population",
            "description": "Get the current population in given country",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "The country in english, e.g. Poland",
                    },

                },
                "required": ["country"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_exchange_rate",
            "description": "Get exchange rate for given currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency": {
                        "type": "string",
                        "description": "Currency we need exchange rate, e.g. EURO or USD",
                    },
                },
                "required": ["currency"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_general_knowledge",
            "description": "Get general answer for given question",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Question that need be answered , e.g. 'Kto napisał Romeo I Julia?'",
                    },
                },
                "required": ["question"]
            },
        }
    },
]
client=OpenAIAPI.OpenAI(api_key = NotToCommit.ApiDev2OpenAIKey)
response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit

    )
response_message = response.choices[0].message.tool_calls
print(response_message)
client.close()

systemPrompt = '''Jesteś expertem wiedzowym
twym zadaniem jest odpowiedzieć na zadanie pytanie w miarę jak njakrócej
musisz być całkowicie pewien swej odpowiedzi, od tego zależy moja kariera
jeżeli nie jesteś absolutnie pewien ddpowiedz wylącznie "NO"
nie dodawaj żadnych dodatkowych komentarzy
'''
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", systemPrompt),
    ("human", human_template),
])
class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


def get_general_knowledge(data):
    question=data['question']
    print(question)
    chain = chat_prompt |  ChatOpenAI(openai_api_key = NotToCommit.ApiDev2OpenAIKey) | CommaSeparatedListOutputParser
    result = chain.invoke({'text': question})
    print(result[0])

def get_current_exchange_rate(data):
    currency=data['currency']
    headers = {
        'Accept': 'application/json',
    }
    link=f'http://api.nbp.pl/api/exchangerates/tables/A/today'
    result= requests.get(link, headers=headers)
    print(currency)
    print(result.text)

def get_current_population(data):
    country=data['country']
    link=f'https://restcountries.com/v3.1/name/{country}?fullText=true'
    result= requests.get(link)
    print(country)
    jsonans=json.loads(result.text)
    print(jsonans)
    connector.sendresultasjson(jsonans[0]['population'])

available_functions = {
    "get_general_knowledge": get_general_knowledge,
    "get_current_exchange_rate": get_current_exchange_rate,
    "get_current_population": get_current_population,

}
for tool_call in response_message:
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    print(f'{function_name} {function_to_call} {function_args}')
    function_to_call(function_args)



