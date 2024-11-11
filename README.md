# streamExcel Light - Excel to JSON/XML Converter

A powerful web application that processes Excel files and converts them to JSON
and XML formats with an interactive data preview interface.

## Features

- Interactive web interface built with Streamlit
- Excel file upload and processing
- Interactive data table with pagination, sorting, and filtering
- Automatic data type detection and standardization
- JSON and XML output generation
- Preview capabilities for processed data
- REST API backend powered by FastAPI

### Technical Stack

- Python 3.11.10
- FastAPI - Backend API
- Streamlit - Frontend Interface
- Pandas - Data Processing
- AgGrid - Interactive Data Table
- XML/JSON - Output Formats

### Docker Setup

Run the application using Docker:

1. Build and start the containers:

```bash
docker-compose up --build
```

2. Access the applications:

- Frontend UI: `http://localhost:8501`
- Backent API: `http://localhost:8000`

The output directory is mounted locally, so you can find your processed files in
the ./output folder.

### Setup without Docker

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the FastAPI backend:

```bash
uvicorn main:app --reload --port 8000
```

3. Run the Streamlit frontend:

```bash
streamlit run app.py
```

### Usage

1. Access the web interface through your browser
2. Upload an Excel file using the drag-and-drop interface
3. Review and edit data in the interactive table
4. Click "Upload and Process" to generate JSON and XML outputs
5. View the processed data in the JSON and XML preview tabs

### API Endpoints

- `POST /upload/`: Accepts Excel files and returns processed JSON and XML data

### Data Processing Features

- Header standardization to lowercase and snake case
- Intelligent data type detection and conversion
- Special handling for:
  - Date/time fields
  - IDs and unique identifiers
  - Boolean values
  - Numeric data
  - Text fields

### Output

- JSON and XML files are saved in the output directory
- Preview of processed data is available in the web interface
- Standardized data format for consistent output

### Requirements

- Python 3.11.10
- Modern web browser
- Network access for API communication

### Directory Structure

├── app.py # Streamlit frontend application ├── main.py # FastAPI backend server
├── output/ # Generated JSON and XML files └── logo.png # Application logo

### Data Validation

The application includes robust validation for both JSON and XML outputs:

- JSON validation ensures proper data structure
- XML validation confirms well-formed documents
- Error handling for malformed data

### UI Features

- Wide layout optimization
- Expandable sidebar with instructions
- Custom styling with blue borders and text
- Material theme for data grid
- Responsive design
- Loading indicators during processing

### Error Handling

- Graceful error handling for file uploads
- Clear error messages for users
- Exception catching for data processing
- HTTP status code responses

### Development

To contribute to this project:

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

### Security Considerations

- Input validation for file uploads
- Safe file handling
- Sanitized data processing
- Protected API endpoints

### Performance

- Efficient data processing with Pandas
- Pagination for large datasets
- Optimized memory usage
- Fast data conversion

### License

MIT License

### Support

For support, please open an issue in the repository.
