import hashlib
from tkinter import *
from system import privateKeyRing
from system import publicKeyRing
from system import autKey

class KeyDisplay(LabelFrame):
    def __init__(self, m, p = True):
        LabelFrame.__init__(self, m)
        if p: self.keyRing = privateKeyRing
        else: self.keyRing = publicKeyRing
    
    def showKeys(self, radio=False):
        for widget in self.winfo_children():
            widget.destroy()
        
        keyRing = self.keyRing
        labels = keyRing.getLabels()
        if(radio): labels[:-3]

        for i,l in enumerate(labels):
            Label(self, text=l, anchor="w").grid(row=0, column=i, sticky="ew")
        
        keys = keyRing.getAllKeys()

        for i,l in enumerate(keys):
            for j, k in enumerate(l.getData()):
                Label(self, text=k, anchor="w").grid(row=i+1, column=j, sticky="ew")
            if(radio):
                Radiobutton(self, variable=autKey, value=str(i)).grid(row=i+1, column=j+1, sticky="ew")
            else:
                Button(self, text='x', width=2, bg="red", fg="white", command= lambda i=i: keyRing.remove(keys[i].getKeyID()) or self.showKeys()).grid(row=i+1, column=j+1, sticky="ew")
                Button(self, text='->', width=2, bg="blue", fg="white", command= lambda i=i: keyRing.export(keys[i].getKeyID())).grid(row=i+1, column=j+2, sticky="ew")
                Button(self, text='o', width=2, bg="green", fg="white", command= lambda i=i: displayKey(keys[i].getKeyID(), 1)).grid(row=i+1, column=j+3, sticky="ew")

def displayKey(keyId, isPrivate):
    dispKey = Toplevel()
    dispKey.title("Prikaz kljuca sa IDem: " + keyId)
    dispKey.geometry("600x500")
    Label(dispKey, text=privateKeyRing.keys[keyId].getPubKey()).pack()
    if(isPrivate):
        enterPass = Toplevel()
        enterPass.title("uneti password kljuca")
        enterPass.geometry("300x150")
        enterPass.attributes("-topmost", True)
        password = Entry(enterPass, width=30,  show='*')
        password.pack()
        error = StringVar(enterPass)
        Button(enterPass, text='Potvrdi', width=15, bg="white", command=lambda:checkPass(password, keyId, enterPass, dispKey, error)).pack()
        Label(enterPass, textvariable=error).pack()
        enterPass.mainloop()
    else:
        #Label(dispKey, text=privateKeyRing.keys[keyId].getPrivKey()).pack()
        dispKey.mainloop()

def checkPass(password, keyId, enterPass, dispKey, error):
    if(privateKeyRing.keys[keyId].password.digest() == hashlib.sha1(bytes(password.get(), 'utf-8')).digest()):
        enterPass.destroy() 
        Label(dispKey, text=privateKeyRing.keys[keyId].getPrivKey()).pack()
        dispKey.lift()
        dispKey.mainloop()
    else:
        error.set("pogresan password")