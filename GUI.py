


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
    else:
        return "Not an action, try again"


def registerCoffee(brenneri, kaffenavn, poeng, smaksnotat):
    return brenneri, kaffenavn, poeng, smaksnotat

def hasTastedList():
    return null

def mostValueForMoney():
    return null

def coffeesDescribedBy(adjective):
    return null

def nonWashedCoffees():
    return null


registerAction()

