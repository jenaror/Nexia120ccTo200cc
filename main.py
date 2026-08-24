import streamlit as st
import io

# Page Info
st.set_page_config(page_title="Nexia Robotic Calibration Tool", page_icon="🤖"
)

# Header
st.title("Fanuc Calibration Data Tool")
st.write("Convert your Fanuc vial calibrations from one size to another.\n\nUpload your .txt file, set your offsets, and download the updated version.\n\nVisit the Github repo for more information: https://github.com/jenaror/Nexia120ccTo200cc")

# Dictionary for Vial Sizes
# Maps a human-readable vial name to its numeric code in the cal data file (column 2, the "|xx|" field).
vial_mapping = {
    "120cc": 28,
    "200cc": 30,
    "250cc": 32,
    "z25": 23,
    "z30": 33,
}

vial_names = list(vial_mapping.keys())

# Source/target vial size selectors
col1, col2 = st.columns(2)
with col1:
    selected_source_vial_name = st.selectbox(
        "Vial size to convert FROM:",
        options=vial_names,
        index=0,
    )
with col2:
    # Default the target to a different entry than the source when possible
    default_target_index = 1 if len(vial_names) > 1 else 0
    selected_target_vial_name = st.selectbox(
        "Vial size to convert TO:",
        options=vial_names,
        index=default_target_index,
    )

# Grab the vial integers from the vial dictionary
source_vial_value = vial_mapping[selected_source_vial_name]
target_vial_value = vial_mapping[selected_target_vial_name]

if source_vial_value == target_vial_value:
    st.warning("⚠️ **Warning:** Source and target vial sizes are the same. Please select two different sizes above.")

# Sidebar for inputs
y_offset = st.number_input("Vertical Position Offset (mm)", value=8.0, step=.1, format="%.1f")
z_offset = st.number_input("Approach Position Offset (mm)", value=-3.0, step=.1, format="%.1f")

updated_file_name = st.text_input("Output File Name (.txt added automatically)", value="Updated_Fanuc_Data")

uploaded_file = st.file_uploader("Choose a FanucCalData file", type="txt")

if abs(y_offset) > 20 or abs(z_offset) > 20:
    st.warning("⚠️ **Warning:** An offset larger than 20mm has been entered. Please verify this is intentional before running the robot.")

def write_human_summary(y_val, z_val):
    y_dir = "lower" if y_val >= 0 else "higher"
    z_dir = "closer to" if z_val >= 0 else "further from"

    summary_text = (
        f"Your **{selected_target_vial_name}** will be **{abs(y_val)}mm {y_dir}** "
        f"and **{abs(z_val)}mm {z_dir}** the dispenser "
        f"than your **{selected_source_vial_name}**."
    )

    return st.info(summary_text)

write_human_summary(y_offset, z_offset)

if uploaded_file is not None and source_vial_value != target_vial_value:
    # Read the file content
    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.splitlines()

    source_ref_data = {}
    # Pass 1: Collect reference rows for the selected source vial size
    for line in lines:
        if "vial" in line.lower(): continue
        parts = line.split('|')
        if len(parts) > 2 and parts[1] == str(source_vial_value):
            source_ref_data[parts[0]] = parts

    # Pass 2: Update rows matching the selected target vial size
    output_lines = []
    updated_count = 0
    for line in lines:
        if "vial" in line.lower():
            output_lines.append(line)
            continue

        parts = line.split('|')
        if len(parts) > 2 and parts[1] == str(target_vial_value) and parts[0] in source_ref_data:
            new_row = source_ref_data[parts[0]].copy()
            new_row[1] = str(target_vial_value)
            new_row[4] = f"{float(new_row[4]) + y_offset:.6f}"
            new_row[5] = f"{float(new_row[5]) + z_offset:.6f}"
            output_lines.append('|'.join(new_row))
            updated_count += 1
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

    if updated_count > 0:
        st.success(f"Processing complete! Updated {updated_count} position(s). Click download above.")
    else:
        st.warning(
            f"No **{selected_target_vial_name}** rows matching a **{selected_source_vial_name}** position were found, "
            "so nothing was changed. Double-check that your file contains both vial size codes."
        )

    if st.checkbox("Show Preview of Changes"):
        st.subheader("Calibration Preview (First 5 Positions)")

        preview_count = 0
        # Loop through the output lines to find the updated target rows
        for line in output_lines:
            if "vial" in line.lower():
                continue

            parts = line.split('|')

            # Look for the target size rows to display
            if len(parts) > 5 and parts[1] == str(target_vial_value):
                cabinet_pos = parts[0]

                # Fetch the original source row data we saved earlier
                if cabinet_pos in source_ref_data:
                    old_parts = source_ref_data[cabinet_pos]

                    # Format the source vial string using columns 3, 4, 5
                    str_source = f"**{selected_source_vial_name}** ➔ X: `{old_parts[3]}` | Y: `{old_parts[4]}` | Z: `{old_parts[5]}`"

                    # Format the target string using columns 3, 4, 5
                    str_target = f"**{selected_target_vial_name}** ➔ X: `{parts[3]}` | Y: `{parts[4]}` | Z: `{parts[5]}`"

                    # Print to the web app using markdown
                    st.markdown(f"#### Position: {cabinet_pos}")
                    st.markdown(f"- {str_source}")
                    st.markdown(f"- {str_target}")

                    preview_count += 1
                    # Limit to 5 examples so it doesn't flood the web page
                    if preview_count >= 5:
                        break

        if preview_count == 0:
            st.write("No matching positions to preview.")