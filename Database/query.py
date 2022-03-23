import sqlite3
from unittest import result
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

        self.con.commit()
        self.con.close
        return userParam

    def testedMost(self):
        names = self.cursor.execute("""
        SELECT Fornavn, Etternavn, count(email) AS AntallSmakt FROM
        (SELECT Fornavn, Etternavn, Email FROM kaffeSmaking
        NATURAL JOIN bruker
        GROUP BY Kaffenavn, Brennerinavn)
		GROUP BY Email
        ORDER BY AntallSmakt DESC;
        """)

        self.con.commit()
        self.con.close


        result = [names.fetchall(), names.description]

        return result

    def mostValue(self):
        coffee = self.cursor.execute("""
        SELECT Brennerinavn, Kaffenavn, Kilospris, ROUND(AVG(Poeng), 2) as Snittscore FROM ferdigbrentKaffe
        NATURAL JOIN kaffeSmaking
        GROUP BY Kaffenavn, Brennerinavn
        ORDER BY Snittscore/Kilospris DESC;
        """)

        self.con.commit()
        self.con.close

        result = [coffee.fetchall(), coffee.description]

        return result

    def describedBy(self, word):
        coffee = self.cursor.execute("""
        SELECT DISTINCT Brennerinavn, Kaffenavn FROM ferdigbrentKaffe
        LEFT OUTER JOIN kaffeSmaking USING(Kaffenavn, Brennerinavn)
        WHERE Notater LIKE "%{}%" COLLATE NOCASE OR Beskrivelse LIKE "%{}%" COLLATE NOCASE;
        """.format(word, word))
        self.con.commit()
        self.con.close

        result = [coffee.fetchall(), coffee.description]

        return result

    def findCoffees(self, kaffeInput):
        innsetting = self.lagString(kaffeInput)

        coffee = self.cursor.execute("""
        SELECT DISTINCT Brennerinavn, Kaffenavn FROM ferdigbrentKaffe
        NATURAL JOIN Foredlingsmetode
        NATURAL JOIN kaffeparti
        NATURAL JOIN gård
        {};
        """.format(innsetting))
        self.con.commit()
        self.con.close

        result = [coffee.fetchall(), coffee.description]

        return result

    def lagString(self, kaffeInput):
        landString = ""
        foredlingsmetode = ""
        ikke_foredlingsmetode = ""

        for item in kaffeInput[0]:
            landString = landString + "land = " + '"' + item + '"' + " COLLATE NOCASE OR "
        landString = landString[:-3]

        for item in kaffeInput[1]:
            foredlingsmetode = foredlingsmetode + "Metodenavn = " + '"' + item + '"' + " COLLATE NOCASE OR "
        foredlingsmetode = foredlingsmetode[:-3]

        for item in kaffeInput[2]:
            ikke_foredlingsmetode = ikke_foredlingsmetode + "Metodenavn <> " + '"' + item + '"' + " COLLATE NOCASE OR "
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
        if totalString != "":
            totalString = "WHERE " + totalString

        return totalString

    """
    Under er koden for admin-funksjonalitet, som brukes for innsetting i databasen.
    """


    def addGård(self, gårdsid, gårdsnavn, moh, region, land): 
        self.cursor.execute("""
        Insert into gård VALUES (:gårdsid, :gårdsnavn, :moh, :region, :land);
        """, {"gårdsid" : gårdsid, "gårdsnavn":gårdsnavn, "moh": moh, "region": region, "land" : land})

        self.con.commit()
        self.con.close

    def sjekkGård(self, gårdsid):
        resultat = self.cursor.execute("""
        SELECT * FROM gård
        WHERE gårdsid = :gårdsid;
        """, {"gårdsid" : gårdsid})
        self.con.commit()
        self.con.close

        return resultat.fetchall()

    def addKaffebønner(self, bønnenavn, kaffeart, gårdsid):
        #Legger til kaffe
        self.cursor.execute("""
        Insert into kaffebønner (Bønnenavn, Kaffeart)
        VALUES (:bønnenavn, :kaffeart);
        """, {"bønnenavn" : bønnenavn, "kaffeart" : kaffeart})

        #sjekker om gården dyrker denne bønna
        #legge til gården som dyrker
        if not (self.sjekkResultat(self.sjekkKaffedyrker(bønnenavn, gårdsid))):
            self.cursor.execute("""
            Insert into dyrkesAv VALUES (:bønnenavn, :gårdsID);
            """, {"bønnenavn" : bønnenavn, "gårdsID" : gårdsid})
            
            self.con.commit()
            self.con.close

    def sjekkKaffedyrker(self, bønnenavn, gårdsid):
        resultat = self.cursor.execute("""
        SELECT * FROM dyrkesAv
        WHERE Bønnenavn = :bønnenavn AND GårdsID = :gårdsid;
        """, {"bønnenavn" : bønnenavn, "gårdsid" : gårdsid})
        self.con.commit()
        self.con.close

        return str(resultat.fetchall()).strip().translate(str.maketrans("", "", ",[]('"))

    def addKaffedyrker(self, bønnenavn, gårdsid):
        self.cursor.execute("""
        Insert into dyrkesAv VALUES (:bønnenavn, :gårdsID);
        """, {"bønnenavn" : bønnenavn, "gårdsID" : gårdsid})
        
        self.con.commit()
        self.con.close



    def sjekkKaffebønner(self, bønnenavn):

        resultat = self.cursor.execute("""
        SELECT * FROM kaffebønner
        WHERE Bønnenavn = :bønnenavn;
        """, {"bønnenavn" : bønnenavn})
        self.con.commit()
        self.con.close

        return str(resultat.fetchall()).strip().translate(str.maketrans("", "", ",[]('"))

    def addForedlingsmetode(self, metodenavn, forklaring):
        #må finne KPID
        IDer = self.cursor.execute("""
        SELECT MetodeID FROM Foredlingsmetode;
        """)
        IDliste = list(filter(None, str(IDer.fetchall()).strip().translate(str.maketrans("", "", ",[]('")).split(")")))
        IDliste = [int(i) for i in IDliste]
        førsteLedigeID = 0

        if (len(IDliste) != 0):
            while førsteLedigeID <= max(IDliste):
                if førsteLedigeID not in IDliste:
                    break
                førsteLedigeID += 1
        
        self.cursor.execute("""
        Insert into foredlingsmetode (MetodeID, Metodenavn, Forklaring)
        VALUES (:metodeID, :metodenavn, :forklaring);
        """, {"metodeID" : førsteLedigeID, "metodenavn" : metodenavn, "forklaring" : forklaring})

        self.con.commit()
        self.con.close

        return førsteLedigeID

    def sjekkMetode(self, metodenavn):
        resultat = self.cursor.execute("""
        SELECT MetodeID FROM Foredlingsmetode
        WHERE Metodenavn = :metodenavn;
        """, {"metodenavn" : metodenavn})
        self.con.commit()
        self.con.close

        return str(resultat.fetchall()).strip().translate(str.maketrans("", "", "[](),"))
    
    def sjekkParti(self, KPID):
        resultat = self.cursor.execute("""
        SELECT KPID FROM kaffeparti
        WHERE KPID = :KPID;
        """, {"KPID" : KPID})
        self.con.commit()
        self.con.close

        return str(resultat.fetchall()).strip().translate(str.maketrans("", "", ",[]()'"))

    def addParti(self, innhøstingsår, kilosprisUSD, gårdsID, metodeID, kaffebønner):
        #må finne KPID
        IDer = self.cursor.execute("""
        SELECT KPID FROM kaffeparti;
        """)

        IDliste = list(filter(None, str(IDer.fetchall()).strip().translate(str.maketrans("", "", ",[]('")).split(")")))
        IDliste = [int(i) for i in IDliste]
        førsteLedigeID = 0

        if (len(IDliste) != 0):
            while førsteLedigeID <= max(IDliste):
                if førsteLedigeID not in IDliste:
                    break
                førsteLedigeID += 1


        self.cursor.execute("""
        Insert into kaffeparti (KPID, Innhøstingsår, KilosprisUSD, GårdsID, MetodeID)
        VALUES (:KPID, :innhøstingsår, :kilosprisUSD, :gårdsID, :metodeID);
        """, {"KPID" : førsteLedigeID, "innhøstingsår" : innhøstingsår, "kilosprisUSD" : kilosprisUSD, "gårdsID" : gårdsID, "metodeID" : metodeID})

        self.con.commit()

        #Legge til bønnene partiet består av
        for item in kaffebønner:
            self.cursor.execute("""
            Insert into bestårAv VALUES (:KPID, :Bønnenavn);
            """, {"KPID" : førsteLedigeID, "Bønnenavn" : item})
            self.con.commit()

        

        self.con.commit()
        self.con.close

        return førsteLedigeID

    def addBrenneri(self, brennerinavn):
        self.cursor.execute("""
        Insert into kaffebrenneri VALUES (:brennerinavn);
        """, {"brennerinavn" : brennerinavn})
 
        self.con.commit()
        self.con.close

    def sjekkBrenneri(self, brennerinavn):
        resultat = self.cursor.execute("""
        SELECT * FROM kaffebrenneri
        WHERE Brennerinavn = :brennerinavn;
        """, {"brennerinavn" : brennerinavn})
        self.con.commit()
        self.con.close

        return str(resultat.fetchall()).strip().translate(str.maketrans("", "", ",[]()'"))
    
    def addFerdigbrentKaffe(self, kaffenavn, brennerinavn, brenningsgrad, brennedato, beskrivelse, kilospris, KPID):
        self.cursor.execute("""
        Insert into ferdigbrentKaffe VALUES (:kaffenavn, :brennerinavn, :brenningsgrad, :brennedato, :beskrivelse, :kilospris, :KPID);
        """, {"kaffenavn" : kaffenavn, "brennerinavn" : brennerinavn, "brenningsgrad" : brenningsgrad, "brennedato" : brennedato, "beskrivelse" : beskrivelse, "kilospris" : kilospris, "KPID" :KPID})

 
        self.con.commit()
        self.con.close

    def sjekkFerdigbrentKaffe(self, kaffenavn, brennerinavn):
        resultat = self.cursor.execute("""
        SELECT * FROM ferdigbrentKaffe
        WHERE Brennerinavn = :brennerinavn AND Kaffenavn = :kaffenavn;
        """, {"brennerinavn" : brennerinavn, "kaffenavn" : kaffenavn})
        self.con.commit()
        self.con.close

        return resultat.fetchall()



    def sjekkResultat(self, resultat):
        formatertResultat = str(resultat).strip().translate(str.maketrans("", "", "[](),"))
        return False if (formatertResultat == "") else True
 
