"""
crowded_check.py
Check crowd levels at tourist destinations in Thailand
"""

from datetime import date, datetime

# Base data for tourist destinations
# high_months: months with many visitors (peak season)
# low_months: months with few visitors (low season)
# remaining months are considered medium

DESTINATION_DATA = {
    "เชียงใหม่": {
        "high_months": [11, 12, 1, 2],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 55,
        "best_time": "November – February (cool, pleasant weather)",
        "avoid_reason": "May–September: heavy rain, possible road flooding",
        "type": "Mountain/Culture"
    },
    "ภูเก็ต": {
        "high_months": [11, 12, 1, 2, 3],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 65,
        "best_time": "November – April (clear sea, calm waves)",
        "avoid_reason": "May–October: southwest monsoon, strong waves, some beaches closed",
        "type": "Beach/Coastal"
    },
    "กระบี่": {
        "high_months": [11, 12, 1, 2, 3],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 60,
        "best_time": "November – April (clear water, great for diving)",
        "avoid_reason": "Monsoon season: ferries may be cancelled, sea can be dangerous",
        "type": "Beach/Nature"
    },
    "เกาะสมุย": {
        "high_months": [12, 1, 2, 3, 7, 8],
        "low_months": [10, 11],
        "base_score": 60,
        "best_time": "December – August (depends on which coast)",
        "avoid_reason": "October–November: heavy rain, risk of tropical storms",
        "type": "Island/Resort"
    },
    "เกาะพะงัน": {
        "high_months": [12, 1, 2, 3, 7, 8],
        "low_months": [10, 11],
        "base_score": 55,
        "best_time": "December – September (avoid Full Moon Party if you dislike crowds)",
        "avoid_reason": "October–November: heavy rain / Full Moon Party nights are extremely crowded",
        "type": "Island/Party"
    },
    "พัทยา": {
        "high_months": [11, 12, 1, 2, 3],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 70,
        "best_time": "November – March (good weather, calm sea)",
        "avoid_reason": "Rainy season: murky sea / Long weekends: very crowded, heavy traffic",
        "type": "Beach/Nightlife"
    },
    "กรุงเทพ": {
        "high_months": [11, 12, 1, 2, 3],
        "low_months": [],
        "base_score": 75,
        "best_time": "November – February (cooler weather)",
        "avoid_reason": "April: very hot / Songkran: heavy traffic but festive atmosphere",
        "type": "City/Shopping"
    },
    "อยุธยา": {
        "high_months": [11, 12, 1, 2],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 50,
        "best_time": "November – February (cool and comfortable)",
        "avoid_reason": "Summer: extremely hot for outdoor temples / Rainy season: possible flooding",
        "type": "History/Culture"
    },
    "สุโขทัย": {
        "high_months": [11, 12, 1, 2],
        "low_months": [5, 6, 7, 8],
        "base_score": 45,
        "best_time": "November – February (Loy Krathong festival in November)",
        "avoid_reason": "Summer: very hot / Rainy season: some routes inaccessible",
        "type": "Historical"
    },
    "น่าน": {
        "high_months": [10, 11, 12, 1, 2],
        "low_months": [5, 6, 7, 8],
        "base_score": 40,
        "best_time": "October – February (Bua Tong fields, cool weather)",
        "avoid_reason": "Summer: very hot / Rainy season: some roads dangerous",
        "type": "Nature/Culture"
    },
    "เลย": {
        "high_months": [10, 11, 12, 1, 2],
        "low_months": [5, 6, 7, 8],
        "base_score": 40,
        "best_time": "October – February (blooming flowers, Phu Kradueng scenic)",
        "avoid_reason": "Rainy season: slippery trails on Phu Kradueng / Summer: very hot",
        "type": "Nature/Adventure"
    },
    "ภูกระดึง": {
        "high_months": [10, 11, 12, 1, 2],
        "low_months": [6, 7, 8, 9],
        "base_score": 45,
        "best_time": "October – February (cool mountain weather)",
        "avoid_reason": "June–September: Phu Kradueng closes every year during monsoon",
        "type": "Nature/Adventure"
    },
    "ขอนแก่น": {
        "high_months": [11, 12, 1, 2],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 35,
        "best_time": "November – February (Khon Kaen Silk Festival)",
        "avoid_reason": "Summer: extremely hot / Rainy season: some flooding",
        "type": "City/Isan Culture"
    },
    "เชียงราย": {
        "high_months": [11, 12, 1, 2],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 50,
        "best_time": "November – February (cool weather, Doi Tung scenic)",
        "avoid_reason": "March–April: very high PM2.5 haze",
        "type": "Nature/Culture"
    },
    "แม่ฮ่องสอน": {
        "high_months": [11, 12, 1, 2],
        "low_months": [5, 6, 7, 8, 9],
        "base_score": 35,
        "best_time": "November – February (sea of mist, cool weather)",
        "avoid_reason": "Rainy season: narrow roads become slippery / March–April: heavy haze",
        "type": "Nature/Culture"
    },
    "หัวหิน": {
        "high_months": [11, 12, 1, 2, 3, 4],
        "low_months": [8, 9, 10],
        "base_score": 60,
        "best_time": "November – April (calm sea, good weather)",
        "avoid_reason": "August–October: rain and waves / Long weekends: packed with Bangkok tourists",
        "type": "Beach/Resort"
    },
    "ประจวบคีรีขันธ์": {
        "high_months": [11, 12, 1, 2, 3],
        "low_months": [8, 9, 10],
        "base_score": 45,
        "best_time": "November – March (good weather, beautiful sea)",
        "avoid_reason": "Rainy season: waves and wind / Weekends: crowded",
        "type": "Beach/Nature"
    },
    "ตรัง": {
        "high_months": [11, 12, 1, 2, 3, 4],
        "low_months": [6, 7, 8, 9, 10],
        "base_score": 40,
        "best_time": "November – May (clear water, beautiful islands, less crowded)",
        "avoid_reason": "June–October: southwest monsoon, strong waves",
        "type": "Beach/Nature"
    },
    "สมุย": {
        "high_months": [12, 1, 2, 3, 7, 8],
        "low_months": [10, 11],
        "base_score": 60,
        "best_time": "December – August (depends on which coast)",
        "avoid_reason": "October–November: heavy rain, risk of tropical storms",
        "type": "Island/Resort"
    },
}

# Special holidays that cause heavy crowding
THAI_HOLIDAYS = {
    # (month, day): (holiday_name, crowd_boost)
    (1, 1): ("New Year's Day", 35),
    (4, 13): ("Songkran (Thai New Year)", 40),
    (4, 14): ("Songkran (Thai New Year)", 40),
    (4, 15): ("Songkran (Thai New Year)", 38),
    (12, 31): ("New Year's Eve", 30),
    (12, 30): ("New Year Period", 25),
    (1, 2): ("New Year Period", 25),
    (5, 1): ("Labour Day", 15),
    (12, 5): ("Father's Day", 20),
    (8, 12): ("Mother's Day", 15),
}

# Month(s) of Loy Krathong (full moon of the 12th lunar month — approximately November)
LOY_KRATHONG_MONTHS = [11]

LEVEL_MAP = [
    (0, 20, "Very Low"),
    (21, 40, "Low"),
    (41, 60, "Moderate"),
    (61, 80, "High"),
    (81, 100, "Very High"),
]

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}


def _normalize_location(location: str) -> str:
    """Find matching destination name in the database"""
    location = location.strip()
    # Exact match
    if location in DESTINATION_DATA:
        return location
    # Partial match
    for dest in DESTINATION_DATA:
        if dest in location or location in dest:
            return dest
    # Keyword match (e.g. "เกาะพะงัน" -> "เกาะพะงัน")
    keywords = {
        "chiang mai": "เชียงใหม่",
        "พะงัน": "เกาะพะงัน",
        "phangan": "เกาะพะงัน",
        "koh phangan": "เกาะพะงัน",
        "สมุย": "เกาะสมุย",
        "koh samui": "เกาะสมุย",
        "ภูกระดึง": "ภูกระดึง",
        "เลย": "เลย",
        "กทม": "กรุงเทพ",
        "bangkok": "กรุงเทพ",
        "chiangmai": "เชียงใหม่",
        "phuket": "ภูเก็ต",
        "krabi": "กระบี่",
        "pattaya": "พัทยา",
        "samui": "เกาะสมุย",
        "nan": "น่าน",
        "chiang rai": "เชียงราย",
        "chiangrai": "เชียงราย",
        "mae hong son": "แม่ฮ่องสอน",
        "maehongson": "แม่ฮ่องสอน",
        "hua hin": "หัวหิน",
        "huahin": "หัวหิน",
        "prachuap": "ประจวบคีรีขันธ์",
        "prachuap khiri khan": "ประจวบคีรีขันธ์",
        "loei": "เลย",
        "khon kaen": "ขอนแก่น",
        "ayutthaya": "อยุธยา",
        "sukhothai": "สุโขทัย",
        "phu kradueng": "ภูกระดึง",
        "trang": "ตรัง",
    }
    lower = location.lower()
    for kw, dest in keywords.items():
        if kw in lower:
            return dest
    return None


def _score_to_level(score: int) -> str:
    """Convert numeric score to crowd level label"""
    score = max(0, min(100, score))
    for lo, hi, label in LEVEL_MAP:
        if lo <= score <= hi:
            return label
    return "Moderate"


def _is_long_weekend(month: int, day: int, year: int) -> bool:
    """Check whether the date falls on a long weekend (Friday or Monday adjacent to a holiday)"""
    try:
        d = date(year, month, day)
        # Friday or Monday
        return d.weekday() in (4, 0)
    except Exception:
        return False


def crowded_check(location: str, month: int, year: int = None, day: int = None) -> dict:
    """
    Check the crowd level at a tourist destination in Thailand.

    Args:
        location: Destination name or province, e.g. Chiang Mai, Phuket
        month: Month number (1-12)
        year: Calendar year (default: current year)
        day: Day of month (1-31) for a specific date check

    Returns:
        dict: {
            crowd_level, score, is_peak_season, reason, best_time_to_visit, warning
        }
    """
    if year is None:
        year = date.today().year

    normalized = _normalize_location(location)

    if normalized is None:
        # Not found in database — use default values
        return {
            "location": location,
            "crowd_level": "Moderate",
            "score": 50,
            "is_peak_season": False,
            "reason": f"No specific data for '{location}'. Using general estimate: {MONTH_NAMES.get(month, str(month))} typically sees moderate tourist traffic.",
            "best_time_to_visit": "November – February (cool season, good weather nationwide)",
            "warning": None
        }

    data = DESTINATION_DATA[normalized]
    base_score = data["base_score"]
    month_bonus = 0
    reasons = []
    warnings = []

    # Calculate score based on season
    if month in data["high_months"]:
        month_bonus += 30
        reasons.append(f"{MONTH_NAMES[month]} is High Season for {normalized}")
        is_peak = True
    elif month in data["low_months"]:
        month_bonus -= 25
        reasons.append(f"{MONTH_NAMES[month]} is Low Season for {normalized}")
        is_peak = False
        if data.get("avoid_reason"):
            warnings.append(data["avoid_reason"])
    else:
        month_bonus += 5
        reasons.append(f"{MONTH_NAMES[month]} is Shoulder Season for {normalized}")
        is_peak = False

    # Check special holidays
    holiday_bonus = 0
    if day:
        key = (month, day)
        if key in THAI_HOLIDAYS:
            holiday_name, bonus = THAI_HOLIDAYS[key]
            holiday_bonus = bonus
            reasons.append(f"{holiday_name} – public holiday, very high tourist traffic")
            warnings.append(f"Warning! Book accommodation and tickets at least 2–3 months ahead for {holiday_name}")

        if _is_long_weekend(month, day, year):
            holiday_bonus += 15
            reasons.append("Long Weekend")
            warnings.append("Hotel and transport prices may rise 30–50% during long weekends")

    # Loy Krathong (approximately November)
    if month in LOY_KRATHONG_MONTHS:
        if normalized in ["สุโขทัย", "เชียงใหม่", "กรุงเทพ"]:
            holiday_bonus += 20
            reasons.append("Loy Krathong festival – very popular, especially in Sukhothai and Chiang Mai")
            warnings.append("Famous Loy Krathong venue – book accommodation 3–4 months in advance")

    # Chiang Mai – Songkran
    if normalized == "เชียงใหม่" and month == 4:
        holiday_bonus += 25
        reasons.append("Chiang Mai Songkran – world-famous, busiest period of the year")
        warnings.append("Chiang Mai Songkran: book 4–6 months ahead, prices surge 200–300%")

    # Calculate final score
    final_score = min(100, max(0, base_score + month_bonus + holiday_bonus))
    crowd_level = _score_to_level(final_score)

    # Build reason text
    reason_text = " / ".join(reasons) if reasons else f"Typical period for {normalized}"

    # Warning text
    warning_text = None
    if warnings:
        warning_text = " | ".join(warnings)

    # Add PM2.5 warning for northern Thailand in March–April
    if normalized in ["เชียงใหม่", "เชียงราย", "แม่ฮ่องสอน", "น่าน"] and month in [3, 4]:
        pm_warning = "⚠️ PM2.5 Warning! Northern Thailand in March–April has heavy haze. N95 mask strongly recommended."
        warning_text = f"{warning_text} | {pm_warning}" if warning_text else pm_warning

    return {
        "location": normalized,
        "original_query": location,
        "crowd_level": crowd_level,
        "score": final_score,
        "is_peak_season": is_peak,
        "month": month,
        "month_name": MONTH_NAMES.get(month, str(month)),
        "year": year,
        "day": day,
        "reason": reason_text,
        "best_time_to_visit": data["best_time"],
        "destination_type": data.get("type", "General"),
        "warning": warning_text,
        "score_breakdown": {
            "base": base_score,
            "season_bonus": month_bonus,
            "holiday_bonus": holiday_bonus,
            "total": final_score
        }
    }
