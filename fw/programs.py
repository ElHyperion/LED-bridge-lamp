from program_generic import ProgramGeneric
from config import Config
from display import Display as Disp
from led_strip import LedStrip as Led


class ManualRGB(ProgramGeneric):
    _name = 'Manual RGB'

    def draw(self):
        Disp.add_label(self._name)
        Disp.add_slider('R', 12, 255, Config.red(), 3,
                        self._changed_r, self._focused)
        Disp.add_slider('G', 12, 255, Config.green(), 3,
                        self._changed_g, self._focused)
        Disp.add_slider('B', 12, 255, Config.blue(), 3, self._changed_b,
                        self._focused)
        Disp.add_slider('Brt', 12, 100, Config.brightness(), 2,
                        self._changed_brt, self._focused)
        super(ManualRGB, self).draw()

    @classmethod
    def led_draw(cls):
        Led.led_all(Config.rgb())
        print('drawing leds')
        cls._changed = False

    @classmethod
    def _changed_brt(cls, value):
        Config.brightness(value)
        cls._changed = True

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

    @staticmethod
    def _focused():
        Config.save()
