from Database.query import queries
import sqlite3
from Bruker import bruker

class App:

    def __init__(self):
        self.SQL =  queries('kaffeDB.db')
        self.user = None

    def runApp(self):
        done = False
        self.logIn()
        while done == False:
            done = self.registerAction()

    
    def logIn(self):
        ok = False
        mode = str(input("Har du en bruker?"))
        if mode == 'Nei':
            while ok == False:
                print('Registrer nå')
                email = str(input("Email:"))
                forname = str(input("Fornavn:"))
                surname = str(input("Etternavn:"))
                password = str(input("Passord:"))
                try:
                    self.SQL.registerUser(email, forname, surname, password)
                    ok = True
                except sqlite3.Error:
                    ok = False
                    prøveIgjen = str(input("Noe gikk feil. Vil du prøve igjen? (Ja/Nei)"))

                if (ok == False and prøveIgjen == "Nei"):
                    ok = True
                if (ok == True):
                    user = bruker(email, forname, surname, password)
                    self.user = user
                
                    
                
        elif mode == 'Ja':
            while ok == False:
                prøveIgjen = "Nei"
                print('Logg inn nå...')
                email = str(input("Email:"))
                password = str(input("Passord:"))
                try:
                    userString = str(self.SQL.getUser(email, password)).strip().translate(str.maketrans("", "", "[]()'"))
                    user = [x for x in userString.split(',')]
                    ok = True
                    error = False
                except sqlite3.Error:
                    ok = False
                    error = True
                    prøveIgjen = str(input("Noe gikk feil. Vil du prøve igjen? (Ja/Nei)"))

                if (len(user) < 4 and error == False):
                    prøveIgjen = str(input("Noe gikk feil. Vil du prøve igjen? (Ja/Nei)"))

                if (prøveIgjen == "Ja"):
                    ok = False
                elif (ok == False and prøveIgjen == "Nei"):
                    ok = True
                else:
                    user = bruker(user[0], user[1], user[2], user[3])
                    self.user = user
                    ok = True

    

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
        action = int(input("Hva har du lyst til å gjøre?"))
        
        if action == 1:
            self.registerCoffeeTaste()
            return False
        elif action == 2:
            tasteList = self.SQL.testedMost()
            for item in tasteList:
                print(item)
            next = str(input("Trykk enter for å fortsette"))
            return False
        elif action == 3:
            mostValue = self.SQL.mostValue()
            for item in mostValue:
                print(item)
            next = str(input("Trykk enter for å fortsette"))
            return False
        elif action == 4:
            word = str(input("Hvilket ord ville beskrevet den?"))
            coffeeDescribedBy = self.SQL.describedBy(word)
            for item in coffeeDescribedBy:
                print(item )
            next = str(input("Trykk enter for å fortsette"))
            return False
        elif action == 5:
            print(self.SQL.testedMost())
            next = str(input("Trykk enter for å fortsette"))
            return False
        elif action == 0:
            return True
        else:
            print("Ugyldig handling, prøv igjen")
            next = str(input("Trykk enter for å fortsette"))
            return False
        


    #Last opp i databasen
    def registerCoffeeTaste(self):
        ok = False
        prøveIgjen = "Nei"
        while ok == False:
            brenneri = str(input("Brennerinavn"))
            kaffenavn = str(input("Kaffenavn"))
            poeng = int(input("Antall poeng (fra 1 til 10"))
            smaksnotat = str(input("Smaksnotat"))

            kaffestreng = str(self.SQL.checkCoffee(kaffenavn, brenneri)).strip().translate(str.maketrans("", "", ",[]()'"))
            if (kaffestreng == ''):
                prøveIgjen = str(input("Kaffen finnes ikke i vår database. Vil du prøve en annen kaffe? (Ja/Nei)"))
                if prøveIgjen == "Ja":
                    continue
                else:
                    break
            try:
                self.SQL.register(brenneri, kaffenavn, poeng, smaksnotat, self.user.getEmail())
            except sqlite3.Error as e:
                print(e)
                ok = False
                error = True
                prøveIgjen = str(input("Noe gikk feil. Vil du prøve igjen? (Ja/Nei)"))
                
            if (ok == False and prøveIgjen == "Nei"):
                        ok = True
            elif (prøveIgjen == "Ja"):
                    ok = False
            

    def hasTastedList(kaffe):
        return print(kaffe)

    def mostValueForMoney():
        return None

    def coffeesDescribedBy(adjective):
        return None

    def nonWashedCoffees():
        return None

teste = App()

teste.runApp()
#registerAction()

