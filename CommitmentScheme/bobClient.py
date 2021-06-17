#!/usr/bin/env python3
import socket as s
import hashlib
import random
1


def makeHash(stringA, stringB, bitOfChoice):

    hashObject = hashlib.sha256()
    hashObject.update(stringA + stringB + bitOfChoice)

    stringY = hashObject.digest()

    return stringY

def main():
    serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
    host = input("podaj ip serwera:\n")
    port = 22222
    serverSocket.connect((host, port))


    print("1szy krok: Podaj ciag a oraz ciag b")
    stringA = input("Podaj string A: ").encode()
    stringB = input("Podaj string B: ").encode()
    print("Wybieram bit randomowo (0 - 1) ")
    bitOfChoice = bytes(random.randint(0, 1))
    print(bitOfChoice.decode())

    stringY = bytes(makeHash(stringA, stringB, bitOfChoice))

    print("Wybralem: ", bitOfChoice.decode())
    print("Wysylam String A oraz Y")

    serverSocket.sendto(stringA, (host, port))
    data = serverSocket.recv(1024)
    print("Recived data: ", repr(data))

    serverSocket.sendto(stringY, (host, port))
    data = serverSocket.recv(1024)
    print("Recived data: ", repr(data))

    print("2gi krok: alice wysyła stringA, stringB oraz bit do  Boba")
    serverSocket.sendto(stringA, (host, port))
    data = serverSocket.recv(1024)
    print("Recived data: ", repr(data))

    serverSocket.sendto(stringB, (host, port))
    data = serverSocket.recv(1024)
    print("Recived data: ", repr(data))

    serverSocket.sendto(bitOfChoice, (host, port))


if __name__ == "__main__":
    main()




