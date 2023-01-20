symbol = '█'
height = int(input('Введите высоту змеи: '))
width = int(input('Введите ширину змеи: '))

for i in range(height // 2):
    print(symbol * width)
    str = symbol.rjust(width,' ')
    if i % 2 == 0:
        print(str,sep='')
    else:
        print(str[::-1],sep='')
if not height % 2 == 0:
    print(symbol * width)