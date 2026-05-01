import json
import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from openai import AsyncOpenAI
from tools import agentic_nakhon_nayok_context, current_datetime
from tools.english_adapter import (
    crowded_check_english,
    search_travel_info_english,
    trend_crowded_check_english,
)

load_dotenv(Path(__file__).resolve().parent / ".env")

SYSTEM_PROMPT = """You are Gemmy Planner, an expert AI Travel Assistant for Thailand.

[CRITICAL LANGUAGE RULE]
This product is English-only.
Always reply entirely in English, even if the user writes in Thai or another language.
Never output Thai text from tool results. If a source/tool contains Thai internally, translate and summarize it in English.

[CURRENT DATE/TIME RULE]
Use current_datetime whenever the user asks about today, tomorrow, this week, next month, the current date/time, or gives a relative travel period.
Do not guess the current date from memory. Use the current_datetime tool.

[TRAVEL PLANNING STEPS]
1. Understand destination, date/month/year, duration, group type, budget, and interests. if user need recommended told the place in thailand that interest.
2. Use crowded_check to estimate the destination crowd level for the requested period.
3. Use trend_crowded_check to compare the destination's year-round crowd trend.
4. Use search_travel_info for places, activities, food, transportation, and budget guidance.
5. Use agentic_nakhon_nayok_context for Nakhon Nayok-specific questions, hidden gems, waterfalls, cafes, dams, local prices, weather, current conditions, or crowd timing.
6. If no destination is specified, compare several suitable Thailand destinations and explain the tradeoffs.
7. If the requested destination has a High or Very high crowd level, recommend similar less-crowded alternatives from the tool result before building the final itinerary.

[RESPONSE STRUCTURE]
Use concise Markdown with these English headers when relevant:
👥 Crowd Status
⭐ Recommendation
📍 Recommended Places
🎯 Activities
🗺️ Suggested Itinerary
🚆 Transportation
💰 Estimated Budget
🌿 Similar Less-Crowded Alternatives

[TONE]
Professional, calm, friendly, and practical."""

TOOL_DECLARATIONS = [
    {
        "name": "crowded_check",
        "description": "Check the estimated crowd level for a Thailand travel destination during a specific month or date.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Destination or province in Thailand, e.g. Chiang Mai, Phuket, Krabi.",
                },
                "month": {"type": "integer", "description": "Travel month as a number from 1 to 12."},
                "year": {
                    "type": "integer",
                    "description": "Gregorian year, e.g. 2026. If omitted, the backend uses the current year.",
                },
                "day": {
                    "type": "integer",
                    "description": "Day of month from 1 to 31, if checking a specific date.",
                },
            },
            "required": ["location", "month"],
        },
    },
    {
        "name": "trend_crowded_check",
        "description": "Return a year-round monthly crowd trend for a Thailand destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Destination or province in Thailand."}
            },
            "required": ["location"],
        },
    },
    {
        "name": "search_travel_info",
        "description": "Find English travel planning information for Thailand destinations, including places, activities, food, transport, and budget.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query, e.g. activities in Chiang Mai."},
                "location": {"type": "string", "description": "Destination or province."},
                "activity_type": {
                    "type": "string",
                    "description": "Activity type: nature, culture, adventure, relaxation, or family.",
                },
                "budget": {"type": "string", "description": "Budget level: budget, mid, or luxury."},
            },
            "required": ["query"],
        },
    },
    {
        "name": "current_datetime",
        "description": "Get the current date and time for accurate travel planning and relative date interpretation.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "IANA timezone name, e.g. Asia/Bangkok. Defaults to Asia/Bangkok.",
                }
            },
            "required": [],
        },
    },
    {
        "name": "agentic_nakhon_nayok_context",
        "description": "Retrieve Nakhon Nayok-specific hidden gem knowledge and optional live context such as weather, season, crowd timing, festivals, or current information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's Nakhon Nayok travel question or planning request.",
                },
                "location": {
                    "type": "string",
                    "description": "Specific Nakhon Nayok place or area. Defaults to Nakhon Nayok.",
                },
            },
            "required": ["query"],
        },
    },
]


def _is_local_base_url(base_url: str) -> bool:
    host = (urlparse(base_url).hostname or "").lower()
    return host in {"localhost", "127.0.0.1", "0.0.0.0"}


def _to_openai_tools(tool_declarations: list[dict]) -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
        }
        for tool in tool_declarations
    ]


def _normalize_history(history: list | None) -> list[dict]:
    normalized = []
    for msg in history or []:
        role = msg.get("role", "assistant")
        if role == "model":
            role = "assistant"
        if role not in {"user", "assistant", "system"}:
            role = "assistant"
        normalized.append({"role": role, "content": msg.get("content", "")})
    return normalized


def _tool_call_message(message) -> dict:
    tool_calls = []
    for tool_call in message.tool_calls or []:
        tool_calls.append(
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments or "{}",
                },
            }
        )
    return {"role": "assistant", "content": message.content or "", "tool_calls": tool_calls}


class TravelAgent:
    def __init__(self):
        base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
        api_key = os.getenv("GROQ_API_KEY")

        self.model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.temperature = float(os.getenv("TEMPERATURE", "0"))
        self.config_error = None
        if not api_key and not _is_local_base_url(base_url):
            self.config_error = "GROQ_API_KEY is not configured. Add it to backend/.env and restart the backend."
        self.client = AsyncOpenAI(api_key=api_key or "not-needed-for-local", base_url=base_url)
        self.tools = _to_openai_tools(TOOL_DECLARATIONS)

    def execute_tool(self, name: str, args: dict) -> dict:
        if name == "crowded_check":
            return crowded_check_english(**args)
        if name == "trend_crowded_check":
            return trend_crowded_check_english(**args)
        if name == "search_travel_info":
            return search_travel_info_english(**args)
        if name == "current_datetime":
            return current_datetime(**args)
        if name == "agentic_nakhon_nayok_context":
            return agentic_nakhon_nayok_context(**args)
        return {"error": f"Unknown tool: {name}"}

    def _execute_tool_call(self, tool_call) -> dict:
        name = tool_call.function.name
        try:
            args = json.loads(tool_call.function.arguments or "{}")
            if not isinstance(args, dict):
                return {"error": f"Tool arguments for {name} must be a JSON object"}
        except json.JSONDecodeError as exc:
            return {"error": f"Could not parse tool arguments for {name}: {exc}"}

        try:
            return self.execute_tool(name, args)
        except Exception as exc:
            return {"error": f"Tool {name} failed: {exc}"}

    async def chat(self, message: str, history: list = None) -> str:
        if self.config_error:
            return self.config_error

        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(_normalize_history(history))
            messages.append({"role": "user", "content": message})

            max_iterations = 5
            for _ in range(max_iterations):
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    parallel_tool_calls=False,
                )

                assistant_message = response.choices[0].message
                tool_calls = assistant_message.tool_calls or []
                if not tool_calls:
                    return assistant_message.content or ""

                messages.append(_tool_call_message(assistant_message))

                for tool_call in tool_calls:
                    result = self._execute_tool_call(tool_call)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": json.dumps(result, ensure_ascii=False),
                        }
                    )

            return "I could not complete the tool workflow within the iteration limit. Please try a more specific travel question."
        except Exception as e:
            return f"An error occurred: {str(e)}"
