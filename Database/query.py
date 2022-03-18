import sqlite3
class queries:
    
    def __init__(self, databaseName):
        self.con = sqlite3.connect(databaseName)
        self.cursor = self.con.cursor()

    
    def registerUser(self, epost, fornavn, etternavn, passord):
        
        self.cursor.execute("""
        Insert into bruker VALUES (:Email, :Fornavn, :Etternavn, :Passord);
        """, {"Email" : epost, "Fornavn" : fornavn, "Etternavn" : etternavn, "Passord" : passord})
        self.con.commit()
        self.con.close

    def checkCoffee(self, kaffenavn, brennerinavn):
        coffee = self.cursor.execute("""
        SELECT * FROM ferdigbrentKaffe
        WHERE Kaffenavn = :Kaffenavn AND Brennerinavn = :Brennerinavn;
        """, {"Kaffenavn" : kaffenavn, "Brennerinavn" : brennerinavn})
        self.con.commit()
        self.con.close
        return coffee.fetchall()


    def register(self,brenneri, kaffenavn, poeng, smaksnotat, email):
        self.cursor.execute("""
        Insert into kaffesmaking (Notater, Poeng, Email, Kaffenavn, Brennerinavn) 
        VALUES (:Notater, :Poeng, :Email, :Kaffenavn, :brennerinavn);
        """, {"brennerinavn" : brenneri, "Kaffenavn" : kaffenavn, "Notater" : smaksnotat, "Poeng" : poeng, "Email" : email})
        self.con.commit()
        self.con.close

    def getUser(self, email, password):
        user = self.cursor.execute("""
        SELECT * from bruker WHERE Email = :email AND Passord = :passord;
        """, {"email" : email, "passord" : password})
        userParam = user.fetchall()
        print(userParam)

        self.con.commit()
        self.con.close
        return userParam

    def testedMost(self):
        names = self.cursor.execute("""
        SELECT Fornavn, Etternavn, count(email) AS AntallSmakt FROM
        (SELECT Fornavn, Etternavn, Email FROM kaffeSmaking
        NATURAL JOIN bruker
        GROUP BY Kaffenavn, Brennerinavn)
		GROUP BY Email;
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

    def findCoffees(self, kaffeInput):
        innsetting = self.lagString(kaffeInput)

        coffee = self.cursor.execute("""
        SELECT DISTINCT Brennerinavn, Kaffenavn FROM ferdigbrentKaffe
        NATURAL JOIN Foredlingsmetode
        NATURAL JOIN kaffeparti
        NATURAL JOIN gård
        WHERE {};
        """.format(innsetting))
        self.con.commit()
        self.con.close
        return coffee.fetchall()

    def lagString(self, kaffeInput):
        landString = ""
        foredlingsmetode = ""
        ikke_foredlingsmetode = ""

        for item in kaffeInput[0]:
            landString = landString + "land = " + '"' + item + '"' + " COLLATE NOCASE OR "
        landString = landString[:-3]

        for item in kaffeInput[1]:
            foredlingsmetode = foredlingsmetode + "Forklaring = " + '"' + item + '"' + " COLLATE NOCASE OR "
        foredlingsmetode = foredlingsmetode[:-3]

        for item in kaffeInput[2]:
            ikke_foredlingsmetode = ikke_foredlingsmetode + "Forklaring <> " + '"' + item + '"' + " COLLATE NOCASE OR "
        ikke_foredlingsmetode = ikke_foredlingsmetode[:-3]

        totalString = ""

        if landString != "":
            totalString += "(" + landString + ")"
        if foredlingsmetode != "":
            if totalString != "":
                totalString += " AND "
            totalString += "(" + foredlingsmetode + ")"
        
        if ikke_foredlingsmetode != "":
            if totalString != "":
                totalString += " AND "
            totalString += "(" + ikke_foredlingsmetode+ ")"


        print(totalString)

        return totalString


