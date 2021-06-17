#!/usr/bin/env python3
import socket as s
import hashlib

def compare_strings_BOB(text):
    stringA = text[0]
    stringY = text[1]

    stringA2 = text[2]
    stringB = text[3]
    bitOfChoiceSent = text[4]

    if stringA == stringA2:
        hashBob = hashlib.sha256()
        hashBob.update(stringA + stringB + bitOfChoiceSent)
        stingYBob = hashBob.digest()

        if stingYBob == stringY:
            print("BIT b ALICE uznany: oba hashe są takie same! bit to: ", bitOfChoiceSent)

        else:
            print("hashe różne")
    else:
        print("różne stringiA")


def main():
    host = s.gethostname()
    port = 22222
    text = []

    print("Mój adres: ", s.gethostbyname(host))
    with s.socket(s.AF_INET, s.SOCK_STREAM) as serverSocket:
        serverSocket.bind((host, port))
        serverSocket.listen()
        connection, addresOfClient = serverSocket.accept()
        with connection:
            print("Polączony z : ", addresOfClient)
            while True:
                data = connection.recv(1024)
                print("Otwrzymane dane: ", data)
                text.append(data)
                if not data:
                    break

                connection.sendall(data)
            compare_strings_BOB(text)

if __name__ == "__main__":
    main()