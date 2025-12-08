#!/bin/bash

brew update
brew install python nmap arp-scan

mkdir -p /opt/scanner
cp -r /vagrant/scanner/* /opt/scanner/
pip3 install -r /opt/scanner/requirements.txt
