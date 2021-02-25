# LED-bridge-lamp

**🚧 Project is still in a very early stage with further development imminent! 🚧**

A project aimed at creating a firmware for controlling a LED bridge lamp with a pair of ARGB LED stripes, controlled with an ESP32 or similar module with a clickable rotary encoder and a monochrome OLED screen wired to the board. It also strives to create a friendly GUI creation framework for creating custom interfaces on a small-scale display (ideally 128x64 pixels).

This project utilises the amazing [MicroPython](https://micropython.org/) embedded implementation of Python 3 for convenience and optimal performance (runs fine on a 252-LED long stripe). It also uses the uasyncio library by creating 3 separate threads for controlling the rotary encoder, OLED display and the LED stripe itself with maximum concurrency.

Any configuration (such as changing PIN numbers or LED count) can be done conveniently by modifying the constants.py file.
