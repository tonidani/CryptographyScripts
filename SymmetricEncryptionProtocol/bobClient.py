#!/usr/bin/env python3
import socket
import pyDH
import pyAesCrypt as cripto
import hashlib

def main():
    d1 = pyDH.DiffieHellman()
    alicePubKey = d1.gen_public_key()


    host = input("Podaj ip servera: ")
    port = 22333

    server = socket.socket()
    server.connect((host, port))
    server.send(str(alicePubKey).encode())

    opti = int(input("Wybierz opcję szyfrowania: AES (wciśnij 1) lub 3DES (wciśnij 2) "))

    msg = server.recv(4096)
    bobPubKey = int(msg.decode("utf-8"))
    print("Klucz Publiczny Boba: ", bobPubKey)

    aliceSharedKey = d1.gen_shared_key(bobPubKey)

    print("Ustalony Sekret: ", aliceSharedKey)
    print("Szyfruje plik za pomocą sekretu...")


    buffer = 64*1024
    sekret = str(hashlib.sha256(str(aliceSharedKey).encode()).digest())

    if opti == 1:
        cripto.encryptFile("plik.jpg", "plik.jpg.aes", sekret, buffer)
        file1 = open("plik.jpg.aes", "rb")
    elif opti == 2:
        cripto.encryptFile("plik.jpg", "plik.jpg.3des", sekret, buffer)
        file1 = open("plik.jpg.3des", "rb")
    fileSize = file1.read(4096)


    print("Wysyłam zaszyfrowany plik")

    while fileSize:
        server.send(fileSize)
        fileSize = file1.read(4096)
    server.close()



if __name__ == "__main__":
    main()