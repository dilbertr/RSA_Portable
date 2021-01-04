import codecs
import sys
import os
import time
import crypto



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



#RSA
currentdir=os.path.dirname(os.path.abspath(__file__))
if len(sys.argv)==1:
	print("Usage: rsa [encrypt/decrypt] [path] [public key path (optional)]")
	exit()
if len(sys.argv)<3 and sys.argv[1] != "uninstall":
	print("Usage: rsa [encrypt/decrypt] [path] [public key path (optional)]")
	exit()
if sys.argv[1]=="uninstall":
	os.system(currentdir+"/uninstall.sh")
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
if len(sys.argv)==4: #if a 3rd argument is provided, which would be the path for a seperate public key
	publicpath=sys.argv[3]
source=sys.argv[2] #source file path
if source[0]!="/" and source[0]!="~" and source[0]!=".":
	source=os.getcwd()+"/"+source
if source[0]==".":
	source=os.getcwd()+source[1:]
operation=sys.argv[1] #encryption or decryption

#reading the public key
public=open(publicpath,"r").read()
public=public.split(",")
for i in [0,1]:
	public[i]=int(public[i])


if operation=="encrypt":
	#start a timer
	start=time.time()
	#add the extension to our destination file
	destination=source+".encrypt"
	#encode the file (this algorithm can only encrypt ASCII)

	#fine the path and filename, to move the decrypted file
	path=source.split("/")
	filename=path[-1]
	path.pop() #remove the filename
	path="/".join(path)

	os.system("uuencode "+source+" "+filename+" > "+source+".uue")
	crypto.encrypt_file(source+".uue",destination,public) #encrypt the encoded version
	os.system("rm "+source+".uue") #remove the encoded version
	os.system("echo "+"Time: "+str(time.time()-start)+" seconds")
if operation=="decrypt":
	if source[-8:]!=".encrypt":
		print("Aborted: wrong file extension")
		exit()
	destination=source[0:-8] #remove the .encrypt extension
	start=time.time()
	private=int(open(privatepath).read()) #read the private key
	crypto.decrypt_file(source,destination+".uue",public,private)

	#find the path and filename, to move the decrypted file
	path=destination.split("/")
	filename=path[-1]
	path.pop() #remove the filename
	path="/".join(path)

	os.system("sudo uudecode "+destination+".uue") #decode
	os.system("sudo mv "+filename+" "+path+" 2> /dev/null") #move the decrypted file
	os.system("chmod +w "+destination)
	os.system("sudo rm "+destination+".uue") #remove the coded file
	os.system("echo")
	print("Time: "+str(time.time()-start)+" seconds")
