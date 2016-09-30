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
      font_size: '22px'
    sign:
      class: Sign
      color: '#CFD8DC'
      background: 'transparent'
      position: [0,100]
      text: ['FREE','ALREADY DISTURBED','DO NOT DISTURB']
      font_size: '64px'
      button_size: '24px'
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
_color: '#000000'_

####Weather
class: Weather
api_key: 123456789abcdefghijklmnopqrstuvw
place_id: 2911298
_background: 'transparent' or '#000000'_
_position: [400,400]_
_color: '#000000'_
_font_size: '22px'_

####Sign
class: Sign
_background: 'transparent' or '#000000'_
_position: [400,400]_
_color: '#000000'_
_font_size: '22px'_
_text: ['']_
_font_size: '64px'_
_button_size: '24px_'