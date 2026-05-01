# app.py
import os
import datetime
import requests
from google import genai
from groq import Groq
from qdrant_client import QdrantClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# ── Config ───────────────────────────────────────────
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq   = Groq(api_key=os.getenv("GROQ_API_KEY"))
qdrant = QdrantClient(path="./qdrant_storage")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Core Functions ────────────────────────────────────
def retrieve(query, top_k=5):
    result = gemini.models.embed_content(
        model="gemini-embedding-2",
        contents=query
    )
    hits = qdrant.query_points(
        collection_name="thailand_provinces",
        query=result.embeddings[0].values,
        limit=top_k
    ).points
    return [{"text": h.payload["text"]} for h in hits]

def llm_generate(prompt):
    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content

# ── Tools ─────────────────────────────────────────────
def rag_search(query):
    results = retrieve(query, top_k=5)
    return "\n\n---\n\n".join([r["text"] for r in results])

def google_search(query):
    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Search and answer with current info: {query} Nakhon Nayok Thailand",
        config={"tools": [{"google_search": {}}]}
    )
    return response.text

def get_weather(location="Nakhon Nayok"):
    try:
        res  = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": f"{location},TH", "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=5
        )
        data = res.json()
        if data.get("cod") != 200:
            return f"Weather data not available for {location}"
        w = data["weather"][0]["description"]
        t = data["main"]["temp"]
        f = data["main"]["feels_like"]
        h = data["main"]["humidity"]
        return f"Weather in {location}: {w}, {t}°C (feels like {f}°C), humidity {h}%. {'Good for outdoor activities' if t < 35 and 'rain' not in w else 'Be cautious'}"
    except Exception as e:
        return f"Could not fetch weather: {e}"

def get_time_and_season():
    now   = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    month = now.month
    if month in [11, 12, 1, 2]:
        season, tip = "Cool & Dry Season (Best time! 🌟)", "Perfect for outdoor activities"
    elif month in [3, 4, 5]:
        season, tip = "Hot Season (35-40°C)", "Visit early morning, stay hydrated"
    else:
        season, tip = "Rainy Season (Waterfalls at best! 🌊)", "Bring rain gear, waterfalls spectacular"
    return f"Current Bangkok time: {now.strftime('%A %B %d %Y %H:%M')} | Season: {season} | Tip: {tip}"

def get_crowd_density(place="Nakhon Nayok"):
    now       = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    is_wkend  = now.weekday() >= 5
    is_peak   = 9 <= now.hour <= 16
    is_hol    = now.month in [12, 1, 4]
    if is_wkend and is_peak and is_hol:
        density, tip = "Very Crowded 🔴", "Arrive before 8AM or after 4PM"
    elif is_wkend and is_peak:
        density, tip = "Moderately Crowded 🟡", "Weekday visits are quieter"
    else:
        density, tip = "Light / Quiet 🟢", "Great time to visit"
    return f"Crowd at {place}: {density} ({'Weekend' if is_wkend else 'Weekday'} {now.strftime('%H:%M')}) — {tip}"

# ── Agent ─────────────────────────────────────────────
def agent_chat(user_message: str) -> str:
    context       = rag_search(user_message)
    extra_context = ""

    msg = user_message.lower()

    if any(w in msg for w in ["weather", "rain", "hot", "cold", "temperature", "umbrella"]):
        extra_context += "\n\n" + get_weather()

    if any(w in msg for w in ["now", "today", "season", "when", "best time"]):
        extra_context += "\n\n" + get_time_and_season()

    if any(w in msg for w in ["crowd", "busy", "quiet", "peak", "people"]):
        extra_context += "\n\n" + get_crowd_density()

    if any(w in msg for w in ["event", "festival", "news", "this month", "this year", "current"]):
        extra_context += "\n\n" + google_search(user_message)

    prompt = f"""
You are a friendly travel companion for Nakhon Nayok, Thailand.
Help foreign tourists plan their trip with practical, honest advice.
Always include prices in both THB and USD.

KNOWLEDGE BASE:
{context}

REAL-TIME DATA:
{extra_context if extra_context else "N/A"}

USER: {user_message}
ASSISTANT:"""

    return llm_generate(prompt)

# ── API Endpoints ─────────────────────────────────────
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Nakhon Nayok Travel API is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    response = agent_chat(req.message)
    return {"response": response}