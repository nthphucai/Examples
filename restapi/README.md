# RestAPI Project

## Overview

This project is a scaffold for building RESTful APIs using FastAPI. It includes essential middleware, exception handling, and a basic structure for organizing routes and services.

## Requirements

- Python 3.10
- Conda (for environment management)

## Installation

1. Create and activate a Conda environment:
   ```bash
   conda create --name productive-api python=3.10
   conda activate productive-api
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Run the application using the provided script:
   ```bash
   bash scripts/run_api.sh
   ```

## Notes

- Ensure that all dependencies listed in `requirements.txt` are installed before running the application.
- For production, update the `main.py` file to disable `reload` and `debug` modes.
