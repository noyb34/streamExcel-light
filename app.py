import pandas as pd
import requests
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Configurable API URL
API_URL = "http://localhost:8000"

# Set Streamlit page configuration
st.set_page_config(
    page_title="streamExcel",
    page_icon="🌟",  # Optional: Add a page icon
    layout="wide",  # Set the layout to wide
    initial_sidebar_state="expanded",  # Optional: Sidebar starts expanded
)

# Add logo and instructions in the sidebar
st.sidebar.image(
    "logo.png",  # Path to your logo file
    use_column_width=True,  # Adjust the logo to fit the sidebar width
)
st.sidebar.title("Instructions")
st.sidebar.markdown(
    """
    1. **Drag and drop** your Excel file in the uploader.
    2. Review and edit the data table:
       - Use pagination, sorting, and filtering.
    3. Click **Upload and Process** to process your file.
    4. View the output in the **JSON Preview** and **XML Preview** tabs.
    """
)

# Streamlit UI
st.title("Excel File Processor")

# Step 1: Drag and Drop File
uploaded_file = st.file_uploader(
    "Drag and drop your Excel file here", type=["xlsx", "xls"]
)

if uploaded_file:
    # Step 2: Display interactive table with streamlit-aggrid
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        st.write("Interactive Table (Paginate, Sort, and Filter):")

        # Inject custom CSS for blue borders and text
        st.markdown(
            """
            <style>
            .custom-grid .ag-header-cell-label {
                color: blue !important; /* Blue header text */
                font-weight: bold;
            }
            .custom-grid .ag-cell {
                border: 2px solid blue !important; /* Blue cell border */
                color: blue !important; /* Blue cell text */
            }
            
            /* Optional: Add blue borders to the entire grid */
            .ag-root-wrapper {
                border: 2px solid blue !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Configure AgGrid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
        gb.configure_default_column(
            editable=True, sortable=True, filter=True
        )  # Enable sorting and filtering
        gb.configure_selection(selection_mode="disabled")  # Disable row selection
        grid_options = gb.build()

        # Display AgGrid
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            height=400,
            width="100%",
            theme="material",  # Other themes: 'streamlit', 'balham', 'material'
            custom_css={"custom-grid": True},
        )

        # Optional: Get the modified DataFrame from AgGrid
        modified_df = pd.DataFrame(grid_response["data"])

        # Show a preview of the modified data
        st.write("Modified Table Preview (First 10 Rows):")
        st.dataframe(modified_df.head(20))

    except Exception as e:
        st.error(f"Error reading the file: {e}")

    # Step 3: Add Upload Button
    if st.button("Upload and Process"):
        with st.spinner("Uploading and processing..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            }
            response = requests.post(f"{API_URL}/upload/", files=files)

        if response.status_code == 200:
            result = response.json()
            st.success(result["message"])

            # Display JSON and XML previews
            tab1, tab2 = st.tabs(["JSON Preview", "XML Preview"])
            with tab1:
                st.write("JSON Data Preview:")
                st.json(result["data_preview"])

            with tab2:
                st.write("XML Data Preview:")
                st.code(result["xml_preview"], language="xml")
        else:
            st.error(f"Error: {response.json().get('detail')}")
