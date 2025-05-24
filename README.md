# FindIt - Documentation 🔍

## Table of Contents 📌

- [Intro](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#intro-)
- [Problem vs Solution](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#problem-vs-solution-)
- [Main Features](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#main-features-)
- [Flowchart Overview](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#flowchart-overview)
- [How to use it](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#how-to-use-it)
- [Project structure](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#project-structure-)
- [Prerequisites](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#prerequisites-)
- [Installation](https://github.com/filippogiorgiorondo/FindIt?tab=readme-ov-file#installation-%EF%B8%8F)

## Intro 📚 
FindIt is a command-line application that allows you to search for a string within the blobs contained in an Azure Blob Storage container (emulated with Azurite).
The results found are saved to Azure Table Storage and can be exported in CSV format.

## Problem vs Solution 💡
Searching for a specific string across a large number of files (e.g. logs, exports, reports) can be extremely time-consuming and error-prone, especially when files are stored in the cloud. Manual inspection of .txt, .json, or .csv files is inefficient and does not scale.

Whether you're debugging logs or scanning reports for key terms, FindIt speeds up the process and integrates smoothly with cloud infrastructure.

## Main Features 🚀 
- Easily connect to an Azurite instance and manage blob containers and files: emulating Azure Blob Storage

- Scan all blobs in a specific container for a target text string

- Automatic file type recognition (.txt, .csv, .json)

- Save matches to Azure Table Storage with CSV export support

- Interactive CLI interface powered by click with input validation

- Display info, warnings, and errors with styled formatting and logging for traceability.

## Flowchart: Overview 📈
![UML Preview](UML.png)

## How to use it 💻 
- For an interactive prompt
```text
python __main__.py
```
- Run with arguments
```text
python search_blobs.py --container mio-container --table searchresults --query error --ignore-case y --export-csv results.csv
```
Where
```text
--container <example>         -> Name of the blob container to search
--table <example>             -> Table name to save results
--query <example>             -> String to search
--ignore-case <y> / <N>       -> Ignore case in search
--export-csv <example.csv>    -> Export the table results to a csv file with the specified name
```
- Example
![CLI Preview](findit.png)

## Project structure 📁
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

## Prerequisites 📦
```text
Software: Python 3.9+ - Visual Studio Code with Azurite extension installed
Libraries: azure-storage-blob, azure-data-tables, click, rich
```
## Installation ⚙️
1. Make sure you satisfy requisites
```text
https://www.python.org/downloads/                -> To install Python
https://code.visualstudio.com/download           -> To install VS Code
Ctrl + Shift + X > Search 'Azurite' > Install    -> In VS Code to install Azurite Extension
```
2. Start Azurite from VS Code
```text
Ctrl + Shift + P > Digit '>Azurite: Start'
```
3. Upload blobs into the container
```text
Make sure to have some test files in the same folder where you're running the scripts.

By default, the script will:
- Create a container named mio-container (if it doesn't already exist)
- Upload a sample file named log.txt
```
4. Search for a string inside the uploaded blobs. You can do it in two ways. 
```text
python __main__.py
```
And fill in the fields required by the program. Or do the following line:
```text
python search_blobs.py --container mio-container --table searchresults --query error --ignore-case y --export-csv results.csv
```
