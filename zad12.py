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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'scraper')

link = connector.question['input']
question= connector.question['question']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}
statuscode=404
while statuscode>200:
    req = requests.get(link, headers = headers)
    print(req)
    statuscode=req.status_code
    print(statuscode)
    info=req.text
    print(info)
    time.sleep(1)



class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


systemPrompt = '''You are assistans that answer in polish 
your job is to answer using only information from context
otherwise say "Nie mam informacji na to 
Maxymalna długość to 180 znaków"

contexst:
{dataToSystem}
'''
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", systemPrompt),
    ("human", human_template),
])

chain = chat_prompt | ChatOpenAI(openai_api_key = NotToCommit.ApiDev2OpenAIKey) | CommaSeparatedListOutputParser()
result = chain.invoke({'dataToSystem': info, 'text': str(question)})
print(result[0])
connector.sendresultasjson(result[0])