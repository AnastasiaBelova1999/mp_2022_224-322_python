import prettytable

height = 10
width = 10
table = prettytable.PrettyTable()
for i in range(height):
    row = [chr(i + height*j + 32) for j in range(width) if i <= 128]
    table.add_row(row)
    
print(table)