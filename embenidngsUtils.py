
import openai as OpenAIAPI
import pandas as pd
import whisper
import requests
import time
import hnswlib #https://github.com/nmslib/hnswlib
import numpy as np
import pickle
from io import StringIO
import tiktoken

class EmbendingsHandle:
    model="text-embedding-ada-002"
    def __init__(self, apikey):
        # https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
        # https://platform.openai.com/docs/api-reference/embeddings/create
        self.apikey=apikey
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.vectorTable = hnswlib.Index(space = 'l2', dim = 1536)

    def GetEnbendingWithRequest(self, inputValue):
        response = OpenAIAPI.Embedding.create(
            api_key = self.apikey,
            input = inputValue,
            model = self.model
        )
        print(response['usage'])
        return response
    def GetEnbending(self, inputValue):
        response = self.GetEnbendingWithRequest(inputValue)
        return [x['embedding'] for x in response['data']]

    def CreateEnbendingsFromDataFrame(self, listToEmbend):
        presentTokenCount = 0
        presentTokens = []
        finalList = []
        waitCounter = 0

        for index, value in enumerate(listToEmbend):
            tokenized = self.encoding.encode(value)
            if presentTokenCount + len(tokenized) > 8190:
                tempTable = self.GetEnbending(presentTokens)
                for embending in tempTable:
                    finalList.append(embending)
                presentTokenCount = 0
                print(f"{index} {len(tempTable)} {len(finalList)} ")
                presentTokens = []
                waitCounter = waitCounter + 1
            presentTokenCount = presentTokenCount + len(tokenized)
            presentTokens.append(tokenized)
            if waitCounter > 47: #after 50 request openai required 1 min cooldown
                print("wait Minute")
                time.sleep(60)
                waitCounter = 0
        tempTable = self.GetEnbending(presentTokens)
        for embending in tempTable:
            finalList.append(embending)
        print(len(finalList))
        return finalList

    def CreateVectorDataBase(self, listToEmbend):
        listToEmbend=self.CreateEnbendingsFromDataFrame(listToEmbend)
        self.vectorTable.init_index(max_elements = len(listToEmbend), ef_construction = 200, M = 16)
        self.vectorTable.add_items(listToEmbend, range(len(listToEmbend)))
        self.vectorTable.set_ef(50)
        return listToEmbend, self.vectorTable

    def SearchInVectorDatabase(self, searchstring, searchDepth=3):
        response = self.GetEnbending(searchstring)
        labels, distances = self.vectorTable.knn_query(response[0], k = searchDepth)
        print(f'{labels} {distances}')
        return labels, distances