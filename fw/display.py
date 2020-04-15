from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
from constants import PIN_I2C_PWR, PIN_I2C_SCL, PIN_I2C_SDA


SCR_MENU = 0
SCR_PROG = 1


class Display():
    _width = 128
    _height = 64
    _pwr = Pin(PIN_I2C_PWR, Pin.OUT)
    _i2c = I2C(scl=Pin(PIN_I2C_SCL), sda=Pin(PIN_I2C_SDA))
    _pwr.on()
    _enabled = True
    _disp = SSD1306_I2C(_width, _height, _i2c)
    _disp.write_cmd(0xa0)
    _disp.write_cmd(0xc0)
    _disp.contrast(50)
    _disp.show()
    _changed = True  # True if the screen needs redrawing
    _selected_item = 0
    _new_selected_item = None  # Item to select after screen change
    _highlighted_item = None
    _screen_top = 0
    _focused = False
    _cur_screen = SCR_MENU
    _items = []

    @classmethod
    def cur_screen(cls):
        return cls._cur_screen

    @classmethod
    def set_cur_screen(cls, value, selected_item=0):
        if value in (SCR_MENU, SCR_PROG) and cls._cur_screen != value:
            cls._new_selected_item = selected_item
            cls._screen_top = 0
            cls._highlighted_item = None
            cls._cur_screen = value
            cls._focused = False
            cls._items = []
            cls._changed = True

    @classmethod
    def changed(cls):
        return cls._changed

    @classmethod
    def selected(cls):
        return cls._selected_item

    @classmethod
    def set_selected(cls, item_i):
        cur_item = item_i
        for item in cls._items[item_i:]:
            if item.selectable:
                cls._selected_item = cur_item
                # Move the screen down if the selected item is out of boundaries
                if item.bottom >= cls._screen_top + cls._height:
                    cls._screen_top = item.bottom - cls._height
                break
            cur_item += 1
        cls._changed = True

    @classmethod
    def highlighted(cls):
        return cls._highlighted_item

    @classmethod
    def focused(cls):
        return cls._focused

    @classmethod
    def select_current(cls):
        pass

    @classmethod
    def set_highlighted(cls, item):
        if cls._highlighted_item != item:
            cls._highlighted_item = item
            cls._changed = True

    @classmethod
    def key_enter(cls):
        cur_item = cls._items[cls._selected_item]
        if isinstance(cur_item, _Link):
            cur_item.execute()
        else:
            cls._focused = not cls._focused
            if isinstance(cur_item, _Slider):
                cur_item.on_focus()
        cls._changed = True

    @classmethod
    def key_next(cls, count):
        for _ in range(count):
            if cls._focused:
                if cls._items[cls._selected_item].key_next():
                    cls._changed = True
            else:
                if cls._selected_item >= len(cls._items) - 1:
                    break
                cur_index = cls._selected_item + 1
                for item in cls._items[cls._selected_item + 1:]:

                    # Move screen top lower if necessary
                    height_diff = cls._screen_top + cls._height + 1
                    if item.bottom > height_diff:
                        cls._screen_top += item.bottom - height_diff
                        cls._changed = True

                    if item.selectable:
                        cls._selected_item = cur_index
                        break
                    cur_index += 1
                else:
                    cur_index = None
                if cur_index is not None:
                    cls._selected_item = cur_index
                    cls._changed = True

    @classmethod
    def key_prev(cls, count):
        for _ in range(count):
            if cls._focused:
                if cls._items[cls._selected_item].key_prev():
                    cls._changed = True
            else:
                if cls._selected_item == 0:
                    break
                cur_index = cls._selected_item - 1
                for item in cls._items[cls._selected_item - 1::-1]:

                    # Move screen top higher if necessary
                    if item.top < cls._screen_top:
                        cls._screen_top -= cls._screen_top - item.top
                        cls._changed = True

                    if item.selectable:
                        cls._selected_item = cur_index
                        break
                    cur_index -= 1
                else:
                    cur_index = None
                if cur_index is not None:
                    cls._selected_item = cur_index
                    cls._changed = True

    @classmethod
    def is_enabled(cls):
        return cls._enabled

    @classmethod
    def enable(cls, enabled):
        if enabled:
            cls._enabled = True
            cls._disp.contrast(50)
        else:
            cls._enabled = False
            cls._disp.contrast(0)

    @classmethod
    def add_label(cls, label: str):
        top = cls._get_new_pos()
        _label = _Label(top, label)
        cls._items.append(_label)

    @classmethod
    def add_link(cls, label: str, link: int):
        top = cls._get_new_pos()
        _link = _Link(top, label, link)
        cls._items.append(_link)

    @classmethod
    def add_slider(cls, label: str, height: int, max_val: int, default_value=0,
                   val_inc=1, on_change=None, on_focus=None):
        top = cls._get_new_pos()
        _slider = _Slider(top, 128, label, height, max_val, default_value,
                          val_inc, on_change, on_focus)
        cls._items.append(_slider)

    @classmethod
    def _get_new_pos(cls):
        if not cls._items:
            return 0
        last = cls._items[-1]
        return last.bottom

    @classmethod
    def refresh(cls):
        cls._disp.fill(0)

        # Set a selected item after finished rendering the screen
        if cls._new_selected_item is not None:
            cls.set_selected(cls._new_selected_item)
            cls._new_selected_item = None

        for i, item in enumerate(cls._items):

            # Ignore items out of screen boundaries
            if item.bottom <= cls._screen_top:
                continue
            if item.top >= cls._screen_top + cls._height:
                break

            if isinstance(item, _Link):  # Draw highlighted links
                # print('Drawing', item._label)
                if cls._highlighted_item == i:
                    item.draw(cls._disp, cls._screen_top, 0)
                else:
                    item.draw(cls._disp, cls._screen_top, 1)
            else:
                item.draw(cls._disp, cls._screen_top)

            if cls._selected_item == i:  # Draw a cursor
                cls._disp.text('#' if cls._focused else '>',
                               0, item.cursor_pos - cls._screen_top)

        cls._disp.show()
        cls._changed = False

    @classmethod
    def is_empty(cls):
        return len(cls._items) == 0

    @classmethod
    def clear(cls):
        cls._highlighted_item = None
        cls._items = []


class _Element():
    def __init__(self, top, height, selectable=False):
        self._top = top
        self._height = height
        self._bottom = top + height
        self._cursor_pos = top + height // 2 - 4
        self._selectable = selectable

    @property
    def height(self):
        return self._height

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    @property
    def cursor_pos(self):
        return self._cursor_pos

    @property
    def selectable(self):
        return self._selectable


class _Label(_Element):
    def __init__(self, top, label):
        super(_Label, self).__init__(top, 10)
        self._label = label

    def draw(self, disp, screen_top):
        disp.text(self._label, 4, self.top - screen_top)


class _Link(_Element):
    def __init__(self, top, label, link):
        super(_Link, self).__init__(top, 12, True)
        self._label = label
        self._link = link

    def draw(self, disp, screen_top, colour=1):
        if colour == 0:
            disp.fill_rect(8, self.top - screen_top, 120, self._height, 1)
        disp.text(self._label, 8, self.top - screen_top + 2, colour)

    def execute(self):
        if isinstance(self._link, int):
            Display.set_cur_screen(self._link)
        else:
            self._link()


class _Slider(_Element):
    def __init__(self, top, scr_width, label, height, max_val, default_value,
                 val_inc, on_change, on_focus):
        super(_Slider, self).__init__(top, 14, True)
        self._label = label
        self._height = height
        self._max_val = max_val
        self._value = default_value
        self._val_inc = val_inc  # Increase / Decrease the value by this
        self._on_change = on_change  # On change (increase/decrease) event
        self._on_focus = on_focus  # On focus / unfocus event
        self._left = 9 + len(self._label) * 8 + (1 if len(self._label) > 0 else 0)
        self._width = scr_width - self._left
        self._recalculate()

    @property
    def value(self):
        return self._value

    def draw(self, disp, screen_top):
        if len(self._label) > 0:
            disp.text(self._label, 8, self.top - screen_top + 2)
        disp.rect(self._left, self.top - screen_top,
                  self._width, self.height, 1)
        disp.fill_rect(self._left + 2, self.top - screen_top + 2,
                       self._bar_width,
                       self.height - 4, 1)
        if self._value / self._max_val * self._width > 30:
            off = -35
            colour = 0
        else:
            off = 5
            colour = 1
        disp.text(self._text,
                  self._left + int(self._value / self._max_val * self._width) + off,
                  self.top + int(self.height / 2) - 3 - screen_top, colour)

    def key_prev(self):
        if self._value > 0:
            self._value -= self._val_inc
            if self._value < 0:
                self._value = 0
            if self._on_change is not None:
                self._on_change(self._value)
                self._recalculate()
            return True
        return False

    def key_next(self):
        if self._value < self._max_val:
            self._value += self._val_inc
            if self._value > self._max_val:
                self._value = self._max_val
            if self._on_change is not None:
                self._on_change(self._value)
                self._recalculate()
            return True
        return False

    def on_focus(self):
        if self._on_focus is not None:
            self._on_focus()

    def _recalculate(self):
        if self._value == int(self._value):
            self._text = '%4s' % str(int(self._value))
        else:
            self._text = '%.1f' % self._value
        self._bar_width = int(self._value / self._max_val * (self._width - 4))
