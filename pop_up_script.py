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


def show_screenshot():
    """display pyautogui prompt - for obtaining name of the defined region"""
    selection = pyautogui.confirm(
        text='Does the Background Image at the defined region always remain constant?\n\n'
             'Please select "Yes" if autoworkflow should detect this image before interacting.\n'
             'Please select "No" if autoworkflow should not detect this image before interacting.',
        title='Screenshot Needed?',
        buttons=["Yes", "No"])  # button options

    return selection

def click_importance():
    """display pyautogui prompt - for obtaining name of the defined region"""
    selection = pyautogui.confirm(
        text='Is the Click position in the defined region important?'
             '\nIf yes - click position will be based on the coordinates that you click.'
             '\nIf No - click position will be based on the centre coordinate of the region defined/image screenshot',
        title='Click Coordinate Importance?',
        buttons=["Yes", "No"])  # button options

    return selection

def run_option():
    """display pyautogui prompt - for obtaining name of the defined region"""
    selection = pyautogui.confirm(
        text='Select "Monitor" for autoworkflow to track your workflow.\n\n'
             'Select "Execute" for autoworkflow to execute a saved workflow.',
        title='Monitor or Execute?',
        buttons=["Monitor", "Execute"])  # button options

    return selection


def workflow_select(buttons):
    """display pyautogui prompt - for obtaining name of the defined region"""
    button_options = buttons.split(" ")
    selection = pyautogui.confirm(
        text='Select the Relevant Workflow to load:',
        title='Workflow Selection',
        buttons=buttons)  # button options

    return selection


def show_alert(text):
    """display pyautogui alert - showing information to the user"""
    pyautogui.alert(text)


if __name__ == '__main__':
    """
    from main.py - sends via sys.argv:
    1. script name, 2. the function to run, 3. text to pass to function
    """
    if len(sys.argv) > 1:
        function_name = sys.argv[1]  # get function name
        if function_name == 'alert':
            text = sys.argv[2]  # get text to pass to function
            show_alert(text)
        elif function_name == 'prompt':
            text = sys.argv[2]  # get text to pass to function
            name = show_prompt(text)  # Show the prompt and get the input
            print(name)  #
        elif function_name == 'screenshot':
            name = show_screenshot()  # Show the prompt and get the input
            print(name)  #
        elif function_name == 'run_option':
            name = run_option()  # Show the prompt and get the input
            print(name)  #
        elif function_name == 'workflow_select':
            buttons = sys.argv[2]  # get text to pass to function
            selection = workflow_select(buttons)
            print(selection)
        elif function_name == 'click_importance':
            selection = click_importance()
            print(selection)

