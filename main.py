import streamlit as st
import io

# Pgae Info
st.set_page_config(page_title="Nexia Robotic Calibration Tool", page_icon="🤖"
)

# Header
st.title("Fanuc Calibration Data Tool")
st.write("Convert your 120cc calibrations to 200cc.\n\nUpload your .txt file, set your offsets, and download the updated version.\n\nVisit the Github repo for more information: https://github.com/jenaror/Nexia120ccTo200cc")

# Dictionary for Vial Sizes
vial_mapping = {
    "200cc":30,
    "250cc":32
}

# Sidebar for inputs
y_offset = st.number_input("Vertical Position Offset (mm)", value=8.0, step=.1, format="%.1f")
z_offset = st.number_input("Approach Position Offset (mm)", value=-3.0, step=.1, format="%.1f")
selected_vial_size = st.selectbox(
    "Vial size to convert to:",
        options=list(vial_mapping.keys())
)

# Grab the vial interget from the vial dictionary
target_vial_value = vial_mapping[selected_vial_size]
                        
updated_file_name = st.text_input("Output File Name (.txt added automatically)", value="Updated_Fanuc_Data")

uploaded_file = st.file_uploader("Choose a FanucCalData file", type="txt")

if abs(y_offset) > 20 or abs(z_offset) > 20:
    st.warning("⚠️ **Warning:** An offset larger than 20mm has been entered. Please verify this is intentional before running the robot.")

def write_human_summary(y_val, z_val):
    y_dir = "lower" if y_val >= 0 else "higher"
    z_dir = "closer to" if z_val >= 0 else "further from"
    
    summary_text = (
        f"Your **{selected_vial_size}** will be **{abs(y_val)}mm {y_dir}** "
        f"and **{abs(z_val)}mm {z_dir}** the dispenser "
        f"than your **120cc**."
    )
    
    return st.info(summary_text)

write_human_summary(y_offset, z_offset)

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
        if len(parts) > 2 and parts[1] == '{target_vial_value}' and parts[0] in ref_28_data:
            new_row = ref_28_data[parts[0]].copy()
            new_row[1] = '{target_vial_value}'
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
        file_name=updated_file_name + ".txt",
        mime="text/plain"
    )
    st.success("Processing complete! Click download above.")

            
    if st.checkbox("Show Preview of Changes"):
        st.subheader("Calibration Preview (First 5 Positions)")
    
        preview_count = 0
        # Loop through the output lines to find the updated '30' rows
        for line in output_lines:
            if "vial" in line.lower(): 
                continue
            
            parts = line.split('|')
        
            # Look for the target size rows to display
            if len(parts) > 5 and parts[1] == '{target_vial_value}':
                cabinet_pos = parts[0]
            
                # Fetch the original '28' row data we saved earlier
                if cabinet_pos in ref_28_data:
                    old_parts = ref_28_data[cabinet_pos]
                
                # Format the 120cc (Size 28) string using columns 3, 4, 5
                    str_120cc = f"**120cc** ➔ X: `{old_parts[3]}` | Y: `{old_parts[4]}` | Z: `{old_parts[5]}`"
                
                # Format the target string using columns 3, 4, 5
                    str_updated_cc = f"**{selected_vial_size}** ➔ X: `{parts[3]}` | Y: `{parts[4]}` | Z: `{parts[5]}`"
                
                # Print to the web app using markdown
                    st.markdown(f"#### Position: {cabinet_pos}")
                    st.markdown(f"- {str_120cc}")
                    st.markdown(f"- {str_updated_cc}")
                
                    preview_count += 1
                # Limit to 5 examples so it doesn't flood the web page
                    if preview_count >= 5:
                        break

