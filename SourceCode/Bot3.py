#https://www.youtube.com/watch?v=KJ5bFv-IRFM

#workspace: AppleSause123
#app Name setup within Slack: TalkWithWinston

import slack_sdk
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter #handle events coming from slack

env_path = Path('..') / '.env'  #sets the current directory
load_dotenv(dotenv_path=env_path) #loads environment varialble file

app=Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'],'/slack/events',app)

client = slack_sdk.WebClient(token=os.environ['SLACK_BOT_TOKEN'])  #load token from .env ile and pass to instatioiont of client object from slack.webclient class

client.chat_postMessage(channel='#talk_to_winston', text="The story begins Part3")
BOT_ID = client.api_call("auth.test")['user_id']

#crete function to handle events
@slack_event_adapter.on('message')
def message(payload):
    #print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel') #will give chaneel id of what was sent in
    user_id = event.get('user') #get id of user sent
    text = event.get('text')

    # check if message was from bot or a real person
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)







if __name__ == "__main__":
    app.run(debug=True)

