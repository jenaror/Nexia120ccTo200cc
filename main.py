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

def write_human_summary(y_val, z_val):
    y_dir = "lower" if y_val >= 0 else "higher"
    z_dir = "closer to" if z_val >= 0 else "further from"
    
    summary_text = (
        f"Your **200cc** will be **{abs(y_val)}mm {y_dir}** "
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
        
        # Look for the size '30' rows to display
        if len(parts) > 5 and parts[1] == '30':
            cabinet_pos = parts[0]
            
            # Fetch the original '28' row data we saved earlier
            if cabinet_pos in ref_28_data:
                old_parts = ref_28_data[cabinet_pos]
                
                # Format the 120cc (Size 28) string using columns 3, 4, 5
                str_120cc = f"**120cc** ➔ X: `{old_parts[3]}` | Y: `{old_parts[4]}` | Z: `{old_parts[5]}`"
                
                # Format the 200cc (Size 30) string using columns 3, 4, 5
                str_200cc = f"**200cc** ➔ X: `{parts[3]}` | Y: `{parts[4]}` | Z: `{parts[5]}`"
                
                # Print to the web app using markdown
                st.markdown(f"#### Position: {cabinet_pos}")
                st.markdown(f"- {str_120cc}")
                st.markdown(f"- {str_200cc}")
                
                preview_count += 1
                # Limit to 5 examples so it doesn't flood the web page
                if preview_count >= 5:
                    break

