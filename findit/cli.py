# Module containing the CLI for the program

import click  # Library for building terminal interfaces
from pathlib import Path  # For handling filesystem paths as objects

# Define the CLI command
@click.command()

# Text to search for (prompted if not provided)
@click.option('--query', prompt="What are you looking for?", help="The text you want to find.")

# Directory in which to search (default is current directory)
@click.option('--path', default='.', type=click.Path(exists=True, file_okay=False), help="Directory to search in.")

# Comma-separated list of file extensions to search in (e.g. .txt,.log). If not specified, default is used.
@click.option('--ext', default=None, help="Comma-separated list of file extensions (e.g. .txt,.csv).")

# Optional flag to ignore case in the search
@click.option('--ignore-case', is_flag=True, default=False, help="Ignore case when searching for the query.")
def cli(query, path, ext, ignore_case):
    """Search for a keyword in all files with specified extensions inside the given directory."""

    # Use default extensions if none are provided
    if ext is None:
        extensions = ['.txt', '.csv', '.log', '.json']
    else:
        extensions = [e.strip() for e in ext.split(',') if e.strip()]

        # Ensure each extension starts with a dot
        for e in extensions:
            if not e.startswith('.'):
                click.echo(f"Invalid extension '{e}'. All extensions must start with a '.'")
                return

    base_path = Path(path)

    # Collect all files matching the extensions
    all_files = []
    for extension in extensions:
        all_files.extend(base_path.rglob(f'*{extension}'))

    if not all_files:
        click.echo(f"No files found with extensions: {', '.join(extensions)}")
        return

    click.echo(f"Searching for '{query}' in: {base_path}")
    click.echo(f"Using extensions: {', '.join(extensions)}")

    found_any = False

    for file in all_files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Match lines according to case sensitivity
        if ignore_case:
            matching_lines = [line.strip() for line in lines if query.lower() in line.lower()]
        else:
            matching_lines = [line.strip() for line in lines if query in line]

        # If matches are found, print them
        if matching_lines:
            if not found_any:
                click.echo("\nSearch completed successfully. Results:")
            found_any = True
            click.echo(f"\n📄 {file}")
            for match in matching_lines:
                click.echo(f"   → {match}")

    if not found_any:
        click.echo("No matches found in any file.")
