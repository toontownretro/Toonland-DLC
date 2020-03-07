# Filename: HackerCrypt.py
# Created by: Cody (August 10th, 2013)
##################################
#
# VERSION : V1.3.0.4
#
# This is the Python implementation of HackerCrypt. It should
# be used for the decompilation and execution of any of your
# main (system) files.
#
##################################

import random
import base64

class HackerCrypt:

    def __init__(self):
        self._magic = ''
        self._key = ''

    ##################################
    #     Function: setMagic
    #  Description: Sets the "magic" used in the cipher process.
    ##################################
    def setMagic(self, value):
        self._magic = value

    ##################################
    #     Function: setKey
    #  Description: Sets the "key" used in the cipher process.
    ##################################
    def setKey(self, value):
        self._key = value

    ##################################
    #     Function: makeIV
    #  Description: Generates and returns a random 4-byte IV that will
    #               be appended to the KEY.
    ##################################
    def makeIV(self):
        iv = ''
        for i in range(4):
            iv += chr(random.randrange(256))
        return iv

    ##################################
    #     Function: encode
    #  Description: Base64-encodes the data provided.
    ##################################
    def encode(self, data):
        return base64.b64encode(data)

    ##################################
    #     Function: decode
    #  Description: Reverses the process of encode on the encoding
    #               that is provided.
    ##################################
    def decode(self, encoding):
        return base64.b64decode(encoding)

    ##################################
    #     Function: encrypt
    #  Description: The actual cipher function.
    ##################################
    def encrypt(self, plainText):
        plainText = self._magic + self.encode(plainText)
        iv = self.makeIV()
        key = self._key + iv
        cipherText = ''
        iKey = 0
        for i in range(len(plainText)):
            iKey %= len(key)
            cipherText += chr(((ord(plainText[i]) ^ ord(key[iKey])) + (ord(key[iKey]) + 5)) % 256)
            iKey += 1
        return (iv + cipherText)

    ##################################
    #     Function: decrypt
    #  Description: Reverses the cipher process.
    ##################################
    def decrypt(self, cipherText):
        cipherTextLen = len(cipherText)
        if cipherTextLen < 4:
            return ''
        iv = cipherText[:4]
        remainingBytes = cipherText[4:]
        key = self._key + iv
        plainText = ''
        iKey = 0
        for i in range(len(remainingBytes)):
            iKey %= len(key)
            plainText += chr(((ord(remainingBytes[i]) - (ord(key[iKey]) + 5)) ^ ord(key[iKey])) % 256)
            iKey += 1
        magic = plainText[:len(self._magic)]
        if magic != self._magic:
            return ''
        return self.decode(plainText[len(self._magic):])