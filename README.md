# AutoAssistant

## Overview
(STILL IN INITIAL DEVELOPMENT)
AutoAssistant is a Python-based tool designed to automate workflow region identification and interaction. 
It currently allows users to define clickable regions on their screen and automates interactions by capturing mouse coordinates, defining regions, and updating region data.

Saved workflows can then be executed/automated by checking if saved screenshots of defined region
is on the screen within the specified coordinates, then click/interact like the user workflow.

Aim: To add ability to detect and execute keyboard keys and other mouse functionalities - i.e. scroll and drag.

### Features
- Pop-Up Script: Provides alerts and prompts for user input.
- Click-Assist: Detects mouse clicks and updates regions.
- Dynamic click coordinate updates: Updates saved center coordinate if clicked within a defined acceptable region.
- Users can define and name regions interactively.
- Captures screenshots of defined regions
- Choose Saved Workflow to Execute 

## How It Works
1. **Define Regions**:
   - Move your mouse around a clickable element in a square shape (anti-clockwise: top-left, bottom-left, bottom-right, top-right).
   - Pause for 2 seconds at each corner.
   - A pop-up will prompt you to name the defined region.
   - A screenshot at this region will be taken and stored.
   - NOTE: CONTINUE DEFINING SQUARE REGION AROUND ELEMENT TO INTERACT WITH UNTIL POP-UP APPEARS.

2. **Detect Clicks**:
   - The tool monitors mouse clicks within defined regions.
   - If a click is within the acceptable region boundary, the center coordinate of the region is updated.

3. **Save Data**:
   - Defined regions are saved in a JSON file, including their coordinates, center, and associated screenshot.
   - Screenshots of regions are captured and saved locally.
   
4 **Execute Workflow**:
   - Saved Workflows can then be executed
   - User selects which workflow to execute 
   - App executes each step of the workflow - detects regions, screenshots, click coordinates (based on information provided by User during Workflow capture) - to navigate through the workflow.

1. Follow on-screen instructions to define regions.
2. Click within defined regions to update coordinates dynamically.
3. Prompts appear identifying if the image at the defined region is important, and if the exact click coordinate is important.

## Setup
### Prerequisites
- Python 3.x
- install required libraries using pip install requirements.txt


## Fail-Safe
To exit the program at any time, move your mouse to the **top-left corner** of the screen.
