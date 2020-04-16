import uasyncio as asyncio
import programs as prg
from machine import Pin, Timer
from controller import Controller, KEY_ENTER, KEY_NEXT, KEY_PREV
from display import Display as Disp, SCR_MENU, SCR_PROG
from config import Config
from constants import PIN_BUILTIN_LED


LED_BUILTIN = Pin(PIN_BUILTIN_LED, Pin.OUT)
TIMER_SCREEN = Timer(0)
PROGRAMS = (
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
    prg.ManualRGB(),
)


def key_menu(key, count):
    if key == KEY_NEXT:
        Disp.key_next(count)
    elif key == KEY_PREV:
        Disp.key_prev(count)
    elif key == KEY_ENTER:
        if Disp.highlighted() != Disp.selected():
            Disp.set_highlighted(Disp.selected())
            Config.cur_program(Disp.highlighted())
            # Config.save()
        else:
            Disp.key_enter()


def draw_menu():
    for prog in PROGRAMS:
        Disp.add_link(prog.name, SCR_PROG)
    Disp.set_highlighted(Config.cur_program())


def key_pressed(key, count=0):
    if Disp.is_enabled():
        init_screen_timer()
        if Disp.cur_screen() == SCR_MENU:
            key_menu(key, count)
        else:
            PROGRAMS[Config.cur_program()].key_pressed(key, count)
    else:
        if key == KEY_NEXT and Config.brightness() < 100:
            Config.brightness(Config.brightness() + count * 2)
            PROGRAMS[Config.cur_program()].led_draw()
        elif key == KEY_PREV and Config.brightness() > 0:
            Config.brightness(Config.brightness() - count * 2)
            PROGRAMS[Config.cur_program()].led_draw()
        elif key == KEY_ENTER:
            Disp.enable(True)
            init_screen_timer()


def screen_timeout(timer):
    Disp.enable(False)
    timer.deinit()


def init_screen_timer():
    TIMER_SCREEN.init(period=10000, mode=Timer.ONE_SHOT, callback=screen_timeout)


async def enc_run():
    while True:
        await asyncio.sleep(0.04)
        key, count = Controller.get_key()
        if key is not False:
            key_pressed(key, count)


async def disp_draw():
    while True:
        await asyncio.sleep(0.1)
        if Disp.is_enabled() and Disp.changed():
            if Disp.is_empty():
                if Disp.cur_screen() == SCR_MENU:
                    draw_menu()
                else:
                    PROGRAMS[Config.cur_program()].draw()
            Disp.refresh()


async def led_draw():
    while True:
        await asyncio.sleep(0.)
        if PROGRAMS[Config.cur_program()].changed():
            LED_BUILTIN.on()
            PROGRAMS[Config.cur_program()].led_draw()
            LED_BUILTIN.off()

init_screen_timer()
LOOP = asyncio.get_event_loop()
LOOP.create_task(enc_run())
LOOP.create_task(disp_draw())
LOOP.create_task(led_draw())
LOOP.run_forever()
