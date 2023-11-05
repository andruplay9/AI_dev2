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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'whisper')
link=re.search("(?P<url>https?://[^\s]+)", connector.question['msg']).group("url")
print(link)

doc = requests.get(link)
with open('myfile.mp3', 'wb') as f:
    f.write(doc.content)



def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = OpenAIAPI.Audio.transcribe("whisper-1", audio_file, api_key = NotToCommit.ApiDev2OpenAIKey)
    return transcription['text']

result=transcribe_audio('myfile.mp3')
print(result)
connector.sendresultasjson(result)