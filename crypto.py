import time
import sys
import codecs
import os
import math
import random
import binascii

def rsa_private_key_known(p,q,e):
	#G=Integers((p-1)*(q-1))
	#return G(e^(-1))
	return pow(e,-1,(p-1)*(q-1))
def rsa_public_key(p,q,e):
	return [p*q,e]
def rsa_encrypt(key,m):
	#return m^key[1]%key[0]
	return pow(m,key[1],key[0])
def rsa_decrypt(public,private,c):
	return pow(c,private,public[0])
def encode(s): #integer to unicode
	hecks=s.encode().hex()
	return int(hecks,16)
def decode(n): #unicode to integer
	hecks=hex(n) #couldn't use the name hex
	hecks=hecks[2:]
	for i in range(8):
		if len(hecks)%8 != 0:
			hecks=str("0")+str(hecks)
	raw=bytes.fromhex(hecks)
	return raw.decode()
def encrypt_file(source,destination,key):
	m=codecs.open(source,"r",encoding="utf-8",errors="ignore") #message
	c=open(destination,"w") #ciphertext
	block=''
	encrypted_block=''
	blocklength=32 #arbitrary, bigger blocklength = smaller file size
	written_block="" #block written to ciphertext
	while True:
		block=""
		block = m.read(blocklength)
		if block=="":
			break
		encrypted_block=""
		encrypted_block=hex(rsa_encrypt(key,encode(block))) #encode as hex
		encrypted_block=encrypted_block[2:]
		for i in range(7):
			if len(encrypted_block)%256!=0:
				encrypted_block="0"+encrypted_block
		#written_block="\n"
		#written_block=written_block+encrypted_block
		c.write(encrypted_block)
	c.close()
	m.close()
def decrypt_file(source,destination,public,private):
	c=codecs.open(source,"r",errors="ignore") #ciphertext
	chars=len(c.read())
	charscompleted=0
	c=codecs.open(source,"r",errors="ignore")
	m=open(destination,"w") #message
	block=''
	char='' #current character
	decrypted_block=""
	done=False #have all characters been read
	while True:
		block=""
		#while True:
		#	char=c.read(1)
		#	if char=="\n":
		#		break #block is complete
		#	if char=="":
		#		done=True #file is complete
		#		break
		#	block = block + char
		#if block != "": #encrypted file starts with \n, so the 1st block is empty
		block=c.read(256)
		charscompleted = charscompleted + 256
		percentage=math.floor(100*charscompleted/chars)
		os.system("echo -n -e \'\\rProgress: "+str(percentage)+"%\\r'")
		if block=="":
			break
		decrypted_block=decode(rsa_decrypt(public,private,int(block,16)))
		m.write(decrypted_block)

	m.close()
	c.close()
def miller_rabin(n, k):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
def next_prime(n):
    i=n
    while True:
        if miller_rabin(i,40):
            return i
        i=i+1