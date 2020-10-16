from os.path import isfile
from sqlite3 import connect

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

cnx = connect(DB_PATH, check_same_thread=False)
cur - cnx.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    
    return inner
    
    @with_commit
    def build():
        if isfile(BUILD_PATH):
            scriptexec(BUILD_PATH)
    
    def commit():
        cnx.commit()
    
    def close():
        cnx.close()
    
    def feild(command, *values):
        cur.execute(command, tuple(values))
        
        if (fetch := cur.fetchone()) is not None:
            return fetch[0]
    
    def record(command, *values):
        cur.execute(command, tuple(values))
        
        return cur.fetchone()
    
    def records(command, *values):
        cur.execute(command, tuple(values))
        
        return cur.fetchall()
    
    def column(command, *values):
        cur.execute(command, tuple(values))
        
        return [item[0[ for item in cur.fetchall()]
        
    def excute(command, *values):
        cur.execute(command, tuple(values))

    def multiexcute(command, *values):
        cur.execute(command, valueset)
        
    def scriptexec(command, *values):
        with open(path, "r", encoding="utf-8") as scritpt:
            cur.executescript(sctipt.read())