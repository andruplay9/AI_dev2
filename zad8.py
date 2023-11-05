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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'embedding')

response = OpenAIAPI.Embedding.create(
    api_key = NotToCommit.ApiDev2OpenAIKey,
    input="Hawaiian pizza",
    model="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']
print(embeddings)
connector.sendresultasjson(embeddings)