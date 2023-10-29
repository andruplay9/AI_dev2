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

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")

connector=aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'liar')
print(connector.question)
qustiontable=['What is capital of Poland?','What is capital of Hungary?','What is capital of USA?','What is capital of France?']
qustion=qustiontable[random.randint(0,len(qustiontable)-1)]
tocheck= connector.sendQuestion(qustion)

humanjson={
    'question': qustion,
    'answer': json.loads(tocheck.text)['answer']
}
print(str(humanjson))

systemPrompt='''You are Guardrails
your job is to check if answer is for given question or not
you get both question and answer in json
you answer only with word YES or NO'''
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
            ("system",systemPrompt),
            ("human",human_template),
        ])

chain = chat_prompt | ChatOpenAI(openai_api_key=NotToCommit.ApiDev2OpenAIKey) | CommaSeparatedListOutputParser()
result = chain.invoke({'text':str(humanjson)})
print(result[0])
connector.sendresultasjson(result[0])
