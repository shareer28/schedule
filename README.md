# Metric Data Uploader

Metric Data Uploader is a full-stack application designed to facilitate the upload, inspection, and management of metric data for organizations. The project consists of a FastAPI-based backend and a modern React frontend, providing a seamless workflow for users to upload files, interact with data, and integrate with Google Sheets.

---

## Project Overview

- **Backend:** Python 3.8+, FastAPI, DuckDB, Google Sheets integration
- **Frontend:** React, TypeScript, Vite, modern UI components
- **Purpose:** Enable organizations to upload, validate, and manage metric data efficiently, with support for data mapping, inspection, and reference.

---

## Architecture

```
[User] ⇄ [React Frontend (Vite)] ⇄ [FastAPI Backend] ⇄ [DuckDB, Google Sheets]
```

- The **frontend** provides a user-friendly interface for uploading files, inspecting data, and managing organizations.
- The **backend** exposes RESTful APIs for file handling, data processing, and integration with Google Sheets and DuckDB for storage and analytics.

---

## Backend (FastAPI)

The backend is implemented in Python using FastAPI, providing robust APIs and integrations.

- **Key Features:**
  - RESTful API endpoints for files, organizations, and specialisms
  - Google Sheets integration for data synchronization
  - DuckDB for efficient data storage and querying
  - Modular structure with routers, services, and models

- **Project Structure:**
  - `app/` — Main application code
    - `main.py` — FastAPI entry point
    - `core/` — Configuration and environment management
    - `google/sheets/` — Google Sheets API integration
    - `models/` — Pydantic models for data validation
    - `routers/` — API route definitions
    - `services/` — Business logic and data operations
    - `utils.py` — Utility functions
    - `agents.py` — Background/async task logic
    - `duckdb.py` — DuckDB integration
  - `data/` — CSV files for mapping, examples, and parsed data
  - `notebooks/` — Jupyter notebooks for prototyping and documentation

- **Setup:**
  1. Install Python 3.8+ and the `uv` package manager.
  2. Create a virtual environment and install dependencies:
      ```bash
      uv venv create
      source venv/bin/activate
      uv install
      ```
  3. Configure Google Sheets credentials and environment variables (see `back-end/README.md` for details).
  4. Run the development server:
      ```bash
      uv run fastapi dev --reload
      ```
  5. Access the API docs at `http://127.0.0.1:8000/docs`.

For more details, see [back-end/README.md](back-end/README.md).

---

## Frontend (React + Vite)

The frontend is a modern React application built with Vite for fast development and optimized builds.

- **Key Features:**
  - File upload and validation UI
  - Data inspection and reference pages
  - Organization management
  - Responsive design and modern UI components

- **Project Structure:**
  - `src/` — Source code (components, pages, hooks, utils)
  - `public/` — Static assets
  - `vite.config.ts` — Vite configuration

- **Setup:**
  1. Install Node.js (v16+) and Yarn or npm.
  2. Install dependencies:
      ```bash
      yarn install
      # or
      npm install
      ```
  3. Start the development server:
      ```bash
      yarn dev
      # or
      npm run dev
      ```
  4. Open [http://localhost:5173](http://localhost:5173) in your browser.

For more details, see [front-end/README.md](front-end/README.md).

---

## Getting Started

1. Clone the repository and set up both the backend and frontend as described above.
2. Configure environment variables and credentials as needed.
3. Start both servers and access the application via the frontend URL.
