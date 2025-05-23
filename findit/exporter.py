import csv
from azure.data.tables import TableClient

# === Exports all entities from an Azure Table to a CSV file ===
def export_table_to_csv(table_client: TableClient, output_file: str):
    entities = table_client.list_entities()
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = None
        for entity in entities:
            if writer is None:
                # First row: headers (dictionary keys)
                headers = list(entity.keys())
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
            writer.writerow(entity)
    print(f"Table successfully exported to '{output_file}'.")

