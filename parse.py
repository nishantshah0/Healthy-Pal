import csv

def parse_food_data():
  food_data = []
  
  file_in = open('FOOD NAME.csv', encoding='UTF-8', errors='replace')
  
  file_in.readline()
  file_in = csv.reader(file_in)
  for line in file_in:
    food_data.append([int(line[0]), str(line[4])])
  return food_data

def parse_conversion_factor():
  conversion_factor = []
  
  file_in = open('CONVERSION FACTOR.csv', encoding='UTF-8', errors='replace')
  
  file_in.readline()
  file_in = csv.reader(file_in)
  
  measure_data = []

  with open('MEASURE NAME.csv', encoding='UTF-8', errors='replace') as file:
      reader = csv.reader(file)
      for row in reader:
          measure_data.append(row)

  
  for line in file_in:
    for row in measure_data:
      if line[1] == row[0]:
        if '100ml' in str(row[1]) or '100g' in str(row[1]):
          conversion_factor.append([int(line[0]), float(line[2])])
  return conversion_factor
  
def parse_nutrient_amount():
  nutrient_amount = []
  
  file_in = open('NUTRIENT AMOUNT.csv', encoding='UTF-8', errors='replace')
  
  file_in.readline()
  file_in = csv.reader(file_in)
  for line in file_in:
    if int(line[1]) in [203, 204, 205, 208, 269]:
      nutrient_amount.append([int(line[0]), int(line[1]), float(line[2])])
  return nutrient_amount

def read_csv(filename):
    data = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    return data

