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
import hnswlib #https://github.com/nmslib/hnswlib
import numpy as np
import pickle
from io import StringIO
import tiktoken


dim = 128
num_elements = 10000

# Generating sample data
data = np.float32(np.random.random((num_elements, dim)))
ids = np.arange(num_elements)

# Declaring index
p = hnswlib.Index(space = 'l2', dim = dim) # possible options are l2, cosine or ip

# Initializing index - the maximum number of elements should be known beforehand
p.init_index(max_elements = num_elements, ef_construction = 200, M = 16)

# Element insertion (can be called several times):
p.add_items(data, ids)

# Controlling the recall by setting ef:
p.set_ef(50) # ef should always be > k

# Query dataset, k - number of the closest elements (returns 2 numpy arrays)
labels, distances = p.knn_query(data, k = 1)

# Index objects support pickling
# WARNING: serialization via pickle.dumps(p) or p.__getstate__() is NOT thread-safe with p.add_items method!
# Note: ef parameter is included in serialization; random number generator is initialized with random_seed on Index load
p_copy = pickle.loads(pickle.dumps(p)) # creates a copy of index p using pickle round-trip

### Index parameters are exposed as class properties:
print(f"Parameters passed to constructor:  space={p_copy.space}, dim={p_copy.dim}")
print(f"Index construction: M={p_copy.M}, ef_construction={p_copy.ef_construction}")
print(f"Index size is {p_copy.element_count} and index capacity is {p_copy.max_elements}")
print(f"Search speed/quality trade-off parameter: ef={p_copy.ef}")


def GetEnbending(inputValue):
    response = OpenAIAPI.Embedding.create(
        api_key = NotToCommit.ApiDev2OpenAIKey,
        input = inputValue,
        model = "text-embedding-ada-002"
    )
    print(response['usage'])
    return response


def CreateEnbendingsFromDataFrame(table, columnToEnbendings):

    #https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    #https://platform.openai.com/docs/api-reference/embeddings/create
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    presentTokenCount = 0
    presentTokens = []
    finalList = []
    waitCounter = 0

    for index, value in enumerate(table[columnToEnbendings]):
        tokenized = encoding.encode(value)
        if presentTokenCount + len(tokenized) > 8190:
            response = GetEnbending(presentTokens)
            tempTable = [x['embedding'] for x in response['data']]
            for embending in tempTable:
                finalList.append(embending)
            presentTokenCount = 0
            print(f"{index} {len(tempTable)} {len(finalList)} ")
            presentTokens = []
            waitCounter = waitCounter + 1
        presentTokenCount = presentTokenCount + len(tokenized)
        presentTokens.append(tokenized)
        if waitCounter > 47:
            print("wait Minute")
            time.sleep(60)
            waitCounter = 0
    response = GetEnbending(presentTokens)
    tempTable = [x['embedding'] for x in response['data']]
    for embending in tempTable:
        finalList.append(embending)

    print(len(finalList))
    table['embendings'] = finalList
    table.to_json(r'Zad14FinalJson.json')


#jsonTable=requests.get("https://unknow.news/archiwum.json")
#table= pd.read_json(StringIO(jsonTable.text))
#print(table)
#print(table.iloc[0]['info'])
#CreateEnbendingsFromDataFrame(table, 'info')

f = open('Zad14FinalJson.json')
table=pd.read_json(f)
print(table)


vectorTable = hnswlib.Index(space = 'l2', dim = 1536)
vectorTable.init_index(max_elements = len(table.index), ef_construction = 200, M = 16)
vectorTable.add_items(table['embendings'].to_list(), table.index.to_list())
vectorTable.set_ef(50)
connector = aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'search')
response = GetEnbending(connector.question['question'])

labels, distances = vectorTable.knn_query(response['data'][0]['embedding'], k = 3)
print(f'{labels[0][0]} {distances}')
connector.sendresultasjson(table['url'][labels[0][0]])



