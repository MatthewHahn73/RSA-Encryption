import random
import os.path
from math import gcd

def GenerateRandom(Min, Max):
    Rand = random.randint(Min, Max)
    while(Rand%2==0 and Rand%3==0 and Rand%5==0
          and Rand%7==0 and Rand%11==0):
        Rand = random.randint(Min, Max)
    return Rand

def GeneratePrimes(n = 100):
    Primes = set()
    for i in range(2,n+1):
        if i not in Primes:
            yield i
            Primes.update(range(i*i,n+1,i))
    return Primes

def GeneratePseudo(Primes, Min, Max):
    Cont = True
    PSet = list(Primes).copy()
    while(Cont):
        RNum = GenerateRandom(Min,Max)
        for x in PSet:
            if(not(pow(x,RNum-1,RNum) == 1)):
                break
            Cont = False
    return RNum

def Public_Key(P, Q):
    Cont = True
    N = P*Q
    PseudoN = ((P-1)*(Q-1))
    while(Cont):
        E = GeneratePseudo(GeneratePrimes(),500,1000)
        if(gcd(E,PseudoN) == 1):
            Cont = False
    PK = (E, N)
    return PK

def EGCD(A, M):
    if A == 0:
        return (M,0,1)
    G,Y,X = EGCD(M%A,A)
    return (G,(X-(M//A)*Y),Y)

def ModInv(E, M):
    G,X,Y = EGCD(E, M)
    if G != 1:
        raise Exception("No modular inverse")
    D = X%M
    return D

def Encrypt(Public, Message):
    e, n = Public
    Encrypted = ""
    for x in Message:
        Encrypted = Encrypted + str(pow(ord(x),e,n)) + " "
    return Encrypted

def Decrypt(Private, Message):
    d, n = Private
    Decrypted = ""
    String = ""
    Characters = list()
    for y in Message:
        if(y != ' '):
            String = String + str(y)
        else:
            Characters.append(String)
            String = ""
    for x in range(0,len(Characters)):
        Decrypted = Decrypted + chr(pow(int(Characters[x]),d,n))
    return Decrypted

def Encrypt_File(PUK, PIK, fileName):
    File = open(fileName, "r")
    Encryption_Data = File.readlines()
    File.close()
    File = open(fileName, "w")
    File.write(Encrypt(PUK, '********') + "\n")
    for x in range(0,len(Encryption_Data)):
        Encryption_Data[x] = Encrypt(PUK, Encryption_Data[x])
        File.write(Encryption_Data[x] + "\n")
    File.close()
    File = open("Files/Keys.txt", "w")
    File.write("Public Key: " + str(PUK) + "\n")
    File.write("Private key: " + str(PIK) + "\n")
    File.close()
    print('\tFile Encrypted Successfully')

def Decrypt_File(PIK, fileName):
    File = open(fileName, "r")
    Encryption_Data = File.readlines()
    File.close()
    if not Decrypt(PIK, Encryption_Data[0][:-2]) == '*******':
        print('\tError: Wrong key set')
    else:
        File = open(fileName, "w")
        for y in range(1,len(Encryption_Data)):
            Encryption_Data[y] = Decrypt(PIK, Encryption_Data[y][:-2])
            File.write(Encryption_Data[y] + "\n")
        File.close()
        print('\tDecryption Successful')

if __name__ == "__main__":
    print('RSA Encryption Algorithm [Version 1.0.2]\nWritten by Matthew Hahn\n')
    while True:
        UI = input(">>").split()
        if UI[0].upper() == 'EXIT':
           break
        if UI[0].upper() == 'ENCRYPT' or UI[0].upper() == 'DECRYPT':
            if len(UI) == 2 and UI[0].upper() == 'ENCRYPT':
                try:
                    myFile = open('Files/' + UI[1])
                    P = GeneratePseudo(GeneratePrimes(),0,10000)
                    Q = GeneratePseudo(GeneratePrimes(),0,10000)
                    PUK = Public_Key(P, Q)
                    E, N = PUK
                    D = ModInv(E, ((P-1)*(Q-1)))
                    PIK = D, N
                    myFile.close()
                    Encrypt_File(PUK, PIK, 'Files/' + UI[1])
                except FileNotFoundError:
                    print('\tError: "' + UI[1] + '" does not exist')
            elif len(UI) == 2 and UI[0].upper() == 'DECRYPT':
                try:
                    myFile = open('Files/' + UI[1])
                    var1, var2 = input("\tEnter Private Key ('D N'): ").split()
                    PIK = int(var1), int(var2)
                    myFile.close()
                    Decrypt_File(PIK, 'Files/' + UI[1])
                except FileNotFoundError:
                    print('\tError: "' + UI[1] + '" does not exist')
            elif len(UI) <= 1 or len(UI) >= 3:
                print('\tError: Invalid parameter input')
        else:
            print('\tUnknown Command: "' + UI[0] + '"')
