
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

connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'functions')

answer={"answer": {
            "name": "addUser",
            "description": "adds user to table",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "provide name of the pizza"
                    },
"surname": {
                        "type": "string",
                        "description": "provide name of the pizza"
                    },
"year": {
                        "type": "integer",
                        "description": "provide name of the pizza"
                    }
                }
            }
        }
}
connector.sendresult(answer)