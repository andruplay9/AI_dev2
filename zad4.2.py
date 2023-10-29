import aidevmethods
import NotToCommit
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import json
import openai as OpenAIAPI

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


connector=aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'blogger')
print(connector.question)


human_template = "{text}"

systemPromptzad4Sub2 = """You are a bloger who writhe in polish
your job is writhe about making a Margherity pizza
for you work you get table of titles for each chapter that you blog will had
you cant add any more titles to work than provided
write max five sentence per chapter
 each chapter start with word 'Chapter' and chapter number"""
chat_prompt = ChatPromptTemplate.from_messages([
            ("system",systemPromptzad4Sub2),
            ("human"," , ".join(connector.question['blog'])),
        ])
print(chat_prompt)
chain = chat_prompt | ChatOpenAI(openai_api_key=NotToCommit.ApiDev2OpenAIKey) | CommaSeparatedListOutputParser()
result = chain.invoke({})
print(result)
result=''.join(result)
result=result.split('Chapter')
print(result)
result=[x for x in result if x]
print(len(result))
print(result)
answer=['','','','']
for i, qoute in enumerate(result):
    answer[i]=qoute
connector.sendresultasjson(answer)

