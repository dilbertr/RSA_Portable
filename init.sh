cd $(dirname $0)
pwd=`pwd`
echo Creating executable...
touch 'rsa'
echo 'sudo python3.8 '$pwd'/rsa.py $1 $2 $3' >> ./rsa
echo Changing permissions to make file 'rsa' executable...
chmod +x rsa
echo Creating a link to file 'rsa' in '/usr/local/bin'...
ln -s $pwd/rsa /usr/local/bin/rsa
echo Creating 'keypaths.dat'
touch $pwd/keypaths.dat
echo 'InCurrentDirectory:True'>>$pwd/keypaths.dat
echo 'public.txt'>>$pwd/keypaths.dat
echo 'private.txt'>>$pwd/keypaths.dat
echo Creating keys...
python3.8 keygen.py
echo Install complete. Do not move any files in this directory.
rm $pwd/install.sh
rm $pwd/init.sh
