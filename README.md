# FindIt - Documentation

## Intro
FindIt is a command-line application that allows you to search for a string within the blobs contained in an Azure Blob Storage container (emulated with Azurite).
The results found are saved to Azure Table Storage and can be exported in CSV format.

## Main Features 🔧
- Easily connect to an Azurite instance and manage blob containers and files: emulating Azure Blob Storage

- Scan all blobs in a specific container for a target text string

- Automatic file type recognition (.txt, .csv, .json)

- Save matches to Azure Table Storage with CSV export support

- Interactive CLI interface powered by click with input validation

- Display info, warnings, and errors with styled formatting and logging for traceability.

## Prerequisites
```text
Software: Python 3.9+ - Visual Studio Code with Azurite extension
Libraries: azure-storage-blob, azure-data-tables, click, rich
```

## Project structure
```text
findit/
│
├── __main__.py            # Entry point: launches the CLI application
├── config.py              # Configuration variables (e.g., connection strings)
├── scanner.py             # Logic to scan/search blobs in Azure Storage
├── logger_config.py       # Logger setup and configuration
├── exporter.py            # Function to export Azure Table to CSV
├── parser.py              # Utilities to parse file contents (CSV, JSON)
├── storage.py             # Azure Storage client helpers (blob, tables, containers)
├── upload_to_container.py # Module to insert blobs into the container
```









