from unittest import result
from Database.query import queries
import sqlite3
from Bruker import bruker

class App:

    def __init__(self):
        self.SQL =  queries('kaffeDB.db')
        self.user = None

    def runApp(self):
        done = False
        loggetInn = self.logIn()

        if (loggetInn == True):
            while done == False:
                done = self.registerAction()

    
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
                            prøveIgjen = str(input("Noe gikk feil. Vil du prøve igjen? (Ja/Nei):  "))
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
                           
                            prøveIgjen = str(input("Noe ble feil. Vil du prøve igjen? (Ja/Nei):  "))
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
                            prøveIgjen = str(input("Noe ble feil. Vil du prøve igjen? (Ja/Nei):  "))
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
                    brenneri = str(input("Brennerinavn:  "))
                    kaffenavn = str(input("Kaffenavn:  "))
                    poeng = int(input("Antall poeng (fra 1 til 10):  "))
                    smaksnotat = str(input("Smaksnotat:  "))
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
                    
                if prøveIgjen == "Ja":
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
                        prøveIgjen = str(input("Noe gikk feil. Vil du prøve igjen? (Ja/Nei):  "))
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

        print("Skriv inn foretrukne land. Trykk enter når du er ferdig.")
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
        print("Skriv inn foretrukne foredlingsmetoder. Trykk enter når du er ferdig.")
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
        print("Skriv inn foredlingsmetoder du IKKE ønsker. Trykk enter når du er ferdig.")
        while True:
            ikke_foredlingsmetode = ""
            try:
                ikke_foredlingsmetode = str(input('{:15}'.format("Unngå foredlingsmetode {}:  ".format(counter))))
                if (ikke_foredlingsmetode in foredlingsmetoder):
                    input("Kan ikke ha samme verdier for foretrukne og ikke foretrukne fordelingsmetorder")
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

        print("  +  "+'\n'.join([''.join(['{}'.format('-'*15 + "  +  ") for x in header])]))
        print('\n'.join([''.join(['{:20}'.format("  |  " + x) for x in header])]) + "  |  ")
        print("  +  " +'\n'.join([''.join(['{}'.format("---------------  +  ") for x in header])]))
        print('\n'.join([''.join(['{:20}'.format("  |  " + x) for x in r ]) + "  |  " for r in rows ]))
        print("  +  "+'\n'.join([''.join(['{}'.format('-'*15 + "  +  ") for x in header])]))


    def mostValueForMoney():
        return None

    def coffeesDescribedBy(adjective):
        return None

    

teste = App()

teste.runApp()
#registerAction()

