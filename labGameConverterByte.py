# конвертер величин
# 2 -> 10

import random
import prettytable
from datetime import datetime

table = prettytable.PrettyTable()
table.field_names = ['Заданное число', 'Ваш ответ', 'Правильный ответ'] 

game_mode = ['dec', 'hex']
base_mode = [10, 16]

choosen_mode = int(input(f'Выберите режим игры[0 - десятичный ответ, 1 - шестнадцатеричный ответ]: '))

game_mode = game_mode[choosen_mode]
base_mode = base_mode[choosen_mode]  

difficult_level = ['1','2','3','4']

difficult_level = int(input(f''' 
Выберите уровент сложности [0-3]
0) детский (числа от 0000 0000 до 0000 0111)
1) легкий (числа от 0000 0000 до 0000 1111)
2) средний (числа от 0000 0000 до 0011 1111)
3) сложный (числа от 0000 0000 до 1111 1111)
Введите цифру: '''))

max_number = ['00000111','00001111','00111111','11111111'][difficult_level]

question_count = int(input('Введите количество вопросов: '))

results = []

def add_row(number, answer):
    digit = int(answer,base_mode) 
    base_answer = f'{digit:#x}' if base_mode == 16 else f'{digit}'
    correct_answer = f'{number:#x}' if base_mode == 16 else f'{number}'
    table.add_row([f'{number:#b}', base_answer.upper(), correct_answer.upper()])

start_time: datetime = datetime.now()
while question_count > 0:
    number = random.randint(0,int(max_number,2))
    print(f'{number:b} = ? {game_mode}')
    answer = input('Ваш ответ:')
    add_row(number,answer)
    result = hex(number) == hex(int(answer,16)) if base_mode == 16 else  number == int(answer,10)
    results.append(result)
    question_count -= 1
    
print(f"Результат: {sum(results)} правильных ответов из {len(results)}")
spend_time = datetime.now() - start_time
print(f"Затраченное время: {spend_time.total_seconds():.2f} секунд")
print(table)
    