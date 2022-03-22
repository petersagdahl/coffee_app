


from sqlalchemy import null


def registerAction():
    action = str(input("Hva vil du gjøre?"))
    
    if action == 'Registrer kaffe':
        brenneri = str(input("Brennerinavn"))
        kaffenavn = str(input("Kaffenavn"))
        poeng = int(input("Antall poeng (fra 1 til 10"))
        smaksnotat = str(input("Smaksnotat"))
        registerCoffee(brenneri, kaffenavn, poeng, smaksnotat)
        return "Supert!"
    else:
        return "Ikke en handling, prøv igjen"


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

