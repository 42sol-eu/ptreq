# mongo_inserter/main.py

import logging                              # https://docs.python.org/3/library/logging.html
import os                                   # https://docs.python.org/3/library/os.html
from pymongo import MongoClient, errors     # https://pymongo.readthedocs.io/en/stable/
import click                                # https://click.palletsprojects.com/en/8.0.x/
from rich.console import Console            # https://rich.readthedocs.io/en/latest/
import yaml                                 # https://pyyaml.org/wiki/PyYAMLDocumentation
from typing import Any, Dict, List          # https://docs.python.org/3/library/typing.html
import re                                   # https://docs.python.org/3/library/re.html    

# [setup] Set up logging
S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(format=S_LOG_MSG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
console = Console()

# [functions]

def setup_mongo_client(uri: str) -> MongoClient:
    """
    Set up the MongoDB client.
    :param uri: MongoDB connection string
    :return: MongoClient instance
    """
    logger.debug(f"setup_mongo_client(uri={uri})")
    try:
        client = MongoClient(uri)
        logger.info("MongoDB client set up successfully.")
        return client
    except errors.ConnectionError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def insert_documents(client: MongoClient, db_name: str, collection_name: str, documents: List[Dict[str, Any]]) -> None:
    """
    Insert documents into a MongoDB collection.
    :param client: MongoClient instance
    :param db_name: Database name
    :param collection_name: Collection name
    :param documents: List of documents to insert
    """
    logger.debug(f"insert_documents(client, db_name={db_name}, collection_name={collection_name}, documents={documents})")
    try:
        db = client.get_database(db_name)
        collection = db.get_collection(collection_name)
        result = collection.insert_many(documents)
        logger.info(f"Inserted documents with IDs: {result.inserted_ids}")
    except errors.PyMongoError as e:
        logger.error(f"Failed to insert documents: {e}")
        raise

def parse_asciidoc_file(file_path: str) -> Dict[str, Any]:
    """
    Parse an AsciiDoc file with YAML front matter.
    :param file_path: Path to the AsciiDoc file
    :return: Parsed document as a dictionary
    """
    logger.debug(f"parse_asciidoc_file(file_path={file_path})")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Extract YAML front matter
            yaml_match = re.match(r'---\n(.*?)\n---\n', content, re.DOTALL)
            if not yaml_match:
                raise ValueError("YAML front matter not found")
            
            yaml_content = yaml_match.group(1)
            yaml_data = yaml.safe_load(yaml_content)
            
            # Extract AsciiDoc content
            asciidoc_content = content[yaml_match.end():].strip()
            yaml_data['content'] = asciidoc_content
            
            logger.debug(f"Parsed YAML data: {yaml_data}")
            return yaml_data
    except Exception as e:
        logger.error(f"Failed to parse AsciiDoc file: {e}")
        raise

def process_files_in_folder(folder_path: str) -> List[Dict[str, Any]]:
    """
    Process all AsciiDoc files in a given folder.
    :param folder_path: Path to the folder containing AsciiDoc files
    :return: List of parsed documents
    """
    logger.debug(f"process_files_in_folder(folder_path={folder_path})")
    documents = []
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.adoc'):
                file_path = os.path.join(folder_path, filename)
                document = parse_asciidoc_file(file_path)
                documents.append(document)
        return documents
    except Exception as e:
        logger.error(f"Failed to process files in folder: {e}")
        raise

@click.command()
@click.option('--uri', required=True, help='MongoDB connection string')
@click.option('--db_name', required=True, help='Database name')
@click.option('--collection_name', required=True, help='Collection name')
@click.option('--folder_path', required=True, help='Path to the folder containing AsciiDoc files')
def main(uri: str, db_name: str, collection_name: str, folder_path: str) -> None:
    """
    Main function to insert documents from AsciiDoc files in a folder into MongoDB.
    :param uri: MongoDB connection string
    :param db_name: Database name
    :param collection_name: Collection name
    :param folder_path: Path to the folder containing AsciiDoc files
    """
    logger.debug(f"main(uri={uri}, db_name={db_name}, collection_name={collection_name}, folder_path={folder_path})")
    try:
        documents = process_files_in_folder(folder_path)
        client = setup_mongo_client(uri)
        insert_documents(client, db_name, collection_name, documents)
        console.log("[bold green]Documents inserted successfully.[/bold green]")
    except Exception as e:
        console.log(f"[bold red]An error occurred: {e}[/bold red]")
    finally:
        if 'client' in locals():
            client.close()
            logger.info("MongoDB client connection closed.")
    logger.info("So long, and thanks for all the fish.")

if __name__ == "__main__":
    main()
