"""
english_adapter.py
Converts local Thailand travel tool results into English-only responses.
"""

from .crowded_check import crowded_check
from .trend_crowded_check import trend_crowded_check
from .search_api import search_travel_info


DESTINATION_EN = {
    "เชียงใหม่": "Chiang Mai",
    "ภูเก็ต": "Phuket",
    "กระบี่": "Krabi",
    "เกาะสมุย": "Koh Samui",
    "สมุย": "Koh Samui",
    "เกาะพะงัน": "Koh Phangan",
    "พัทยา": "Pattaya",
    "กรุงเทพ": "Bangkok",
    "อยุธยา": "Ayutthaya",
    "สุโขทัย": "Sukhothai",
    "น่าน": "Nan",
    "เลย": "Loei",
    "ภูกระดึง": "Phu Kradueng",
    "ขอนแก่น": "Khon Kaen",
    "เชียงราย": "Chiang Rai",
    "แม่ฮ่องสอน": "Mae Hong Son",
    "หัวหิน": "Hua Hin",
    "ประจวบคีรีขันธ์": "Prachuap Khiri Khan",
    "ตรัง": "Trang",
    "ไม่ระบุ": "Not specified",
}

DESTINATION_TYPE_EN = {
    "ภูเขา/วัฒนธรรม": "mountains and culture",
    "ทะเล/ชายหาด": "beaches and seaside",
    "ทะเล/ธรรมชาติ": "beaches and nature",
    "เกาะ/รีสอร์ต": "island resorts",
    "เกาะ/ปาร์ตี้": "islands and nightlife",
    "ทะเล/กลางคืน": "beaches and nightlife",
    "เมือง/ช้อปปิ้ง": "city and shopping",
    "ประวัติศาสตร์/วัฒนธรรม": "history and culture",
    "ประวัติศาสตร์": "history",
    "ธรรมชาติ/วัฒนธรรม": "nature and culture",
    "ธรรมชาติ/ผจญภัย": "nature and adventure",
    "เมือง/วัฒนธรรมอีสาน": "city and Isan culture",
    "ทะเล/รีสอร์ต": "beaches and resorts",
    "เกาะ/รีสอร์ต": "island resorts",
    "ทั่วไป": "general travel",
}

MONTH_EN = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

LEVEL_EN = {
    "ปิด": "Closed",
    "น้อยมาก": "Very low",
    "น้อย": "Low",
    "ปานกลาง": "Moderate",
    "มาก": "High",
    "มากมาย": "Very high",
}

BEST_TIME_EN = {
    "Chiang Mai": "November to February, when the weather is cooler and comfortable.",
    "Phuket": "November to April, when the sea is calmer and clearer.",
    "Krabi": "November to April, especially for island hopping and snorkeling.",
    "Koh Samui": "December to August, depending on beach side and weather patterns.",
    "Koh Phangan": "December to September; avoid Full Moon Party dates if you prefer quiet trips.",
    "Pattaya": "November to March, when the weather is milder and the sea is calmer.",
    "Bangkok": "November to February, when the weather is less hot.",
    "Ayutthaya": "November to February, when walking around temples is more comfortable.",
    "Sukhothai": "November to February, especially around the Loy Krathong festival.",
    "Nan": "October to February for cooler weather and scenic mountain routes.",
    "Loei": "October to February for cool weather, flowers, and mountain trips.",
    "Phu Kradueng": "October to February; the park is normally closed during part of the rainy season.",
    "Khon Kaen": "November to February for cooler weather and local festivals.",
    "Chiang Rai": "November to February for cool weather and mountain scenery.",
    "Mae Hong Son": "November to February for misty mountain views and cooler weather.",
    "Hua Hin": "November to April for calmer seas and pleasant resort weather.",
    "Prachuap Khiri Khan": "November to March for beach and nature trips.",
    "Trang": "November to May for clear seas and island trips.",
}

SIMILAR_ALTERNATIVES = {
    "Chiang Mai": ["Chiang Rai", "Nan", "Mae Hong Son", "Loei"],
    "Chiang Rai": ["Nan", "Mae Hong Son", "Chiang Mai", "Loei"],
    "Nan": ["Chiang Rai", "Mae Hong Son", "Loei"],
    "Mae Hong Son": ["Nan", "Chiang Rai", "Loei"],
    "Loei": ["Nan", "Mae Hong Son", "Chiang Rai"],
    "Phu Kradueng": ["Loei", "Nan", "Mae Hong Son"],
    "Phuket": ["Krabi", "Trang", "Koh Samui"],
    "Krabi": ["Trang", "Koh Samui", "Phuket"],
    "Trang": ["Krabi", "Koh Samui", "Phuket"],
    "Koh Samui": ["Trang", "Krabi", "Koh Phangan"],
    "Koh Phangan": ["Koh Samui", "Trang", "Krabi"],
    "Pattaya": ["Hua Hin", "Prachuap Khiri Khan", "Koh Samui"],
    "Hua Hin": ["Prachuap Khiri Khan", "Trang", "Koh Samui"],
    "Prachuap Khiri Khan": ["Hua Hin", "Trang", "Krabi"],
    "Bangkok": ["Ayutthaya", "Sukhothai", "Khon Kaen"],
    "Ayutthaya": ["Sukhothai", "Nan", "Khon Kaen"],
    "Sukhothai": ["Ayutthaya", "Nan"],
    "Khon Kaen": ["Nan", "Loei", "Ayutthaya"],
}

ALTERNATIVE_REASON = {
    "Chiang Rai": "similar northern culture and mountain scenery, usually calmer than Chiang Mai",
    "Nan": "quiet northern scenery, temples, cafes, and slow travel atmosphere",
    "Mae Hong Son": "misty mountains and local culture with a more remote feel",
    "Loei": "cool-weather mountain nature with a quieter pace",
    "Phu Kradueng": "mountain trekking and nature, best for active travelers",
    "Krabi": "limestone cliffs, beaches, islands, and nature similar to Phuket",
    "Trang": "clear-water islands and beaches with a quieter, more local feel",
    "Koh Samui": "island resorts and beaches with a different seasonal pattern",
    "Koh Phangan": "island beaches and nature with calmer areas outside party dates",
    "Hua Hin": "easy beach resort mood with a calmer family-friendly pace",
    "Prachuap Khiri Khan": "quiet beach and nature atmosphere close to Hua Hin",
    "Ayutthaya": "historic temples and culture close to Bangkok",
    "Sukhothai": "ancient temples and history with a slower atmosphere",
    "Khon Kaen": "city conveniences with Isan culture and lower tourist density",
    "Bangkok": "urban food, shopping, and culture with many neighborhood options",
    "Pattaya": "beach city energy and nightlife close to Bangkok",
}

ALIAS_TO_EN = {
    "chiang mai": "Chiang Mai",
    "chiangmai": "Chiang Mai",
    "phuket": "Phuket",
    "krabi": "Krabi",
    "koh samui": "Koh Samui",
    "samui": "Koh Samui",
    "koh phangan": "Koh Phangan",
    "phangan": "Koh Phangan",
    "pattaya": "Pattaya",
    "bangkok": "Bangkok",
    "ayutthaya": "Ayutthaya",
    "sukhothai": "Sukhothai",
    "nan": "Nan",
    "loei": "Loei",
    "phu kradueng": "Phu Kradueng",
    "khon kaen": "Khon Kaen",
    "chiang rai": "Chiang Rai",
    "chiangrai": "Chiang Rai",
    "mae hong son": "Mae Hong Son",
    "maehongson": "Mae Hong Son",
    "hua hin": "Hua Hin",
    "huahin": "Hua Hin",
    "prachuap": "Prachuap Khiri Khan",
    "prachuap khiri khan": "Prachuap Khiri Khan",
    "trang": "Trang",
}

ACTIVITY_LABELS = {
    "nature": "nature",
    "culture": "culture",
    "adventure": "adventure",
    "relaxation": "relaxation",
    "relax": "relaxation",
    "family": "family",
    "ธรรมชาติ": "nature",
    "วัฒนธรรม": "culture",
    "ผจญภัย": "adventure",
    "ผ่อนคลาย": "relaxation",
    "ครอบครัว": "family",
}

TRAVEL_GUIDES_EN = {
    "Chiang Mai": {
        "places": ["Doi Suthep", "Old City temples", "Doi Inthanon", "Nimman", "Mae Kampong"],
        "activities": {
            "nature": ["Visit Doi Inthanon", "Explore Mae Kampong", "See waterfalls around Doi Suthep-Pui"],
            "culture": ["Visit Doi Suthep", "Walk the Old City temples", "Explore Sunday Walking Street"],
            "adventure": ["Try ziplining", "Go rafting in Mae Taeng", "Cycle around the Old City"],
            "relaxation": ["Enjoy a Thai massage", "Visit Nimman cafes", "Walk the Night Bazaar"],
            "family": ["Visit Chiang Mai Night Safari", "Choose an ethical elephant sanctuary", "Join a cooking class"],
        },
        "food": ["Khao soi", "Sai ua sausage", "Nam prik noom with pork crackling", "Gaeng hung lay"],
        "transport": ["Fly from Bangkok in about 1 hour", "Use red songthaews, Grab, or rented scooters in town"],
        "budget": {"budget": "700-1,200 THB/day", "mid": "1,800-3,000 THB/day", "luxury": "4,500+ THB/day"},
    },
    "Phuket": {
        "places": ["Phuket Old Town", "Kata Beach", "Karon Beach", "Big Buddha", "Phi Phi Islands"],
        "activities": {
            "nature": ["Take a Phi Phi Islands day trip", "Snorkel around clear-water islands", "Relax at Kata Noi"],
            "culture": ["Walk Phuket Old Town", "Visit Wat Chalong", "Explore the Sunday Lard Yai market"],
            "adventure": ["Try surfing at Kata", "Go island hopping by speedboat", "Ride an ATV tour"],
            "relaxation": ["Book a spa day", "Stay near a quieter beach", "Enjoy a sunset seafood dinner"],
            "family": ["Visit Phuket Aquarium", "Plan a beach day at Kata", "Choose a gentle island tour"],
        },
        "food": ["Moo hong", "Hokkien noodles", "Southern Thai curries", "Fresh seafood"],
        "transport": ["Fly from Bangkok in about 1.5 hours", "Use Grab, hotel transfers, or a rental car for longer distances"],
        "budget": {"budget": "900-1,500 THB/day", "mid": "2,500-4,000 THB/day", "luxury": "6,000+ THB/day"},
    },
    "Krabi": {
        "places": ["Railay Beach", "Ao Nang", "Hong Islands", "Tiger Cave Temple", "Koh Lanta"],
        "activities": {
            "nature": ["Take a Four Islands tour", "Visit Railay Beach", "Kayak through mangroves"],
            "culture": ["Climb Tiger Cave Temple", "Explore Krabi Town night market"],
            "adventure": ["Try rock climbing at Railay", "Kayak at Ao Thalane", "Snorkel on island tours"],
            "relaxation": ["Watch sunset at Ao Nang", "Choose a quiet beach resort", "Book a spa session"],
            "family": ["Choose a larger-boat island tour", "Spend time at Ao Nang beach", "Visit easy viewpoints"],
        },
        "food": ["Seafood", "Southern Thai curry", "Fresh coconut", "Night market snacks"],
        "transport": ["Fly to Krabi Airport", "Use longtail boats for Railay and island transfers"],
        "budget": {"budget": "700-1,200 THB/day", "mid": "2,000-3,500 THB/day", "luxury": "5,000+ THB/day"},
    },
    "Koh Samui": {
        "places": ["Chaweng", "Lamai", "Fisherman's Village", "Big Buddha", "Ang Thong Marine Park"],
        "activities": {
            "nature": ["Visit Ang Thong Marine Park", "See Na Muang Waterfall", "Relax on quieter beaches"],
            "culture": ["Visit Big Buddha", "Walk Fisherman's Village night market"],
            "adventure": ["Take an ATV tour", "Join a snorkeling trip", "Go kayaking in the marine park"],
            "relaxation": ["Book a beach resort", "Enjoy spa treatments", "Take a sunset cruise"],
            "family": ["Choose calm beaches", "Visit night markets", "Take a gentle boat tour"],
        },
        "food": ["Seafood", "Coconut-based curries", "Southern Thai dishes", "Night market snacks"],
        "transport": ["Fly direct to Samui or fly to Surat Thani and take a ferry", "Rent a car or use taxis on the island"],
        "budget": {"budget": "900-1,600 THB/day", "mid": "2,800-4,500 THB/day", "luxury": "7,000+ THB/day"},
    },
    "Pattaya": {
        "places": ["Koh Larn", "Sanctuary of Truth", "Nong Nooch Garden", "Jomtien Beach", "Central Pattaya"],
        "activities": {
            "nature": ["Visit Koh Larn on a weekday", "Walk Nong Nooch Garden", "Relax at Jomtien Beach"],
            "culture": ["Visit Sanctuary of Truth", "Explore local markets"],
            "adventure": ["Try parasailing", "Go snorkeling near Koh Larn", "Book water sports carefully"],
            "relaxation": ["Choose Jomtien for a calmer stay", "Book a spa", "Have a seafood dinner"],
            "family": ["Visit Nong Nooch Garden", "Plan a Koh Larn beach day", "Go to family-friendly attractions"],
        },
        "food": ["Fresh seafood", "Thai street food", "Grilled squid", "Local market snacks"],
        "transport": ["Drive from Bangkok in about 2-3 hours", "Use baht buses, Grab, and ferries to Koh Larn"],
        "budget": {"budget": "700-1,200 THB/day", "mid": "2,000-3,500 THB/day", "luxury": "5,000+ THB/day"},
    },
    "Chiang Rai": {
        "places": ["White Temple", "Blue Temple", "Black House", "Doi Tung", "Singha Park"],
        "activities": {
            "nature": ["Visit Doi Tung", "Explore tea plantations", "Drive scenic mountain roads"],
            "culture": ["Visit White Temple", "Visit Blue Temple", "Explore local art spaces"],
            "adventure": ["Take a mountain road trip", "Cycle scenic routes", "Explore viewpoints"],
            "relaxation": ["Visit cafes and tea plantations", "Stay in a mountain resort"],
            "family": ["Visit Singha Park", "Choose temple sightseeing", "Plan short scenic stops"],
        },
        "food": ["Northern Thai dishes", "Khao soi", "Tea plantation snacks", "Local coffee"],
        "transport": ["Fly from Bangkok or drive from Chiang Mai", "Rent a car for flexible temple and mountain routes"],
        "budget": {"budget": "600-1,000 THB/day", "mid": "1,600-2,800 THB/day", "luxury": "4,000+ THB/day"},
    },
    "Nan": {
        "places": ["Wat Phumin", "Doi Samer Dao", "Bo Kluea", "Pua", "Nan Old Town"],
        "activities": {
            "nature": ["Visit Doi Samer Dao", "Drive to Bo Kluea", "Stay in Pua rice-field views"],
            "culture": ["Visit Wat Phumin", "Walk Nan Old Town", "Explore local museums"],
            "adventure": ["Take scenic mountain drives", "Visit viewpoints", "Cycle quiet roads"],
            "relaxation": ["Stay in a quiet homestay", "Enjoy cafes with rice-field views"],
            "family": ["Visit temples and old town", "Choose easy viewpoints", "Plan slow scenic drives"],
        },
        "food": ["Northern Thai food", "Local noodles", "Nan coffee", "Seasonal fruit"],
        "transport": ["Fly or drive via northern Thailand", "Rent a car for mountain routes"],
        "budget": {"budget": "600-1,000 THB/day", "mid": "1,500-2,600 THB/day", "luxury": "3,500+ THB/day"},
    },
    "Mae Hong Son": {
        "places": ["Jong Kham Lake", "Wat Jong Kham", "Ban Rak Thai", "Tham Lod", "Pai"],
        "activities": {
            "nature": ["See morning mist viewpoints", "Visit Tham Lod", "Drive to Ban Rak Thai"],
            "culture": ["Visit Shan-style temples", "Explore Ban Rak Thai", "Walk local markets"],
            "adventure": ["Drive the mountain loop", "Visit caves", "Plan viewpoint stops"],
            "relaxation": ["Stay near the lake", "Enjoy mountain cafes", "Travel slowly between towns"],
            "family": ["Visit temples and lake areas", "Choose shorter drives", "Plan gentle sightseeing"],
        },
        "food": ["Khao soi", "Shan-style dishes", "Tea at Ban Rak Thai", "Northern Thai snacks"],
        "transport": ["Fly via Chiang Mai or drive mountain roads", "Rent a car if comfortable with winding routes"],
        "budget": {"budget": "500-900 THB/day", "mid": "1,400-2,500 THB/day", "luxury": "3,500+ THB/day"},
    },
    "Trang": {
        "places": ["Koh Kradan", "Koh Mook", "Emerald Cave", "Hat Chao Mai", "Trang morning market"],
        "activities": {
            "nature": ["Visit Koh Kradan", "Snorkel around Trang islands", "Explore Emerald Cave with a guide"],
            "culture": ["Visit Trang morning market", "Explore old-town food spots"],
            "adventure": ["Swim into Emerald Cave", "Kayak around island areas", "Join snorkeling tours"],
            "relaxation": ["Stay on a quieter island", "Enjoy beach sunsets", "Plan slow seafood meals"],
            "family": ["Choose safe snorkeling tours", "Visit calm beaches", "Explore morning markets"],
        },
        "food": ["Trang roast pork", "Dim sum breakfast", "Local coffee", "Seafood"],
        "transport": ["Fly to Trang, then transfer by van and boat", "Use local boats for islands"],
        "budget": {"budget": "600-1,000 THB/day", "mid": "1,700-3,000 THB/day", "luxury": "4,000+ THB/day"},
    },
    "Hua Hin": {
        "places": ["Hua Hin Beach", "Cicada Market", "Khao Takiab", "Mrigadayavan Palace", "Vana Nava"],
        "activities": {
            "nature": ["Visit Khao Takiab", "Take a beach walk", "Plan a Kaeng Krachan side trip"],
            "culture": ["Visit Mrigadayavan Palace", "Explore night markets", "See old railway heritage"],
            "adventure": ["Try water parks", "Ride horses on the beach", "Play golf"],
            "relaxation": ["Choose a seaside resort", "Visit a spa", "Enjoy a calm seafood dinner"],
            "family": ["Visit water parks", "Explore markets", "Plan easy beach time"],
        },
        "food": ["Seafood", "Night market snacks", "Thai desserts", "Grilled seafood"],
        "transport": ["Drive or take a train from Bangkok", "Use taxis, songthaews, or hotel shuttles locally"],
        "budget": {"budget": "700-1,200 THB/day", "mid": "2,000-3,500 THB/day", "luxury": "5,000+ THB/day"},
    },
}

DEFAULT_GUIDE = {
    "places": ["Old town areas", "local markets", "temples", "nearby nature spots"],
    "activities": {
        "nature": ["Visit scenic viewpoints", "Explore parks or beaches", "Plan a slow outdoor day"],
        "culture": ["Visit temples", "Walk local markets", "Explore museums or old-town streets"],
        "adventure": ["Try guided outdoor activities", "Plan a day trip", "Explore viewpoints"],
        "relaxation": ["Choose a comfortable hotel", "Visit cafes", "Book a spa or wellness activity"],
        "family": ["Choose short travel legs", "Visit easy attractions", "Plan flexible rest time"],
    },
    "food": ["Local dishes", "street food", "seasonal fruit", "regional specialties"],
    "transport": ["Use local taxis, ride-hailing, or rental vehicles depending on distance"],
    "budget": {"budget": "600-1,200 THB/day", "mid": "1,800-3,500 THB/day", "luxury": "4,500+ THB/day"},
}


def _destination_to_english(value: str) -> str:
    if not value:
        return "Not specified"
    if value in DESTINATION_EN:
        return DESTINATION_EN[value]

    lower = value.strip().lower()
    for alias, destination in ALIAS_TO_EN.items():
        if alias in lower:
            return destination

    return value


def _level_to_english(level: str) -> str:
    return LEVEL_EN.get(level, level or "Moderate")


def _season_from_breakdown(raw: dict) -> str:
    season_bonus = raw.get("score_breakdown", {}).get("season_bonus", 0)
    if raw.get("is_peak_season") or season_bonus >= 25:
        return "high season"
    if season_bonus <= -20:
        return "low season"
    return "shoulder season"


def _score_note(score: int) -> str:
    if score == 0:
        return "Closed or not recommended for this month."
    if score >= 81:
        return "Very crowded peak travel period."
    if score >= 61:
        return "Busy high-season period."
    if score >= 41:
        return "Moderate crowd level."
    if score >= 21:
        return "Low crowd level and usually easier to travel."
    return "Very quiet period."


def _similar_less_crowded_alternatives(destination: str, month: int, year: int = None, day: int = None, original_score: int = 50) -> list:
    alternatives = []
    for candidate in SIMILAR_ALTERNATIVES.get(destination, []):
        raw = crowded_check(location=candidate, month=month, year=year, day=day)
        candidate_name = _destination_to_english(raw.get("location", candidate))
        candidate_score = raw.get("score", 50)

        if candidate_score >= original_score:
            continue

        alternatives.append(
            {
                "location": candidate_name,
                "crowd_level": _level_to_english(raw.get("crowd_level")),
                "score": candidate_score,
                "crowd_advantage": f"{max(0, original_score - candidate_score)} points lower than the requested destination",
                "why_similar": ALTERNATIVE_REASON.get(candidate_name, "similar travel style with a calmer crowd profile"),
                "best_time_to_visit": BEST_TIME_EN.get(candidate_name, "Check the monthly trend before booking."),
            }
        )

    return sorted(alternatives, key=lambda item: item["score"])[:3]


def crowded_check_english(location: str, month: int, year: int = None, day: int = None) -> dict:
    raw = crowded_check(location=location, month=month, year=year, day=day)
    destination = _destination_to_english(raw.get("location", location))
    month_name = MONTH_EN.get(raw.get("month", month), str(month))
    season = _season_from_breakdown(raw)
    score = raw.get("score", 50)
    holiday_bonus = raw.get("score_breakdown", {}).get("holiday_bonus", 0)

    reason_parts = [f"{month_name} is estimated to be {season} for {destination}."]
    if holiday_bonus:
        reason_parts.append("Public holidays, festivals, or long weekends may increase crowd levels.")
    if score <= 40:
        reason_parts.append("This is generally a quieter period, but weather and seasonal closures should still be checked.")
    elif score >= 75:
        reason_parts.append("Book accommodation and transport early because demand can be high.")

    warning = None
    if raw.get("warning"):
        warning = "Check weather, local operating conditions, and transport availability before booking."
    if destination in {"Chiang Mai", "Chiang Rai", "Mae Hong Son", "Nan"} and raw.get("month") in [3, 4]:
        warning = "Northern Thailand can have heavy haze and PM2.5 in March and April."

    alternatives = []
    if score >= 61:
        alternatives = _similar_less_crowded_alternatives(
            destination=destination,
            month=raw.get("month", month),
            year=raw.get("year", year),
            day=raw.get("day", day),
            original_score=score,
        )

    return {
        "language": "English",
        "location": destination,
        "original_query": location,
        "crowd_level": _level_to_english(raw.get("crowd_level")),
        "score": score,
        "is_peak_season": bool(raw.get("is_peak_season")),
        "season": season,
        "month": raw.get("month", month),
        "month_name": month_name,
        "year": raw.get("year", year),
        "day": raw.get("day", day),
        "reason": " ".join(reason_parts),
        "best_time_to_visit": BEST_TIME_EN.get(destination, "November to February is often comfortable for many Thailand destinations."),
        "destination_type": DESTINATION_TYPE_EN.get(raw.get("destination_type"), raw.get("destination_type", "general travel")),
        "warning": warning,
        "similar_less_crowded_alternatives": alternatives,
        "similar_low_crowd_alternatives": alternatives,
        "score_breakdown": raw.get("score_breakdown", {}),
    }


def trend_crowded_check_english(location: str) -> dict:
    raw = trend_crowded_check(location=location)
    destination = _destination_to_english(raw.get("location", location))

    trend_data = []
    for item in raw.get("trend_data", []):
        score = item.get("score", 50)
        month = item.get("month")
        trend_data.append(
            {
                "month": month,
                "month_name": MONTH_EN.get(month, str(month)),
                "score": score,
                "level": _level_to_english(item.get("level")),
                "notes": _score_note(score),
            }
        )

    best_months = raw.get("best_months", [])
    avoid_months = raw.get("avoid_months", [])
    closed_months = raw.get("closed_months", [])
    best_names = [MONTH_EN.get(m, str(m)) for m in best_months]
    avoid_names = [MONTH_EN.get(m, str(m)) for m in avoid_months]
    closed_names = [MONTH_EN.get(m, str(m)) for m in closed_months]
    average_score = raw.get("average_score")

    recommendation_parts = []
    if best_names:
        recommendation_parts.append(f"Recommended months: {', '.join(best_names[:4])}.")
    if avoid_names:
        recommendation_parts.append(f"Very crowded months to avoid: {', '.join(avoid_names)}.")
    if closed_names:
        recommendation_parts.append(f"Closed or not recommended: {', '.join(closed_names)}.")

    return {
        "language": "English",
        "location": destination,
        "original_query": location,
        "trend_data": trend_data,
        "best_months": best_months,
        "best_months_names": best_names,
        "avoid_months": avoid_months,
        "avoid_months_names": avoid_names,
        "closed_months": closed_months,
        "closed_months_names": closed_names,
        "average_score": average_score,
        "overall_trend": f"{destination} has an average crowd score of {average_score}. Use the monthly scores to balance weather, cost, and crowd comfort.",
        "recommendation": " ".join(recommendation_parts) if recommendation_parts else "Review the monthly crowd trend before booking.",
    }


def search_travel_info_english(query: str, location: str = None, activity_type: str = None, budget: str = None) -> dict:
    raw = search_travel_info(query=query, location=location, activity_type=activity_type, budget=budget)
    destination = _destination_to_english(raw.get("location") or location or query)
    guide = TRAVEL_GUIDES_EN.get(destination, DEFAULT_GUIDE)

    activity_key = ACTIVITY_LABELS.get((activity_type or "").lower(), activity_type or "")
    if not activity_key:
        activity_key = "nature"
    activities_by_type = guide.get("activities", DEFAULT_GUIDE["activities"])
    selected_activities = activities_by_type.get(activity_key, guide.get("places", DEFAULT_GUIDE["places"]))

    budget_key = budget if budget in {"budget", "mid", "luxury"} else "mid"
    budget_guide = guide.get("budget", DEFAULT_GUIDE["budget"])

    return {
        "language": "English",
        "location": destination,
        "original_location": location,
        "query": query,
        "activity_type_filter": activity_key,
        "budget_filter": budget_key,
        "results": {
            "places": guide.get("places", DEFAULT_GUIDE["places"]),
            "activities": selected_activities,
            "all_activities_by_type": activities_by_type,
            "food": guide.get("food", DEFAULT_GUIDE["food"]),
            "transportation": guide.get("transport", DEFAULT_GUIDE["transport"]),
            "budget_guide": {
                "selected": budget_guide.get(budget_key, budget_guide.get("mid")),
                "all": budget_guide,
            },
            "tips": [
                "Book earlier for weekends, public holidays, and peak season.",
                "Check weather and transport availability close to your travel date.",
                "Keep the itinerary flexible if traveling during rainy season.",
            ],
            "schedule_suggestions": [
                {"day": 1, "morning": "Arrive and explore the main town area", "afternoon": "Visit a signature attraction", "evening": "Try local food or a night market"},
                {"day": 2, "morning": "Plan a nature or culture highlight", "afternoon": "Add a relaxed cafe, viewpoint, or beach stop", "evening": "Have a slower dinner and rest"},
                {"day": 3, "morning": "Do a short final activity", "afternoon": "Buy local snacks or souvenirs", "evening": "Depart or extend the stay"},
            ],
        },
        "source": "English curated Thailand travel knowledge base",
        "disclaimer": "Prices, opening dates, weather, and transport schedules can change. Verify important details before traveling.",
    }
