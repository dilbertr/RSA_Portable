cd $(dirname $0)
pwd=`pwd`
echo -n 'Are you sure? (Y/n): '
read sure

if [ "$sure" != 'Y' ]
then
	echo 'Aborted'
	exit 0
fi
sudo rm /usr/local/bin/rsa
sudo rm -rf $pwd
