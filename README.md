# AutoAssistant

## Overview
(STILL IN INITIAL DEVELOPMENT)
AutoAssistant is a Python-based tool designed to automate workflow region identification and interaction. 
It currently allows users to define clickable regions on their screen and automates interactions by capturing mouse coordinates, defining regions, and updating region data.

AIM: To develop further to capture user workflows, then automate user workflows by checking if saved screenshot of defined region
is on the screen within the specified coordinates, then click/interact like the user workflow.

### Key Features
- Pop-Up Script: Provides alerts and prompts for user input.
- Click-Assist: Detects mouse clicks and updates regions.
- Dynamic click coordinate updates: Updates saved center coordinate if clicked within a defined acceptable region.
- Users can define and name regions interactively.
- Captures screenshots of defined regions

## How It Works
1. **Define Regions**:
   - Move your mouse around a clickable element in a square shape (anti-clockwise: top-left, bottom-left, bottom-right, top-right).
   - Pause for 2 seconds at each corner.
   - A pop-up will prompt you to name the defined region.

2. **Detect Clicks**:
   - The tool monitors mouse clicks within defined regions.
   - If a click is within the acceptable region boundary, the center coordinate of the region is updated.

3. **Save Data**:
   - Defined regions are saved in a JSON file, including their coordinates, center, and associated screenshot.
   - Screenshots of regions are captured and saved locally.

1. Follow on-screen instructions to define regions.
2. Click within defined regions to update coordinates dynamically.

## Setup
### Prerequisites
- Python 3.x
- Required Python libraries: `pyautogui`, `os`, `subprocess`, `json`


## Fail-Safe
To exit the program at any time, move your mouse to the **top-left corner** of the screen.
