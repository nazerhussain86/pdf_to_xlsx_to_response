import streamlit as st
import pandas as pd
import json
from io import StringIO

st.set_page_config(page_title="HSN Excel → JSON", layout="wide")

st.title("HSN Excel → JSON Converter")

st.write(
    """
    Upload your Excel file containing HSN details.  
    The app will try to detect columns like:
    **S. NO, Chapter, HS Code, Description, Ministry/Department**, and keep all other columns too.
    """
)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

def detect_column(col_name: str) -> str | None:
    """
    Try to map raw Excel column names to standard names:
    sno, chapter, hsncode, description, ministry
    """
    c = col_name.lower().replace(" ", "").replace(".", "").replace("_", "")

    if "sno" in c or c == "sno":
        return "sno"
    if "chapter" in c:
        return "chapter"
    if ("hscode" in c) or ("hscode8" in c) or (c == "hsncode") or (c == "hsn"):
        return "hsncode"
    if "description" in c or "desc" in c:
        return "description"
    if "ministry" in c or "department" in c or "dept" in c:
        return "minister"
    return None

if uploaded_file is not None:
    # Read full Excel (first sheet by default – you can change sheet_name if needed)
    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Build rename map for known columns
    rename_map = {}
    for col in df.columns:
        mapped = detect_column(col)
        if mapped is not None:
            rename_map[col] = mapped

    # Rename detected columns (others stay as they are – "and more")
    df_renamed = df.rename(columns=rename_map)

    st.subheader("Normalized Data (with standard column names)")
    st.write(
        "Detected standard columns (if present): **sno, chapter, hsncode, description, minister**. "
        "All other columns are kept as-is."
    )
    st.dataframe(df_renamed.head())

    # Convert to JSON (array of objects)
    records = df_renamed.to_dict(orient="records")
    json_str = json.dumps(records, indent=2, ensure_ascii=False)

    st.subheader("JSON Preview")
    st.code(json_str[:2000] + ("\n...\n" if len(json_str) > 2000 else ""), language="json")

    # Download button
    st.download_button(
        label="⬇️ Download JSON file",
        data=json_str,
        file_name="hsn_data.json",
        mime="application/json",
    )
else:
    st.info("Please upload an Excel file to get started.")
