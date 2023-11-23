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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'meme')

imagesrc = connector.question['image']
texttoinput = connector.question['text']

data = {
    "template": "boring-toads-float-softly-1509",
    "data": {
        "TextField.text": texttoinput,
        "Name.src": imagesrc
    }
}
headers = {
    'X-API-KEY': NotToCommit.apirenderform,
    'Content-Type': 'application/json'
}

result = requests.post(url = 'https://get.renderform.io/api/v2/render', headers = headers, data =json.dumps(data))
print(result)
print(result.text)
connector.sendresultasjson(json.loads(result.text)['href'])
