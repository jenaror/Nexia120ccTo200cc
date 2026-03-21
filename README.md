# Nexia120ccTo200cc

***https://nexiacaldata.streamlit.app***

This tool allows you to convert Nexia/RFM 120cc calibrations to 200cc calibrations with an X and Z offset. 

## What this does
This tool takes a Fanuc Cal Data .txt file from Robotic Filling Manager and modifies it. It will copy all the dispenser position data for 120cc and copy it to 200cc with a user defined offset. This means if C1R1S1 is calibrated at 100,100,10 for 120cc, the tool will add the 200cc calibration and set it for 100, 108, 7. It will do this for ALL dispenser positions. 

## What this tool DOESN'T do
This tool will not modify any position that's not a dispenser position, meaning it won't modify vial pickup or dropoff, or maintenance/home positions. 

This tool cannot convert 200cc positions to 120cc positions. 

## Why you would use this tool
If you calibrated the robot manually for 120cc and don't want to manually offset all the positions to match the bigger vial size for 200cc, this tool will apply the offset in seconds. 

## How to use this tool

### Prepping the calibrations
The robot should be fully calibrated for 120cc bottles at all positions, including pick up and drop off. The robot should also be separetly calibrated for the 200cc pick and drop off. Follow standard procedure for getting these calibrations.

### Calculating the offset
To calculate the offset, we need to find the difference in height from where the bottle sits in the robot grippers. First pick up a 120cc bottle from the pick up position via the calibration menu, then measure the distance from the top of the bottle to the top of the gripper fingers. Do the same for 200cc and calculate the difference in height to get your offset.

Perform the same procedure but this time measuring the distance from the base of the gripper fingers to center of the bottle between the two sizes. The difference in distances is how much the 200cc bottles sticks out further than the 120cc bottles.

### Retrieving the Cal Data file

### Setting the offsets

### Loading the Cal Data file
Navigate to the web tool at https://nexiacaldata.streamlit.app Set your offsets (in millimeters) on the right side. Export the Fanuc Cal Data from Robotic Filling Manager and upload the .txt file to the tool. Download the modified file. In RFM, you will have to manually delete the 200cc positions before uploading the modified file. Make sure you hit close after deleting the 200cc positions to save them as empty (RFM will not override existing postions by uploading a calibration file). 
