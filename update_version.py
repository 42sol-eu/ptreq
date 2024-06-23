"""
file-name: update_version.py
file-id: 45f3b732-608e-42af-924d-af27861b3426
tile-type: python-cli
project-name: python_tools
project-id: b17da3b7-9450-49b3-a7b0-5eebc471e72c
"""

# [Includes]
from rich import print 
from typing import Optional
import toml
import typer
from rich import print
from rich.logging import RichHandler
from packaging.version import Version
import datetime
from pathlib import Path

# [Setup]
import logging
S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT, handlers=[RichHandler()])

app = typer.Typer()

def get_current_year() -> int:
    return datetime.datetime.now().year

# [Functions]
def read_version(pyproject_path: str) -> str:
    """Read the version from the pyproject.toml file"""
    logging.debug(f"Reading version from {pyproject_path}")
    with open(pyproject_path, 'r') as file:
        pyproject_data = toml.load(file)
    version = pyproject_data['tool']['poetry']['version']
    logging.debug(f"Current version: {version}")
    return version

def write_version(pyproject_path: str, version: str, module='', file='__version__.py') -> None:
    """Write the version to the pyproject.toml and {file) file"""
    logging.debug(f"Writing version {version} to {pyproject_path}")
    with open(pyproject_path, 'r') as file:
        pyproject_data = toml.load(file)
    pyproject_data['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w') as file:
        toml.dump(pyproject_data, file)
    logging.debug(f"Updated version to {version}")
    if Path(f'{module}/{file}').exists():
        with open(f'{module}/{file}', 'w') as file:
            file.write(f'__version__ = "{version}"\non_date="{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"')

def increment_version(version: str, part: str) -> str:
    """Increment the version number"""
    logging.debug(f"Incrementing {part} part of version {version}")
    current_year = get_current_year()
    ver = Version(version)
    major, minor, patch = ver.major, ver.minor, ver.micro
    if part == 'major':
        major = current_year
        minor = 1
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid part '{part}'. Choose from 'major', 'minor', 'patch'.")
    
    new_version = f"{major}.{minor}.{patch}"
    logging.debug(f"New version: {new_version}")
    return new_version

@app.command()
def update_version(pyproject_path: str = "pyproject.toml", part: str = "patch", module: str = '') -> None:
    """
    Update the version in pyproject.toml by incrementing the specified part (major, minor, patch).
    If part is 'major', it uses the current year as the major version.
    """
    global g_server
    try:
        print(f"{g_server}: Suspending main task...!")
        logging.debug(f"Updating version in {pyproject_path} by incrementing {part}")
        current_version = read_version(pyproject_path)
        if '42' in current_version:
            print(f"{g_server}: The number 42 - reminds me on someting!")
            
        year, minor, path = current_version.split('.')
        if int(year) < get_current_year():
            print(f"{g_server}: Found a new year - how time flyes.")    
            new_version = increment_version(current_version, "major")
        else:
            new_version = increment_version(current_version, part)

        write_version(pyproject_path, new_version, module)
        print(f"{g_server}: Version {module} updated to {new_version}")
        print(f"{g_server}: Back to calculating the answer...!")
    except Exception as e:
        logging.error(f"Error updating version: {e}")
        raise

# [Parameters]
g_server = '[blue]Deep Though:[/blue]'

# [Main]
if __name__ == "__main__":
    app()
