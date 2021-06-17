#!/usr/bin/env python3
import socket
import pyDH
import pyAesCrypt as cripto
import hashlib

def main():
    host = socket.gethostname()
    port = 22333

    s = socket.socket()
    print("Mój adres: ", socket.gethostbyname(host))
    s.bind((host, port))
    s.listen()
    flag = True

    opti = int(input("Wybierz opcję szyfrowania: AES (wciśnij 1) lub 3DES (wciśnij 2) "))

    while True:

        clientsocket, adress = s.accept()
        data = clientsocket.recv(4096)

        while flag:
            print("Klucz publiczny Alice:", data.decode())

            d2 = pyDH.DiffieHellman()
            alicePubKey = int(data.decode())
            bobPubKey = d2.gen_public_key()

            msg = str(bobPubKey).encode()
            clientsocket.send(msg)
            bobSharedKey = d2.gen_shared_key(alicePubKey)
            print("Ustalony Sekret: ", bobSharedKey)
            flag = False

        data = clientsocket.recv(4096)
        if opti == 1:
            file = open("file_client.jpg.aes", "wb")
        elif opti == 2:
            file = open("file_client.jpg.3des", "wb")
        while data:
            file.write(data)
            data = clientsocket.recv(4096)
        file.close()
        clientsocket.close()
        s.close()
        break


    print("otrzymałem plik: file_client")

    opt = input("ten plik jest zaszyfrowany, chcesz go odszyfrować? (y/n): ")
    sekret = str(hashlib.sha256(str(bobSharedKey).encode()).digest())

    if opt == 'y' and opti == 1:
        buff = 64 * 1024
        cripto.decryptFile("file_client.jpg.aes", "file_client_aes.jpg", sekret, buff)
        print("odszyfrowany :)")

    elif opt =='y' and opti == 2:
        buff = 64 * 1024
        cripto.decryptFile("file_client.jpg.3des", "file_client_3des.jpg", sekret, buff)
        print("odszyfrowany :)")

    else:
        print("jeżeli nie chcesz to nic się nie stało, zostanie zaszyzfrowany")





if __name__ == "__main__":
    main()