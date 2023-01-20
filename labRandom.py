import random

# Вернуть псевдослучайное дробное число в интервале [0.0,1.0)

print(random.random())

# Вернуть целое число в диапазоне от <начало> до <конец>
print(random.randint(100,999))

print(random.randrange(100,999,100))

# Перемешать список
numbers = list(range(10))
print(numbers)
random.shuffle(numbers)
print(numbers)

# вернуть случайный элемент из последовательности
print(random.choices("ПРИВЕТ"))
print(random.choices("ПРИВЕТ",k=20))
print(random.choices(list(range(10)),k=20))

#HW
# добавить использование других методов из random