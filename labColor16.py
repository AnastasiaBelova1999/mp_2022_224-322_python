effects = [f'\033[{i}m' for i in range(0,8)]
print(f'{effects=}')
text_colors = {i: f'\033[{i}m' for i in range(30,38)}
print(f'{text_colors=}')
console_colors = {i: f'\033[{i}m' for i in range(40,48)}
print(f'{console_colors=}')

for text_color in text_colors.items():
    for console_color in console_colors.items():
        print(f'{text_color[1]}{console_color[1]}{text_color[0]}:{console_color[0]}',end=' ')
        print(f'{text_colors[30]}{console_colors[40]}',end='')
    print()
    
for index, effect in enumerate(effects):
    print(f'effect {index}: {effect}abc')
    print(f'{effects[0]}',end='')

print(f'{text_colors[30]}{console_colors[40]}{effects[0]}')