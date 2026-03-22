import streamlit as st
import io

st.set_page_config(page_title="Nexia Robotic Calibration Tool", page_icon="🤖"
)

st.title("Fanuc Calibration Data Tool")
st.write("Convert your 120cc calibrations to 200cc.\n\nUpload your .txt file, set your offsets, and download the updated version.\n\nVisit the Github repo for more information: https://github.com/jenaror/Nexia120ccTo200cc")

# Sidebar for inputs
y_offset = st.number_input("Vertical Position Offset (mm)", value=8.0, step=.1, format="%.1f")
z_offset = st.number_input("Approach Position Offset (mm)", value=-3.0, step=.1, format="%.1f")
updated_file_name = st.text_input("Output File Name (.txt added automatically)", value="Updated_Fanuc_Data")

uploaded_file = st.file_uploader("Choose a FanucCalData file", type="txt")

# Preview
if y_offset < 0:
    st.write("Your 200cc bottle will be " + str(y_offset) + "mm lower than your 120cc bottle")
if y_offset == 0:
    st.write("Your 200cc bottle calibration will not change")
else:
    st.write("Your 200cc bottle will be " + str(y_offset) + "mm higher than your 120cc bottle")




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

    if st.checkbox("Show Preview of Changes"):
    import pandas as pd
    # Show the first 10 modified rows as a sample
    preview_data = [line.split('|') for line in output_lines if '|30|' in line]
    df = pd.DataFrame(preview_data).iloc[:10] # Show first 10
    st.table(df)

    # Prepare for download
    final_output = "\n".join(output_lines)
    st.download_button(
        label="Download Updated File",
        data=final_output,
        file_name=updated_file_name + ".txt",
        mime="text/plain"
    )
    st.success("Processing complete! Click download above.")
