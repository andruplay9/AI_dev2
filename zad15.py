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

jsonTable=requests.get("https://zadania.aidevs.pl/data/people.json")
table= pd.read_json(StringIO(jsonTable.text))
pd.set_option('display.max_columns', None)

print(table.head())
table['ImieNazwisko']=table.apply(lambda x: x['imie']+' '+x['nazwisko'], axis = 1)
print(table.head())
table['Mieszka']=table.apply(lambda x:  x['o_mnie'].split(".")[1].split(" ")[3:], axis = 1)
print(table.head())
embUtils=embenidngsUtils.EmbendingsHandle(NotToCommit.ApiDev2OpenAIKey)
embUtils.CreateVectorDataBase(table['ImieNazwisko'])
connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'people')
questionText=connector.question['question']
labels, _ = embUtils.SearchInVectorDatabase(questionText)
index=labels[0][0]
answer=''
if 'kolor' in questionText:
    answer=table['ulubiony_kolor'][index]
elif 'mieszka' in questionText:
    answer=table['Mieszka'][index]
elif 'film' in questionText:
    answer=table['ulubiony_film'][index]
elif 'serial' in questionText:
    answer=table['ulubiony_serial'][index]
connector.sendresultasjson(answer)