import json
import os
import re
import warnings
import xml.etree.ElementTree as ET
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


app = FastAPI()

# Define the output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# validation functions
def validate_json(json_string):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError as e:
        print(f"JSON validation error: {e}")
        return False


def validate_xml(xml_string):
    try:
        ET.fromstring(xml_string)
        return True
    except ET.ParseError as e:
        print(f"XML validation error: {e}")
        return False


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize header names to lowercase and snake case
    def standardize_header(header):
        header = header.strip()
        header = re.sub(
            r"[^0-9a-zA-Z]+", "_", header
        )  # Replace non-alphanumeric characters with "_"
        return header.lower()

    df.columns = [standardize_header(col) for col in df.columns]

    # Preprocess each column based on type and name
    for col in df.columns:
        if col == "max_right_end_date":
            # Directly convert to string without datetime parsing
            df[col] = df[col].fillna("").astype(str)
        elif "date" in col or "time" in col or col.endswith("_ts"):
            # Convert other datetime columns to strings
            df[col] = pd.to_datetime(
                df[col], errors="coerce", unit="ms" if col.endswith("_ts") else None
            )
            df[col] = df[col].apply(
                lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if pd.notna(x) else ""
            )
        elif col == "unique_id":
            # Preserve unique_id as a string
            df[col] = df[col].fillna("").astype(str)
        elif col.endswith("_id") and col != "unique_id":
            # Handle other ID columns as integers
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        elif df[col].dropna().apply(lambda x: isinstance(x, (int, float))).all():
            # Retain numeric columns
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        elif df[col].dropna().isin(["True", "False", "true", "false", 1, 0]).all():
            # Handle boolean-like columns explicitly
            df[col] = df[col].map(
                {
                    "True": True,
                    "False": False,
                    "true": True,
                    "false": False,
                    1: True,
                    0: False,
                }
            )
        else:
            # Handle all other columns as strings
            df[col] = df[col].fillna("").astype(str)

    return df


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Extract the file name without extension
        base_filename = os.path.splitext(file.filename)[0]
        # Read Excel file into a Pandas DataFrame
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))  # Dynamically handle structure

        # Preprocess the DataFrame
        processed_df = preprocess_dataframe(df)

        excel_data = processed_df

        # Convert DataFrame to JSON
        json_data = excel_data.to_json(orient="records")
        json_preview = processed_df.head(10).to_json(orient="records")

        if not validate_json(json_preview):
            raise HTTPException(status_code=400, detail="Invalid JSON data")
        # save the json file
        json_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}.json")
        with open(json_output_path, "w") as json_file:
            json_file.write(json_data)

        # Convert DataFrame to XML
        xml_data = processed_df.to_xml(root_name="data", row_name="record", index=False)
        if not validate_xml(xml_data):
            raise HTTPException(status_code=400, detail="Invalid XML data")

        xml_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}.xml")
        with open(xml_output_path, "w") as xml_file:
            xml_file.write(xml_data)

        return {
            "message": "File processed successfully",
            "data_preview": json_preview,
            "xml_preview": xml_data[:2500],
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
