import codecs
import sys
import os
import time
import crypto
import binascii


#-------LEFTOVER SAGE CODE----------
#def all_primitive_roots(n):
#	roots=[]
#	g=primitive_root(n)
#	for i in range(n):
#			roots.append(g^i%n)
#	roots.sort()
#	return roots
#def dlog(g,h,n):
#	#uses baby step giant step algorithm
#	G=Integers(n)
#	BabySteps={}
#	for i in range(floor(sqrt(n))):
#		BabySteps[G(g^i)]=i
#	for i in range(n):
#		if G(h*g^(-i*floor(sqrt(n)))) in BabySteps.keys():
#			value=G(h*g^(-i*floor(sqrt(n))))
#			return G((BabySteps[value]+i*floor(sqrt(n))))
#-----------------------------------
user=sys.argv[1]
#RSA
currentdir=os.path.dirname(os.path.abspath(__file__))
if len(sys.argv)==2:
	print("Usage: rsa [encrypt/decrypt] [path] [public key path (optional)]")
	exit()
if len(sys.argv)<4 and sys.argv[2] != "uninstall":
	print("Usage: rsa [encrypt/decrypt] [path] [public key path (optional)]")
	exit()
if sys.argv[2]=="uninstall":
	os.system("bash "+currentdir+"/uninstall.sh")
	exit()
#usage is rsa [operation] [source] [public key (optional)]

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
if len(sys.argv)==5: #if a 3rd argument is provided, which would be the path for a seperate public key
	publicpath=sys.argv[5]
source=sys.argv[3] #source file path
if source[0]!="/" and source[0]!="~" and source[0]!=".":
	source=os.getcwd()+"/"+source
if source[0]==".":
	source=os.getcwd()+source[1:]
operation=sys.argv[2] #encryption or decryption

#reading the public key
public=open(publicpath,"r").read()
public=public.split(",")
for i in [0,1]:
	public[i]=int(public[i])


if operation=="encrypt":
	#add the extension to our destination file
	destination=source+".encrypt"
	password=input("Password: ")
	password=int(binascii.hexlify(password.encode()),16)
	#start a timer
	start=time.time()
	crypto.encrypt_file_counter(source,destination,password)
	os.system("echo "+"Time: "+str(time.time()-start)+" seconds")
	os.system("chown "+user+" "+destination)
	os.system("chmod 644 "+destination)
if operation=="decrypt":
	if source[-8:]!=".encrypt":
		print("Aborted: wrong file extension")
		exit()
	destination=source[0:-8] #remove the .encrypt extension
	private=int(open(privatepath).read()) #read the private key
	password=input("Password: ")
	password=int(binascii.hexlify(password.encode()),16)
	start=time.time()
	crypto.decrypt_file_counter(source,destination,password)
	os.system("chown "+user+" "+destination)
	os.system("chmod 644 "+destination)
	os.system("echo")
	print("Time: "+str(time.time()-start)+" seconds")
