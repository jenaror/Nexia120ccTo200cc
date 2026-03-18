import streamlit as st
import io

st.set_page_config(page_title="Nexia Robotic Calibration Tool", page_icon="🤖")

st.title("Fanuc Calibration Data Tool")
st.write("Convert your 120cc calibrations to 200cc.\nUpload your .txt file, set your offsets, and download the updated version.\nVisit the Github repo for more information: https://github.com/jenaror/Nexia120ccTo200cc")

# Sidebar for inputs
y_offset = st.number_input("Vertical Position Offset (in mm)", value=8.0)
z_offset = st.number_input("Approach Position Offset (in mm)", value=-3.0)

uploaded_file = st.file_uploader("Choose a FanucCalData file", type="txt")

if uploaded_file is not None:
    # Read the file content
    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.splitlines()
    
    ref_28_data = {}
    # Pass 1: Collect reference 28s
    for line in lines:
        if "vial" in line.lower(): continue
        parts = line.split('|')
        if len(parts) > 2 and parts[1] == '28':
            ref_28_data[parts[0]] = parts

    # Pass 2: Update 30s
    output_lines = []
    for line in lines:
        if "vial" in line.lower():
            output_lines.append(line)
            continue
            
        parts = line.split('|')
        if len(parts) > 2 and parts[1] == '30' and parts[0] in ref_28_data:
            new_row = ref_28_data[parts[0]].copy()
            new_row[1] = '30'
            new_row[4] = f"{float(new_row[4]) + y_offset:.6f}"
            new_row[5] = f"{float(new_row[5]) + z_offset:.6f}"
            output_lines.append('|'.join(new_row))
        else:
            output_lines.append(line)

    # Prepare for download
    final_output = "\n".join(output_lines)
    st.download_button(
        label="Download Updated File",
        data=final_output,
        file_name="Updated_Fanuc_Data.txt",
        mime="text/plain"
    )
    st.success("Processing complete! Click download above.")
