# Acessflow

A FastAPI-based file handling pipeline designed for cloud deployment.

## Description

Acessflow is a cloud-ready file processing application built with FastAPI, PostgreSQL, and SQLAlchemy. It provides a robust pipeline for handling file operations with database integration.

## Requirements

- Python 3.13 or higher
- `fastapi>=0.135.3`
- `uvicorn>=0.44.0`
- `sqlalchemy>=2.0.49`
- `psycopg[binary]>=3.3.3`

## Project Structure

```
acessflow/
├── main.py           # Main FastAPI application
├── pyproject.toml    # Project configuration and dependencies
└── README.md         # This file
```

## Configuration

Database connection and other configurations should be set up in environment variables before deployment.
