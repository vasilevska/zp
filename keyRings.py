from time import sleep
from tkinter import filedialog

class KeyRing:
    def __init__(self):
        self.keys = {}

    def getAllKeys(self):
        return list(self.keys.values())

    def getLabels(self):
        return ["KeyID"]

    def add(self, key):
        self.keys[key.getKeyID()] = key
    
    def remove(self, keyID):
        self.keys.pop(keyID)
    
    def export(self, keyID):
        return self.keys[keyID].export()

    def importk(self):
        filename = filedialog.askopenfilename()
        arr = []
        with open(filename, 'r') as f:
            arr = f.readlines()
        print(arr)
        pukar = []
        pikar = []
        fleg = False
        for a in arr:
            if(a[:6] == "-----B"): continue
            if not fleg:
                if(a[:8] != "-----END"): pukar.append(a[:-1])
                else: fleg = True
            else:
                if(a[:8] != "-----END"): pikar.append(a[:-1])
        pubk = ''.join(pukar)
        privk = ''.join(pikar)
        print(pubk)
        print(privk)
        return [bytes(pubk.encode()), bytes(privk.encode())]

class PrivateKeyRing(KeyRing):
    def __init__(self):
        KeyRing.__init__(self)

    def getLabels(self):
        return ["Time", "KeyID", "UserID", "Algorithm", "Size", "Delete", "Export", "Display"]
    
    def importk(self):
        keys = super().importk()


class PublicKeyRing(KeyRing):
    def __init__(self):
        KeyRing.__init__(self)
    def getLabels(self):
        return ["Time", "KeyID", "UserID", "Algorithm", "Size","Delete", "Export", "Display"]

    def importk(self):
        keys = super().importk()
