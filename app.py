import streamlit as st
st.title("🚀 It’s Alive!")
import pandas as pd
from main import validate_input_file, compare_files, create_templates

# Generate templates locally when app starts
create_templates()

st.set_page_config(page_title="Premium Comparison App", layout="centered")
st.title("Premium Comparison App")

# Add download buttons for templates
with st.expander("📥 Download Templates", expanded=True):
    with open("Census_Template.xlsx", "rb") as census_file:
        st.download_button("Download Census File Template", census_file, file_name="Census_Template.xlsx")

    with open("Carrier_Template.xlsx", "rb") as carrier_file:
        st.download_button("Download Carrier File Template", carrier_file, file_name="Carrier_Template.xlsx")

# Upload Section
st.markdown("### Upload Files Below")
census_file = st.file_uploader("Upload Census File", type=["csv", "xlsx"])
carrier_file = st.file_uploader("Upload Carrier File", type=["csv", "xlsx"])

if census_file and carrier_file:
    try:
        df_census = pd.read_excel(census_file) if "xlsx" in census_file.name else pd.read_csv(census_file)
        df_carrier = pd.read_excel(carrier_file) if "xlsx" in carrier_file.name else pd.read_csv(carrier_file)

        required_census_columns = ['FIRST NAME', 'LAST NAME', 'TOTAL PREMIUM']
        required_carrier_columns = ['FIRST NAME', 'LAST NAME', 'CARRIER PREMIUM']

        validate_input_file(df_census, required_census_columns, "Census File")
        validate_input_file(df_carrier, required_carrier_columns, "Carrier File")

        result = compare_files(df_census, df_carrier)
        st.success("✅ Comparison completed successfully!")
        st.dataframe(result)

        st.download_button("📄 Download Results as CSV", result.to_csv(index=False), file_name="Comparison_Results.csv")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
