from tabula import read_pdf
from langdetect import detect
import json
import re
import math
import os
import datetime

pdf_address = "https://www.nlcsjeju.co.kr/userfiles/nlcsjejumvc/NLCSjeju_menu_3%EC%9B%941%EC%A3%BC%EC%B0%A8.pdf"

################## PARAMETER CONFIG #########################
green_start = 1;
green_end = 10;

salad_start = green_end
salad_end = salad_start + 2

salad2_start = 13
salad2_end = salad2_start + 2

morning_snack_start = salad2_end #15
morning_snack_end = morning_snack_start + 1

morning_snack2_start = morning_snack_end # 16
morning_snack2_end = morning_snack2_start + 1

lunch_start = 1
lunch_end = lunch_start + 8

yellow_start = lunch_end 
yellow_end = yellow_start + 3 #12

orange_start = yellow_end
orange_end = orange_start + 2 #14

vegeterian_start = 16
vegeterian_end = vegeterian_start + 1 

lunchBox_start = vegeterian_end
lunchBox_end = lunchBox_start + 1 # 18

saladBar_start = lunchBox_end
saladBar_end = saladBar_start + 1 # 19

Afternoon_start = saladBar_end
Afternoon_end = Afternoon_start + 3 #22

greenDinner_start = 1
greenDinner_end = 9

orangeDinner_start = greenDinner_end
orangeDinner_end = orangeDinner_start + 3 #12

vegDinner_start = orangeDinner_end
vegDinner_end = vegDinner_start + 1

saladDinner_start = vegDinner_end
saladDinner_end = saladDinner_start + 1 #14

################## PARAMETER CONFIG #########################

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

    # GREEN (from mon, sat)
    unordered = []
    for x in range(green_start, green_end):
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

    # SALAD Bar @1
    unordered = []
    for x in range(salad_start, salad_end):
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

    # SALAD bar @2
    unordered = []
    for x in range(salad2_start, salad2_end):
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

    # MORNING SNACK @1
    unordered = []
    for x in range(morning_snack_start,morning_snack_end):
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

    # MORNING SNACK @2
    unordered = []
    for x in range(morning_snack2_start, morning_snack2_end):
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

    # GREEN the bob
    unordered = []
    for x in range(lunch_start,lunch_end):
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

    # YELLOW
    unordered = []
    for x in range(yellow_start,yellow_end):
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

    # ORANGE
    unordered = []
    for x in range(orange_start, orange_end):
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

    # VEGETARIAN
    unordered = []
    for x in range(vegeterian_start, vegeterian_end):
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

    # Lunch BOX
    unordered = []        
    for x in range(lunchBox_start,lunchBox_end):
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

    # SALAD Bar
    unordered = []        
    for x in range(saladBar_start,saladBar_end):
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

    # AFTERNOON SNACK
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

    # GREEN the bob
    unordered = []
    for x in range(greenDinner_start,greenDinner_end):
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

    # ORANGE
    unordered = []
    for x in range(orangeDinner_start, orangeDinner_end):
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

    # VEGETARIAN
    unordered = []
    for x in range(vegDinner_start, vegDinner_end):
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

    # SALAD Bar
    unordered = []
    for x in range(saladDinner_start, saladDinner_end):
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

def return_today_menu(meal_type): # meal_type = Breakfast, lunch, dinner
    today_menu = {} # menu to be returned.
    with open(os.path.join(os.getcwd(), 'main', 'static', meal_type +'.json'), 'r') as f:
        menu = json.load(f)
        menu = menu[today_day()]

    if meal_type == "breakfast":
        today_menu = {
            "main": {
                "GREEN": []
            },
            "salad": {
                "SPECIAL SALAD": [],
                "NORMAL SALAD": []
            },
            "snack": {
                "MORNING SNACK": [],
                "PACKAGE SNACK": []
            }
        }
        for single_menu in menu:
            if single_menu == "green":
                for food in menu[single_menu]:
                    today_menu['main']['GREEN'].append(food)
            if single_menu == "salad1":
                for food in menu[single_menu]:
                    today_menu['salad']['SPECIAL SALAD'].append(food)
            if single_menu == "salad2":
                today_menu['salad']['NORMAL SALAD'] = menu[single_menu]
            if single_menu == "insnack":
                for food in menu[single_menu]:
                    today_menu['snack']['MORNING SNACK'].append(food)     
            if single_menu == "pksnack":
                for food in menu[single_menu]:
                    today_menu['snack']['PACKAGE SNACK'].append(food)     
    
    if meal_type == "lunch":
        today_menu = {
            "main": {
                "GREEN": [],
                "YELLOW": [],
                "ORANGE": [],
                "VEGETARIAN": []
            },
            "salad": {
                "SALAD": []
            },
            "snack": {
                "BOX": [],
                "AFTERNOON SNACK": []
            }
        }
        for single_menu in menu:
            if single_menu == "green":
                for food in menu[single_menu]:
                    today_menu['main']['GREEN'].append(food)
            if single_menu == "yellow":
                for food in menu[single_menu]:
                    today_menu['main']['YELLOW'].append(food)
            if single_menu == "orange":
                for food in menu[single_menu]:
                    today_menu['main']['ORANGE'].append(food)
            if single_menu == "veg":
                for food in menu[single_menu]:
                    today_menu['main']['VEGETARIAN'].append(food)
            if single_menu == "salad":
                today_menu['salad']['SALAD'] = menu[single_menu]
            if single_menu == "box":
                for food in menu[single_menu]:
                    today_menu['snack']['BOX'].append(food)
            if single_menu == "afsnack":
                for food in menu[single_menu]:
                    today_menu['snack']['AFTERNOON SNACK'].append(food)
        
    if meal_type == "dinner":

        today_menu = {
            "main": {
                "GREEN": [],
                "ORANGE": [],
                "VEGETARIAN": []
            },
            "salad": {
                "SALAD": []
            }
        }
        for single_menu in menu:
            if single_menu == "green":
                for food in menu[single_menu]:
                    today_menu['main']['GREEN'].append(food)
            if single_menu == "orange":
                for food in menu[single_menu]:
                    today_menu['main']['ORANGE'].append(food)
            if single_menu == "veg":
                for food in menu[single_menu]:
                    today_menu['main']['VEGETARIAN'].append(food)
            if single_menu == "salad":
                today_menu['salad']['SALAD'] = menu[single_menu]

    return today_menu

if __name__ == '__main__':
    pass

