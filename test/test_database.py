"""
file-name:    test_database.py
file-id:      ba12f56a-2c3a-408e-9d87-aa8340e217cd
project-name: ptreq
project-id:   11320d17-f243-4e2f-a841-e52098b2b439
"""
import pytest                                       # https://docs.pytest.org/en/stable/   
from pymongo import MongoClient                     # https://pymongo.readthedocs.io/en/stable/
from pymongo import errors
from ptreq import setup_mongo_client, insert_documents

@pytest.fixture
def database_name():
    return "test"


@pytest.fixture
def mongo_uri(database_name):
    return f"mongodb://localhost:27017/{database_name}"

    
def test_connect(mongo_uri):
    # Exercise (in setup)
    client = setup_mongo_client(mongo_uri)
    # Verify
    print(type(client))
    assert isinstance(client, MongoClient), f"ERROR {id}: Client should be a MongoClient instance"
    # Cleanup
    client.close()        



@pytest.fixture
def collection_name():
    return "test_collection_1"

@pytest.fixture
def documents():
    return [{"name": "requirement"}, {"name": "identifier"}]

def test_insert(mongo_uri, database_name, collection_name, documents):
    # Setup - in mongo_database
    client = setup_mongo_client(mongo_uri)

    # Exercise 
    insert_documents(client, database_name, collection_name, documents)
    
    db = client.get_database(database_name)
    collections = db.list_collection_names()
    assert collection_name in collections, f"ERROR {id}: Collection {collection_name} should exist"
    
    collection = db.get_collection(collection_name)
    assert collection.count_documents({}) == 2, f"ERROR {id}: Collection should have two documents"
    
    # Cleanup
    collection.drop()
    client.close()
