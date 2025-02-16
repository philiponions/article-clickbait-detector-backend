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

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-report/")
def generate_report(item: URLItem):
    
    title = "GTA 6 LIVE: Official release date update revealed as part of Take-Two earnings call"
    content = "GTA 6 rumours and speculation continue to swirl as fans eagerly await any further updates on the most anticipated game in history."

    prompt = f'''You are a bot that helps frustrated users determine whether or not an article is clickbait bullshit. an article is defined as bullshit if it promises something in the title but does not actually talk about it or beats around the bush. You will be given a title and the content of the article and you will determine whether or not it's bullshit in terms of bullshit percentage. You will first give Consensus %, then a breakdown, and then a final one line TLDR.

    Example1)
    Title: Bloodborne is coming to Playstation 5
    Article: (only contains stuff about directors vaguely discussing the thought of porting it to playstation. no concrete proof of it actually happening)
    Consensus: 70% Bullshit

    STRICTLY OUTPUT JSON ONLY AND FOLLOW THE EXAMPLE OUTPUT CLOSELY

    Example Output) 

    {{
        "percentage": 85,
        "explanation": "The title promises that Bloodborne is "officially returning," which strongly implies a new game, remaster, or re-release. However, the article is just about Bloodborne music being played at a PlayStation concert—nothing about the game itself coming back in any meaningful way. The content also tries to stretch this weak connection into speculation about a potential remaster, which isn't backed by any real evidence. Classic clickbait.": 
        "tldr": "Article provides no release date update, despite promising one in the title; pure clickbait"
    }}

    Here's an actual article:
    Title:  {title}

    Content: {content}

    '''

    client = genai.Client(api_key="AIzaSyApK9yImqBxE6WOh470g6dxeEbaDkAd6kw")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    # Extracting response text safely
    generated_text = response.text if hasattr(response, "text") else str(response)

    return {"response": generated_text}

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