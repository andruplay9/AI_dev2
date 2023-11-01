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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'inprompt')
# print(connector.question)
data = connector.question['input']
print(data)
keys = [key.split()[0] for key in data]
print(keys)
question = connector.question['question']
questionKeywords = question.split()
print(questionKeywords)
bad_chars = [';', ':', '!', "*", " ", "?"]

for index, toCorrect in enumerate(questionKeywords):
    for i in bad_chars:
        toCorrect = toCorrect.replace(i, '')
    questionKeywords[index] = toCorrect

print(questionKeywords)
person = ''
for keyword in set(questionKeywords) & set(keys):
    print(keyword)
    person = keyword
info = ''
for i, key in enumerate(keys):
    if key == person:
        print(data[i])
        info = data[i]
print(info)


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


systemPrompt = '''You are assistans that answer in polish 
your job is to answer using only information from context
otherwise say "Nie mam informacji na to pytanie"

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
