#!/usr/bin/python

import sys
import string
import hashlib
import os
import random
import struct
import getpass
import datetime
import json
import requests #pip install requests
import traceback
import subprocess
from datetime import timedelta
from Crypto.Cipher import AES
from pybitcoin import BitcoinPrivateKey
from OpenSSL import crypto, SSL
from ecdsa import SigningKey
#For pybitcoin download and install from:
#https://github.com/blockstack/pybitcoin.git

art = r'''

  ____  _            _           _____ _____ _
 |  _ \| |          | |         / ____/ ____| |Smart
 | |_) | | ___   ___| | _______| (___| (___ | |Contract
 |  _ <| |/ _ \ / __| |/ /______\___ \\___ \| |Client script
 | |_) | | (_) | (__|   <       ____) |___) | |v0.1
 |____/|_|\___/ \___|_|\_\     |_____/_____/|______|

 Block-SSL - SSL/TLS Certificate Authority Replacement
        through the Ethereum Smart Contracts

 Thesis Project - Aristotle University of Thessaloniki

                    By Cr0wTom

 ------------------------------------------------------

'''

def clientscript():
    # create a key pair
    print "Creating a new key pair:"
    print "Warning: This is a pseudo-random generation.\n"
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    priv = raw_input("Which is your private key? (in hexadecimal format)\n")  #Private Key of the owner
    priv = BitcoinPrivateKey(priv)
    pub = priv.get_verifying_key()
    pub = pub.to_string()
    keccak.update(pub)
    address = keccak.hexdigest()[24:]
    open("Address.txt", "w").write(address)
    # create a self-signed cert
    cert = crypto.X509()
    createCert(k, cert)

    open("certificate.crt", "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open("keys.key", "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    print "\nCertificate created in file: certificate.crt"
    print "\nKeys saved in file: keys.key\n"
    #Hashing of the certificate
    f = open("certificate.crt", "rb") #read file in binary mode
    fr = f.read()
    cert_hash = hashlib.sha256() #use the SHA256 hashing algorithm
    cert_hash.update(fr)
    data = cert_hash.hexdigest()
    print "\nYour Certificate hash is: ", data
    subprocess.Popen(["geth"])
    os.system("BZZKEY=" + address)
    subprocess.Popen(["$GOPATH/bin/swarm --bzzaccount $BZZKEY"])
    os.system("curl -H \"Content-Type: text/plain\" --data-binary \"some-data\" http://localhost:8500/bzz:/") #todo: find swarm gateways
    #todo: print Certificate expiration date
    #todo: print the expiration date and the days that left
    print "Please open the BlockSSL Smart Contract and paste this info in the required fields."

    sys.exit()

def createCert(k, cert):
    # create a self-signed cert
    country = raw_input("Country Name (2 letter code): ")
    cert.get_subject().C = country
    state = raw_input("State or Province Name (full name): ")
    cert.get_subject().ST = state
    local = raw_input("Locality Name (eg, city): ")
    cert.get_subject().L = local
    org = raw_input("Organization Name (eg, company): ")
    cert.get_subject().O = org
    orgu = raw_input("Organizational Unit Name (eg, section): ")
    cert.get_subject().OU = orgu
    cn = raw_input("Common Name (eg, fully qualified host name): ")
    cert.get_subject().CN = cn
    email = raw_input("email Address: ")
    cert.get_subject().emailAddress = email
    cert.set_serial_number(1000) #Actual serial number added in the contract
    cert.gmtime_adj_notBefore(0)
    now = datetime.datetime.now() #setting the time right now
    tr = 0
    while tr == 0:
        an = int(raw_input("For how long do you need to update the certificate in days? (maximum: 365)\n"))
        if an < 366 and an > 0:
            cert.gmtime_adj_notAfter(60*60*24*an)
            tr += 1
        else:
            print "Please give a number smaller than 366.\n"
            tr = 0
    diff = datetime.timedelta(an)
    future = now + diff
    print future.strftime("\nYour certificate expires on %m/%d/%Y") #print the expiration date
    print "\nAdding the GE and RV signatures to the issuer field..."
    message_gen = open("Address.txt", "rb").read()
    message_gen = message_gen.strip('\n')
    m1 = hashlib.sha256()
    m1.update(message_gen)
    m1 = m1.hexdigest()
    cert.get_issuer().CN = m1 #Ethereum address at the CN issuer field
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    return cert

def checkforSwarn():
        name = "$GOPATH/bin/swarm"
        try: #check if swarn exists
            devnull = open(os.devnull)
            subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
            print "\tSwarn exists.\n"
        except OSError as e: #install swarn - os specific
                if e.errno == os.errno.ENOENT:
                    if sys.platform == "linux" or sys.platform == "linux2":
                        print "Installing Swarn: \n"
                        os.system("sudo apt install golang git")
                        os.system("mkdir ~/go")
                        os.system("export GOPATH=\"$HOME/go\"")
                        os.system("echo \'export GOPATH=\"$HOME/go\"\' >> ~/.profile")
                        os.system("mkdir -p $GOPATH/src/github.com/ethereum | cd $GOPATH/src/github.com/ethereum | git clone https://github.com/ethereum/go-ethereum | cd go-ethereum | git checkout master | go get github.com/ethereum/go-ethereum")
                        os.system("go install -v ./cmd/geth")
                        os.system("go install -v ./cmd/swarm")
                        os.system("$GOPATH/bin/swarm version")
                    elif sys.platform == "win32": #all Windows versions
                        print "Swarn is not supported on Windows, please use Linux or Mac.\n"
                    elif sys.platform == "darwin": #all OSX versions
                        print "Installing Swarn: \n"
                        os.system("brew install go git")
                        os.system("mkdir ~/go")
                        os.system("export GOPATH=\"$HOME/go\"")
                        os.system("echo \'export GOPATH=\"$HOME/go\"\' >> ~/.profile")
                        os.system("mkdir -p $GOPATH/src/github.com/ethereum | cd $GOPATH/src/github.com/ethereum | git clone https://github.com/ethereum/go-ethereum | cd go-ethereum | git checkout master | go get github.com/ethereum/go-ethereum")
                        os.system("go install -v ./cmd/geth")
                        os.system("go install -v ./cmd/swarm")
                        os.system("$GOPATH/bin/swarm version")


def main(argu):
    try:
        if argu[1] == "--help" or argu[1] == "-h":
            #Option to helo with the usage of the script
            print art
            print "Usage: \"client_script.py -c\""
            print "\n"
        elif argu[1] == "-c":
            print art
            clientscript()
    except IndexError:
        print art
        print "Usage: \"client_script.py -c\""
        print "\nFor help use the --help or -h option."
        print "\n"



if __name__ == "__main__":
    main(sys.argv)
