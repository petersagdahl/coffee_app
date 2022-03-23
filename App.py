from msilib.schema import Error
from unittest import result
from Database.query import queries
import sqlite3
from Bruker import bruker
import datetime

class App:

    def __init__(self):
        self.SQL =  queries('kaffeDB.db')
        self.user = None

    def runApp(self):
        done = False
        print("""
Skriv inn tall:
    1. Bruker
    2. Admin 
""")
        start = int(input('{:15}'.format("Valg:  ")))

        if (start == 1):
            loggetInn = self.logIn()
            

            if (loggetInn == True):
                while done == False:
                    done = self.registerAction()
        elif (start == 2):
            self.admin()

    def admin(self):
        print("""
Regsitrer en kaffe.
        """)
        kaffebønner = []
        gårdsid = None
        metodeID = None
        kaffeparti = None
        kaffebrenneri = None

        #Kaffeparti
        print("Skriv inn kaffepartiet kaffen består av.")
        while True:
            try:
                respond = str(input("Er partiet allerede registrert? (Ja/Nei):  "))
                if (respond.casefold() != "ja" and respond.casefold() != "nei"):
                    print("Ugyldig input. Prøv igjen...")
                    continue
                break
            except Exception as e:
                print(e)
        
        while True and respond.casefold() == "ja":
            
            print("Registrer kaffepartiet kaffen består av.")
            try: 
                kaffepartiFraBruker = int(input('{:15}'.format("KPID:  ")))
                
                if (self.SQL.sjekkParti(kaffepartiFraBruker)):
                    kaffeparti = kaffepartiFraBruker
                    break

                else:
                    input("Kaffepartiet finnes ikke")
                    respond = str(input("Er partiet allerede registrert? (Ja/Nei):  "))
                    continue
            except Exception as e:
                    print(e)
        if (respond.casefold() == "nei"):
            #GÅRD
            print("Hvilken gård dyrker kaffens bønner?")
            while True:
                try:
                    gårdsid = int(input('{:15}'.format("GårdsID:  ")))
                    break
                except Exception as e:
                    print(e)
            if (self.SQL.sjekkResultat(self.SQL.sjekkGård(gårdsid)) == False):
                respond = str(input("Gården finnes ikke, vil du registrere en ny? (Ja/Nei)"))
                while True:
                    if (respond.casefold() == "ja"):
                        try:
                            gårdsid = str(input('{:15}'.format("GårdsID:  ")))
                            gårdsnavn = str(input('{:15}'.format("Gårdsnavn:  ")))
                            moh = str(input('{:15}'.format("Meter over havet:  ")))
                            region = str(input('{:15}'.format("Region:  ")))
                            land = str(input('{:15}'.format("Land:  ")))
                    
                            self.SQL.addGård(gårdsid, gårdsnavn, moh, region, land)
                            break
                        except Exception as e:
                            print(e)


                    else:
                        return
            #foredlingsmetode
            
            done = False
            while done == False:
                metodenavn = str(input('{:15}'.format("Foredlingmetode:  "))).casefold()
                try:
                    if (self.SQL.sjekkMetode(metodenavn) != ""):
                        respond = str(input("""
                        
Det finnes allerede metode(r) med samme navn. 
Vil du likevelregistrere ny metode med samme navn? (Ja/Nei):  
"""))
                        if (respond.casefold() == "nei"):
                            metodeID = self.SQL.sjekkMetode(metodenavn)
                            break
                        elif (respond.casefold() == "ja"):
                            forklaring = str(input('{:15}'.format("Foklaring:  ")))
                            metodeID = self.SQL.addForedlingsmetode(metodenavn, forklaring)
                            break
                    else:
                        forklaring = str(input('{:15}'.format("Foklaring:  ")))
                        metodeID = self.SQL.addForedlingsmetode(metodenavn, forklaring)
                        break

                except Exception as e:
                    print(e)

            #kaffebønner
            bønnenavn = ""
            print("""
Skriv inn de kaffebønnene ditt kaffeparti består av. 
Husk at alle disse må produseres av gården du har valgt.
""")
            while bønnenavn != "ferdig":
            
                try:
                    bønnenavn = str(input('{:15}'.format("Skriv inn bønnenavn:  "))).casefold()
                    if (self.SQL.sjekkResultat(self.SQL.sjekkKaffebønner(bønnenavn)) and bønnenavn.casefold() != "ferdig"):
                        self.SQL.addKaffedyrker(bønnenavn, gårdsid)
                        input("Denne er allerede registrert. Enter for å fortsette.")
                        kaffebønner.append(bønnenavn)
                        continue
                    elif bønnenavn.casefold() != "ferdig":
                        kaffeart = str('{:15}'.format(input("Kaffeart:  ")))[:-1]
                        self.SQL.addKaffebønner(bønnenavn, kaffeart, gårdsid)
                        kaffebønner.append(bønnenavn)
                        continue
                    elif bønnenavn.casefold() == "ferdig" and len(kaffebønner) == 0:
                        input("Et kaffeparti må bestå av minst én kaffebønne. Trykk enter for å fortsette.")
                        bønnenavn = "Ikke-ferdig"
                except Exception as e:
                    print(e)

            #kaffeparti
            
            while True:
                print("Registrer kaffepartiet kaffen består av.")
                try:
                        innhøstingsår = int(input('{:15}'.format("Innhøstingsår:  ")))
                        kilosprisUSD = float(input('{:15}'.format("Kilospris i USD:  ")))
                        kaffeparti = self.SQL.addParti(innhøstingsår, kilosprisUSD, gårdsid, metodeID, kaffebønner)
                        break

                except Exception as e:
                        print(e)

        #kaffebrenneri
        while True:
            print("Hvilket kaffebrenneri har brent kaffen?")
            try:
                kaffebrenneri = str(input('{:15}'.format("Brennerinavn:  ")))

                if (self.SQL.sjekkResultat(self.SQL.sjekkBrenneri(kaffebrenneri))):
                    kaffebrenneri = self.SQL.sjekkBrenneri(kaffebrenneri)
                    break
                else:
                    self.SQL.addBrenneri(kaffebrenneri)
                    break
            except Exception as e:
                print(e)

        #ferdigbrentkaffe
        while True:
            print("Registrer ferdigbrent kaffe")
            try:
                kaffenavn = str(input('{:15}'.format("Kaffenavn:  ")))
                brenningsgrad = str(input('{:15}'.format("Brenningsgrad (lys, middels eller mørk):  ")))
                dato = False
                while dato == False:
                    brennedato = str(input('{:15}'.format("Brennedato:  ")))
                    dato = self.sjekkDato(brennedato)
                beskrivelse = str(input('{:15}'.format("Beskrivelse:  ")))
                kilospris = float(input('{:15}'.format("Kilopris:  ")))

                if (self.SQL.sjekkResultat(self.SQL.sjekkFerdigbrentKaffe(kaffenavn, kaffebrenneri))):
                    input("Kaffen eksisterer fra før. Velg et annet kaffenavn for å fortsette.")
                    continue
                else:
                    self.SQL.addFerdigbrentKaffe(kaffenavn, kaffebrenneri, brenningsgrad, brennedato, beskrivelse, kilospris, kaffeparti) 
                    break
            except Exception as e:
                print(e)




                

    def sjekkDato(self, datostring):
        try:   
            datetime.datetime.strptime(datostring, '%Y-%m-%d')
        except ValueError:
            return False
        return True




    def logIn(self):
        ok = False
        
        while True:
            try:
                mode = str(input("Har du en bruker?:  "))
                if (mode.casefold() != "ja" and mode.casefold() != "nei"):
                    print("Ugyldig input. Prøv igjen...")
                    continue
                break
            except Exception as e:
                    print(e)

        if mode.casefold() == 'nei':
            while ok == False:
                print('Registrer nå')
                email = str(input('{:15}'.format("Email:  ")))
                forname = str(input('{:15}'.format("Fornavn:  ")))
                surname = str(input('{:15}'.format("Etternavn:  ")))
                password = str(input('{:15}'.format("Passord:  ")))
                try:
                    self.SQL.registerUser(email, forname, surname, password)
                    ok = True
                except sqlite3.Error:
                    ok = False
                    while True:
                        try:
                            prøveIgjen = str(input("Noe gikk galt. Vil du prøve igjen? (Ja/Nei):  "))
                            if (mode.casefold() != "ja" and mode.casefold() != "nei"):
                                print("Ugyldig input. Prøv igjen...")
                                continue
                            break
                        except Exception as e:
                                print(e)

                                

                if (ok == False and prøveIgjen.casefold() == "nei"):
                    return False
                if (ok == True):
                    user = bruker(email, forname, surname, password)
                    self.user = user
                    return True
                
                    
                
        elif mode.casefold() == 'ja':
            while ok == False:
                prøveIgjen = "Nei"
                print('Logg inn nå...')
                email = str(input('{:15}'.format("Email:  ")))
                password = str(input('{:15}'.format("Passord:  ")))
                try:
                    userString = str(self.SQL.getUser(email, password)).strip().translate(str.maketrans("", "", "[]()'"))
                    user = [x for x in userString.split(',')]
                    ok = True
                    error = False

                except sqlite3.Error:
                    ok = False
                    error = True
                    while True:
                        try:
                           
                            prøveIgjen = str(input("Noe gikk galt. Vil du prøve igjen? (Ja/Nei):  "))
                            if (mode.casefold() != "ja" and mode.casefold() != "nei"):
                                print("Ugyldig input. Prøv igjen...")
                                continue
                            break
                        except Exception as e:
                            error = False


                if (len(user) < 4 and error == False):
                    ok = False
                    while True:
                        try:
                            prøveIgjen = str(input("Noe gikk galt. Vil du prøve igjen? (Ja/Nei):  "))
                            if (mode.casefold() != "ja" and mode.casefold() != "nei"):
                                print("Ugyldig input. Prøv igjen...")
                                continue
                            break
                        except Exception as e:
                                print(e)
                if (prøveIgjen.casefold() == "ja"):
                    continue
                elif (ok == False and prøveIgjen.casefold() == "nei"):
                    return False
                else:
                    user = bruker(user[0], user[1], user[2], user[3])
                    self.user = user
                    ok = True
                    return True

        
    

    def registerAction(self):
        print("""
        Skriv inn tall:
            1. Registrer kaffesmaking
            2. Hvem har smakt flest unike kaffe?
            3. Hvilken kaffe gir mest for pengene?
            4. Hvilke kaffer er blitt beskrevet med ()?
            5. Kaffe fra land: 
            Foredlet:
            0. Ferdig
        """)
        while True:
            error = False
            try:
                action = int(input("Hva har du lyst til å gjøre?: "))
                break
            except Exception as e:
                print("Ugyldig handling, prøv igjen")
        
        
        if action == 1:
            self.registerCoffeeTaste()
            next = input("Trykk enter for å fortsette")
            return False
        elif action == 2:
            tasteList = self.SQL.testedMost()
            
            self.printFormat(tasteList)

            next = input("Trykk enter for å fortsette")
            return False
        elif action == 3:
            mostValue = self.SQL.mostValue()
            
            self.printFormat(mostValue)
  
            next = input("Trykk enter for å fortsette")
            return False
        elif action == 4:
            error = False
            while True:
                try:
                    word = str(input("Hvilket ord ville beskrevet den?:  "))
                except Exception as e:
                        error = True
                        print(e)
                if (error == False):
                            break
            
            coffeeDescribedBy = self.SQL.describedBy(word)

            self.printFormat(coffeeDescribedBy)
            
            next = input("Trykk enter for å fortsette")
            return False
        elif action == 5:
            kaffeInput = self.foretrukketKaffe()
            kaffe = self.SQL.findCoffees(kaffeInput)

            self.printFormat(kaffe)

            if (len(kaffe) == 0):
                print("Ingen resultater...")
            
            next = input("Trykk enter for å fortsette")
            return False
        elif action == 0:
            return True
        else:
            print("Ugyldig handling, prøv igjen")
            next = input("Trykk enter for å fortsette")
            return False
        


    #Last opp i databasen
    def registerCoffeeTaste(self):
        ok = False
        prøveIgjen = "Nei"
        while ok == False:
            while True:
                try:
                    brenneri = str(input('{:30}'.format("Brennerinavn:  ")))
                    kaffenavn = str(input('{:30}'.format("Kaffenavn:  ")))
                    poeng = int(input('{:30}'.format("Antall poeng (fra 1 til 10):  ")))
                    smaksnotat = str(input('{:30}'.format("Smaksnotat:  ")))
                    break
                except Exception as e:
                        print(e)
                
            

            kaffestreng = str(self.SQL.checkCoffee(kaffenavn, brenneri)).strip().translate(str.maketrans("", "", ",[]()'"))
            if (kaffestreng == ''):
                while True:
                    try:
                        prøveIgjen = str(input("Vi har ikke kaffen din i databasen. Vil du prøve en annen kaffe? (Ja/Nei):  "))
                        break
                    except Exception as e:
                            print(e)
                    
                if prøveIgjen.casefold() == "ja":
                    continue
                else:
                    break
            try:
                self.SQL.register(brenneri, kaffenavn, poeng, smaksnotat, self.user.getEmail())
                ok = True
            except sqlite3.Error as e:
                print(e)
                ok = False
                while True:
                    try:
                        prøveIgjen = str(input("Noe gikk galt. Vil du prøve igjen? (Ja/Nei):  "))
                        break
                    except Exception as e:
                            print(e)
                
            if (ok == False and prøveIgjen == "Nei"):
                    ok = True
            elif (prøveIgjen == "Ja"):
                    break

    def foretrukketKaffe(self):
        land = []
        foredlingsmetoder = []
        ikke_foredlingsmetoder = []

        counter = 1

        print("Skriv inn ett foretrukket land av gangen. Trykk enter uten input når du er ferdig.")
        while True:
            inputLand = ""
            try:
                inputLand = str(input('{:15}'.format("Land {}:  ".format(counter))))
                if (inputLand != ""):
                    land.append(inputLand)
                counter += 1
            except Exception as e:
                    print(e)
            if (inputLand == ""):
                break 
            
        counter = 1
        print("Skriv inn én foretrukket foredlingsmetode av gangen. Trykk enter uten input når du er ferdig.")
        while True:
            foredlingsmetode = ""
            try:
                foredlingsmetode = str(input('{:15}'.format("Foredlingsmetode {}:  ".format(counter))))
                if (foredlingsmetode != ""):
                    foredlingsmetoder.append(foredlingsmetode)
                counter += 1
            except Exception as e:
                    print(e)
            if (foredlingsmetode == ""):
                break    

        counter = 1
        print("""Skriv inn én foredlingsmetode du IKKE ønsker av gangen. (Kan ikke være samme som foretrukne.)
Trykk enter uten input når du er ferdig.""")
        while True:
            ikke_foredlingsmetode = ""
            try:
                ikke_foredlingsmetode = str(input('{:15}'.format("Unngå foredlingsmetode {}:  ".format(counter))))
                if (ikke_foredlingsmetode in foredlingsmetoder):
                    input("Kan ikke ha samme verdier for foretrukne og ikke-foretrukne fordelingsmetoder")
                    continue
                if (ikke_foredlingsmetode != ""):
                    ikke_foredlingsmetoder.append(ikke_foredlingsmetode)
                counter += 1
            except Exception as e:
                    print(e)
            if (ikke_foredlingsmetode == ""):
                break  

        kaffeInput = [land, foredlingsmetoder, ikke_foredlingsmetoder]
        return kaffeInput

    def printFormat(self, values):
        columnList = values[1]
        resultList = values[0]
        columnNames = []

        for items in columnList:
            columnNames.append(items[0])

    

        header = str(columnNames).strip().translate(str.maketrans("", "", "[]()'")).split(",")
        rows = []
        
        for items in resultList:
            row = []
            columns = str(items).strip().translate(str.maketrans("", "", "[]()'")).split(",")
            for item in columns:
                row.append(item)
            rows.append(row)

        if (len(rows) == 0):
            print("Et slikt resultat finnes ikke.")
            return

        print("  +  "+'\n'.join([''.join(['{}'.format('-'*15 + "  +  ") for x in header])]))
        print('\n'.join([''.join(['{:20}'.format("  |  " + x) for x in header])]) + "  |  ")
        print("  +  " +'\n'.join([''.join(['{}'.format("---------------  +  ") for x in header])]))
        print('\n'.join([''.join(['{:20}'.format("  |  " + x) for x in r ]) + "  |  " for r in rows ]))
        print("  +  "+'\n'.join([''.join(['{}'.format('-'*15 + "  +  ") for x in header])]))



    

teste = App()

teste.runApp()
#registerAction()

