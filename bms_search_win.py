#main automation

#open a browser, 2) search BookMyShow, and 3) click the www.bookmyshow.com result.

import time
import os
import datetime
import platform
import pyautogui as pg
from pointer import print_mouse_position

# =========================
# CONFIG (edit as needed)
# =========================
QUERY = "BookMyShow"
SEARCH_ENGINE_URL = "https://www.google.com"
RESULT_IMAGE = "bms_link.png"     # tight crop of "www.bookmyshow.com" from results
BROWSER_TO_OPEN = "chrome"        # "chrome", "msedge", or "firefox"
RESULTS_LOAD_WAIT = 3.0           # seconds to wait for results to load
OPEN_WAIT = 2.0                   # seconds to wait after opening browser
CONFIDENCE = 0.85                 # OpenCV confidence level
SAVE_RESULT_SCREENSHOT = "bms_result.png"

# Safety & pacing
pg.FAILSAFE = True
pg.PAUSE = 0.15

# =========================
# OS checks (Windows only)
# =========================
assert platform.system().lower() == "windows", "This script is for Windows 10."

# =========================
# Core functions
# =========================
def open_browser_via_run():
    """Open browser using Win+R."""
    pg.hotkey("win", "r")
    time.sleep(0.3)
    pg.typewrite(BROWSER_TO_OPEN)
    pg.press("enter")
    time.sleep(OPEN_WAIT)

def focus_address_bar():
    """Focus the address bar."""
    pg.hotkey("ctrl", "l")
    time.sleep(0.2)

def go_to_search_engine():
    focus_address_bar()
    pg.typewrite(SEARCH_ENGINE_URL)
    pg.press("enter")
    time.sleep(OPEN_WAIT)

def submit_query(query):
    pg.typewrite(query)
    pg.press("enter")
    time.sleep(RESULTS_LOAD_WAIT)

def click_result_with_image(template_path, confidence=CONFIDENCE):
    """Locate and click the BookMyShow link via image recognition."""
    try:
        box = pg.locateOnScreen(template_path, confidence=confidence)
        if box:
            cx, cy = pg.center(box)
            pg.click(cx, cy)
            return True
    except Exception:
        pass
    return False

def open_first_result_keyboard_fallback(tab_steps=2):
    """If image not found, use Tab + Enter to open first link."""
    for _ in range(tab_steps):
        pg.press("tab")
        time.sleep(0.1)
    pg.press("enter")

def scroll_down_to_content():
    """Scroll down slightly to move past promotional slider."""
    time.sleep(3)  # wait for BookMyShow to load
    pg.scroll(-500)  # scroll down
    time.sleep(1)

def take_fullscreen_screenshot(filename="BookMyShow_Page.png"):
    """Take full-screen screenshot and save it to Downloads."""
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(filename)
    final_name = f"{name}_{timestamp}{ext or '.png'}"
    save_path = os.path.join(downloads_path, final_name)
    ss = pg.screenshot()
    ss.save(save_path)
    print(f"Screenshot saved to: {save_path}")

def close_browser():
    """Close the active browser window."""
    time.sleep(5)  # wait 5 seconds before closing
    pg.hotkey("alt", "f4")
    print("Browser closed successfully.")

def save_reference_screenshot():
    """Take quick local screenshot (optional)."""
    ss = pg.screenshot()
    ss.save(SAVE_RESULT_SCREENSHOT)

# =========================
# MAIN FLOW
# =========================
def main():
    print("Starting in 1.5s… Move mouse to TOP-LEFT to ABORT.")
    time.sleep(1.5)

    # 1) Open browser
    open_browser_via_run()

    # 2) Go to Google
    go_to_search_engine()

    # 3) Search for BookMyShow
    submit_query(QUERY)

    # 4) Click BookMyShow link (image match)
    clicked = click_result_with_image(RESULT_IMAGE, confidence=CONFIDENCE)
    if not clicked:
        open_first_result_keyboard_fallback(tab_steps=2)

    # 5) Scroll down a bit after site loads
    scroll_down_to_content()

    # 6) Take a full-screen screenshot after scroll
    take_fullscreen_screenshot("BookMyShow_Page.png")

    # 7) Close the browser after 5 seconds
    close_browser()

    # 8) Optional local reference screenshot
    # save_reference_screenshot()

if __name__ == "__main__":
    main()
