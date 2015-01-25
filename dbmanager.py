#!/usr/bin/env python
#  coding: utf-8

import sqlite3 as lite
import threading

#NOTE: Because flask is multi-threaded we need to force sqlite to not
#check threads and lock and realease explicitly

class Database():
    def __init__(self):
        self.lock = threading.Lock()
        self.con  = lite.connect('meessages.db', check_same_thread = False)
        self.cur  = self.con.cursor()
        self.createTablesStructure()

    def createTablesStructure(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS messages(date TEXT NOT NULL, \
                                                              loglevel TEXT NOT NULL, \
                                                              via TEXT NOT NULL, \
                                                              message TEXT NOT NULL, \
                                                              destination TEXT, \
                                                              subject TEXT, \
                                                              delivered INTEGER NOT NULL)")
    
    def getVersion(self):
        self.lock.acquire()
        self.cur.execute('SELECT SQLITE_VERSION()')
        data = self.cur.fetchone()
        self.lock.release()
        return data
        
    
    def insertMessage(self, date, loglevel, via, message, destination=None, subject=None, delivered=0):
        self.lock.acquire()
        self.cur.execute("insert into messages values (?, ? ,? ,? ,? ,? ,?)", (date, loglevel, via, message, destination, subject, delivered))
        self.con.commit()
        self.lock.release()
    
    def get_last_messages(self, howmany):
        self.lock.acquire()
        self.cur.execute("SELECT * FROM messages ORDER BY rowid DESC LIMIT "+(str(howmany)))
        result = self.cur.fetchall()
        self.lock.release()
        return result
        
    def setDelivered(self):
        self.lock.acquire()
        lastrowid = self.cur.lastrowid
        self.cur.execute("UPDATE messages SET delivered=? WHERE rowid=?", (1, lastrowid))
        self.con.commit()
        self.lock.release()
        
    def close(self):
        self.con.close()
        
if __name__ == '__main__':
    import time 
    db = Database()
    print "SQLite version: ", db.getVersion() 
    date = timestamp = time.strftime('%Y-%M-%d %H:%M:%S',time.localtime())
    db.insertMessage(date, 'DEBUG', 'internal', 'debug message')
    lastrowid = db.cur.lastrowid
    db.setDelivered()
    db.cur.execute("SELECT * FROM messages")

    rows = db.cur.fetchall()

    for row in rows:
        print row
    db.close()
