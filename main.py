import aidevmethods
import NotToCommit

connector=aidevmethods.ConnectionToAiDevs(NotToCommit.apikey, 'helloapi')
answer = {'answer': connector.question['cookie']}
connector.sendresult(answer)