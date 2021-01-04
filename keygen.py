import crypto
import math
import random
import sys
import os
sure=input("This will make all previously encrypted files unreadable. Are you sure? (Y/n): ")
currentdir=os.path.dirname(os.path.abspath(__file__))
keypathspath=currentdir+"/keypaths.dat"
keypaths=open(keypathspath,"r").readlines()
for i in [1,2]:
	keypaths[i]=keypaths[i][0:-1] #get rid of the \n
publicpath=keypaths[1] #set the public path to the second line
privatepath=keypaths[2]
if keypaths[0]=="InCurrentDirectory:True\n":
	#reset public and private key paths to include the current directory
	publicpath=currentdir+"/"+keypaths[1]
	privatepath=currentdir+"/"+keypaths[2]

if sure=="Y" or sure=="y":
    p=crypto.next_prime((math.floor(random.random()*(2**256)))*2**256+math.floor(random.random()*(2**256)))
    q=crypto.next_prime((math.floor(random.random()*(2**256)))*2**256+math.floor(random.random()*(2**256)))
    public=open(publicpath,"w")
    private=open(privatepath,"w")
    public.write(str(p*q)+",65537")
    private.write(str(crypto.rsa_private_key_known(p,q,65537)))
    public.close()
    private.close()
else:
	print("Aborted.")