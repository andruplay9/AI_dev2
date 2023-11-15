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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'tools')

messages = [{"role": "user", "content": connector.question['question']},{"role": "system", "content": "Today is Wednesday 2023-11-15"}]
print(messages)
tools = [
    {
        "type": "function",
        "function": {
            "name": "Process_task",
            "description": "Process task that is on given day",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to do, e.g. 'spotkanie z marianem' or 'kupic mleko'",
                    },
                    "taskType": {
                        "type": "string",
                        "enum": ["ToDo", "Calendar"],
                        "description": "if had date is calendar type, else TODO"
                    },
                    "data": {
                        "type": "string",
                        "description": "Date of task in YYYY-MM-DD format, e.g. '2023-11-22'",
                    },


                },
                "required": ["task", "taskType"],
            },
        },
    },
]
client=OpenAIAPI.OpenAI(api_key = NotToCommit.ApiDev2OpenAIKey)
response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit

    )
response_message = response.choices[0].message.tool_calls
print(response_message)

def set_task(data):
    task=data['task']
    taskType=data['taskType']
    answer=''
    if taskType == "Calendar" or 'data' in data:
        date = data['data']
        answer={"tool":"Calendar","desc":task,"date":date}
    else:
        answer={"tool":"ToDo","desc":task}
    connector.sendresultasjson(answer)

available_functions = {
    "Process_task": set_task,
}

embenidngsUtils.process_function_calling(response_message, available_functions)