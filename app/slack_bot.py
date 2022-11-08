from dotenv import load_dotenv
import os
import requests

load_dotenv()

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "task-notifications"


def send_message_to_slack(text):
    query_params = {"text": text, "channel": SLACK_CHANNEL}
    headers={'Authorization': SLACK_BOT_TOKEN}
    response = requests.post(
                    url=SLACK_API_URL, 
                    data= query_params,
                    headers= headers)
    return response.json(), 200 #### what is to return?

    # what is the good place for this file.

# testing function    
# text = "Hello"
# print(send_message_to_slack(text))

