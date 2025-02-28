"""
added
    - pop-up script - for alerts and prompts for input
    - click-assist - for detecting clicks
    - updates saved centre coordinate if clicked within defined acceptable region
        (acceptable click region relative to size of defined region)

Next:
    . . . .
"""
import pyautogui
import time
import os
import subprocess
import json
import time
import pyscreeze
import PIL
from PIL import Image
# global variables
screen_region_coordinates = []  # holds accepted defined region coordinates
current_region = 1  # counter for default region name
scaling_factor = 1  # scaling factor - as pyautogui screenshot and mouse coordinates use different scales
box_define_delay = 1  # delay between checking mouse coordinates

# file paths
region_folder = "./auto_assist"  # main directory to hold all workflow paths
coordinates_file = "click_coordinates.json"  # holds click coordinates
json_data_file = "workflow_data.json"  # holds defined region workflow data
workflow_path = None  # holds the current workflow directory path for 'Monitor' mode

# info text
initial_text = ("Autoassistant captures defined regions of your workflow. "
                "\n\nTo define a region, click around the clickable element by creating a square with "
                "the element in the center. \n\nStart by moving the mouse to the top-left corner, "
                "then bottom-left, bottom-right, and top-right (anti-clockwise), pausing for "
                "2 seconds at each point. \nIf successful, a pop-up will ask you to name the region. "
                "You can use the default name, provide a custom name, or cancel."
                "\n\n\nTO ESCAPE: Send Mouse to TOP LEFT of the SCREEN.")


def calculate_defined_centre(region):
    """
    Calculates the inner box boundary of the passed defined box region.
    Used to create a new region to define if a click is within the accepted centre of the passed region.
    The calculated new region is relative to the region size, i.e. smaller regions allow clicks within a larger area
    of the passed region, and larger regions allow clicks within a smaller area.
    """
    screen_size = pyautogui.size()
    # get passed region width and height
    region_width = region[2]
    region_height = region[3]

    # get width and height boundary relative to the screen size
    width_boundary = round((1 - (region_width / screen_size.width))**2, 2)
    height_boundary = round((1 - (region_height / screen_size.height))**2, 2)

    # define new x, y, width and height for acceptable click area
    new_region_x = region[0] + (region[2] * ((1 - width_boundary) / 2))
    new_region_width = region[2] - (region[2] * (1 - width_boundary))
    new_region_y = region[1] + (region[3] * ((1 - height_boundary) / 2))
    new_region_height = region[3] - (region[3] * (1 - height_boundary))

    # set new region
    new_region = [new_region_x, new_region_y, new_region_width, new_region_height]

    """print statements if need more information"""
    # print(f"Boundary percentage width for region: {width_boundary}")
    # print(f"Boundary percentage height for region: {height_boundary}")
    # print(f"Defined previous region: {region}")
    # print(f"New region with boundary: {new_region}")

    """to view the defined centre region if needed"""
    # pyautogui.moveTo(new_region_x, new_region_y, duration=0.5)
    # pyautogui.moveTo(new_region_x, new_region_y + new_region_height, duration=0.5)
    # pyautogui.moveTo(new_region_x + new_region_width, new_region_y + new_region_height, duration=0.5)
    # pyautogui.moveTo(new_region_x + new_region_width, new_region_y, duration=0.5)

    return new_region


def start_mouse_listener_process():
    """Starts the mouse listener in a separate subprocess, passing coordinate file path as argument"""
    coordinates_file_path = f"{workflow_path}/{coordinates_file}"
    subprocess.Popen(['python3', 'click_assist.py', coordinates_file_path])


def run_prompt():
    """Calls external script in separate subprocess to display pyautogui prompt for region name"""
    text = f'Box region {current_region}'  # default name
    result = subprocess.run(
        ['python3', 'pop_up_script.py', 'prompt', text],
        capture_output=True,  # Capture output
        text=True  # Output returned as string
    )
    return result.stdout.strip()  # Return output from script


def run_screenshot_prompt():
    """Calls external script in separate subprocess to display pyautogui confirm
    for whether screenshot is important"""
    result = subprocess.run(
        ['python3', 'pop_up_script.py', 'screenshot'],
        capture_output=True,  # Capture output
        text=True  # Output returned as string
    )
    return result.stdout.strip()  # Return output from script


def run_click_coordinate_prompt():
    """Calls external script in separate subprocess to display pyautogui confirm
    for whether screenshot is important"""
    result = subprocess.run(
        ['python3', 'pop_up_script.py', 'click_importance'],
        capture_output=True,  # Capture output
        text=True  # Output returned as string
    )
    return result.stdout.strip()  # Return output from script


def run_start_option():
    """Calls external script in separate subprocess to display pyautogui confirm
    for whether screenshot is important"""
    result = subprocess.run(
        ['python3', 'pop_up_script.py', 'run_option'],
        capture_output=True,  # Capture output
        text=True  # Output returned as string
    )
    return result.stdout.strip()  # Return output from script


def run_workflow_select(number_buttons):
    """Calls external script in separate subprocess to display pyautogui confirm
    for whether screenshot is important"""
    result = subprocess.run(
        ['python3', 'pop_up_script.py', 'workflow_select', number_buttons],
        capture_output=True,  # Capture output
        text=True  # Output returned as string
    )
    return result.stdout.strip()  # Return output from script



def run_alert(text):
    """Calls external script in separate subprocess to display pyautogui alert with info"""
    subprocess.run(['python3', 'pop_up_script.py', 'alert', text])


def get_resolution_scaling():
    """calculates the scaling factor - to switch between different pyautogui screenshot and mouse scales"""
    global scaling_factor
    screen_size = pyautogui.size()
    screenshot_size = pyautogui.screenshot().size
    scaling_factor = screenshot_size[0] / screen_size.width
    print(f"Scaling Factor: {scaling_factor}")


def within_box_range(new_coordinate, comparison_coordinate, distance_axis, variance_axis, below=False):
    """
    Checks whether the new coordinate obtained is within an accepted x ond y-axis degree of freedom.
    :param new_coordinate: new coordinate to maybe add
    :param comparison_coordinate: a previous coordinate to check new coordinate against
    :param distance_axis: (0 or 1) x or y axis that gets distance from comparison coordinate to new coordinate
    :param variance_axis: (0 or 1) the other axis to distance axis to calc degree of freedom of new point
    :param below: passed flag for ensuring second point is below the first point.
    :return: True or False
    """
    if below:  # new coordinate must be below the previous coordinate
        if comparison_coordinate[distance_axis] - new_coordinate[distance_axis] > 0:
            return False

    # distance between new and previous point
    distance = abs(comparison_coordinate[distance_axis] - new_coordinate[distance_axis])

    # calc accepted degree of freedom for the new point
    degree_freedom = distance * 0.1

    """to display more information if needed"""
    # print(f"comparison axis: {comparison_coordinate[variance_axis]}, "
    #       f"degrees freedom: {degree_freedom}, "
    #       f"new coordinate axis: {new_coordinate[variance_axis]}")

    # checks if new point within accepted x/y-axis with calculated degree of freedom
    if (comparison_coordinate[variance_axis] - degree_freedom
            <= new_coordinate[variance_axis]
            <= comparison_coordinate[variance_axis] + degree_freedom):
        return True

    return False


def check_if_box_coordinate(current_position, region_list_size):
    """
    Checks if the new coordinate is a valid next box region coordinate.
    :param current_position: new coordinate.
    :param region_list_size: the number of box coordinates already added.
    :return: True if should add coordinate. False if should not add and reset the list.
    """
    if region_list_size == 0:  # no previous coordinates added
        return True
    elif region_list_size == 1:  # check if current_position is 'below' the 'first' point
        valid = within_box_range(current_position, screen_region_coordinates[0],
                                 1, 0, below=True)
        return valid

    elif region_list_size == 2:  # check if current_position is 'right' to 'second' point
        valid = within_box_range(current_position, screen_region_coordinates[1], 0, 1)
        return valid

    elif region_list_size == 3:  # check if current_position above third point and right to first position
        first_valid = within_box_range(current_position, screen_region_coordinates[2], 1, 0)
        second_valid = within_box_range(current_position, screen_region_coordinates[0], 0, 1)
        if first_valid and second_valid:
            return True
        else:
            return False


def add_coordinate(current_position):
    """Adds new coordinate to list holding box region coordinates if a valid coordinate."""
    global screen_region_coordinates

    if current_position not in screen_region_coordinates:
        # check if valid next box coordinate
        valid_coordinate = check_if_box_coordinate(current_position, len(screen_region_coordinates))

        if valid_coordinate:  # add coordinate
            screen_region_coordinates.append(current_position)
            print(f"Added {current_position}")

        else:  # reset list
            screen_region_coordinates.clear()
            print(f"Coordinates Reset")


def get_box_region():
    """
    Calculates the final box region from the collected box region coordinates.
    Obtains the average x, y, width, height
    :return tuple of box region coordinates for mouse scale and screenshot scale
    """
    # average x-axis
    left = int((screen_region_coordinates[0][0] + screen_region_coordinates[1][0]) // 2)
    # average y-axis
    top = int((screen_region_coordinates[0][1] + screen_region_coordinates[3][1]) // 2)
    # average width
    width = int(((screen_region_coordinates[3][0] - left) + (screen_region_coordinates[2][0] - left)) // 2)
    # average height
    height = int(((screen_region_coordinates[1][1] - top) + (screen_region_coordinates[2][1] - top)) // 2)

    # box region with pyautogui mouse scaled coordinates
    movement_region = (left, top, width, height)
    # box region with pyautogui screenshot/locateOnScreen scaled coordinates
    locate_region = (int(left * scaling_factor), int(top * scaling_factor),
                     int(width * scaling_factor), int(height * scaling_factor))

    return movement_region, locate_region


def centre_position(region):
    """returns the centre coordinate for a passed box region"""
    centre_x = region[0] + int((region[2] // 2))
    centre_y = region[1] + int((region[3] // 2))
    return [centre_x, centre_y]


def get_plus_save_image(screenshot_img, name):
    """saves passed screenshot image to workflow directory. Returns img path to screenshot image."""
    if not os.path.isdir(workflow_path):
        os.mkdir(workflow_path)

    img_path = f"{workflow_path}/{name}.png"
    screenshot_img.save(img_path)

    return img_path


def save_region(name, mouse_region, locate_region, screenshot_img):
    """Saves the box region coordinates, centre coordinates and saved screenshot path to json file."""
    # save screenshot and get saved screenshot file path
    img_path = get_plus_save_image(screenshot_img, name)

    screenshot_needed = run_screenshot_prompt()
    click_importance = run_click_coordinate_prompt()

    # format box region for adding to json file
    region = {
        'name': name,
        'mouse_region': mouse_region,
        'mouse_center_coordinate': centre_position(mouse_region),
        'mouse_click_coordinate_user': ["None", "None"],
        'locate_region': locate_region,
        'locate_center_coordinate': centre_position(locate_region),
        'locate_click_coordinate_user': ["None", "None"],
        'img_path': img_path,
        'img_needed': screenshot_needed,
        'centre_provided': "None",
        'click_importance': click_importance
    }

    # define the json file path
    region_file_name = f"{workflow_path}/{json_data_file}"
    # get any previous data
    if os.path.isfile(region_file_name):
        with open(region_file_name, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # add and save the data
    data.append(region)
    with open(region_file_name, 'w') as file:
        json.dump(data, file, indent=4)

    print("should have saved")


def box_region_obtained():
    """Called after all box region are colected. Collects the data needed for saving the region data."""
    global current_region, screen_region_coordinates
    name = run_prompt()  # obtain name from user for the region identified

    if name != "None":
        region_name = name  # get the name of the region
        mouse_movement_region, locate_screen_region = get_box_region()  # get coordinates (left, top, width, height)
        screenshot = pyautogui.screenshot(region=mouse_movement_region)  # get the screenshot
        save_region(region_name, mouse_movement_region, locate_screen_region, screenshot)  # save region details
        current_region += 1  # increment the default region name number

    screen_region_coordinates.clear()  # clear region coordinates


def get_last_region():
    """Returns the last saved region, or None if none saved"""
    try:
        # get data from file
        with open(f"{workflow_path}/{json_data_file}", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                last_region = None
            else:  # get the last region saved
                if isinstance(data, list) and data:
                    last_region = data[-1]

    except FileNotFoundError:  # no saved data yet
        last_region = None

    return last_region


def check_coordinate_in_region(region, x, y):
    """checks if the click coordinate within the defined accepted region"""
    defined_region = calculate_defined_centre(region['mouse_region'])  # calc accepted region box
    # checks if click within accepted region
    if ((defined_region[0] <= x <= defined_region[0] + defined_region[2]) and
            (defined_region[1] <= y <= defined_region[1] + defined_region[3])):
        print("Within Region - centre updated")
        return True
    print("Outside Region - centre not updated")
    return False


def update_region(region, key_name, value, data_index, add_centre=False):
    """
    Updates the passed region with the passed new value for the passed key.
    If add centred passed then calcs and updates the scaled centre coordinates.
    """
    # update the region
    region[key_name] = value
    if add_centre:
        region['locate_click_coordinate_user'] = [value[0] * scaling_factor, value[1] * scaling_factor]
        region["centre_provided"] = "True"

    # load saved data
    with open(f"{workflow_path}/{json_data_file}", "r") as file:
        data = json.load(file)

    # update and save the data
    data[data_index] = region
    with open(f"{workflow_path}/{json_data_file}", "w") as file:
        json.dump(data, file, indent=4)


def check_click_coordinates():
    """
    checks if the user clicked coordinates are specific to the previous defined region,
    and then updates the 'centre coordinate' for that region.
    Deletes click coordinates after executing.
    """
    if os.path.isfile(f"{workflow_path}/{coordinates_file}"):
        # obtain click coordinates
        with open(f"{workflow_path}/{coordinates_file}", 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("Error obtaining click coordinates")
            else:
                try:
                    # click coordinates
                    click_x = data["x"]
                    click_y = data["y"]
                    # last saved defined region
                    last_defined_region = get_last_region()
                    if last_defined_region:
                        # checks if click within acceptable region area
                        if check_coordinate_in_region(last_defined_region, click_x, click_y):
                            # updates the saved region data with the click coordinates
                            update_region(last_defined_region, 'mouse_click_coordinate_user',
                                          [click_x, click_y], -1, add_centre=True)
                except KeyError:
                    pass
            # delete the coordinates
            os.remove(f"{workflow_path}/{coordinates_file}")


def get_screen_coordinates():
    """
    Gets the mouse position coordinates from user.
    Checks whether the coordinates are purposeful coordinates that are defining a box region.
    If box region defined - then saves the region.
    If click coordinates added - then checks if coordinates should be added to region data.
    """
    global screen_region_coordinates

    previous_coordinate = []  # holds previous while loop mouse position
    while True:
        try:
            current_position = list(pyautogui.position())  # x, y

            # activate FAILSAFE if top left of screen
            if current_position[0] == 0 and current_position[1] == 0:
                raise pyautogui.FailSafeException

            if not previous_coordinate:  # add coordinate if empty list
                previous_coordinate.append(current_position)

            else:
                # if mouse staying still
                if current_position == previous_coordinate[0]:
                    # stores if valid box region coordinate
                    add_coordinate(current_position)
                    # if 4 valid region coordinates (box defined)
                    if len(screen_region_coordinates) == 4:
                        box_region_obtained()  # organise and save box region

                # mouse not stationary - reset previous coordinate
                previous_coordinate = [current_position]

            time.sleep(box_define_delay)  # delay between mouse coordinate check
            check_click_coordinates()  # check if click coordinates added

        except pyautogui.FailSafeException:  # close application
            print("FailSafe triggered. Exiting.")
            break


def activate_auto_assist():

    set_next_saving_directory()  # create current workflow directory
    run_alert(initial_text)  # show user info
    start_mouse_listener_process()  # activate mouse click listener
    get_screen_coordinates()  # main loop tracking workflow


def autogui_failsafe():
    """activate failsafe"""
    pyautogui.FAILSAFE = True


def set_up_assist_directory():
    """Create main workflow directory"""
    if not os.path.isdir(region_folder):
        os.mkdir(region_folder)


def set_next_saving_directory():
    """creates next workflow directory, with workflow name incremented from last workflow number."""
    global workflow_path
    try:  # get last workflow directory number
        folders = os.listdir(region_folder)
        folders.sort()
        folder = folders[-1]
        previous_saved_workflow = folder.split('-')[-1]
    except IndexError:  # is first workflow directory
        previous_saved_workflow = 0

    next_region_directory = f"workflow-{int(previous_saved_workflow) + 1}"
    workflow_path = f"{region_folder}/{next_region_directory}"

    # create the workflow directory
    if not os.path.isdir(workflow_path):
        os.mkdir(workflow_path)


def activate_execute_assist():
    """
    Selects the workflow choice from the user, and executes each step of the workflow.
    """
    # gets the wordflow folders
    folders = os.listdir(region_folder)
    if not folders:  # prevent further execution if no saved worflows
        print("No Previous Workflows saved. . . \nPlease run again in 'Monitor' mode first.")
        return

    folders.sort()
    workflow_numbers = [workflow.split("-")[1] for workflow in folders]
    # show option prompt for user to select which workflow
    workflow_selection = run_workflow_select(" ".join(workflow_numbers))

    if not workflow_selection:
        print("None Selected. . . Please Try again")
        return

    # set the relative file path to the selected workflow
    workflow_folder_execute = f"{region_folder}/workflow-{workflow_selection}"
    workflow_data = get_json_data(workflow_folder_execute)

    if not workflow_data:
        return

    # execute each step of the workflow
    for i, step in enumerate(workflow_data):
        success = execute_step(step)
        if not success:
            print(f"Error in step {i+1}/{len(workflow_data)}")


def check_near_img_region(locate_region, img_region, screen_size):
    """
    Checks whether the locateOnScreen bbox coordinates for the identified image is within
    a specified threshold of the original stated img location bbox region.
    i.e. allows some flexibility for the img region specified to be changed slightly.
    - but larger differences relative to screen size will return False
    :param locate_region: previously specified image locate region
    :param img_region: current locateOnScreen bbox image region
    :param screen_size: screen.size() (width and height of screen)
    :return: True if bbox within accepted boundary. False if not
    """
    def check_img_boundary(idx, locate_width_height=0, img_width_height=0, thresh=0.1, screen=screen_size):
        """performs the calculation for checking if bbox region is in accepted boundary"""
        if ((locate_region[idx] + locate_width_height) - (screen[idx] * thresh)  # top left boundary
                <= img_region[idx] + img_width_height
                <= (locate_region[idx] + locate_width_height) + (screen[idx] * thresh)):  # bottom right boundary
            return True
        return False

    img_region = list(img_region)  # convert bbox region to list so indexable

    if (check_img_boundary(0) and  # left position
            check_img_boundary(1) and  # top position
            check_img_boundary(0, locate_width_height=locate_region[2],  # right position
                               img_width_height=img_region[2])
            and check_img_boundary(1, locate_width_height=locate_region[3],  # bottom position
                                   img_width_height=img_region[3])):
        return True

    return False


def execute_step(workflow_step):
    """
    Executes a step of the workflow - based on the workflow_step information provided.
    Checks first if the region to interact with is within the screen dimensions.
    Then checks if the screenshot image of the interactable region is present (if specified to locate).
    Then moves mouse to click coordinates and clicks.
    :param workflow_step: A dictionary entry from a previously saves workflow_data.json file.
    :return: True if all steps successful, else False."""

    print(f"Executing step: {workflow_step["name"]}")
    # 1. make sure coordinates for the region are within the screen boundaries
    screen_size = pyautogui.size()
    region_boundary = workflow_step["mouse_region"]
    if not (region_boundary[0] + region_boundary[2] <= screen_size.width) \
        and (region_boundary[1] + region_boundary[3] <= screen_size.height):
        print("Different screen setup - not suitable for current workflow execution")
        return False
    print("Within screen boundary")

    # 2. check if the screenshot is needed
    img_needed = True if workflow_step["img_needed"] == "Yes" else False
    if img_needed:
        locate_img_region = workflow_step["locate_region"]
        # find saved region image at saved region coordinates
        img_path = workflow_step["img_path"]
        try:
            img_located = pyautogui.locateOnScreen(img_path, region=locate_img_region, confidence=0.4)
        except pyscreeze.ImageNotFoundException:
            print("Could not locate image in defined region")
            # find saved image anywhere on the screen
            try:
                img_located = pyautogui.locateOnScreen(img_path, confidence=0.4)
            except pyscreeze.ImageNotFoundException:
                print("No img found - not suitable for current workflow execution")
                return False
            else:
                # check if img found is within acceptable boundary to saved region coordinates
                within_range = check_near_img_region(locate_img_region, img_located, screen_size)
                if not within_range:
                    print("img found - but in different location - not suitable for current workflow execution")
                    return False
                else:
                    print("Second image found")

        else:
            print("Image Found")

    # 3. check which click coordinate to use
    specified_click_coordinates = True if workflow_step["click_importance"] == "Yes" else False
    if specified_click_coordinates:  # user specifically specified a coordinate to click
        click_coordinate = workflow_step["mouse_click_coordinate_user"]
    elif not specified_click_coordinates and img_needed:  # no specified coordinate but img is important
        print("In Here")
        x, y = pyautogui.center(img_located)
        click_coordinate = [int(x // scaling_factor), int(y // scaling_factor)]
    else:  # centre coordinate for defined region for this step
        click_coordinate = workflow_step["mouse_center_coordinate"]

    # 4. move to click coordinate
    pyautogui.moveTo(click_coordinate[0], click_coordinate[1], duration=0.5)
    time.sleep(1)
    pyautogui.click()  # click
    time.sleep(2.5)
    print("Coordinate clicked\n")
    return True


def get_json_data(workflow_folder):
    """Gets the JSON data of the specified workflow"""
    if workflow_folder:
        data = []
        with open(f"{workflow_folder}/workflow_data.json", 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"Error reading data in {workflow_folder}")
        return data


if __name__ == '__main__':

    # initial setup for Monitor and Execute app
    set_up_assist_directory()  # create main directory
    autogui_failsafe()  # activate FAILSAFE
    get_resolution_scaling()  # get scaling factor

    run_choice = run_start_option()  # choice of app for user
    if run_choice == "Monitor":
        activate_auto_assist()  # run autoassistant capture
    else:
        activate_execute_assist()  # run autoassistant execution


