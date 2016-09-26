# Entropy

A modular information display project

Installation
------------
Tested under ArchARM

```
yaourt -Sy python-yaml python-pyqt5
pip install pyowm
git clone https://github.com/budb/Entropy.git
cd ./Entropy/
python main.py
```

Usage
-----
A configfile is required to initialize the program. P the file config.yml in the program folder.
The api key can be acquired from http://openweathermap.org/appid

Example
```YAML  
general:
  background: './wallpaper.jpg'
widgets:
    clock:
      class: DigClock
      transparency: 'True'
    weather:
      class: Weather
      api_key: 123456789abcdefghijklmnopqrstuvw
      place_id: 2911298
      transparency: 'True'
```    