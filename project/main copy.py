import argparse
import os
import hashlib
from datetime import datetime
from prettytable import PrettyTable
from database import DataBase
import csv
import multiprocessing
from copy import deepcopy

parser = argparse.ArgumentParser()

class BadArgumentError(ValueError):
    pass

parser.add_argument('-s','--source', nargs='+', default='') # путь к папке-источнику
parser.add_argument('--intypes', nargs='+', default='') # включить файлы с данным типом в синхронизацию
parser.add_argument('--extypes', nargs='+', default='') # исключить файлы с данным типом из синхронизации
parser.add_argument('--depth', nargs='+', default=None) # вложенность
parser.add_argument('--dbpath', nargs='+', default='') # путь к базе данных
parser.add_argument('--type', nargs='+', default='', choices=['sha256', 'data']) # тип сравнения файлов
parser.add_argument('--out',nargs='+', default='')
parser.add_argument('--show', nargs=argparse.REMAINDER)


s_path = None
intypes = None 
extypes = None
depth = None
dbpath = None

args = parser.parse_args()

s_path = args.source if len(args.source) == 1 else os.getcwd() # если путь не указан то анализируется текущая папка
intypes = args.intypes
extypes = args.extypes 
depth = args.depth
dbpath = args.dbpath

if depth is not None and len(depth) >= 2:
    raise BadArgumentError("В качестве значения вложенности необходимо одно число")

if len(dbpath) == 0:
    print("Путь до базы данных не указан. База данных будет создана в текущей директории")
    
    
def get_full_file_info(file):
    info = os.stat(file)
    stmode = info.st_mode
    atime = info.st_atime
    mtime = info.st_mode
    ctime = info.st_ctime
    
    return {'name': file, 'stmode': stmode, 'atime': atime, 'mtime': mtime, 'ctime': ctime}
    # здесь дописать данные для БД
    
def get_file_info(file):
    info = os.stat(file)
    file_name = os.path.basename(file)
    created_time = datetime.fromtimestamp(info.st_ctime)
    return { 'name': file_name, 'created_time':created_time, 'size':info.st_size }

# хэш всего файла
def get_hash(file):
    with open(file, 'rb') as f:
        digest = hashlib.file_digest(f, 'sha256')
        
    return digest.hexdigest()

# хэш содержимого файла
def get_content_hash(file_content: str):
    return hashlib.sha256(file_content.encode('utf-8')).hexdigest()

def compare_info(file1, file2):
    return file1['name'] == file2['name'] and \
           file1['created_time'] == file2['created_time'] and \
           file1['size'] == file2['size']

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

def compare_files(data: list, type: str):
    duplicates = []
    copy_d = deepcopy(data)
    for file in data:
        for j in copy_d:   
            if type == 'data': # метаданные
                if compare_info(file, j):
                    duplicates.append((file, j))
            elif type == 'hash':
                if compare_hash(file, j):
                    duplicates.append((file, j))

def get_hashes(files: list):
    
    with multiprocessing.Pool() as pool:
        hashes = pool.map(get_hash,files)
    
    return hashes
    

def walk(path, intypes, extypes, depth):
    start_dir = path
    all_files = []
    
    for current_dir, dirs, files in os.walk(start_dir):
        if not is_correct_depth(start_dir, current_dir, depth):
            continue
        for file in files:
            ext = os.path.splitext(file)[1][1:]
            
            if intypes is None and extypes is None:
                full_path = os.path.join(current_dir,*dirs,file)
                all_files.append(full_path)
                continue
                
            if intypes is not None and ext in intypes:
                full_path = os.path.join(current_dir,*dirs,file)
                all_files.append(full_path)
                continue
            
            if extypes is not None and ext not in extypes:
                full_path = os.path.join(current_dir,*dirs,file)
                all_files.append(full_path)
                continue

        print(os.path.abspath(current_dir), dirs, files)
    
    return all_files 
        
def create_txt(out_file, dbpath):
    table = PrettyTable()
    table.field_names = ['','']
    db = DataBase(dbpath)
    data = db.get_data()
    table.add_rows(data)
    
    with open(out_file, 'w') as w:
        w.write(str(table))
    

def create_csv(out_file, dbpath):
    db = DataBase(dbpath)
    data = db.get_data()
    
    with open(out_file, 'w') as w:
        writer = csv.writer(w, delimiter=';', lineterminator='\n')
        writer.writerows(data)


files = walk(s_path, intypes, extypes, depth)

duplicate_files = compare_files(files,'hash')
print(duplicate_files)
