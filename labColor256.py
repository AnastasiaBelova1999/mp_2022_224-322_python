
def fg(text,color):
    return f"\33[38;5;{color}m{text}\33[0m"

def bg(text,color):
    return f"\33[48;5;{color}m{text}\33[0m"

def print_colors(row, func, end="\n"):
    for col in range(1,7):
        color = row * 6 + col
        text = f"{color:3d}"
        print (func(text,color), end=" ")
        
    print(end="    ")
    print(end=end)

for row in range(0, 43):
    print_colors(row, fg, " ")
    print_colors(row, bg)