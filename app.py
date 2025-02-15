import os
from fastapi import FastAPI
from pydantic import BaseModel
from models import CommunityReport
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from fastapi import HTTPException

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["main"]

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

def convert_object_id(report_dict):
    if "_id" in report_dict:
        report_dict["_id"] = str(report_dict["_id"])
    return report_dict

@app.post("/add-report/")
def add_report(report: CommunityReport):
    reports_collection = db["reports"]
    report_dict = report.dict()
    result = reports_collection.insert_one(report_dict)
    report_dict["_id"] = str(result.inserted_id)
    return {"message": "Report added", "report": convert_object_id(report_dict)}

@app.get("/reports/")
def get_reports():
    reports_collection = db["reports"]
    reports = list(reports_collection.find())
    return {"reports": [convert_object_id(report) for report in reports]}

@app.get("/reports/{report_id}")
def get_report(report_id: str):
    reports_collection = db["reports"]
    if not ObjectId.is_valid(report_id):
        raise HTTPException(status_code=400, detail="Invalid report ID")
    report = reports_collection.find_one({"_id": ObjectId(report_id)})
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report": convert_object_id(report)}