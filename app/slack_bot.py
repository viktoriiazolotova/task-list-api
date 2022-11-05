from dotenv import load_dotenv
import os
import requests

load_dotenv()

SLACK_API_URL= "https://slack.com/api/chat.postMessage" # is this needs to be in .env?
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CHANNEL = "task-notifications"
# CHANNEL = "C049V3YP1BK" #is this needs to be in .env?




def send_message_to_slack(text):
    query_params = {"text": text, "channel": CHANNEL}
    headers={'Authorization': SLACK_BOT_TOKEN}
    response = requests.post(
                    url=SLACK_API_URL, 
                    data= query_params,
                    headers= headers)
    return response.json(), 200 #### what is to return?
    
# text = "Hello"
# print(send_message_to_slack(text))
#### what is the best place for this file? in app is ok?
