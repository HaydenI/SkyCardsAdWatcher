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

def load_templates(paths):
    """Loads template images from a list of paths into memory."""
    loaded_templates = {}
    for path in paths:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            raise IOError(f"Could not load template image: {path}")
        loaded_templates[path] = img
    return loaded_templates

def get_screenshot(device):
    """Captures and decodes a screenshot from the device."""
    screen_capture = device.screencap()
    screen_np = np.frombuffer(screen_capture, np.uint8)
    return cv2.imdecode(screen_np, cv2.IMREAD_COLOR)

def find_and_tap(device, screen_cv, template_cv, template_path_for_logging):
    """Finds a template on the screen and taps it."""
    try:
        template_height, template_width, _ = template_cv.shape
        result = cv2.matchTemplate(screen_cv, template_cv, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= CONFIDENCE_THRESHOLD:
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            print(f"Found '{template_path_for_logging}' with {max_val*100:.2f}% confidence. Tapping now.")
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

def try_close_ad(device, screen_cv, templates):
    """Tries to find and tap any of the close ad buttons."""
    for path in CLOSE_AD_BUTTON_PATHS:
        template_img = templates[path]
        if find_and_tap(device, screen_cv, template_img, path):
            perform_countdown(random.randint(4, 6), "Ad closed. Waiting for main screen in")
            return True
    return False

def try_watch_ad(device, screen_cv, templates):
    """Tries to find and tap the 'Watch Ad' button."""
    template_img = templates[WATCH_AD_BUTTON_PATH]
    if find_and_tap(device, screen_cv, template_img, WATCH_AD_BUTTON_PATH):
        perform_countdown(random.randint(38, 48), "Watching ad. Time remaining:")
        return True
    return False

def try_open_ad_dialog(device, screen_cv, templates):
    """Tries to find and tap the camera button to open the ad dialog."""
    template_img = templates[CAMERA_BUTTON_PATH]
    if find_and_tap(device, screen_cv, template_img, CAMERA_BUTTON_PATH):
        perform_countdown(random.randint(2, 4), "Tapped camera button. Waiting for dialog in")
        return True
    return False

def run_automation_loop(device, templates):
    """The main automation loop."""
    print("Starting automation loop. Press Ctrl+C to stop.")
    
    while True:
        try:
            screen_cv = get_screenshot(device)
            if screen_cv is None:
                print("Could not get screenshot. Retrying...")
                time.sleep(5)
                continue

            # The order of these checks is important.
            # 1. Try to close an ad if one is present.
            if try_close_ad(device, screen_cv, templates):
                continue

            # 2. If no ad is open, try to start watching one.
            if try_watch_ad(device, screen_cv, templates):
                continue

            # 3. If the watch ad button isn't there, try to open the dialog.
            if try_open_ad_dialog(device, screen_cv, templates):
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

    all_template_paths = [CAMERA_BUTTON_PATH, WATCH_AD_BUTTON_PATH] + CLOSE_AD_BUTTON_PATHS
    try:
        templates = load_templates(all_template_paths)
        print("Templates loaded successfully.")
    except IOError as e:
        print(f"Error: {e}")
        return

    run_automation_loop(device, templates)

if __name__ == "__main__":
    main()