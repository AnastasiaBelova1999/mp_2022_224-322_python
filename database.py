import sqlite3
from datetime import datetime
import os 
class DataBase:
    
    def __init__(self, dbpath):
        self.path = dbpath
        

    def create_table(self):
        
        if os.path.exists(self.path):
            os.remove(self.path)
        
        query = '''
        CREATE TABLE IF NOT EXISTS duplicate_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename VARCHAR(255),
            mode,
            atime datetime,
            mtime datetime,
            ctime datetime,
            hash VARCHAR(1024)
        )
        '''
        
        with sqlite3.connect(self.path) as con:
            con.execute(query)
                
    
    def insert_data(self, *file):
        
        atime = datetime.fromtimestamp(file[2]).strftime('%Y-%m-%d %H:%M:%S')
        mtime = datetime.fromtimestamp(file[3]).strftime('%Y-%m-%d %H:%M:%S')
        ctime = datetime.fromtimestamp(file[4]).strftime('%Y-%m-%d %H:%M:%S')
        
        query = f'''
            insert into duplicate_info (filename, mode, atime, mtime, ctime, hash)
            values ('{file[0]}', {file[1]}, '{atime}', '{mtime}', '{ctime}', '{file[5]}')
        '''        
        with sqlite3.connect(self.path) as con:
            con.execute(query)
                
    
    def get_data(self):
        
        query = '''
            select * from duplicate_info
        '''
        
        with sqlite3.connect(self.path) as con:
                return con.execute(query).fetchall()