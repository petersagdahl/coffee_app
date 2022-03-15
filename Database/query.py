import sqlite3

from sqlalchemy import null





class queries:
    
    def __init__(self, databaseName):
        self.con = sqlite3.connect(databaseName)
        self.cursor = self.con.cursor()
        

    @classmethod
    def register(self,brenneri, kaffenavn, poeng, smaksnotat, email):
        self.cursor.execute("""
        Insert into kaffebrenneri VALUES (:brenneri);
        Insert into kaffesmaking (SID, Notater, Poeng, Smaksdato, Email, Kaffenavn, Brennerinavn) 
        Values (:Notater, :Poeng, :Email, :Kaffenavn)
        """, {"brenneri" : brenneri, "Kaffenavn" : kaffenavn, "Notater" : smaksnotat, "Poeng" : poeng, "Email" : email})
        self.con.commit()
        self.con.close

    @classmethod
    def getUser(self, email, password):
        self.cursor.execute("""
        """, {})

        forname = null
        surname = null

        self.con.commit()
        self.con.close
        return forname, surname

