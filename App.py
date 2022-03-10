


from sqlalchemy import null


def registerAction():
    action = str(input("What do you want to do?"))
    
    if action == 'registrer kaffe':
        brenneri = str(input("Brennerinavn"))
        kaffenavn = str(input("Kaffenavn"))
        poeng = int(input("Antall poeng (fra 1 til 10"))
        smaksnotat = str(input("Smaksnotat"))
        registerCoffee(brenneri, kaffenavn, poeng, smaksnotat)
        return "Cool"
    elif action == 'hvem har smakt kaffe':
        kaffe  = str(input("Hvilken kaffe spør du etter?"))
        hasTastedList(kaffe)
    else:
        return "Not an action, try again"


#Last opp i databasen
def registerCoffee(brenneri, kaffenavn, poeng, smaksnotat):
    return print(brenneri, kaffenavn, poeng, smaksnotat)

def hasTastedList(kaffe):
    return print(kaffe)

def mostValueForMoney():
    return null

def coffeesDescribedBy(adjective):
    return null

def nonWashedCoffees():
    return null


registerAction()

