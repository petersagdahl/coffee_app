import sqlite3

from sqlalchemy import null




class queries:
    
    def __init__(self, databaseName):
        self.con = sqlite3.connect(databaseName)
        self.cursor = self.con.cursor()
        

    @classmethod
    def register(self):
        self.cursor.execute("""
        Insert into
        """)
        self.con.close

