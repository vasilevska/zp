import time
import hashlib
from tkinter import filedialog
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class PrivateKey:
    def __init__(self, name, mail, algorithm, size, password):
        self.timestamp = time.time()
        self.userID = name + "$" + mail
        self.algorithm = algorithm
        self.size = size
        self.keyID = None
        self.password = password
        self.privateRSAkey = None
        self.publicRSAkey = None
        self.rawPass = password
        if(algorithm == 0): self.genRSA()
        else: self.genDSAandElGamal()
    
    def getKeyID(self): return self.keyID

    def getData(self):
        if(self.algorithm == 0): tmp = "RSA" 
        else: tmp = "DSA + ELGamal"
        return [self.timestamp, self.keyID, self.userID, tmp, self.size]

    def genRSA(self):
        privateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.size,
            backend=default_backend(),
        )
        self.privateRSAkey = privateKey
        #.private_bytes(
        #    encoding=serialization.Encoding.PEM,
        #    format=serialization.PrivateFormat.PKCS8,
        #    encryption_algorithm=serialization.BestAvailableEncryption(self.password)
        #)

        self.privBytes = self.privateRSAkey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        self.publicRSAkey = privateKey.public_key()
        
        #.public_bytes(
        #    encoding=serialization.Encoding.PEM,
        #    format=serialization.PublicFormat.SubjectPublicKeyInfo
        #)

        self.password = hashlib.sha1(self.password)
        self.keyID = self.publicRSAkey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )[-41:-37].hex()

    def getPubKey(self):
        return self.publicRSAkey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def getPrivKey(self):
        return self.privBytes

    def genDSAandElGamal(self):
        pass

    
    def export(self):
        filename = filedialog.asksaveasfile(mode='wb', defaultextension=".pem")
        filename.write(self.publicRSAkey)
        #filename.write(self.privateRSAkey)
        filename.close()

    def sign(self, message):
        sig = self.privateRSAkey.sign(
            message, 
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA1()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA1
        )
        print(sig)
        print(message)
        return sig

    def decrypt(self):
        pass
