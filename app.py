import sys, os
sys.path.append('/main')
import sys
import json
import requests
from flask import Flask, request, render_template, send_from_directory
import datetime
import main.meal as meal


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

@app.route('/meal/breakfast', methods = ['GET'])
def breakfast():
    return send_from_directory(os.path.join('main','static'), 'breakfast.json')

@app.route('/meal/lunch', methods = ['GET'])
def lunch():
    return send_from_directory(os.path.join('main','static'), 'lunch.json')

@app.route('/meal/dinner', methods = ['GET'])
def dinner():
    return send_from_directory(os.path.join('main','static'), 'dinner.json')

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
    send_initial_message(sender_id, "🚧 현재 늘봇의 대규모 수정 및 재개발이 진행중입니다. 🚧")

def receive_postback(event):
    sender_id = event["sender"]["id"]
    payload = event["postback"]["payload"]
    if payload == "greeting": # Initial greeting postback
        send_initial_message(sender_id, "🚧 안녕. 현재 늘봇의 대규모 수정 및 재개발이 진행중입니다. 🚧")
    else:
        send_message(sender_id,"?")

def receive_quick_reply(event):
    sender_id = event["sender"]["id"]
    payload = event["message"]['quick_reply']["payload"]
    if (payload == "meal"):
        send_quick_reply(sender_id, 1, "식단")
    elif (payload == "breakfast"):
        send_quick_reply(sender_id, 2, "아침")
    elif (payload == "lunch"):
        send_quick_reply(sender_id, 3, "점심")
    elif (payload == "dinner"):
        send_quick_reply(sender_id, 4, "저녁")
    else: # Meal specific
        meal_type = payload.split('_')
        message_data = build_meal_template(sender_id, meal.return_today_menu(meal_type[0]), meal_type[1], meal_type[0])
        message_json = json.dumps(message_data,ensure_ascii = False).encode("utf-8")
        send_api(message_json)

def build_meal_template(recipient_id, menu_list, menu_type, meal_type_):
    message_data = {
        "recipient" : {"id" : recipient_id},
        "message" : { 
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": "compact",
                    "sharable": "true",
                    "elements": [],
                    "buttons": [{
                        "title": "돌아갈래",
                        "type": "postback",
                        "payload": meal_type_
                    }]
                }
            }
        }
    }
    if len(menu_list[menu_type]) < 2:
        message_data['message']['attachment']['payload']['template_type'] = "generic"
        del message_data['message']['attachment']['payload']['top_element_style']

    for meal_type in menu_list[menu_type]:
        element = {"title": "", "subtitle": ""}
        element['title'] += meal_type
        if not (menu_list[menu_type][meal_type]):
            element['subtitle'] += "제공되지 않음"
        for food in menu_list[menu_type][meal_type]:
            element['subtitle'] += food+" "
        message_data['message']['attachment']['payload']['elements'].append(element)
    return message_data

# Send back the message.
def send_message(recipient_id, message_text):
    message_data = json.dumps({
        "recipient" : { "id" : recipient_id},
        "message" : {"text": message_text}
    })
    send_api(message_data)

def send_initial_message(recipient_id, greeting):
    send_quick_reply(recipient_id, 0, greeting)

def send_quick_reply(recipient_id, level, greeting):
    level_dic = {
        0 : [["🍴식단", "meal"], ["📡지원", "help"]],
        1 : [["🍴아침", "breakfast"], ["🍴점심", "lunch"], ["🍴저녁", "dinner"]],
        2 : [["🍴메인", "breakfast_main"], ["🍴샐러드", "breakfast_salad"], ["🍴스낵", "breakfast_snack"]],
        3 : [["🍴메인", "lunch_main"], ["🍴샐러드", "lunch_salad"], ["🍴스낵", "lunch_snack"]],
        4 : [["🍴메인", "dinner_main"], ["🍴샐러드", "dinner_salad"]]
    }
    message_data = {
        "recipient" : {"id" : recipient_id},
        "message" : { 
            "text" : greeting,
            "quick_replies" : []
        }
    }
    for values in level_dic[level]:
        message_data["message"]["quick_replies"].append({
            "content_type" : "text",
            "title" : values[0],
            "payload" : values[1]
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