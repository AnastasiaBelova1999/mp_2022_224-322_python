import argparse
import os
import hashlib
from datetime import datetime
from prettytable import PrettyTable
from database import DataBase
import csv
import multiprocessing
from copy import deepcopy
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()

class BadArgumentError(ValueError):
    pass

parser.add_argument('-s','--source', nargs='+', default='') # путь к анализируемой папке
parser.add_argument('--intypes', nargs='+', default='') # сканировать только файлы данного расширения
parser.add_argument('--extypes', nargs='+', default='') # сканировать все файлы, за исключением файлов данного расширения
parser.add_argument('--depth', nargs='+', default=None) # вложенность
parser.add_argument('--dbpath', nargs='+', default='') # путь к БД
parser.add_argument('--type', nargs='+', default='', choices=['sha256', 'data']) # тип сравнения файлов
parser.add_argument('--out',nargs='+', choices=['txt', 'csv'], default='') # выбор типа результирующего файла

args = parser.parse_args()

s_path = args.source[0] if len(args.source) == 1 else os.getcwd() # если путь не указан то анализируется текущая папка
intypes = args.intypes if len(args.intypes) > 0 else None
extypes = args.extypes if len(args.extypes) > 0 else None
depth = args.depth
dbpath = args.dbpath if len(args.dbpath) > 0 else os.path.join(os.getcwd(),'duplicate.db')
out_type = args.out if len(args.out) > 0 else None

s_path = os.path.abspath(s_path)


if depth is not None and len(depth) >= 2:
    raise BadArgumentError("В качестве значения вложенности необходимо одно число")

if len(dbpath) == 0:
    print("Путь до базы данных не указан. База данных будет создана в текущей директории")
    
    
# получить всю необходимую информацию о файле
def get_full_file_info(file):
    info = os.stat(file)
    stmode = info.st_mode
    atime = info.st_atime
    mtime = info.st_mode
    ctime = info.st_ctime
    
    return {'name': file, 'stmode': stmode, 'atime': atime, 'mtime': mtime, 'ctime': ctime}

# получить информацию о файле, необходимую для сравнения
def get_file_info(file):
    info = os.stat(file)
    file_name = os.path.basename(file)
    created_time = datetime.fromtimestamp(info.st_ctime)
    return { 'name': file_name, 'created_time':created_time, 'size':info.st_size }

# хэш всего файла
def get_hash(file):
    with open(file, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# сравнить два файла на основе метаинформации
def compare_info(file1, file2):
    
    file1 = get_file_info(file1)
    file2 = get_file_info(file2)
    file1['name'] = os.path.basename(file1['name'])
    file2['name'] = os.path.basename(file2['name'])
    
    return file1['name'] == file2['name'] and \
           file1['created_time'] == file2['created_time'] and \
           file1['size'] == file2['size']

# сравнить два хэша на совпадение
def compare_hash(file1, file2):
    return file1 == file2

# функция проверки глубины
def is_correct_depth(start_dir, current_dir: str, depth):
    
    if depth is None:
        return True 
    
    current_depth = current_dir.removeprefix(start_dir)
    
    if current_depth.count('\\') > depth:
        return False
    return True

# добавить информацию о файле в бд
def insert_file(name, hash, dbpath):
    db = DataBase(dbpath)
    info = get_full_file_info(name)
    db.insert_data(info['name'], info['stmode'], info['atime'], info['mtime'], info['ctime'], hash)

# удалить одинаковые пары файлов
def remove_mirror(duplicates):
    new_d = []
    for i in duplicates:
        if (i[1], i[0]) not in new_d:
            new_d.append((i[0],i[1]))
            
    return new_d

# функция сравнения всех файлов
def compare_files(data: list, type: str):
    duplicates = []
    
    hashes = get_hashes(data)
    for filename, hash in hashes:
        insert_file(filename, hash, dbpath)
    
    if type == 'hash':
        for i in hashes:
            for j in hashes:
                if i == j:
                    continue 
                if compare_hash(i[1],j[1]):
                    duplicates.append((i[0],j[0]))
                    
    if type == 'data':
        for i in data:
            for j in data:
                if i == j:
                    continue
                if compare_info(i,j):
                    duplicates.append((i,j))
                    
    return remove_mirror(duplicates)

# получить все хэшы файлов (параллельно)
def get_hashes(files: list):
    
    with multiprocessing.Pool() as pool:
        hashes = pool.map(get_hash,files)
    
    return list(zip(files,hashes))
    
# функция обхода каталога
def walk(path, intypes, extypes, depth):
    start_dir = path
    all_files = []
    
    for current_dir, dirs, files in os.walk(start_dir):
        if not is_correct_depth(start_dir, current_dir, depth):
            continue
        for file in files:
            ext = os.path.splitext(file)[1][1:]
            
            if intypes is None and extypes is None:
                full_path = os.path.join(current_dir,file)
                all_files.append(full_path)
                continue
                
            if intypes is not None and ext in intypes:
                full_path = os.path.join(current_dir,file)
                all_files.append(full_path)
                continue
            
            if extypes is not None and ext not in extypes:
                full_path = os.path.join(current_dir,file)
                all_files.append(full_path)
                continue
    
    return all_files 

# создание txt файла с выводом анализа каталога      
def create_txt(out_file, dbpath):
    table = PrettyTable()
    table.field_names = ['id', 'filename', 'mode', 'atime', 'mtime', 'ctime', 'hash']
    db = DataBase(dbpath)
    data = db.get_data()
    table.add_rows(data)
    
    with open(out_file, 'w', encoding='utf-8') as w:
        w.write(str(table))
    
# создание csv файла с выводом анализа каталога
def create_csv(out_file, dbpath):
    db = DataBase(dbpath)
    data = db.get_data()
    
    with open(out_file, 'w', encoding='utf-8') as w:
        writer = csv.writer(w, delimiter=';', lineterminator='\n')
        writer.writerows(data)

# удаление многомерно совпадающих файлов 
def delete_duplicate(duplicate):
    
    for i in duplicate:
        if get_hash(i[0]) == get_hash(i[1]):
            os.remove(i[1])
            
# решение удалять файлы или нет
def choise(duplicate):
    
    if len(duplicate) == 0:
        print('Дубликатов файлов не обнаружено')
        return
    
    answer = input(f'Обнаружено {len(duplicate)} дубликатов файлов. Удалить? [y\\n] ')
    if answer.strip() == 'y':
        for _ in duplicate:
            delete_duplicate(duplicate)
    elif answer.strip() == 'n':
        return 
    else:
        print('Указан неверный формат ответа. Пожалуйста, перезапустите программу')           
    

if __name__ == '__main__':
    DataBase(dbpath).create_table()
    
    files = walk(s_path, intypes, extypes, depth)
    duplicate_files = compare_files(files,'hash')
    
    if out_type is not None:
        if 'csv' in out_type:
            create_csv('.\\result.csv',dbpath)
        if 'txt' in out_type:
            create_txt('.\\result.txt', dbpath)
    
    choise(duplicate_files)
