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
	m=open(source,"rb") #message
	c=open(destination,"wb") #ciphertext
	block=''
	encrypted_block=''
	blocklength=32 #arbitrary, bigger blocklength = smaller file size
	written_block="" #block written to ciphertext
	while True:
		block=""
		block = m.read(blocklength)
		if block==b'':
			break
		encrypted_block=""
		block=binascii.hexlify(block)
		block=int(block,16)
		encrypted_block=hex(rsa_encrypt(key,block)) #encode as hex
		encrypted_block=encrypted_block[2:]
		for i in range(7):
			if len(encrypted_block)%256!=0:
				encrypted_block="0"+encrypted_block
		written_block=binascii.unhexlify(encrypted_block)
		#written_block="\n"
		#written_block=written_block+encrypted_block
		c.write(written_block)
	c.close()
	m.close()
def decrypt_file(source,destination,public,private):
	c=open(source,"rb") #ciphertext
	chars=len(c.read())
	charscompleted=0
	c=open(source,"rb")
	m=open(destination,"wb") #message
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
		charscompleted = charscompleted + 128
		percentage=math.floor(100*charscompleted/chars)
		os.system("echo -n -e \'\\rProgress: "+str(percentage)+"%\\r'")
		if block=="":
			break
		block=binascii.hexlify(block)
		print(block)
		decrypted_block=str(hex(rsa_decrypt(public,private,int(block,16))))[2:]
		if len(decrypted_block)%2 != 0:
			decrypted_block="0"+str(decrypted_block)
		decrypted_block=binascii.unhexlify(decrypted_block)
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

def keygen():
	p=next_prime((math.floor(random.random()*(2**256)))*2**256+math.floor(random.random()*(2**256)))
	q=next_prime((math.floor(random.random()*(2**256)))*2**256+math.floor(random.random()*(2**256)))
	public=str(p*q)+",65537"
	private=str(rsa_private_key_known(p,q,65537))
	return [public,private]
def encrypt_file_counter(source,destination,counter):
	blocknum=0
	counterblock=""
	m=open(source,"rb") #message
	c=open(destination,"wb") #ciphertext
	block=''
	encrypted_block=''
	blocklength=32 #arbitrary, bigger blocklength = smaller file size
	written_block="" #block written to ciphertext
	lastblock=""
	block_unmodified=""
	print("Generating RSA key...")
	keys=keygen()
	public=keys[0]
	c.write(public.encode()+b"\n")
	public=public.split(',')
	for i in [0,1]:
		public[i]=int(public[i])
	print("Starting encryption...")
	while True:
		block=""
		block = m.read(blocklength)
		block_unmodified=block
		if block==b'':
			c.write(str(len(lastblock)).encode())
			break
		encrypted_block=""
		block=binascii.hexlify(block)
		block=int(block,16)
		counter_block=counter+blocknum
		counter_block=rsa_encrypt(public,counter_block)%(2**256)
		encrypted_block=hex(counter_block^block)[2:]
		while True:
			if len(encrypted_block)%64!=0:
				encrypted_block="0"+encrypted_block
			else:
				break
		written_block=binascii.unhexlify(encrypted_block)
		#written_block="\n"
		#written_block=written_block+encrypted_block
		c.write(written_block)
		blocknum=blocknum+1
		lastblock=block_unmodified
	c.close()
	m.close()
def decrypt_file_counter(source,destination,counter):
	
	blocknum = 0
	done = False
	counterblock = ""
	m = open(source,"rb") #message
	c = open(destination,"wb") #ciphertext

	public=str(m.readlines(1)[0])[2:-3].split(',')
	for i in [0,1]:
		public[i]=int(public[i])
	block = ''
	encrypted_block = ''
	blocklength = 32 #arbitrary, bigger blocklength = smaller file size
	written_block = "" #block written to ciphertext
	lastblock = ""
	oneahead = m.read(blocklength)
	twoahead = m.read(blocklength)
	while True:
		block = ""
		block = oneahead
		oneahead = twoahead
		twoahead = m.read(blocklength)
		if twoahead==b'':
			done = True
			oneahead = int(oneahead)
		encrypted_block=""
		block=binascii.hexlify(block)
		block=int(block,16)
		counter_block=counter+blocknum
		counter_block=rsa_encrypt(public,counter_block)%(2**256)
		encrypted_block=hex(counter_block^block)[2:]
		if not done:
			while True:
				if len(encrypted_block)%64!=0:
					encrypted_block="0"+encrypted_block
				else:
					break
		else:
			while True:
				if len(encrypted_block)%oneahead!=0:
					encrypted_block="0"+encrypted_block
				else:
					break
		written_block=binascii.unhexlify(encrypted_block)
		#written_block="\n"
		#written_block=written_block+encrypted_block
		c.write(written_block)
		blocknum=blocknum+1
		if done:
			break
	c.close()
	m.close()





