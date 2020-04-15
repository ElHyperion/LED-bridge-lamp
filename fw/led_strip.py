from machine import Pin
from neopixel import NeoPixel
from constants import PIN_LEDS, LED_TOTAL, LED_COUNT
from config import Config


class LedStrip():
    _np = NeoPixel(Pin(PIN_LEDS), LED_TOTAL)

    # Set colour of a single LED pair
    @classmethod
    def led(cls, i, colour):
        if 0 <= i < LED_COUNT:
            brightness = Config.brightness() / 100
            cls._np[i] = (int(colour[0] * brightness),
                          int(colour[1] * brightness),
                          int(colour[2] * brightness))
            cls._np[LED_TOTAL - i - 1] = \
                (int(colour[0] * brightness),
                 int(colour[1] * brightness),
                 int(colour[2] * brightness))

    # Set colour of all LEDs with set brightness
    @classmethod
    def led_all(cls, colour):
        brightness = Config.brightness() / 100
        col = (int(colour[0] * brightness),
               int(colour[1] * brightness),
               int(colour[2] * brightness))
        for i in range(LED_TOTAL):
            cls._np[i] = col

        # TODO Remove write from here and make a propper LED_strip class like the Display class
        cls._np.write()
