import os
from fastapi import FastAPI
from pydantic import BaseModel
from models import CommunityReport
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["clickbait_db"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

#
class URLItem(BaseModel):
    url: str

@app.post("/submit-url/")
def submit_url(item: URLItem):
    return {"message": "URL received", "url": item.url}

@app.post("/add-report/")
def add_report(report: CommunityReport):
    reports_collection = db["reports"]
    report_dict = report.dict()
    reports_collection.insert_one(report_dict)
    return {"message": "Report added", "report": report_dict}