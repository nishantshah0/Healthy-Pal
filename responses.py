import parse
import time
import csv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

food_data = parse.parse_food_data()
#[[foodID, food], [foodID, food]]
conversion_factor = parse.parse_conversion_factor()
#[[ID, conversion factor], [ID, conversion factor]] CONVERSION TO 100ml SERVING
nutrition_amount = parse.parse_nutrient_amount()
#[[foodID, nutrientID, amount of nutrient]]
#203 = protein, 204 = fat, 205 = carbs, 208 = calories, 269 = sugar

user_sleep_timers = {}
def send_message(message):
  print("Chat: " + message)



def get_response(user_message: str, message_info: list) -> str:
  p_message = user_message.lower()
  help()
  if p_message == '!help':
    return help()
  if p_message.startswith('!sleep'):
    return handle_sleep_command(str(message_info.author), p_message)
  if p_message == '!nutrition':
    return nutrition(message_info)
  if p_message == '!hydration':
    return 'unfinished'
  if p_message.startswith('!exercise'):
    parts = p_message.split()
    if len(parts) != 3:
      return "Invalid command format. Usage: !exercise [push/pull/legs] [muscle group]"

    _, exercise_type, muscle_group = parts

    if exercise_type not in ['push', 'pull', 'legs']:
      return "Inval1236id exercise type. Choose from: push, pull, legs"

    return get_exercise_suggestions(exercise_type, muscle_group)
  if p_message == '!food':
    return '# Link to food to ID search: \nhttps://food-nutrition.canada.ca/cnf-fce/doSearch'
  if p_message[:8] == '!addfood':
    return addfood(p_message[9:], message_info)
  if p_message == '!clearfood':
    return clearfood(message_info)
  if p_message == '!suggest':
    return suggest(message_info)
  return ' '


### EXTRA FUNCTIONS


#def hydration():
#  client = commands.AutoShardedBot(commands.when_mentioned_or('!'), #help_command=None)
#  @client.command()
#  async def reminder(ctx, time: int,*,msg):
#    while True:
#      await s(60'time)
#      await ctx.send(f'{msg}{ctx.author.mention}')
  


def help():
  help = f''' 
  !help - Gives a list of commands
  !sleep - Times how long you slept for.
  !exercise - Give it a workout area(push - chest, shoulders, triceps) (Pull - back, biceps) (legs - quads, hamstrings, calves) and it will give you exercises based on what you chose. For example !exercise push chest
  !food - Gives a link to a search engine that matches foods and their ID
  !nutrition - Gives the nutritional values of your diet.
  !addfood - Lets user add food to their diet by using food IDs
  !clearfood - Removes all diet data for the user
  !suggest - Gives food suggestions based on the user diet
  '''
  return help
  
def get_exercise_suggestions(exercise_type, muscle_group):
    exercises = {
        'push': {
            'chest': ['bench press', 'push-ups', 'dips'],
            'shoulders': ['shoulder press', 'lateral raises', 'front raises'],
            'triceps': ['tricep dips', 'skull crushers', 'close-grip push-ups']
        },
        'pull': {
            'back': ['pull-ups', 'rows', 'deadlifts'],
            'biceps': ['bicep curls', 'chin-ups', 'hammer curls'],
        },
        'legs': {
            'quads': ['squats', 'lunges', 'leg press'],
            'hamstrings': ['deadlifts', 'hamstring curls', 'good mornings'],
            'calves': ['calf raises', 'jump rope', 'box jumps']
        }
    }

    if exercise_type in exercises and muscle_group in exercises[exercise_type]:
        exercise_list = ', '.join(exercises[exercise_type][muscle_group])
        response = f"For {muscle_group} during {exercise_type} exercises, you can do: {exercise_list}"
    else:
        response = f"No exercise suggestions found for {muscle_group} during {exercise_type} exercises."

    return response



def addfood(p_message, message_info):
  users_csv = parse.read_csv('users.csv')
  if len(p_message) == 0:
    return "Your message does not provide your diet. Try the following format:\n!addfood {food ID}:{amount in mL},{food ID}:{amount in mL}..."
  
  foods = p_message.split(',')
  protein = 0
  fat = 0
  carbs = 0
  cal = 0
  sugar = 0
  user_line = -1
  conversion = 0

  if len(users_csv) > 0:
    for user in users_csv:
      if user[0] == str(message_info.author):
        protein = float(user[1])
        fat = float(user[2])
        carbs = float(user[3])
        cal = float(user[4])
        sugar = float(user[5])
        user_line = users_csv.index(user)
  for food1 in foods:
    food = food1.split(':')
    for i in conversion_factor:
      if int(food[0]) == i[0]:
        conversion = i[1]
    for j in nutrition_amount:
      if int(food[0]) == j[0] and j[1] == 203:
        print(protein)
        protein += j[2] * conversion * (int(food[1])/100)
        print(protein)
      if int(food[0]) == j[0] and j[1] == 204:
        fat += j[2] * conversion * (int(food[1])/100)
      if int(food[0]) == j[0] and j[1] == 205:
        carbs += j[2] * conversion * (int(food[1])/100)
      if int(food[0]) == j[0] and j[1] == 208:
        cal += j[2] * conversion * (int(food[1])/100)
      if int(food[0]) == j[0] and j[1] == 269:
        sugar += j[2] * conversion * (int(food[1])/100)
  if user_line == -1:
    with open("users.csv", 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([str(message_info.author), protein, fat, carbs, cal, sugar])
  else:
    with open("users.csv", 'w', newline='') as file:
      writer = csv.writer(file)
      users_csv[user_line] = [str(message_info.author), protein, fat, carbs, cal, sugar]
      file.truncate()
      for user in users_csv:
        writer.writerow(user)
  return f"**Data updated ({message_info.author})**\nProtien={protein:.2f}g\nFat={fat:.2f}g\nCarbohydrates={carbs:.2f}g\nCalories={cal:.2f}kCal\nSugar={sugar:.2f}g\n"

def clearfood(message_info):
  users_csv = parse.read_csv('users.csv')
  user_line = -1
  for user in users_csv:
    if user[0] == str(message_info.author):
      user_line = users_csv.index(user)
      users_csv.pop(user_line)
  with open("users.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    file.truncate()
    for user in users_csv:
      writer.writerow(user)

  return f"**{message_info.author}'s** diet has been removed."

def handle_sleep_command(user_id, command):
  global user_sleep_timers

  if command == '!sleep start':
    if user_id in user_sleep_timers:
      return "Sleep timer is already running."
    user_sleep_timers[user_id] = time.time()
    send_message("Timer started!")
    return "Sleep timer started. Use '!sleep end' when you wake up."
  elif command == '!sleep end':
    if user_id not in user_sleep_timers:
      return "Sleep timer is not running."
    sleep_duration = time.time() - user_sleep_timers[user_id]
    del user_sleep_timers[user_id]
    store_sleep_duration(user_id, sleep_duration)
    return f"You slept for {format_duration(sleep_duration)}."

def format_duration(duration):
  hours = int(duration // 3600)
  minutes = int((duration % 3600) // 60)
  seconds = int(duration % 60)
  return f"{hours} hours, {minutes} minutes, {seconds} seconds"

def store_sleep_duration(user_id, duration):
  with open('user.csv', 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow([user_id, duration])

def nutrition(message_info):
  users_csv = parse.read_csv('users.csv')
  protein = 0
  fat = 0
  carbs = 0
  cal = 0
  sugar = 0

  
  if len(users_csv) > 0:
    for user in users_csv:
      if user[0] == str(message_info.author):
        protein = float(user[1])
        fat = float(user[2])
        carbs = float(user[3])
        cal = float(user[4])
        sugar = float(user[5])

    return f"**Your Diet ({message_info.author})**\nProtien={protein:.2f}g\nFat={fat:.2f}g\nCarbohydrates={carbs:.2f}g\nCalories={cal:.2f}kCal\nSugar={sugar:.2f}g\n"
  else:
    return "You have not added your diet into the database. Try **!addfood**"

def suggest(message_info):
  users_csv = parse.read_csv('users.csv')
  
  protein = 0
  fat = 0
  carbs = 0
  cal = 0
  sugar = 0
  foodname = ''

  protein_target = 50
  fat_target = 70
  carbs_target = 310
  cal_target = 2250
  sugar_target = 90

  if len(users_csv) > 0:
    for user in users_csv:
      if user[0] == str(message_info.author):
        protein = float(user[1])
        fat = float(user[2])
        carbs = float(user[3])
        cal = float(user[4])
        sugar = float(user[5])
        
        protein_excess = protein_target - protein
        fat_excess = fat_target - fat
        carbs_excess = carbs_target - carbs
        cal_excess = cal_target - cal
        sugar_excess = sugar_target - sugar

        user_diet = [protein_excess, fat_excess, carbs_excess, cal_excess, sugar_excess]
        nutrient_data = convert_nutrient_data(nutrition_amount)
        closest_food = find_closest_set(nutrient_data, user_diet)

        for food in food_data:
          if int(food[0]) == int(closest_food[0]):
            foodname = food[1]
          
        
        return f'**Results (Quantities are for 100mL serving size)**\nFood ID: {str(closest_food[0])}\nProtein: {str(closest_food[1])}\nFat: {str(closest_food[2])}\nCarbohydrates: {str(closest_food[3])}\nCalories: {str(closest_food[4])}\nSugar: {str(closest_food[5])}\n```Food: {foodname}```'
  else:
    return "Your information is not in the database"
  #protein: 50g
  #fat: 70g
  #carb: 310g
  #calorie: 2250kCal
  #sugar: 90g

def average_difference(user_diet, food):
    total_diff = sum(abs(a - b) for a, b in zip(user_diet, food[1:]))
    return total_diff / len(user_diet)

def find_closest_set(nutrient_data, user_diet):
    closest_distance = float('inf')
    closest_food = None
    
    for food in nutrient_data:
        distance = average_difference(user_diet, food)
        if distance < closest_distance:
            closest_distance = distance
            closest_food = food
    
    return closest_food


def convert_nutrient_data(data):
  new_list = []
  for i in range(0, len(data), 5):
    elements = [data[i][0]]
    for j in conversion_factor:
      if int(data[i][0]) == j[0]:
        conversion = j[1]
    for lst in data[i:i+5]:
      elements.append(round(lst[2]*conversion, 2))
    new_list.append(elements)
  return new_list

  
