import os

from fastapi import FastAPI
from dotenv import load_dotenv
import pymongo

import routes

app = FastAPI()
load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
routes.mount(app, client)

