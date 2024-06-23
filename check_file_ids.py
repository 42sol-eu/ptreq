"""
file-name: check_file_ids.py
file-id: 9cef02c0-faf7-40a7-a672-dd51b995dd8e
tile-type: python-cli
project-name: python_tools
project-id: b17da3b7-9450-49b3-a7b0-5eebc471e72c
"""
# [Imports]
import os
import re
import uuid
from collections import defaultdict
from typing import List, Optional
import typer
from rich.console import Console
from rich.markdown import Markdown

# [Setup]
import logging
S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(format=S_LOG_MSG_FORMAT, level=logging.INFO)
console = Console()

# [Variables]
g_id_to_file = {}
g_file_to_id = {}

# [Functions]

def write_table_header() -> str:
    """
    Writes the table header for the output.
    
    :return: The table header in Markdown format.
    """
    return "| No | File-ID | File-Path | Remark |\n| --- | ------- | --------- | ------ |\n"

def find_file_ids(directory: str, filter_project : str = 'ptreq', use_color: bool = False) -> None:
    """
    Scans the given directory for text files, extracts file-ids, and outputs filenames with file-ids.
    Marks lines red if file-id is missing or duplicated.
    
    :param directory: Path to the directory to scan.
    """
    global g_id_to_file
    global g_file_to_id
    counter = 0

    logging.debug("find_file_ids() called with directory=%s", directory)

    file_ids = defaultdict(list)
    file_id_pattern = re.compile(r'file-id:\s*([0-9a-fA-F-]+)$', re.MULTILINE)
    project_ids = defaultdict(list)
    project_id_pattern = re.compile(r'project-id:\s*([0-9a-fA-F-]+)$', re.MULTILINE)
    project_names = defaultdict(list)
    project_name_pattern = re.compile(r'project-name:\s*(.+)$', re.MULTILINE)

    for root, _, files in os.walk(directory):
        for filename in files:
            # Get extension of file
            extension = filename.split(".")[-1]
            if extension in ['adoc', 'md', 'txt', 'py', 'sh']:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    content = file.read()
                    
                    match_project_id = project_id_pattern.search(content)
                    project_id = ''
                    if match_project_id:
                        project_id = match_project_id.group(1)
                        project_ids[filepath].append(project_id) 
                    else:
                        logging.warning("No project-id found in file: %s", filepath)
                    
                    match_project_name = project_name_pattern.search(content)
                    project_name = ''
                    if match_project_name:
                        project_name = match_project_name.group(1)
                        project_names[filepath].append(project_name) 
                    else:
                        logging.warning("No project-name found in file: %s", filepath)
                        

                    match = file_id_pattern.search(content)
                    if match:
                        file_id = match.group(1)
                        try:
                            uuid.UUID(file_id)
                            file_ids[file_id].append(filepath)
                            g_file_to_id[filepath] = file_id
                            g_id_to_file[file_id] = filepath
                        except ValueError:
                            logging.error("Invalid UUID found in file: %s", filepath)
                            file_ids[None].append(filepath)
                    else:
                        logging.warning("No file-id found in file: %s", filepath)
                        file_ids[None].append(filepath)

    data = write_table_header()
    if use_color:
        console.print(Markdown(data))

    for file_id, paths in file_ids.items():
        counter += 1
        if file_id is None:
            for path in paths:
                project_name = project_names[path][0]
                if filter_project == project_name:
                    line = f'| {counter} | Missing file-id | {path} | **{project_name}**, (no file-id found) |'
                    if use_color:
                        console.print(Markdown(line), style="blue")
                    data += line + '\n'
        elif len(paths) > 1:
            for path in paths:
                project_name = project_names[path][0]
                if filter_project == project_name:
                    line = f'| {counter} | {file_id} | {path} | **{project_name}**, (duplicated with {g_id_to_file[file_id]}) |'
                    if use_color:
                        console.print(Markdown(line), style="red")
                    data += line + '\n'
        else:
            project_name = project_names[paths[0]][0]
            if filter_project == project_name:
                line = f'| {counter} | {file_id} | {paths[0]} | **{project_name}** |'
                if use_color:
                    console.print(Markdown(line), style="green")
                data += line + '\n'

    # Output Markdown table
    if not use_color:
        console.print(Markdown(data))
    return data
    logging.info("Completed scanning the directory")
    logging.info("So long, and thanks for all the fish.")

# [Main]

def main(directory: str = typer.Argument(..., help="Directory to scan for text files")):
    """
    Main function to run the Typer CLI application.
    
    :param directory: Path to the directory to scan.
    """
    logging.debug("main() called with directory=%s", directory)
    find_file_ids(directory)

if __name__ == "__main__":
    typer.run(main)
