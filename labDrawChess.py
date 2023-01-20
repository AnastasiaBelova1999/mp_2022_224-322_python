import string

width = int(input('Введите ширину шахматной доски: '))
height = int(input('Введите высоту шахматной доски: '))
letters = string.ascii_lowercase + string.ascii_uppercase

white = '██'
black = '  '
line = '-'

def reverse(symbol):
    return black if symbol == white else white

print(f'{" " * 4}|{" ".join(letters[:width])}| ')
print(''.rjust(width*3,line))
st = []
symbol = white
for i in range(width):
    symbol = reverse(symbol)
    st.append(symbol)
    
def reverse_line(line):
    return list(map(reverse,line))

for j in range(1,height + 1):
    st = reverse_line(st)
    if j >= 10:
        print(f'{black}{j}|{"".join(st)}{black.rstrip()}|{j}',end='')
    else:
        print(f'{black} {j}|{"".join(st)}{black.rstrip()}|{j}',end='')
    print(black)

print(''.rjust(width*3,line))
print(f'{" " * 4}|{" ".join(letters[:width])}| ')