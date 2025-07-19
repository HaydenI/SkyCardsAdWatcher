# SkyCards Ad Watcher

This script automates the process of watching advertisements in SkyCards on an Android device to earn in-game photos. It uses ADB to interact with the device and OpenCV for image recognition to find and tap on buttons.

## ⚠️ Disclaimer

**Using this script may be against the terms of service of the game. Automating in-game actions can be considered cheating and may result in your account being suspended or permanently banned. Use this script at your own risk.**

## Features

- Automatically finds and taps the "Camera" button.
- Automatically finds and taps the "Watch Ad" button.
- Waits for the ad to finish playing.
- Automatically finds and taps various types of "Close Ad" buttons.
- Repeats the cycle indefinitely.
- Keeps a running count of successfully watched ads.
- Includes randomized delays to mimic human behavior.
- **Failsafe**: If no buttons are found for three consecutive attempts, the script will automatically kill and restart the app to recover from a stuck state.
- **Debug Mode**: A `-debug` flag can be used to show detailed output, including image detection confidence scores.

## Prerequisites

1.  **Python 3.6+**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
2.  **Android Debug Bridge (ADB)**: ADB is required to communicate with your Android device.
    - You can install it as part of the [Android Studio SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools).
    - Ensure `adb` is in your system's PATH. You can verify this by running `adb --version` in your terminal.
3.  **Android Device**:
    - An Android device connected to your computer via USB.
    - **USB Debugging** must be enabled on the device. You can find this in `Developer options` in your device's settings.

## Installation

1.  **Clone or download the project files.**
    Make sure you have `ad_watcher.py`, `requirements.txt`, and the `images/` folder.

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The script relies on template matching to find buttons on the screen. The template images are located in the `images/` directory.

-   **Screen Resolution**: The provided images are likely specific to a certain screen resolution. If the script cannot find the buttons on your device, you will need to replace the images in the `images/` directory with screenshots from your own device. Make sure to crop the images tightly around the buttons you want to detect.

-   **Confidence Threshold**: You can adjust the `CONFIDENCE_THRESHOLD` in `ad_watcher.py` if the script is not detecting buttons correctly. A lower value is less strict, while a higher value is more strict.
    ```python
    CONFIDENCE_THRESHOLD = 0.9
    ```

## Usage

1.  **Connect your Android device** to your computer via USB and ensure USB Debugging is enabled and authorized.

2.  **Verify ADB connection**:
    Open a terminal or command prompt and run:
    ```bash
    adb devices
    ```
    You should see your device listed. If it says "unauthorized", you may need to check your phone's screen for an authorization prompt.

3.  **Run the script**:
    Make sure you are in the project directory and your virtual environment is activated.
    ```bash
    python3 ad_watcher.py
    ```

    To see more detailed output, such as image detection confidence scores, run in debug mode:
    ```bash
    python3 ad_watcher.py -debug
    ```

4.  **Stopping the script**:
    Press `Ctrl+C` in the terminal where the script is running to stop the automation.

## Troubleshooting

-   **"Error: No device found."**:
    -   Make sure your device is connected and USB debugging is on.
    -   Run `adb devices` to check the connection status.
    -   Ensure the ADB server is running. You can restart it with `adb kill-server` followed by `adb start-server`.

-   **Buttons not being found**:
    -   This is likely due to a mismatch in screen resolution or UI changes in the app.
    -   You need to take new screenshots of the buttons on your device and replace the corresponding files in the `images/` directory.
    -   Try adjusting the `CONFIDENCE_THRESHOLD` in the script.
