import time
from tkinter import filedialog

class PublicKey:
    def __init__(self, key, userid, algorithm):
        self.timestamp = time.time()
        self.algorithm = algorithm
        self.keyID = key[-41:-37].hex()
        self.publicRSAkey = key
        self.userID = userid

    def getKeyID(self): return self.keyID

    def getData(self):
        if(self.algorithm == 0): tmp = "RSA" 
        else: tmp = "DSA + ELGamal"
        return [self.timestamp, self.keyID, self.userID, tmp, self.size]
    
    def export(self):
        filename = filedialog.asksaveasfile(mode='wb', defaultextension=".pem")
        filename.write(self.publicRSAkey)
        #filename.write(self.privateRSAkey)
        filename.close()
