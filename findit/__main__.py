import click
from config import connection_string, table_connection_string
from scanner import search_all_blobs
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, TableClient
from logger_config import setup_logger
import re
import csv

logger = setup_logger(__name__)

# === Validates the container name format according to Azure rules ===
def validate_container_name(ctx, param, value):
    if not value:
        raise click.BadParameter("Container name is required.")
    pattern = r'^[a-z0-9]([a-z0-9\-]{1,61}[a-z0-9])?$'
    if not re.match(pattern, value):
        raise click.BadParameter(
            "Invalid container name. It must be 3-63 characters long, use only lowercase letters, numbers, and dashes, "
            "and must start and end with a letter or number."
        )
    return value

# === Validates the table name format according to Azure rules ===
def validate_table_name(ctx, param, value):
    if not value:
        raise click.BadParameter("Table name is required.")
    pattern = r'^[A-Za-z][A-Za-z0-9_]{2,62}$'
    if not re.match(pattern, value):
        raise click.BadParameter(
            "Invalid table name. It must be 3-63 characters long, start with a letter, "
            "and contain only letters, numbers, and underscores."
        )
    return value

# === Ensures the search query is not empty ===
def validate_query(ctx, param, value):
    if not value or not value.strip():
        raise click.BadParameter("Query cannot be empty.")
    return value.strip()

# === Parses yes/no input to a boolean value ===
def parse_ignore_case(value):
    # Accept y/n as input in prompt
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in ['y', 'yes', 'true', '1']:
        return True
    elif value in ['n', 'no', 'false', '0']:
        return False
    else:
        raise click.BadParameter("Invalid answer, use y/n")

# === Exports the contents of a table to a CSV file ===
def export_table_to_csv(table_client: TableClient, output_file: str):
    entities = table_client.list_entities()
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = None
        for entity in entities:
            if writer is None:
                headers = list(entity.keys())
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
            writer.writerow(entity)
    print(f"[INFO] Table successfully exported to '{output_file}'.")

# === CLI entry point for querying blobs and storing results in a table ===
@click.command()
@click.option('--container', prompt='Container name', callback=validate_container_name, help='The name of the blob container to use')
@click.option('--table', prompt='Table name', callback=validate_table_name, help='The name of the table to store the results')
@click.option('--query', prompt='Search query', callback=validate_query, help='The string to search for in the blobs')
@click.option('--ignore-case', prompt='Ignore case? (y/n)', callback=lambda ctx, param, val: parse_ignore_case(val), default=False, help='Ignore case differences in the query')
@click.option('--export-csv', prompt='CSV file name to export (leave blank to skip)', default='', help='Path to a CSV file to export table results')
def cli(container, table, query, ignore_case, export_csv):
    """Program to search a query string in Azure Blob Storage and store the results in Azure Table Storage."""

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        table_service = TableServiceClient.from_connection_string(table_connection_string)
        table_client = table_service.get_table_client(table)
        try:
            table_client.create_table()
            logger.info(f"Table '{table}' created (or already exists).")
        except Exception:
            logger.info(f"Table '{table}' already exists.")

        search_all_blobs(container, blob_service_client, query, table_client, ignore_case)

        if export_csv:
            export_table_to_csv(table_client, export_csv)

    except Exception as e:
        logger.error(f"Execution error: {e}")

if __name__ == '__main__':
    cli()
