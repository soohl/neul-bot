from tabula import read_pdf
from langdetect import detect
import json
import re
import math
import os
import datetime

pdf_address = "https://www.nlcsjeju.co.kr/userfiles/nlcsjejumvc/NLCSjeju_menu_12%EC%9B%941%EC%A3%BC%EC%B0%A8.pdf"

def breakfast():
    json = read_pdf(pdf_address, output_format="json", pages=2)
    row = json[0]['data']
    menus = {
        "mon": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []},
        "tue": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []},
        "wed": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []},
        "thu": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []},
        "fri": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []},
        "sat": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []},
        "sun": {"green": [], "salad1": [], "salad2": [], "insnack": [], "pksnack": []}
    }

    # Green (from mon, sat)
    unordered = []
    for x in range(1,10):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko' and not re.compile('<|>').search(food): #exclude brunch
                            unordered.append(food.strip())

                        
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%6]]["green"].append(food)
    menus["sun"]["green"].append("브런치")

    # Salad Bar @1
    unordered = []
    for x in range(10,12):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko' and not re.compile('<|>').search(food): #exclude brunch
                            unordered.append(food.strip())
                        
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%6]]["salad1"].append(food)
    menus["sun"]["salad1"].append("브런치")

    # Salad bar @2
    unordered = []
    for x in range(12,14):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split('/'):
                    if food == '-':
                        unordered.append(food)
                    else:
                        unordered.append(food.strip())

    for day in menus:
        for food in unordered:
            if not food == '-' and not food == '':
                menus[day]["salad2"].append(food)

    # Morning Snack @1
    unordered = []
    for x in range(14,15):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko' and not re.compile('간식').search(food): #exclude brunch
                            unordered.append(food.strip())


    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%6]]["insnack"].append(food)

    # Morning Snack @2
    unordered = []
    for x in range(15,16):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko' and not re.compile('간식').search(food): #exclude brunch
                            unordered.append(food.strip())
                            
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%6]]["pksnack"].append(food)

    return menus

def lunch():
    json = read_pdf(pdf_address, output_format="json", pages=4)
    row = json[0]['data']

    # Lunch Menu 
    menus = {
        "mon": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []},
        "tue": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []},
        "wed": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []},
        "thu": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []},
        "fri": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []},
        "sat": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []},
        "sun": {"green": [], "yellow": [], "orange": [], "veg": [], "box": [], "salad": [], "afsnack": []}
    }

    # Green the bob
    unordered = []
    for x in range(1,9):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())

    unordered.insert(6,'')
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            if index%7 == 6: # treat sunday seperately
                    menus["sun"]["green"].append(food)
                    menus["sun"]["yellow"].append(food)
                    menus["sun"]["orange"].append(food)
                    menus["sun"]["veg"].append(food)
                    menus["sun"]["box"].append(food)
            else:
                menus[list(menus)[index%7]]["green"].append(food)

    # Yellow
    unordered = []
    for x in range(9,12):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())
                
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            if index%7 == 6: # treat sunday seperately
                menus["sun"]["green"].append(food)
                menus["sun"]["yellow"].append(food)
                menus["sun"]["orange"].append(food)
                menus["sun"]["veg"].append(food)
                menus["sun"]["box"].append(food)
            else:
                menus[list(menus)[index%7]]["yellow"].append(food)

    # Orange
    unordered = []
    for x in range(12,14):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())

    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            if index%7 == 6: # treat sunday seperately
                menus["sun"]["salad"].append(food)
            else:
                menus[list(menus)[index%7]]["orange"].append(food)

    # Vegetarian
    unordered = []
    for x in range(16,17):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())
                            
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            if index%7 == 6: # treat sunday seperately
                    menus["sun"]["salad"].append(food)
            else:
                    menus[list(menus)[index%7]]["veg"].append(food)

    # Lunch Box
    unordered = []        
    for x in range(17,18):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())
                            
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            if index%7 == 6: # treat sunday seperately
                menus["sun"]["salad"].append(food)
            else:
                menus[list(menus)[index%7]]["box"].append(food)

    # Salad Bar
    unordered = []        
    for x in range(18,19):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split('/'):
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())

    for day in menus:
        if not day == "sun":
            for food in unordered[:-1]:
                if not food == '' and not food == '-':
                    menus[day]["salad"].append(food)        
        else:
            if not unordered[-1] == '' and not unordered[-1] == '-':
                menus[day]["salad"].append(unordered[-1])

    # Afternoon Snack
    unordered = []        
    for x in range(19,22):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko' and not re.compile('간식').search(food):
                            unordered.append(food.strip())

    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%7]]["afsnack"].append(food)
    
    return menus

def dinner():
    json = read_pdf(pdf_address, output_format="json", pages=6)
    row = json[0]['data']
    # Dinner Menu 
    menus = {
        "mon": {"green": [], "orange": [], "veg": [], "salad": []},
        "tue": {"green": [], "orange": [], "veg": [], "salad": []},
        "wed": {"green": [], "orange": [], "veg": [], "salad": []},
        "thu": {"green": [], "orange": [], "veg": [], "salad": []},
        "fri": {"green": [], "orange": [], "veg": [], "salad": []},
        "sat": {"green": [], "orange": [], "veg": [], "salad": []},
        "sun": {"green": [], "orange": [], "veg": [], "salad": []}
    }

    # Green the bob
    unordered = []
    for x in range(1,9):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())
                        
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%7]]["green"].append(food)

    # Orange
    unordered = []
    for x in range(9,12):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())
                            
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%7]]["orange"].append(food)

    # Vegetarian
    unordered = []
    for x in range(12,13):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split():
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko':
                            unordered.append(food.strip())
                            
    for index, food in enumerate(unordered):
        if not food == '' and not food == '-':
            menus[list(menus)[index%7]]["veg"].append(food)

    # Salad Bar
    unordered = []
    for x in range(13,14):
        for element in row[x]:
            if not element['text'] == '':
                text = element['text'].strip()
                for food in text.split('/'):
                    if food == '-':
                        unordered.append(food)
                    else:
                        if detect(food) == 'ko' and not re.compile('Bar').search(food):
                            unordered.append(food.strip())
                        
    for day in menus:
        for food in unordered:
            if not food == '-' and not food == '':
                menus[day]["salad"].append(food)
    
    return menus

def write_json():
    with open(os.path.join('static', 'breakfast.json'), 'w') as outfile:
        json.dump(breakfast(), outfile, indent=4, ensure_ascii=False)
    with open(os.path.join('static', 'lunch.json'), 'w') as outfile:
        json.dump(lunch(), outfile, indent=4, nsure_ascii=False)
    with open(os.path.join('static', 'dinner.json'), 'w') as outfile:
        json.dump(dinner(), outfile, indent=4, ensure_ascii=False)
    return True

def today_day():
    date = datetime.datetime.today()
    week_day = {
        0 : "mon",
        1 : "tue",
        2 : "wed", 
        3 : "thu",
        4 : "fri",
        5 : "sat", 
        6 : "sun"
    }
    return week_day[date.weekday()]

def return_breakfast():
    today_menu = []
    with open(os.path.join(os.getcwd(),'main', 'static', 'breakfast.json'), 'r') as f:
        menu = json.load(f)
    for day_menu in menu[today_day()]:
        for single_menu in day_menu:
            today_menu.append(single_menu)
    return today_menu


if __name__ == '__main__':
    pass