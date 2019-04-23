#!/bin/bash

VERSION="1.8.0"
PLATFORM="x86-64"
GREENGRASS_RELEASE_URL=https://d1onfpft10uf5o.cloudfront.net/greengrass-core/downloads/${VERSION}/greengrass-linux-${PLATFORM}-${VERSION}.tar.gz

# Setup
sudo adduser --system ggc_user
sudo groupadd --system ggc_group

# Install pre-reqs
sudo apt-get update
sudo apt-get install -y sqlite3 python2.7 binutils curl

# Download and unpack greengrass binaries
wget $GREENGRASS_RELEASE_URL
GREENGRASS_RELEASE=$(basename $GREENGRASS_RELEASE_URL)
sudo tar -xzf $GREENGRASS_RELEASE -C /
rm $GREENGRASS_RELEASE

# Install ML inference dependencies (MXNet)
sudo apt-get install -y python-pip python-dev gcc
sudo pip install mxnet
sudo apt-get install -y python-opencv

# Get root certificate
wget -O /vagrant/certs/root.ca.pem http://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem

# Copy certificates and configurations
sudo cp /vagrant/certs/* /greengrass/certs
sudo cp /vagrant/config/* /greengrass/config

# Create a source for images to map into the Lambda space later
sudo mkdir /images
sudo chown ggc_user:ggc_group /images

# Back up group.json - you'll thank me later
sudo cp /greengrass/ggc/deployment/group/group.json /greengrass/ggc/deployment/group/group.json.orig

cd /greengrass/ggc/core
sudo ./greengrassd start