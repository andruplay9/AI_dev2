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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'gnome')

client=OpenAIAPI.OpenAI(api_key = NotToCommit.ApiDev2OpenAIKey)

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Jakiego koloru jest czapka? Jeżeli nie znalazleś czapki zwróć 'error'. Nie dodawaj żadnych komentarzy i odpowiadaj jak najkrócej"},
        {
          "type": "image_url",
          "image_url": {
            "url": connector.question['url'],
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0].message.content)
connector.sendresultasjson(response.choices[0].message.content)