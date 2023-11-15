import requests
import json

from langchain.schema import BaseOutputParser


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
    def getnewquestion(self):
        self.question =self.getquestion()
        return self.question
    def sendQuestion(self, question):
        sendQuestion=requests.post(self.urlQuestion, data={'question':question})
        print(sendQuestion.text)
        return sendQuestion

    def sendresult(self, answer):
        sendResult = requests.post(self.urlAnswer, json=answer)
        print(sendResult.text)

    def sendresultasjson(self, text):
        answer = {'answer': text}
        self.sendresult(answer)

