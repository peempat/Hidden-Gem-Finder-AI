"""
Agentic RAG helpers adapted from the root app.py.

This module keeps the Nakhon Nayok-specific RAG/weather/time/crowd functions
available to the hack4-1 backend as a normal tool. If the local Qdrant store is
not present, retrieval falls back to the bundled JSON knowledge base.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

try:
    from google import genai
except Exception:  # pragma: no cover - optional dependency/runtime config
    genai = None

try:
    from qdrant_client import QdrantClient
except Exception:  # pragma: no cover - optional dependency/runtime config
    QdrantClient = None


ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")
load_dotenv(BACKEND_DIR / ".env")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_PATHS = [ROOT_DIR / "qdrant_storage", BACKEND_DIR / "qdrant_storage"]
KNOWLEDGE_BASE_PATH = ROOT_DIR / "nakhonnayok_knowledge_base.json"


def _json_text(value: Any) -> str:
    if isinstance(value, dict):
        parts = []
        for key, child in value.items():
            parts.append(f"{key}: {_json_text(child)}")
        return "; ".join(parts)
    if isinstance(value, list):
        return ", ".join(_json_text(item) for item in value)
    return str(value)


def _load_knowledge_items() -> list[dict[str, Any]]:
    if not KNOWLEDGE_BASE_PATH.exists():
        return []

    with KNOWLEDGE_BASE_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    items = []
    for section, values in data.items():
        if isinstance(values, list):
            for value in values:
                items.append({"section": section, "text": _json_text(value), "raw": value})
        elif isinstance(values, dict):
            items.append({"section": section, "text": _json_text(values), "raw": values})
        else:
            items.append({"section": section, "text": str(values), "raw": values})
    return items


def _keyword_retrieve(query: str, top_k: int = 5) -> list[dict[str, str]]:
    items = _load_knowledge_items()
    if not items:
        return []

    terms = [term.lower() for term in query.replace(",", " ").split() if len(term) > 2]

    scored = []
    for item in items:
        text = item["text"]
        lower_text = text.lower()
        score = sum(lower_text.count(term) for term in terms)
        name = item.get("raw", {}).get("name") if isinstance(item.get("raw"), dict) else None
        if isinstance(name, dict):
            score += sum(3 for term in terms if term in name.get("english", "").lower())
        scored.append((score, text))

    scored.sort(key=lambda row: row[0], reverse=True)
    selected = [text for score, text in scored if score > 0][:top_k]
    if not selected:
        selected = [text for _, text in scored[:top_k]]
    return [{"text": text} for text in selected]


def _qdrant_retrieve(query: str, top_k: int = 5) -> list[dict[str, str]]:
    if not genai or not QdrantClient or not GEMINI_API_KEY:
        return []

    qdrant_path = next((path for path in QDRANT_PATHS if path.exists()), None)
    if not qdrant_path:
        return []

    client = genai.Client(api_key=GEMINI_API_KEY)
    qdrant = QdrantClient(path=str(qdrant_path))
    result = client.models.embed_content(model="gemini-embedding-2", contents=query)
    hits = qdrant.query_points(
        collection_name="thailand_provinces",
        query=result.embeddings[0].values,
        limit=top_k,
    ).points
    return [{"text": hit.payload.get("text", "")} for hit in hits if hit.payload.get("text")]


def retrieve_nakhon_nayok(query: str, top_k: int = 5) -> list[dict[str, str]]:
    try:
        qdrant_results = _qdrant_retrieve(query, top_k=top_k)
        if qdrant_results:
            return qdrant_results
    except Exception:
        pass

    return _keyword_retrieve(query, top_k=top_k)


def rag_search(query: str) -> str:
    results = retrieve_nakhon_nayok(query, top_k=5)
    return "\n\n---\n\n".join(result["text"] for result in results)


def google_current_search(query: str) -> str:
    if not genai or not GEMINI_API_KEY:
        return "Current Google search is unavailable because GEMINI_API_KEY is not configured."

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Search and answer with current info: {query} Nakhon Nayok Thailand",
        config={"tools": [{"google_search": {}}]},
    )
    return response.text or ""


def get_weather(location: str = "Nakhon Nayok") -> str:
    if not OPENWEATHER_API_KEY:
        return "Weather data is unavailable because OPENWEATHER_API_KEY is not configured."

    try:
        res = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": f"{location},TH", "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=5,
        )
        data = res.json()
        if data.get("cod") != 200:
            return f"Weather data is not available for {location}."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        outdoor_tip = "Good for outdoor activities" if temp < 35 and "rain" not in weather else "Be cautious"
        return (
            f"Weather in {location}: {weather}, {temp} C "
            f"(feels like {feels_like} C), humidity {humidity}%. {outdoor_tip}."
        )
    except Exception as exc:
        return f"Could not fetch weather: {exc}"


def get_time_and_season() -> str:
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    month = now.month
    if month in [11, 12, 1, 2]:
        season, tip = "Cool and dry season", "Perfect for outdoor activities"
    elif month in [3, 4, 5]:
        season, tip = "Hot season", "Visit early morning and stay hydrated"
    else:
        season, tip = "Rainy season", "Bring rain gear; waterfalls can be spectacular"
    return f"Current Bangkok time: {now.strftime('%A %B %d %Y %H:%M')} | Season: {season} | Tip: {tip}"


def get_crowd_density(place: str = "Nakhon Nayok") -> str:
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    is_weekend = now.weekday() >= 5
    is_peak_hour = 9 <= now.hour <= 16
    is_holiday_season = now.month in [12, 1, 4]

    if is_weekend and is_peak_hour and is_holiday_season:
        density, tip = "Very crowded", "Arrive before 8 AM or after 4 PM"
    elif is_weekend and is_peak_hour:
        density, tip = "Moderately crowded", "Weekday visits are quieter"
    else:
        density, tip = "Light / quiet", "Great time to visit"
    return f"Crowd at {place}: {density} ({'weekend' if is_weekend else 'weekday'} {now.strftime('%H:%M')}) - {tip}"


def agentic_nakhon_nayok_context(query: str, location: str = "Nakhon Nayok") -> dict[str, Any]:
    msg = query.lower()
    real_time_data = []

    if any(word in msg for word in ["weather", "rain", "hot", "cold", "temperature", "umbrella"]):
        real_time_data.append(get_weather(location))
    if any(word in msg for word in ["now", "today", "season", "when", "best time"]):
        real_time_data.append(get_time_and_season())
    if any(word in msg for word in ["crowd", "busy", "quiet", "peak", "people"]):
        real_time_data.append(get_crowd_density(location))
    if any(word in msg for word in ["event", "festival", "news", "this month", "this year", "current"]):
        try:
            real_time_data.append(google_current_search(query))
        except Exception as exc:
            real_time_data.append(f"Current search failed: {exc}")

    return {
        "language": "English",
        "location": location,
        "query": query,
        "knowledge_base": rag_search(query),
        "real_time_data": real_time_data,
        "pricing_rule": "When using this context, include prices in both THB and USD whenever prices are mentioned.",
        "source": "Nakhon Nayok agentic RAG context from local knowledge base plus optional live tools",
    }
