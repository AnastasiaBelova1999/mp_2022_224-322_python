
# if 
# if-else
# if-elif-else

# and , or, not

x = int(input("x="))
y = int(input("y="))

# (1)

if x > 0 and y > 0:
    print(1)
else:
    if x < 0 and y > 0:
        print(2)
    else:
        print(0)
        
# тернарный условный оператор
z = 5
print('Yes' if z == 5 else 'No')