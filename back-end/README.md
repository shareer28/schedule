# FastAPI Project

## Getting Started with Development

This project is built using FastAPI. To start developing locally, follow these steps:


### Structure 
### Prerequisites

- Python 3.8 or higher installed
- `uv` package manager

### Installation

1. Create and activate a virtual environment using `uv`:

```bash
uv venv create
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install the required dependencies using `uv`:

```bash
uv install
```

This will install the dependencies specified in `uv.lock`.

### Running the Development Server

Run the FastAPI development server with:

```bash
uv run fastapi dev --reload
```

This will start the server at `http://127.0.0.1:8000` with auto-reload enabled for development.

## Structure

The project is organized as follows:

- `app/`  
  Main application code for the FastAPI backend.
  - `main.py`  
    Entry point for the FastAPI application.
  - `core/`  
    Core configuration and settings for the application.
    - `config.py`  
      Handles environment variables and application configuration.
  - `google/`  
    Integrations with Google services.
    - `sheets/`  
      Logic for interacting with Google Sheets.
      - `service.py`  
        Service functions for Google Sheets API.
  - `models/`  
    Pydantic models and data schemas for files, organizations, and specialisms.
  - `routers/`  
    API route definitions for different resources.
    - `files.py`, `organizations.py`, `specialisms.py`  
      Routers for handling respective endpoints.
  - `services/`  
    Business logic and service classes for handling core operations.
    - `file_service.py`, `organization_service.py`  
      Service logic for files and organizations.
  - `utils.py`  
    Utility functions used throughout the application.
  - `agents.py`  
    Agent logic for background or async tasks.
  - `api.py`  
    API initialization and route inclusion.
  - `duckdb.py`  
    Integration with DuckDB for data storage or querying.

- `data/`  
  Contains CSV files for data mapping, examples, and parsed data.

- `notebooks/`  
  Jupyter notebooks for data exploration, prototyping, or documentation.

- `.env.example`  
  Example environment variable file.

- `pyproject.toml`, `uv.lock`  
  Project dependencies and package management.

- `README.md`  
  Project documentation.
## Google Sheets Credentials

To enable Google Sheets integration, you need to set up credentials as follows:

- **credentials.json**:  
  Obtain this file from the [Google Cloud Console](https://console.cloud.google.com/) by creating OAuth 2.0 credentials for a Desktop application. Download the `credentials.json` file and place it in the project root directory.

- **token.pickle**:  
  This file is generated automatically after the first authentication. When you run the application for the first time, you will be prompted to log in with your Google account in a browser window. Upon successful authentication, `token.pickle` will be created to store your access and refresh tokens.

- **GOOGLE_SHEET environment variable**:  
  Set this variable in your `.env` file to specify the Google Sheet to use. Example:
  ```
  GOOGLE_SHEET=YOUR-GOOGLE-SHEET-ID
  ```
  (Note: Some sheet IDs may be hardcoded in the code. Check the relevant service files if you need to use a different sheet.)

**Summary of steps:**
1. Create OAuth 2.0 credentials in Google Cloud Console and download `credentials.json`.
2. Place `credentials.json` in the project root.
3. Set the `GOOGLE_SHEET` variable in your `.env` file.
4. On first run, complete the authentication flow in your browser to generate `token.pickle`.


### Additional Notes

- Make sure to check for any environment variables or configuration settings in `app/core/config.py`.
- Define the API endpoint information by setting environment variables inside the virtual environment. For example, after activating the virtual environment, you can create a `.env` file or export variables directly:

```bash
export API_HOST=127.0.0.1
export API_PORT=8000
```

- Alternatively, you can create a `.env` file in the project root with the following content:

```
API_HOST=127.0.0.1
API_PORT=8000
```

- Use the `/docs` endpoint in the browser to access the interactive API documentation.
