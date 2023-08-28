#https://www.youtube.com/watch?v=KJ5bFv-IRFM

##slack events: https://api.slack.com/events

# slack bot on windows app service
#https://www.youtube.com/watch?v=fTEwGcPqLa8
#https://github.com/daveebbelaar/langchain-experiments/tree/deployment



#workspace: AppleSause123
#app Name setup within Slack: TalkWithWinston

#good video on emplementing slack events. This would be a better way of directing questions to winston
# https://www.youtube.com/watch?v=6gHvqXrfjuo


# ####to run the winston slack bot
# 1. run BOT-BhamMarket.py
# 2. run ngrok located at C:\Users\ryanc\PycharmProjects\WinstonBot1\ngrok.exe. ie) ngrok http 5000
# 3. copy endpoint
# 4. paste endpoint into slack api
#     a. go to this URL: https://api.slack.com/apps/
#     b. open the TalkWithWinston App
#     c. Open "Event Subscriptions"
#     d. paste endpoint coppied in step. It shoud look something like: https://b971-216-243-30-60.ngrok.io/slack/events. don't forget to add the /slack/events to the end.
#     e. Click save changes
# ***The "Talk_to_Winston" channel in the applesauce123 workspace should now be ready to interact with.
#
#
# *********Things to add
# * create event to talk with winston. Some sort of directive at the beginning of a message that indicates you are asking a question to winston
# * develop a program to scrap data from webpages as training input for winston

import slack_sdk
import random
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv #use to set environmental variables
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter #handle events coming from slack
from LLM_BhamMarket import QueryLLM
import openai


# the load_dotenv() function sets environment variables using the ".env" file. The load_dotenv() function uses the find_dotenv() function to locate the ".env" file in the project. This is kinda magic and I'm not entirely shure how this works but it does.
load_dotenv()

app=Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'],'/slack/events',app) #set from ".env" file through load_dotenv() function


client = slack_sdk.WebClient(token=os.environ['SLACK_BOT_TOKEN'])  #load token from .env ile and pass to instatioiont of client object from slack.webclient class

client.chat_postMessage(channel='#talk_to_winston', text="chatBot initialized")


BOT_ID = client.api_call("auth.test")['user_id']

greeting = ['Hello', 'Sup', 'Howdy', 'Hi', 'Hola', 'Greetings', 'Namaste']

hope = ["Hope you're having a great week!", "Hope you're having a great day!", "Hope you're doing well!", "Hope you're doing good!"]

Encourage_message = ['I am learning from your responses','You are helping me adapt my context database','You are helping me adapt my context database. The more interaction I have, the better I understand your cadence and tone of individual users', 'That was an unexpected question... I have noted it for additional training', 'I am guessing on that one...?', 'I also interpret misspelled words', 'I detect you are using a mobile device.']




message_counts = {}

def greet_user(name):
    value = random.choice(greeting)
    value2 = random.choice(hope)
    return(value + ', ' + name + '! ' + value2)

def encourage_user():
    value = random.choice(Encourage_message)
    return(value)

def Get_UserNameFromProfile(UserID):
    var1 = client.users_profile_get(user=UserID)
    var2 = var1['profile']['real_name']

    return var2



#crete function to handle events
@slack_event_adapter.on('message')
def message(payload):
    #print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel') #will give chaneel id of what was sent in
    user_id = event["user"]
    messageText = event.get('text')

    if BOT_ID != user_id:
        if user_id not in message_counts:
            client.chat_postMessage(channel='#talk_to_winston',
                                text=".\n\n\n_>>>>To send a question to Winston, enter a slash(/) followed by winston and then your question. For example: \n\n     /winston What is the case about?   \n\n\n.")


@app.route('/winston', methods=['POST'])
def winston():
    data = request.form
    user_id = data.get('user_id')
    user_name = Get_UserNameFromProfile(user_id)
    channel_id = data.get('channel_id')
    greeting_Text= greet_user(user_name)
    messageText = data['text']


    client.chat_postMessage(channel='#talk_to_winston', text="*Message sent to Winston:* " + "_" + messageText + "_")


    if BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1
            client.chat_postMessage(channel='#talk_to_winston', text=greeting_Text)
            client.chat_postMessage(channel='#talk_to_winston',
                                    text="Ignore OPERATION_TIMEOUT errors. They are expected and will be resolved later when my backend hardware improves.")





    llm_response = QueryLLM(messageText)
    client.chat_postMessage(channel=channel_id, text="*Winston Response:* " + llm_response)

    if message_counts[user_id]%5 == 0:
        client.chat_postMessage(channel='#talk_to_winston', text="********************************" + encourage_user() + "**********************")




    return Response(), 200







@app.route('/TerminateNGROK', methods=['POST'])
def TerminateNGROK():
    data = request.form
    messageText = data['text']


    if messageText == 'applesauce123':
        client.chat_postMessage(channel='#talk_to_winston',text="terminating NGROK")
        os.system("taskkill /f /im  ngrok.exe")
    else:
        client.chat_postMessage(channel='#talk_to_winston', text="command ignored")



    return Response(), 200



if __name__ == "__main__":
    app.run(debug=True)

