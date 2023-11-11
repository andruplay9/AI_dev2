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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'whoami')

answer="NO"

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


systemPrompt = '''Jesteś expertem od znanych ludzi
twym zadaniem jest zgadnąć o kogo chodzi
musisz być całkowicie pewien swej odpowiedzi, od tego zależy moja kariera
jeżeli nie jesteś absolutnie pewien ddpowiedz wylącznie "NO"
jeżeli jesteś absolutnie pewien, że to ta osoba i nikt inny to odpowiedz imieniem i nazwiskiem osoby na przyklad "Karol Wojtyła"
nie dodawaj żadnych dodatkowych komentarzy
'''
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", systemPrompt),
    ("human", human_template),
])
hints=''

while answer=="NO":
    hints =hints+'. '+ connector.question['hint']
    chain = chat_prompt | ChatOpenAI(openai_api_key = NotToCommit.ApiDev2OpenAIKey) | CommaSeparatedListOutputParser()
    result = chain.invoke({'text': hints})
    print(result[0])
    print(hints)
    answer=result[0]
    connector.getnewquestion()


connector.sendresultasjson(answer)