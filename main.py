import base64
import time
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Button, Radiobutton, Checkbutton
import zlib
from privateKey import PrivateKey
import system
from keyDisplay import KeyDisplay
from cryptography.hazmat.primitives.asymmetric import dsa, rsa

def generateKeys():
    genKeys = Toplevel()
    genKeys.title("Generisanje kljuceva")

    Label(genKeys, text="Ime").grid(row=0, column=0)
    
    Entry(genKeys, textvariable=name, width=30).grid(row=0, column=1)

    Label(genKeys, text="Mejl").grid(row=1, column=0)
    
    Entry(genKeys, textvariable=mail, width=30).grid(row=1, column=1)

    
    Label(genKeys, text="Algoritam").grid(row=2)
    Radiobutton(genKeys, text="RSA", variable=algorithm, value=0).grid(row=3, column=0)
    Radiobutton(genKeys, text="DSA + ElGamal", variable=algorithm, value=1).grid(row=3, column=1)
    
    
    Label(genKeys, text="Velicina").grid(row=4)
    Radiobutton(genKeys, text="1024", variable=size, value=1024).grid(row=5, column=0)
    Radiobutton(genKeys, text="2048", variable=size, value=2048).grid(row=5, column=1)

    Label(genKeys, text="Password", height=3).grid(row=6, column=0)
    
    Entry(genKeys, textvariable=password, width=30,  show='*').grid(row=6, column=1)

    thisbutton = Button(genKeys, text='Generisi', width=25)
    thisbutton.config(command=lambda b=thisbutton: b.config(state="disabled") or system.privateKeyRing.add(PrivateKey(name.get(), mail.get(), algorithm.get(), size.get(), bytes(password.get(), 'utf-8'))) or displayPriv.showKeys() or genKeys.destroy())
    thisbutton.grid(row=7, column=0, columnspan=2)
    
    genKeys.mainloop()

def sendMessage():
    sendMsg = Toplevel()
    sendMsg.title("Slanje poruke")
    Label(sendMsg, text="Opcije").pack()
    Checkbutton(sendMsg, text="tajnost", variable=isSecret, onvalue=1, offvalue=0, command=pickEnc).pack()
    Checkbutton(sendMsg, text="autenticnost", variable=isSigned, onvalue=1, offvalue=0, command=pickSign).pack()
    Checkbutton(sendMsg, text="kompresija", variable=isCompressed, onvalue=1, offvalue=0).pack()
    Checkbutton(sendMsg, text="radix64", variable=isConverted, onvalue=1, offvalue=0).pack()
    Entry(sendMsg, textvariable=subject, width=30).pack()
    txt = Text(sendMsg, height = 5, width = 52)
    txt.pack()
    Button(sendMsg, text="Posalji", width=25, command=lambda: message.set(txt.get("1.0",'end-1c')) or send()).pack(pady=(20,0))
    sendMsg.mainloop()

def pickSign():
    if(isSigned.get()):
        auth = Toplevel()
        auth.title("Izabrati kljuc za autentifikaciju")
        display = KeyDisplay(auth)
        display.pack()
        display.showKeys(True)
       
        Button(auth, text="Potvrdi", command=auth.destroy).pack()

        auth.mainloop()

def pickEnc():
    if(isSecret.get()):
        enc = Toplevel()
        enc.title("")
        Label(enc, text="Algoritam").pack()
        Radiobutton(enc, text="alg0", variable=autAlg, value=0).pack()
        Radiobutton(enc, text="alg1", variable=autAlg, value=1).pack()

def send():
    block = []
    messageBlock = []
    messageBlock.append(subject.get())
    messageBlock.append(str(time.time()))
    messageBlock.append(message.get())
    msgcontent = '/n'.join(messageBlock)
    block.append(msgcontent)
    if(isSigned.get()):
        signature = system.privateKeyRing.keys[system.autKey.get()].sign(block[0])
        block.insert(0, signature)
        msgcontent = '/n'.join(block)
        block = []
        block.append(msgcontent)
        pass
    if(isCompressed.get()):
        block[0] = zlib.compress(block[0].encode('utf-8'))
    if(isSecret.get()):
        pass
    if(isConverted.get()):
        msg = '\n'.join(block)
        block = []
        block.append(base64.b64encode(msg))
    msgcontent = '\n'.join(block)
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    filename.write(msgcontent)
    filename.close()
    
    
    
    

mainwin = Tk()
mainwin.geometry("1200x600")
mainwin.configure(bg="white")
mainwin.title('ZP projekat')
displayPriv = KeyDisplay(mainwin)
displayPriv.pack(pady=(50, 50))
displayPriv.showKeys()
Button(mainwin, text='Generisanje kljuceva', width=25, command=generateKeys).pack()
Button(mainwin, text='Uvezi privatni kljuc', width=25, command=system.privateKeyRing.importk).pack()

display = KeyDisplay(mainwin, False)
display.pack(pady=(50, 50))
display.showKeys()
Button(mainwin, text='Uvezi javni kljuc', width=25, command=system.publicKeyRing.importk).pack(pady=(0, 100))
Button(mainwin, text='Posalji poruku', width=25, command=sendMessage).pack()
Button(mainwin, text='Primi poruku', width=25).pack()

name=StringVar(None)
mail=StringVar(None)
algorithm=IntVar(0)
size=IntVar(0)
size.set(1024)
password=StringVar(None)
isSecret=IntVar(0)
isCompressed=IntVar(0)
isSigned=IntVar(0)
isConverted=IntVar(0)
autAlg = IntVar(0)
system.autKey = StringVar(None)
system.signKey = StringVar(None)
message = StringVar(None)
subject = StringVar(None)

mainwin.mainloop()

