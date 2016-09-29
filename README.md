# Entropy

A modular information display project

Installation
------------
Tested under ArchARM

```
yaourt -Sy python-yaml python-pyqt5
pip install pyowm pytz
git clone https://github.com/budb/Entropy.git
cd ./Entropy/
python main.py
```

Usage
-----
A configfile is required to initialize the program. P the file config.yml in the program folder.
The api key can be acquired from http://openweathermap.org/appid. The place id can also be found at http://openweathermap.org/.

Example
```YAML  
general:
  background: './wallpaper.jpg'
  frameless: 'True'
widgets:
    clock:
      class: DigClock
      background: '#CFD8DC'
      position: center
      color: '#222222'
    weather:
      class: Weather
      api_key: 123456789abcdefghijklmnopqrstuvw
      place_id: 2911298
      color: '#222222'
      background: '#CFD8DC'
      position: [400,400]
```    

Documentation
-------------

_optional_
[Default]

####General

background: \<path to wallpaper> or '#000000'
_frameless: 'True' [False]_

####Clock

class: DigClock 
_position: center_[0,0]
_background: 'transparent' or '#000000'_
_color: '#000000' <= hex color_

####Weather
class: Weather
api_key: 123456789abcdefghijklmnopqrstuvw
place_id: 2911298
_background: 'transparent' or '#000000' <= hex color_
_position: [400,400]_
_color: '#000000' <= hex color_