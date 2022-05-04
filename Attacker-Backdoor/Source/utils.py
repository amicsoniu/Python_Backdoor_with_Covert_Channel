######################################################################################################
#utils.py
#COMP 8505 - Assignment 3
#By: Alexandru Micsoniu
#Instructor: Aman Abdulla & D'Arcy Smith
#Nov 2, 2021
#Purpose: Using the Cryptodome module, encrypt and decrypt messages and ciphers respectfully
#Reference: https://pypi.org/project/pycrypto/
#######################################################################################################

from Crypto.Cipher import AES

key = b"H" * 32 # prefix each message with a ciphertext length of 32 bits
IV = b"H" * 16
BS = 16

pad   = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0: -ord(s[-1])] 

def encrypt(message):
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padded_message = pad(message)
    encrypted_message = encryptor.encrypt(padded_message)
    return encrypted_message

def decrypt(cipher):
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    decrypted_message = unpad(decrypted_padded_message)
    return decrypted_message
