#                                     мини план

#1 определить тип файла который мы будем загружать в тз написано что (CSV;JSON;TXT)

import os
import csv
import json


file = "sdalfghs/asdfwqe/sdfqw/eq\qwerqdssa.txt"
type_file = os.path.splitext(file)[1].lower()
print(type_file)

#2 выбрать по какому пути мы пойдем после того как опредилим тип файла

def csv_read(filename):
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def json_read(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)
    
def txt_read(filename):
    print(" ")


while True:
    if type_file.lower() == ".csv":
        print("дада сюда функцию для сым")
        date = csv_read(file)
    elif type_file.lower() == ".json":
        print("дада сюда функцию для json")
        date = json_read(file)
    elif type_file.lower() == ".txt":
        print("дада сюда также ток для тхт")
        date = txt_read(file)


    else:
        print("чтото пошло не так!")


#3 нам надо написать функции для разных типов файлов выш )

# date = ()
# kod = str()
# name = str()
# category = str() 
# quantity = int()
# prise = float()


# sortirovka Quick Sort

# через циклы можно(сумма, количество, среднее значение)

# придумать как сохранить 

# работа с ошибками


# :( Код должен быть читаемым и структурированным


# проверка 


# а еще надо написать интерфейс ) сайтик надо выбрать фронт что у нас 
# будет в фронте надо подумать 

