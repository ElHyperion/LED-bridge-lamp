from program_generic import ProgramGeneric
from config import Config
from display import Display as Disp
from constants import LED_COUNT
from led_strip import LedStrip as Led


class ManualRGB(ProgramGeneric):
    _name = 'Manual RGB'
    _left = None
    _right = None

    def draw(self):
        Disp.add_label(self._name)
        Disp.add_slider('R', 12, 0, 255, Config.red(), 3,
                        self._changed_r, self._focused)
        Disp.add_slider('G', 12, 0, 255, Config.green(), 3,
                        self._changed_g, self._focused)
        Disp.add_slider('B', 12, 0, 255, Config.blue(), 3, self._changed_b,
                        self._focused)
        Disp.add_slider('Brt', 12, 0, 100, Config.brightness(), 2,
                        self._changed_brt, self._focused)
        Disp.add_slider('Wdt', 12, 0, LED_COUNT, Config.width(), 2,
                        self._changed_wdt, self._focused)
        Disp.add_slider('Off', 12, -LED_COUNT // 2, LED_COUNT // 2, Config.offset(),
                        1, self._changed_off, self._focused)
        super(ManualRGB, self).draw()

    @classmethod
    def led_draw(cls):
        if cls._left is None:
            cls._left, cls._right = cls._calculate_band()
        if Config.width() == LED_COUNT and Config.offset() == 0:
            Led.led_all(Config.rgb())
        else:
            Led.led_band(Config.rgb(), cls._left, cls._right)
        cls._changed = False

    @classmethod
    def _changed_r(cls, value):
        Config.red(value)
        cls._changed = True

    @classmethod
    def _changed_g(cls, value):
        Config.green(value)
        cls._changed = True

    @classmethod
    def _changed_b(cls, value):
        Config.blue(value)
        cls._changed = True

    @classmethod
    def _changed_brt(cls, value):
        Config.brightness(value)
        cls._changed = True

    @classmethod
    def _changed_wdt(cls, value):
        Config.width(value)
        cls._left, cls._right = cls._calculate_band()
        cls._changed = True

    @classmethod
    def _changed_off(cls, value):
        Config.offset(value)
        cls._left, cls._right = cls._calculate_band()
        cls._changed = True

    @staticmethod
    def _focused():
        Config.save()

    @staticmethod
    def _calculate_band():
        left = max(Config.offset() - Config.width() // 2 + LED_COUNT // 2, 0)
        right = min(Config.offset() + Config.width() // 2 + LED_COUNT // 2,
                    LED_COUNT)
        return left, right
