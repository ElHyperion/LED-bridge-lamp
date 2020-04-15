from display import Display as Disp, SCR_MENU
from controller import KEY_ENTER, KEY_NEXT, KEY_PREV
from config import Config


class ProgramGeneric():
    _name = 'Program generic'
    _changed = True

    def __init__(self):
        self._redrawed = False
        self._anim_frame = 0
        self._frame_period = 10  # Sleep time for async await

    @staticmethod
    def _go_back():
        Disp.set_cur_screen(SCR_MENU, Config.cur_program())

    @staticmethod
    def key_pressed(key, count):
        if key == KEY_NEXT:
            Disp.key_next(count)
        elif key == KEY_PREV:
            Disp.key_prev(count)
        elif key == KEY_ENTER:
            Disp.key_enter()

    @classmethod
    def changed(cls):
        return cls._changed

    @property
    def name(self):
        return self._name

    @property
    def frame_period(self):
        return self._frame_period

    @frame_period.setter
    def frame_period(self, period):
        if period <= 0:
            self._frame_period = 10
        self._frame_period = 10 / period * 0.1

    def draw(self):
        Disp.add_link('Back', self._go_back)
