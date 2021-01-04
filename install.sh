#!/bin/sh -
cd $(dirname $0)
pwd=`pwd`
basename=`basename $pwd`
chmod +x init.sh
chmod +x uninstall.sh
cd ..
sudo cp -r $pwd /usr/local/lib
sudo "/usr/local/lib/$basename/init.sh"
