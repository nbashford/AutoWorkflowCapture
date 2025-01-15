"""
Script to run a pynput mouse listener to detect user clicks.
Outside the main script as running within the main thread in prevented
from the pyautogui thread.
"""
import json
import sys
from pynput.mouse import Listener

# Path to file where coordinates will be saved
coordinates_file_path = None


def on_click(x, y, button, pressed):
    """Captures click coordinates and writes to file."""
    if pressed and coordinates_file_path:
        coordinates = {'x': int(round(x)), 'y': int(round(y))}
        print(f"Clicked: ({x}, {y})")
        # Save coordinates to JSON file
        with open(coordinates_file_path, 'w') as f:
            json.dump(coordinates, f)


def start_listener():
    """Starts the pynput mouse listener"""
    with Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    """runs when called from main thread with subprocess Popen and argument: file path"""
    if len(sys.argv) > 1:
        coordinates_file_path = sys.argv[1]  # get the click coordinate file path to save to
        start_listener()  # start the listener
