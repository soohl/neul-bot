import os
import sys
import json
import requests
from flask import Flask, request, render_template

app = Flask(__name__, static_folder=os.path.join(os.getcwd(),'main','static'))

@app.route('/', methods = ['GET'])
def verification():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification failed. The tokens do not match.", 403
        return request.args["hub.challenge"], 200
    return "Hi, this is Nuel Bot", 200

@app.route('/privacy', methods = ['GET'])
def privacy_policy():
    return render_template('privacy.html')

# All callbacks to the messenger will be POSTED to here. 
@app.route('/', methods = ['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for event in entry["messaging"]:
                process_message(event)
    return "received", 200

def process_message(event):
    if event.get("message"):
        if event['message'].get('quick_reply'):
            receive_quick_reply(event)
        else:
            receive_message(event)
    elif event.get("postback"):
        receive_postback(event)
    else:
        pass

def receive_message(event):
    sender_id = event["sender"]["id"]
    message = event["message"]
    message_text = message["text"]
    #send_message(sender_id, message_text)
    send_initial_message(sender_id)

def receive_postback(event):
    sender_id = event["sender"]["id"]
    payload = event["postback"]["payload"]
    if payload == "greeting": # Initial greeting postback
        send_initial_message(sender_id)
    else:
        send_message(sender_id,"?")

def receive_quick_reply(event):
    sender_id = event["sender"]["id"]
    payload = event["message"]['quick_reply']["payload"]
    if (payload == "meal"):
        send_message(sender_id,"🚧 식단. 현재 늘봇의 대규모 수정 및 재개발이 진행중입니다. 🚧")
    else:
        send_message(sender_id,"🚧 지원. 현재 늘봇의 대규모 수정 및 재개발이 진행중입니다. 🚧")


# Send back the message.
def send_message(recipient_id, message_text):
    message_data = json.dumps({
        "recipient" : { "id" : recipient_id},
        "message" : {"text": message_text}
    })
    send_api(message_data)

def send_initial_message(recipient_id):
    #send_message(recipient_id, "🚧 안녕하세요. 늘봇입니다. 현재 늘봇의 대규모 수정 및 재개발이 진행중입니다. 🚧")
    send_quick_reply(recipient_id, 0, "안녕하세요. 늘봇입니다.")

def send_quick_reply(recipient_id, level, greeting):
    level_dic = {
        0 : [["🍴식단", "meal"], ["📡지원", "help"]]
    }
    message_data = {
        "recipient" : {"id" : recipient_id},
        "message" : { 
            "text" : greeting,
            "quick_replies" : []
        }
    }
    for key,values in level_dic.items():
        for value in values:
            message_data["message"]["quick_replies"].append({
                "content_type" : "text",
                "title" : value[0],
                "payload" : value[1]
            })
    message_json = json.dumps(message_data,ensure_ascii = False).encode("utf-8")
    send_api(message_json)


def send_api(message_data):
    params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=message_data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(msg, *args, **kwargs):
    print(msg)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)