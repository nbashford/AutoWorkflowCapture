"""
Script to show pyautogui alert and prompt to the user.
Outside the main script as running alerts and prompt within the main thread results in
the alerts and prompts never closing.
"""
import sys
import pyautogui


def show_prompt(text):
    """display pyautogui prompt - for obtaining name of the defined region"""
    name = pyautogui.prompt(
        text='Enter Name for selected region',
        title='Region Name',
        default=text)  # displays passed default value

    return name


def show_alert(text):
    """display pyautogui alert - showing information to the user"""
    pyautogui.alert(text)


if __name__ == '__main__':
    """
    from main.py - sends via sys.argv:
    1. script name, 2. the function to run, 3. text to pass to function
    """
    if len(sys.argv) > 2:
        function_name = sys.argv[1]  # get function name
        text = sys.argv[2]  # get text to pass to function
        if function_name == 'alert':
            show_alert(text)
        elif function_name == 'prompt':
            name = show_prompt(text)  # Show the prompt and get the input
            print(name)  #
