class bruker:
    def __init__(self, email, fornavn, etternavn, passord):
        self.email = email
        self.fornavn = fornavn
        self.etternavn = etternavn
        self.passord = passord
    
    def getEmail(self):
        return self.email
    def getFornavn(self):
        return self.fornavn
    def getEtternavn(self):
        return self.etternavn
    def getPassord(self):
        return self.passord
