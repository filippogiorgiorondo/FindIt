import json
import csv
import io
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from logger_config import setup_logger
from urllib.parse import quote

from rich.console import Console
from rich.table import Table

logger = setup_logger(__name__)
console = Console()

# === Searches for a query within the content of a blob ===
def search_blob_content(container_name, blob_name, blob_service_client, query, table_client, ignore_case=False):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        content = blob_client.download_blob().content_as_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error reading blob '{blob_name}': {e}")
        console.print(f"[bold red]Error reading blob '{blob_name}':[/] {e}")
        return []

    # Detect file format
    if blob_name.endswith('.json'):
        lines = extract_json_strings(content)
    elif blob_name.endswith('.csv'):
        lines = extract_csv_strings(content)
    else:
        lines = content.splitlines()  # plain text

    # Search for query
    if ignore_case:
        matches = [line for line in lines if query.lower() in line.lower()]
    else:
        matches = [line for line in lines if query in line]

    found = []
    if matches:
        logger.info(f"Found matches in blob '{blob_name}':")
        console.print(f"[bold green]Matches found in '{blob_name}':[/]")
        for match in matches:
            logger.info(f" → {match}")
            console.print(f"[green] → {match}[/]")
            save_result_to_table(blob_name, query, match, table_client)
            found.append((blob_name, match))
    else:
        logger.info(f"No matches found in '{blob_name}' for query '{query}'.")
        console.print(f"[yellow]No matches found in '{blob_name}'.[/]")
    return found

# === Extracts all non-empty cell strings from CSV content ===
def extract_csv_strings(content):
    result = []
    reader = csv.reader(io.StringIO(content))
    for row in reader:
        result.extend(cell.strip() for cell in row if cell.strip())
    return result

# === Recursively extracts all strings from JSON content ===
def extract_json_strings(content):
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
        logger.error("Invalid JSON file.")
        console.print("[bold red]Invalid JSON file.[/]")
    return result

# === Saves a result match into Azure Table Storage ===
def save_result_to_table(blob_name: str, query: str, match: str, table_client):
    now = datetime.now(timezone.utc)

    # Ensure blob_name is safely encoded
    safe_blob_name = quote(str(blob_name), safe='')

    entity = {
        "PartitionKey": "SearchResults",
        "RowKey": f"{safe_blob_name}_{now.timestamp()}",
        "ScanTime": now.isoformat(),
        "BlobName": blob_name,
        "Query": query,
        "Match": match[:250],
    }

    try:
        table_client.create_entity(entity=entity)
    except Exception as e:
        logger.error(f"Failed to save result to Table Storage: {e}")
        console.print(f"[bold red]Failed to save result to Table Storage:[/] {e}")

# === Scans all blobs in a container looking for the query ===
def search_all_blobs(container_name, blob_service_client, query, table_client, ignore_case=False):
    logger.info(f"Scanning all blobs in container '{container_name}' for query: '{query}'")
    console.print(f"[blue]Scanning all blobs in container '{container_name}' for query: '{query}'[/]")
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()

    all_matches = []
    for blob in blob_list:
        found = search_blob_content(container_name, blob.name, blob_service_client, query, table_client, ignore_case)
        all_matches.extend(found)

    if all_matches:
        table = Table(title="Matches Found")
        table.add_column("Blob", style="cyan")
        table.add_column("Query", style="magenta")
        table.add_column("Match", style="green")

        for blob_name, match in all_matches:
            table.add_row(blob_name, query, match)

        console.print(table)
    else:
        console.print("[bold yellow]No results found.[/]")
