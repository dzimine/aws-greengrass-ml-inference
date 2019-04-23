#!/bin/bash
#
# Run this script inside Vagrant VM, as SUDO, from /vagrant/scripts directory.
# It will be feeding images for GreengrassImageClassification Lambda.

files=(../images/*.jpg)

RANDOM=$$$(date +%s)

while [[ 1 ]]; do
    f=${files[$RANDOM % ${#files[@]}]}
    echo "Placing $(basename $f)..."
    d=/images/$(basename $f)
    cp $f $d
    mv "$d" "${d%.jpg}.jpeg"
    sleep 5
done