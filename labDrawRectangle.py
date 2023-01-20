symbol = '█'
flag = True

def draw(width,height,isFill):
    if isFill:
        for h in range(height):
            print(symbol * width)
    else:
        print(symbol * width)
        for i in range(height - 2):
            print(symbol,' ' * (width - 2), symbol,sep='')
        print(symbol * width)


while flag:
    height = int(input('Введите высоту прямоугольника: '))
    width = int(input('Введите ширину прямоугольника: '))
    fill = input('Закрасить? [y/n]: ')
    isFill = fill.lower() == 'y'
    draw(width, height, isFill)
    flag = True if input('Повторить? [y/n]: ') == 'y' else False