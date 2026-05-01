"""
trend_crowded_check.py
Analyse year-round crowd trends for tourist destinations in Thailand
"""

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

MONTH_NAMES_SHORT = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# Monthly crowd scores for each destination
# score: 0-100 (0=very empty, 100=very crowded)
MONTHLY_SCORES = {
    "เชียงใหม่": {
        1: (80, "High Season – cool weather, packed with international tourists"),
        2: (78, "High Season – best weather, Bua Tong fields in bloom"),
        3: (55, "Getting hot, PM2.5 haze rising, tourist numbers declining"),
        4: (75, "Songkran! Busiest period of the year"),
        5: (30, "Low Season – rain begins"),
        6: (25, "Low Season – frequent rain"),
        7: (28, "Low Season – regular rainfall"),
        8: (30, "Low Season – heavy rain"),
        9: (32, "Low Season – last rains"),
        10: (50, "Shoulder Season begins, weather improving"),
        11: (72, "High Season starts – Chiang Mai Loy Krathong is famous"),
        12: (85, "Peak Season – New Year, fully packed"),
    },
    "ภูเก็ต": {
        1: (85, "High Season – beautiful sea, packed with international tourists"),
        2: (83, "High Season – excellent weather"),
        3: (78, "High Season – still good before monsoon"),
        4: (65, "Shoulder – getting hot"),
        5: (30, "Low Season – southwest monsoon"),
        6: (25, "Low Season – strong waves, some beaches closed"),
        7: (28, "Low Season – frequent rain"),
        8: (30, "Low Season – rainy"),
        9: (27, "Low Season – heaviest rain"),
        10: (35, "Shoulder – rain easing"),
        11: (70, "High Season begins"),
        12: (90, "Peak Season – Christmas and New Year, very crowded"),
    },
    "กระบี่": {
        1: (82, "High Season – clear water, beautiful islands"),
        2: (80, "High Season – best weather"),
        3: (75, "High Season – still good"),
        4: (60, "Getting hot, tourist numbers declining"),
        5: (28, "Low Season – monsoon, some ferry routes suspended"),
        6: (22, "Low Season – very strong waves"),
        7: (25, "Low Season – frequent rain"),
        8: (23, "Low Season – heavy rain"),
        9: (20, "Low Season – heaviest rain"),
        10: (30, "Beginning to recover"),
        11: (68, "High Season begins"),
        12: (88, "Peak Season – very crowded"),
    },
    "เกาะสมุย": {
        1: (80, "High Season – east coast sea looks beautiful"),
        2: (78, "High Season"),
        3: (72, "High Season – before monsoon"),
        4: (60, "Shoulder Season"),
        5: (45, "Rain begins"),
        6: (40, "Moderate rain"),
        7: (65, "High Season on west coast, many tourists"),
        8: (68, "High Season on west coast"),
        9: (50, "Shoulder"),
        10: (25, "Low Season – possible tropical storms"),
        11: (20, "Low Season – heaviest rain"),
        12: (82, "Peak Season – very crowded for New Year"),
    },
    "เกาะพะงัน": {
        1: (75, "High Season"),
        2: (72, "High Season"),
        3: (68, "High Season"),
        4: (55, "Shoulder"),
        5: (40, "Rain begins"),
        6: (38, "Moderate rain"),
        7: (62, "High Season on west coast + Full Moon Party"),
        8: (65, "High Season + Full Moon Party"),
        9: (48, "Shoulder"),
        10: (22, "Low Season – heavy rain"),
        11: (18, "Low Season – storm risk"),
        12: (78, "Peak Season + New Year Full Moon Party"),
    },
    "พัทยา": {
        1: (78, "High Season – packed with international tourists"),
        2: (75, "High Season"),
        3: (70, "High Season"),
        4: (72, "Pattaya Songkran is famous"),
        5: (40, "Shoulder"),
        6: (35, "Low Season"),
        7: (38, "Low Season"),
        8: (40, "Low Season"),
        9: (35, "Low Season – heavy rain"),
        10: (42, "Shoulder"),
        11: (65, "High Season begins"),
        12: (85, "Peak Season – Christmas and New Year"),
    },
    "กรุงเทพ": {
        1: (72, "High Season – cool weather, packed with tourists"),
        2: (70, "High Season"),
        3: (65, "Shoulder – getting hot"),
        4: (68, "Bangkok Songkran – heavy traffic"),
        5: (60, "Shoulder"),
        6: (55, "Shoulder"),
        7: (58, "Shoulder"),
        8: (60, "Shoulder"),
        9: (55, "Shoulder"),
        10: (62, "Shoulder – improving"),
        11: (68, "High Season begins"),
        12: (80, "Peak Season – New Year, fully packed"),
    },
    "อยุธยา": {
        1: (68, "High Season – cool weather, great for temple walks"),
        2: (65, "High Season"),
        3: (50, "Shoulder – getting hot"),
        4: (40, "Very hot, few visitors"),
        5: (30, "Low Season"),
        6: (28, "Low Season"),
        7: (30, "Low Season"),
        8: (28, "Low Season – possible flooding"),
        9: (25, "Low Season – flooding some years"),
        10: (35, "Shoulder"),
        11: (58, "High Season begins – Loy Krathong"),
        12: (72, "Peak Season"),
    },
    "สุโขทัย": {
        1: (62, "High Season"),
        2: (58, "High Season"),
        3: (42, "Shoulder – getting hot"),
        4: (35, "Very hot"),
        5: (25, "Low Season"),
        6: (22, "Low Season"),
        7: (24, "Low Season"),
        8: (22, "Low Season"),
        9: (25, "Shoulder"),
        10: (38, "Shoulder"),
        11: (80, "Peak Season – Sukhothai Loy Krathong festival!! Very crowded"),
        12: (65, "High Season"),
    },
    "น่าน": {
        1: (60, "High Season – cool weather"),
        2: (55, "High Season"),
        3: (40, "Shoulder"),
        4: (30, "Shoulder"),
        5: (20, "Low Season"),
        6: (18, "Low Season"),
        7: (20, "Low Season"),
        8: (22, "Low Season"),
        9: (25, "Beginning to recover"),
        10: (65, "Peak Season – Bua Tong fields"),
        11: (70, "Peak Season – great weather"),
        12: (62, "High Season"),
    },
    "เลย": {
        1: (58, "High Season – cool weather, Phu Kradueng open"),
        2: (52, "High Season"),
        3: (35, "Shoulder"),
        4: (28, "Shoulder"),
        5: (20, "Low Season"),
        6: (15, "Low Season – Phu Kradueng closed"),
        7: (15, "Low Season – Phu Kradueng closed"),
        8: (15, "Low Season – Phu Kradueng closed"),
        9: (15, "Low Season – Phu Kradueng closed"),
        10: (55, "Peak Season – Phu Kradueng reopens, flowers blooming"),
        11: (70, "Peak Season – cool weather"),
        12: (65, "High Season"),
    },
    "ภูกระดึง": {
        1: (65, "High Season – cool weather"),
        2: (60, "High Season"),
        3: (40, "Shoulder"),
        4: (30, "Shoulder"),
        5: (20, "Shoulder"),
        6: (0, "Closed! Phu Kradueng closed for rainy season (Jun–Sep)"),
        7: (0, "Closed! Phu Kradueng closed for rainy season"),
        8: (0, "Closed! Phu Kradueng closed for rainy season"),
        9: (0, "Closed! Phu Kradueng closed for rainy season"),
        10: (60, "Reopened! Visitors flock in during first weeks"),
        11: (72, "Peak Season"),
        12: (68, "High Season"),
    },
    "ขอนแก่น": {
        1: (52, "High Season – Silk Festival"),
        2: (48, "Shoulder"),
        3: (40, "Shoulder"),
        4: (38, "Shoulder"),
        5: (30, "Low Season"),
        6: (28, "Low Season"),
        7: (30, "Low Season"),
        8: (32, "Low Season"),
        9: (30, "Low Season"),
        10: (38, "Shoulder"),
        11: (52, "High Season"),
        12: (58, "High Season – New Year"),
    },
    "เชียงราย": {
        1: (68, "High Season – cool weather, historic temples"),
        2: (65, "High Season"),
        3: (40, "Shoulder – PM2.5 haze"),
        4: (35, "Haze / very hot"),
        5: (25, "Low Season"),
        6: (20, "Low Season"),
        7: (22, "Low Season"),
        8: (25, "Low Season"),
        9: (28, "Shoulder"),
        10: (50, "High Season begins"),
        11: (65, "High Season"),
        12: (72, "Peak Season – New Year"),
    },
    "แม่ฮ่องสอน": {
        1: (62, "High Season – sea of mist, cool weather"),
        2: (58, "High Season"),
        3: (35, "Shoulder – haze starting"),
        4: (25, "Heavy PM2.5 haze"),
        5: (18, "Low Season"),
        6: (15, "Low Season – roads may be dangerous"),
        7: (15, "Low Season"),
        8: (15, "Low Season"),
        9: (18, "Low Season"),
        10: (45, "Getting better"),
        11: (65, "High Season"),
        12: (68, "Peak Season"),
    },
    "หัวหิน": {
        1: (72, "High Season – calm sea, Bangkok tourists flock here"),
        2: (70, "High Season"),
        3: (68, "High Season"),
        4: (65, "High Season – Songkran"),
        5: (50, "Shoulder"),
        6: (45, "Shoulder"),
        7: (55, "Shoulder – holiday visitors"),
        8: (35, "Low Season – heavy rain"),
        9: (28, "Low Season – heavy rain"),
        10: (30, "Low Season"),
        11: (62, "High Season begins"),
        12: (80, "Peak Season – New Year"),
    },
    "ประจวบคีรีขันธ์": {
        1: (62, "High Season"),
        2: (60, "High Season"),
        3: (58, "High Season"),
        4: (52, "Shoulder"),
        5: (40, "Shoulder"),
        6: (35, "Shoulder"),
        7: (38, "Shoulder"),
        8: (28, "Low Season"),
        9: (22, "Low Season"),
        10: (25, "Low Season"),
        11: (50, "Shoulder"),
        12: (68, "High Season"),
    },
    "ตรัง": {
        1: (60, "High Season – clear water, not crowded"),
        2: (58, "High Season"),
        3: (55, "High Season"),
        4: (52, "Shoulder"),
        5: (35, "Shoulder"),
        6: (20, "Low Season – monsoon"),
        7: (18, "Low Season"),
        8: (15, "Low Season"),
        9: (12, "Low Season – heaviest rain"),
        10: (15, "Low Season"),
        11: (45, "Shoulder"),
        12: (62, "High Season"),
    },
}

LEVEL_MAP = [
    (0, 0, "Closed"),
    (1, 20, "Very Low"),
    (21, 40, "Low"),
    (41, 60, "Moderate"),
    (61, 80, "High"),
    (81, 100, "Very High"),
]


def _score_to_level(score: int) -> str:
    for lo, hi, label in LEVEL_MAP:
        if lo <= score <= hi:
            return label
    return "Moderate"


def _normalize_location(location: str) -> str:
    location = location.strip()
    if location in MONTHLY_SCORES:
        return location
    for dest in MONTHLY_SCORES:
        if dest in location or location in dest:
            return dest
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
        "phuket": "ภูเก็ต",
        "chiangmai": "เชียงใหม่",
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


def trend_crowded_check(location: str) -> dict:
    """
    Analyse the year-round crowd trend for a destination.

    Args:
        location: Destination name or province in Thailand

    Returns:
        dict: {
            location, trend_data: [{month, month_name, score, level, notes}],
            best_months, avoid_months, overall_trend
        }
    """
    normalized = _normalize_location(location)

    if normalized is None:
        # Default data for destinations not in the database
        default_scores = {
            1: 65, 2: 62, 3: 55, 4: 58, 5: 40, 6: 35,
            7: 38, 8: 40, 9: 38, 10: 50, 11: 60, 12: 70
        }
        trend_data = []
        for m in range(1, 13):
            score = default_scores[m]
            trend_data.append({
                "month": m,
                "month_name": MONTH_NAMES[m],
                "month_short": MONTH_NAMES_SHORT[m],
                "score": score,
                "level": _score_to_level(score),
                "notes": "General estimate"
            })
        return {
            "location": location,
            "normalized_location": location,
            "trend_data": trend_data,
            "best_months": [2, 3, 10, 11],
            "avoid_months": [5, 6, 7, 8, 9],
            "overall_trend": f"No specific data found for '{location}'. Generally, Thailand has High Season from November–February and Low Season from May–September.",
            "recommendation": "Recommended travel period: November – March for good weather nationwide"
        }

    monthly = MONTHLY_SCORES[normalized]
    trend_data = []
    scores = []

    for m in range(1, 13):
        score, notes = monthly[m]
        level = _score_to_level(score)
        trend_data.append({
            "month": m,
            "month_name": MONTH_NAMES[m],
            "month_short": MONTH_NAMES_SHORT[m],
            "score": score,
            "level": level,
            "notes": notes
        })
        scores.append(score)

    # Find best months (low score but not 0)
    valid_scores = [(m + 1, s) for m, s in enumerate(scores) if s > 0]
    sorted_by_low = sorted(valid_scores, key=lambda x: x[0])

    # best months = score 20-55
    best_months = [m for m, s in valid_scores if 15 <= s <= 55]
    if not best_months:
        best_months = [m for m, s in sorted(valid_scores, key=lambda x: x[1])[:3]]

    # avoid months = score > 75 or 0 (closed)
    avoid_months = [m for m, s in valid_scores if s >= 75]
    closed_months = [m + 1 for m, s in enumerate(scores) if s == 0]

    avg_score = sum(s for s in scores if s > 0) / len([s for s in scores if s > 0])

    if avg_score > 65:
        overall = f"{normalized} is a highly popular destination with tourists year-round. High Season is especially crowded — always book in advance."
    elif avg_score > 45:
        overall = f"{normalized} has moderate tourist traffic with pleasant periods that are comfortable to visit without excessive crowds."
    else:
        overall = f"{normalized} is a destination that is not yet heavily crowded, ideal for travellers who prefer tranquillity — but be mindful of seasonal conditions."

    best_months_names = [MONTH_NAMES[m] for m in best_months]
    avoid_months_names = [MONTH_NAMES[m] for m in avoid_months]
    closed_months_names = [MONTH_NAMES[m] for m in closed_months]

    recommendation_parts = []
    if best_months_names:
        recommendation_parts.append(f"Recommended months: {', '.join(best_months_names[:4])}")
    if avoid_months_names:
        recommendation_parts.append(f"Months to avoid (very crowded): {', '.join(avoid_months_names)}")
    if closed_months_names:
        recommendation_parts.append(f"Closed / not recommended months: {', '.join(closed_months_names)}")

    return {
        "location": normalized,
        "original_query": location,
        "trend_data": trend_data,
        "best_months": best_months,
        "best_months_names": best_months_names,
        "avoid_months": avoid_months,
        "avoid_months_names": avoid_months_names,
        "closed_months": closed_months,
        "closed_months_names": closed_months_names,
        "average_score": round(avg_score, 1),
        "overall_trend": overall,
        "recommendation": " | ".join(recommendation_parts) if recommendation_parts else "Check individual months for more details"
    }
