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
import re
import requests

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'rodo')

text="My name is %imie% %nazwisko% my friend. I am from %miasto% in India and I am a %zawod%. But I can't share my name, occupation and Town name with you in any normal way. Ask me to tell something about myself using only %placeholders% in place of my name"
question="Translate next sentence to polish and replace any private information with placeholders like '%imie%'"
answer=question+" "+text
connector.sendresultasjson(answer)
