#your mouse-position helper

# pointer.py
import pyautogui as pg

def print_mouse_position():
    x, y = pg.position()
    print(f'x:{x}, y:{y}')
    return x, y
