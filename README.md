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
### Calculating the offset

### Retrieving the Cal Data file

### Setting the offsets

### Loading the Cal Data file
Navigate to the web tool at https://nexiacaldata.streamlit.app Set your offsets (in millimeters) on the right side. Export the Fanuc Cal Data from Robotic Filling Manager and upload the .txt file to the tool. Download the modified file. In RFM, you will have to manually delete the 200cc positions before uploading the modified file. Make sure you hit close after deleting the 200cc positions to save them as empty (RFM will not override existing postions by uploading a calibration file). 
