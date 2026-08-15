#!/bin/sh
# I add these as functions to my .bashrc, .zshrc etc to help me upload
# files to my CircuitPython ESP32 web workflow devices. Update $CPYPASS 
# as needed
CPYPASS="passw0rd"
function cpyupload(){
  curl -v -u :${CPYPASS} -T $2 -L --location-trusted http://$1/fs/$2
}
function cpydownload(){
  curl -v -u :${CPYPASS} -L --location-trusted http://$1/fs/$2 -o $2
}
