from dotenv import load_dotenv
import os
import requests

load_dotenv()

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "task-notifications"


def send_message_to_slack(text):
    '''
    Function takes a parameter text as string and sends it 
    to the given slack channel.
    '''
    query_params = {"text": text, "channel": SLACK_CHANNEL}
    headers={'Authorization': SLACK_BOT_TOKEN}
    response = requests.post(
                    url=SLACK_API_URL, 
                    data= query_params,
                    headers= headers)
    
    return response
    



