#!/bin/sh

python gentooconfig.py

# cleanup previous files
rm -r install
rm install.tar.gz

mkdir install

cp install.sh install/
cp chroot.sh install/
cp make.conf install/
cp disks.sfdisk install/
cp fstab.txt install/

dos2unix install/install.sh
dos2unix install/chroot.sh
dos2unix install/make.conf
dos2unix install/disks.sfdisk
dos2unix install/fstab.txt

tar czfv install.tar.gz  install/*
