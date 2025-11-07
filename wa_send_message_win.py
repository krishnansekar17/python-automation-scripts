#Send a message in whatsapp group using PyAutoGui Concept

import time
import os
import datetime
import platform
import pyautogui as pg

# =========================
# CONFIG
# =========================
BROWSER_TO_OPEN      = "chrome"          # "chrome", "msedge", or "firefox"
WHATSAPP_URL         = "https://web.whatsapp.com/"
GROUP_NAME           = "SE - AI-B3 - 2"   # used only for typing; matching uses wa_group.png
MESSAGE_TEXT         = "One Week Completed PyAutoGUI"
OPEN_WAIT            = 2.0
LOAD_WAIT            = 3.0               # wait for page states
CONFIDENCE           = 0.85

# Template files placed next to this script
IMG_SEARCH_FIELD     = "wa_search.png"
IMG_GROUP_ITEM       = "wa_group.png"
IMG_MESSAGE_INPUT    = "wa_input.png"

# Safety & pacing
pg.FAILSAFE = True       # move mouse to top-left to abort
pg.PAUSE    = 0.15

assert platform.system().lower() == "windows", "This script is tailored for Windows 10."

# =========================
# Helpers
# =========================
def open_browser_via_run():
    """Open browser using Win+R."""
    pg.hotkey("win", "r")
    time.sleep(0.3)
    pg.typewrite(BROWSER_TO_OPEN)
    pg.press("enter")
    time.sleep(OPEN_WAIT)

def focus_address_bar():
    pg.hotkey("ctrl", "l")
    time.sleep(0.2)

def go_to_whatsapp_web():
    focus_address_bar()
    pg.typewrite(WHATSAPP_URL)
    pg.press("enter")
    time.sleep(LOAD_WAIT + 2)  # give WhatsApp Web a bit more time

def maximize_active_window():
    pg.hotkey("win", "up")
    time.sleep(0.05)
    pg.hotkey("win", "up")
    time.sleep(0.2)

def locate_and_click(img_path, confidence=CONFIDENCE, region=None, click_offset=(0,0)):
    """Locate an image on screen and click its center (+ optional offset)."""
    try:
        box = pg.locateOnScreen(img_path, confidence=confidence, region=region)
        if box:
            x, y = pg.center(box)
            x += click_offset[0]
            y += click_offset[1]
            pg.click(x, y)
            return True
    except Exception:
        pass
    return False

def get_content_region():
    """Restrict matches to the content area (avoid tab bar/taskbar)."""
    sw, sh = pg.size()
    top_margin = 120
    bottom_margin = 60
    return (0, top_margin, sw, sh - top_margin - bottom_margin)

def search_and_open_group():
    """Click the search box, type the group name, then click the group item."""
    region = get_content_region()

    # 1) Click search field
    if not locate_and_click(IMG_SEARCH_FIELD, confidence=CONFIDENCE, region=region):
        # Retry once after a tiny scroll (sometimes hidden)
        pg.scroll(600)  # up a bit
        time.sleep(0.2)
        if not locate_and_click(IMG_SEARCH_FIELD, confidence=CONFIDENCE, region=region):
            # As a fallback, try Tab a few times then type
            for _ in range(6):
                pg.press("tab")
                time.sleep(0.05)
            # Type anyway
    time.sleep(0.3)

    # 2) Type the group name to filter the list
    pg.typewrite(GROUP_NAME)
    time.sleep(1.0)

    # 3) Click the group item
    if not locate_and_click(IMG_GROUP_ITEM, confidence=CONFIDENCE, region=region):
        # If image match fails, try pressing Enter to select first filtered result
        pg.press("enter")
    time.sleep(LOAD_WAIT)

def focus_message_input():
    """Click the message input field."""
    region = get_content_region()
    if not locate_and_click(IMG_MESSAGE_INPUT, confidence=CONFIDENCE, region=region):
        # Fallback: click near bottom-center of the window
        sw, sh = pg.size()
        pg.click(int(sw * 0.5), int(sh * 0.92))
    time.sleep(0.2)

def send_message(text):
    pg.typewrite(text)
    pg.press("enter")

def optional_screenshot_to_downloads(prefix="WA_Send"):
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(downloads, f"{prefix}_{stamp}.png")
    ss = pg.screenshot()
    ss.save(path)
    print(f"Screenshot saved: {path}")

def close_browser_after(seconds=5):
    time.sleep(seconds)
    pg.hotkey("alt", "f4")
    print("Browser closed.")

# =========================
# MAIN
# =========================
def main():
    print("Starting in 1.5s… Move mouse to TOP-LEFT corner to ABORT.")
    time.sleep(1.5)

    # 1) Open browser & WhatsApp Web
    open_browser_via_run()
    maximize_active_window()
    go_to_whatsapp_web()

    # (Assumes you are already logged in / 'Keep me signed in' checked)

    # 2) Search and open the target group
    search_and_open_group()

    # 3) Focus the message input and send the message
    focus_message_input()
    send_message(MESSAGE_TEXT)

    # 4) Optional: take a full-screen screenshot as proof
    optional_screenshot_to_downloads(prefix="WA_SE-AI-B3-2_Message")

    # 5) Close browser after 5 seconds
    close_browser_after(seconds=5)

if __name__ == "__main__":
    main()
