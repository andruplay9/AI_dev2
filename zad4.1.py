import aidevmethods
import NotToCommit
import openai as OpenAIAPI


connector=aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'moderation')
print(connector.question)
answer=[0,0,0,0]

for i, quote in enumerate(connector.question['input']):
    response = OpenAIAPI.Moderation.create(
        input=quote,
        api_key=NotToCommit.ApiDev2OpenAIKey
    )
    output = response["results"][0]
    print(output["flagged"])
    answer[i]=int(output["flagged"])
print(answer)
connector.sendresultasjson(answer)
