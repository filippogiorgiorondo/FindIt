import csv
import io
import json

# === Extracts all non-empty cell strings from CSV content ===
def extract_csv_strings(content: str) -> list[str]:
    
    result = []
    reader = csv.reader(io.StringIO(content))
    for row in reader:
        result.extend(cell.strip() for cell in row if cell.strip())
    return result

# === Recursively extracts all strings from JSON content ===
def extract_json_strings(content: str) -> list[str]:

    result = []

    def extract(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                extract(value)
        elif isinstance(obj, list):
            for item in obj:
                extract(item)
        elif isinstance(obj, str):
            result.append(obj.strip())

    try:
        json_obj = json.loads(content)
        extract(json_obj)
    except json.JSONDecodeError:
        print("Invalid JSON file.")
    return result
