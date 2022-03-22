import sqlite3
class queries:
    
    def __init__(self, databaseName):
        self.con = sqlite3.connect(databaseName)
        self.cursor = self.con.cursor()

    
    def registerUser(self, epost, fornavn, etternavn, passord):
        self.con.commit()
        self.con.close
        self.cursor.execute("""
        Insert into bruker VALUES (:Email, :Fornavn, :Etternavn, :Passord);
        """, {"Email" : epost, "Fornavn" : fornavn, "Etternavn" : etternavn, "Passord" : passord})
        self.con.commit()
        self.con.close


    def register(self,brenneri, kaffenavn, poeng, smaksnotat, email):
        self.cursor.execute("""
        Insert into kaffebrenneri VALUES (:brenneri);
        Insert into kaffesmaking VALUES (SID, Notater, Poeng, Smaksdato, Email, Kaffenavn, Brennerinavn) 
        (:Notater, :Poeng, :Email, :Kaffenavn);
        """, {"brenneri" : brenneri, "Kaffenavn" : kaffenavn, "Notater" : smaksnotat, "Poeng" : poeng, "Email" : email})
        self.con.commit()
        self.con.close

    def getUser(self, email, password):
        user = self.cursor.execute("""
        SELECT * from bruker WHERE Email = :email AND Passord = :passord;
        """, {"email" : email, "passord" : password})
        userParam = user.fetchall()
        

        self.con.commit()
        self.con.close
        return userParam

    def testedMost(self):
        names = self.cursor.execute("""
        SELECT Fornavn, Etternavn, max(antallKaffe) as AntallSmakt FROM
        (SELECT Fornavn, Etternavn, count(*) as antallKaffe FROM kaffeSmaking
        NATURAL JOIN bruker
        GROUP BY Kaffenavn, Brennerinavn);
        """)

        self.con.commit()
        self.con.close
        return names.fetchall()

    def mostValue(self):
        coffee = self.cursor.execute("""
        SELECT Brennerinavn, Kaffenavn, Kilospris, AVG(Poeng) as Snittscore FROM ferdigbrentKaffe
        NATURAL JOIN kaffeSmaking
        GROUP BY Kaffenavn, Brennerinavn
        ORDER BY Snittscore/Kilospris DESC;
        """)

        self.con.commit()
        self.con.close
        return coffee.fetchall()

    def describedBy(self, word):
        coffee = self.cursor.execute("""
        SELECT DISTINCT Brennerinavn, Kaffenavn FROM ferdigbrentKaffe
        NATURAL JOIN kaffeSmaking
        WHERE Notater LIKE "%{}%" COLLATE NOCASE OR Beskrivelse LIKE "%{}%" COLLATE NOCASE;
        """.format(word, word))
        self.con.commit()
        self.con.close
        return coffee.fetchall()

    def findCoffees(self, ):
        coffee = self.cursor.execute("""
        SELECT DISTINCT Brennerinavn, Kaffenavn FROM ferdigbrentKaffe
        NATURAL JOIN Foredlingsmetode
        NATURAL JOIN kaffeparti
        NATURAL JOIN gård
        WHERE Metodenavn <> "vasket" COLLATE NOCASE AND (land = "Rwanda" COLLATE NOCASE OR land = "Colombia");
        """.format())
        self.con.commit()
        self.con.close
        return coffee.fetchall()
