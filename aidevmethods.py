import requests
import json


class ConnectionToAiDevs:
    url = 'https://zadania.aidevs.pl/token/'
    urlQuestionBegin = 'https://zadania.aidevs.pl/task/'
    urlAnswerBegin = 'https://zadania.aidevs.pl/answer/'
    tokenApiKey = {'apikey': ''}
    urlQuestion = ''
    urlAnswer = ''

    def __init__(self, apikey, taskname):
        self.gettoken(apikey, taskname)
        self.question=self.getquestion()

    def gettoken(self, apikey, taskname):
        tokenApiKey = {'apikey': apikey}
        token = json.loads(requests.post(self.url+taskname, json=tokenApiKey).text)
        print(token)
        self.urlQuestion = self.urlQuestionBegin + token['token']
        self.urlAnswer = self.urlAnswerBegin + token['token']
        return self.urlQuestion, self.urlAnswer

    def getquestion(self):
        question = json.loads(requests.get(self.urlQuestion).text)
        print(question)
        return question

    def sendresult(self, answer):
        sendResult = requests.post(self.urlAnswer, json=answer)
        print(sendResult.text)