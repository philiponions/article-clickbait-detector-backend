import os
from fastapi import FastAPI
from pydantic import BaseModel
from models import CommunityReport
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from fastapi import HTTPException
from google import genai
from fastapi.middleware.cors import CORSMiddleware
import json
from ai import gen_report, gen_summary
from models import *
from scraper import Scraper

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

gem_key = os.getenv("KEY")

client = MongoClient(mongo_uri)
db = client["main"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

origins = [    
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

#


@app.post("/submit-url")
def submit_url(item: URLItem):
    reports_collection = db["reports"]
    existing_report = reports_collection.find_one({"url": item.url})
    
    if existing_report:
        return convert_object_id(existing_report)
    
    # Scraper here
    

@app.post("/generate-report/")
def generate_report(content: ContentItem):    
    response = gen_report("", content.content)
    
    response_dict = json.loads(response.parsed.json())
    response_dict["url"] = content.url
    response_dict["website"] = content.url.split("//")[-1].split("/")[0]
    return response_dict

# Summary post request
@app.post("/generate-summary/")
def generate_summary(content: ContentItem):
    generated_summary = gen_summary(content)

    return {"summary": generated_summary}

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

@app.post("/scrape-data/")
def scrape(url :str):
    title, thumbnail_url, article_text = Scraper(url)
    return{
            "title": title, 
            "thumbnail_url": thumbnail_url,
            "article_text": article_text
            }

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
