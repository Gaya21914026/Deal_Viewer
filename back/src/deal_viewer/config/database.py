from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

app = FastAPI()

client = MongoClient(config["ATLAS_URI"])
database = client[config["DB_NAME"]]
print("Connected to the MongoDB database!")


def get_collection(name: str):
    return database[name]

def init_indexes():
    deals = get_collection("deals")
    deals.create_index("reference", unique=True)

init_indexes()