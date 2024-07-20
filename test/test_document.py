"""
file-name:    test_database.py
file-id:      ba12f56a-2c3a-408e-9d87-aa8340e217cd
project-name: ptreq
project-id:   11320d17-f243-4e2f-a841-e52098b2b439
"""
import pytest                                       # https://docs.pytest.org/en/stable/   
from pymongo import MongoClient                     # https://pymongo.readthedocs.io/en/stable/
from pymongo import errors
from ptreq import parse_asciidoc_file
from rich import print                              # https://rich.readthedocs.io/en/latest/
from datetime import datetime,date                  # https://docs.python.org/3/library/datetime.html   

@pytest.fixture
def file_path_1():
    return "./test_document_1.adoc"

def test_parse_asciidoc_file(file_path_1):
    # Exercise
    document = parse_asciidoc_file(file_path_1)

    # Verify
    assert document["id"] == "REQ-001", f"ERROR {id}: ID should be 'REQ-1'"
    assert document["title"] == "Sample Requirement", f"ERROR {id}: Title should be 'Document 1'"
    assert document["author"] == "Jane Doe", f"ERROR {id}: Author should be 'Jane Doe'"
    assert document["status"] == "draft", f"ERROR {id}: State should be 'draft'"
    print(document["created_at"])
    assert document["created_at"] == date(2024,7,20), f"ERROR {id}: Created at should be '2024-07-20'"
    assert document["title"] =='Sample Requirement', f"ERROR {id}: Title should be 'Sample Requirement'"
    assert '= Sample Requirement Document' in document["content"], f"ERROR {id}: Content should be 'Sample Requirement'"
    # Cleanup
    print(document)