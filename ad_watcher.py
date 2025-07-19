import cv2
import numpy as np
import time
import random
import sys
from ppadb.client import Client as AdbClient

CONFIDENCE_THRESHOLD = 0.8
HOST = "127.0.0.1"
PORT = 5037
CAMERA_BUTTON_PATH = 'images/step1_camera_button.png'
WATCH_AD_BUTTON_PATH = 'images/step2_watch_ad_button.png'
CLOSE_AD_BUTTON_PATHS = [
    'images/close_x_only_black.png',
    'images/close_x_only_white.png',
    'images/just_x.png'
]

def find_and_tap(device, template_path):
    try:
        screen_capture = device.screencap()
        screen_np = np.frombuffer(screen_capture, np.uint8)
        screen_cv = cv2.imdecode(screen_np, cv2.IMREAD_COLOR)
        template_cv = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template_cv is None:
            return False
        template_height, template_width, _ = template_cv.shape
        result = cv2.matchTemplate(screen_cv, template_cv, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= CONFIDENCE_THRESHOLD:
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            print(f"Found '{template_path}' with {max_val*100:.2f}% confidence. Tapping now.")
            device.input_tap(center_x, center_y)
            return True
        return False
    except Exception as e:
        print(f"An error occurred in find_and_tap: {e}")
        return False

def perform_countdown(duration, message):
    for i in range(duration, 0, -1):
        sys.stdout.write(f"\r{message} {i:02d} seconds...")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r")
    sys.stdout.flush()

def try_close_ad(device):
    """Tries to find and tap any of the close ad buttons."""
    for close_button_path in CLOSE_AD_BUTTON_PATHS:
        if find_and_tap(device, close_button_path):
            perform_countdown(random.randint(4, 6), "Ad closed. Waiting for main screen in")
            return True
    return False

def try_watch_ad(device):
    """Tries to find and tap the 'Watch Ad' button."""
    if find_and_tap(device, WATCH_AD_BUTTON_PATH):
        perform_countdown(random.randint(38, 48), "Watching ad. Time remaining:")
        return True
    return False

def try_open_ad_dialog(device):
    """Tries to find and tap the camera button to open the ad dialog."""
    if find_and_tap(device, CAMERA_BUTTON_PATH):
        perform_countdown(random.randint(2, 4), "Tapped camera button. Waiting for dialog in")
        return True
    return False

def run_automation_loop(device):
    """The main automation loop."""
    print("Starting automation loop. Press Ctrl+C to stop.")
    
    while True:
        try:
            # The order of these checks is important.
            # 1. Try to close an ad if one is present.
            if try_close_ad(device):
                continue

            # 2. If no ad is open, try to start watching one.
            if try_watch_ad(device):
                continue

            # 3. If the watch ad button isn't there, try to open the dialog.
            if try_open_ad_dialog(device):
                continue
            
            # 4. If no other actions were taken, wait before trying again.
            perform_countdown(random.randint(5, 8), "No buttons found. Checking again in")

        except KeyboardInterrupt:
            print("\n\nStopping script.")
            break
        except Exception as e:
            print(f"\nA critical error occurred: {e}")
            perform_countdown(10, "Restarting loop in")

def main():
    client = AdbClient(host=HOST, port=PORT)
    try:
        device = client.devices()[0]
        print(f"Connected to device: {device.serial}")
    except IndexError:
        print("Error: No device found.")
        return

    run_automation_loop(device)

if __name__ == "__main__":
    main()