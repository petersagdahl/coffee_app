from Database.query import queries

print('Hei')

SQL =  queries('kaffeDB.db')

def runApp():
    done = False
    user = logIn()
    while done == False:
        done = registerAction(user)

   
def logIn():
    mode = str(input("Do you have a user?"))
    if mode == 'no':
        print('Register now...')
        email = str(input("Email:"))
        forname = str(input("Forname:"))
        surname = str(input("Surname:"))
        password = str(input("Passord:"))
        SQL.registerUser(email, forname, surname, password)
    elif mode == 'yes':
        print('Log in now...')
        email = str(input("Email:"))
        password = str(input("Passord:"))
        user = SQL.getUser(email, password)
        print(user)
        


def registerAction(user):
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
    action = int(input("What do you want to do?"))
    
    if action == 1:
        brenneri = str(input("Brennerinavn"))
        kaffenavn = str(input("Kaffenavn"))
        poeng = int(input("Antall poeng (fra 1 til 10"))
        smaksnotat = str(input("Smaksnotat"))
        registerCoffeeTaste(brenneri, kaffenavn, poeng, smaksnotat, user[0])
        return False
    elif action == 2:
        tasteList = SQL.testedMost()
        for item in tasteList:
            print(item)
        next = str(input("Enter to continiue"))
        return False
    elif action == 3:
        mostValue = SQL.mostValue()
        for item in mostValue:
            print(item)
        next = str(input("Enter to continiue"))
        return False
    elif action == 4:
        word = str(input("What word should it be described by?"))
        coffeeDescribedBy = SQL.describedBy(word)
        for item in coffeeDescribedBy:
            print(item)
        next = str(input("Enter to continiue"))
        return False
    elif action == 5:
        print(SQL.testedMost())
        next = str(input("Enter to continiue"))
        return False
    elif action == 0:
        return True
    else:
        print("Not an action, try again")
        next = str(input("Enter to continiue"))
        return False
    


#Last opp i databasen
def registerCoffeeTaste(brenneri, kaffenavn, poeng, smaksnotat, email):
    SQL.register(brenneri, kaffenavn, poeng, smaksnotat, email)
    return print(brenneri, kaffenavn, poeng, smaksnotat)

def hasTastedList(kaffe):
    return print(kaffe)

def mostValueForMoney():
    return None

def coffeesDescribedBy(adjective):
    return None

def nonWashedCoffees():
    return None

runApp()
#registerAction()

