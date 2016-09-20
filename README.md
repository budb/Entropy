# Entropy

###Preparations
###kudos to http://bendo.github.io/pi/
Scroll pHAT

sudo pip install cffi smbus-cffi scrollphat requests psutil i2c

in # /boot/config.txt add: 
dtparam=i2c_arm=on

in # /etc/modules-load.d/raspberrypi.conf add: 
i2c-dev
i2c-bcm2708

reboot

check if it works 
sudo i2cdetect -y 1

