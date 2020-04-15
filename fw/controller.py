from machine import Pin
from rotary_irq_esp import RotaryIRQ
from constants import PIN_ENC1, PIN_ENC2, PIN_BUTTON


KEY_ENTER = 0
KEY_NEXT = 1
KEY_PREV = 2


class Controller():
    _enc = RotaryIRQ(PIN_ENC1, PIN_ENC2)
    _but = Pin(PIN_BUTTON, Pin.IN)
    _pressed = False

    @classmethod
    def get_key(cls):

        # Next / previous
        count = cls._enc.value()
        if count != 0:
            cls._enc.reset()
            return KEY_NEXT if count > 0 else KEY_PREV, abs(count)

        # Enter
        if cls._but.value() == 0 and not cls._pressed:
            cls._pressed = True
            return KEY_ENTER, count
        if cls._but.value() and cls._pressed:
            cls._pressed = False

        return False, count
