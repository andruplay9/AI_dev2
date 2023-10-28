import NotToCommit
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import openai


llm = OpenAI(openai_api_key=NotToCommit.ApiDev2OpenAIKey)
chat_model = ChatOpenAI(openai_api_key=NotToCommit.ApiDev2OpenAIKey)

#text = "What would be a good company name for a company that makes colorful socks?"
#print(llm.predict(text))
#print(chat_model.predict(text))


#prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
#prompt.format(product="colorful socks")

from langchain.prompts.chat import ChatPromptTemplate

template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

output=chat_prompt.format_messages(input_language="English", output_language="French", text="I love programming.")
print(output)
import json
response = openai.Moderation.create(
    input="Sample text goes here",
    api_key=NotToCommit.ApiDev2OpenAIKey
)
output = response["results"][0]
print(output)
print(output["flagged"])


from langchain.schema import BaseOutputParser


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")

class TestSendPromptAndGetIt():

    def send(self):
        template = """You are a helpful assistant who generates comma separated lists.
        A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
        ONLY return a comma separated list, and nothing more."""
        human_template = "{text}"
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template),
        ])
        chain = chat_prompt | ChatOpenAI(openai_api_key=NotToCommit.ApiDev2OpenAIKey) | CommaSeparatedListOutputParser()
        result=chain.invoke({"text": "cloths"})
        print(result)

