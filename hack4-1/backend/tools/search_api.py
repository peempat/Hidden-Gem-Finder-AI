"""
search_api.py
Simulates travel information search from Thai travel blogs and community knowledge
"""

TRAVEL_KNOWLEDGE_BASE = {
    "เชียงใหม่": {
        "activities": [
            "Visit Doi Suthep Temple",
            "Walk the Night Bazaar and Sunday Walking Street",
            "Thai cooking class or cookie workshop",
            "Bicycle tour of the Old City",
            "Visit Doi Inthanon (highest peak in Thailand)",
            "Shopping in Nimman – the trendy quarter",
            "Visit Wat Chedi Luang and Wat Chiang Man",
            "Traditional Thai massage and spa",
            "Hill tribe village tour",
            "Explore Mango Tango and famous cafes",
            "Elephant Nature Park (ethical sanctuary)",
            "Chiang Mai Night Safari",
        ],
        "must_eat": [
            "Khao Soi (Northern Thai curry noodle soup with crispy noodles)",
            "Hang Lay Curry (Burmese-style pork curry)",
            "Khao Nom Jin Nam Ngiao (rice noodles in tomato-pork broth)",
            "Khaep Mu + Nam Prik Noom (pork crackling with green chilli dip)",
            "Chiang Mai sausage (Sai Ua) and Naem",
            "Laab Mueang (northern-style minced meat salad)",
            "Mango Sticky Rice (Khao Niao Mamuang)",
            "Doi coffee (Doi Chang, Doi Tung brands)",
            "Northern-style stir-fried morning glory",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight: 1 hour, THB 800–3,000 (AirAsia, Nok Air, Thai AirAsia)",
                "Train: 10–13 hours, THB 200–1,500 (sleeper air-conditioned)",
                "Bus: 9–11 hours, THB 350–800"
            ],
            "In the city": [
                "Red Songthaew (shared pickup truck): THB 30–60 per person",
                "Grab / Bolt: THB 50–200 depending on distance",
                "Scooter rental: THB 150–250 per day",
                "Bicycle rental: THB 50–100 per day",
                "Tuk-tuk: THB 60–150 per trip (negotiate fare)"
            ]
        },
        "budget_per_day": {
            "budget": "THB 500–800 (guesthouse + market food)",
            "mid": "THB 1,500–2,500 (3-star hotel + restaurant meals)",
            "luxury": "THB 4,000–8,000+ (5-star hotel + spa + guided tours)"
        },
        "accommodation": [
            "Riverside Guest House (on the Ping River, budget)",
            "De Naga Hotel (Old City, mid-range)",
            "137 Pillars House (luxury boutique)",
            "Nimman Sook Hostel (Nimman, budget-friendly)",
            "Four Seasons Chiang Mai (luxury, rice field setting)",
        ],
        "pantip_tips": [
            "Saturday Walking Street (Wua Lai) is more authentic than Sunday's — fewer tourists, lower prices",
            "Rent a motorbike and ride up Doi Suthep before 7 am — no crowds, stunning views",
            "Warorot Market (Kad Luang) is the cheapest place for souvenirs — bargaining required",
            "During Chiang Mai Songkran, Tapae Road is the heart of the water fight — bring a waterproof bag",
            "Mae Sai Khao Soi roadside shop has cheap, more delicious khao soi than the famous city restaurants",
            "Grab in Chiang Mai can be scarce in some areas, especially in the rain — keep a local red songthaew number handy",
        ],
        "nearby_attractions": ["Doi Inthanon", "Mae Kampong", "Suan Dok", "Wat Umong", "Doi Pui", "Mae Klang Waterfall"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Doi Inthanon", "Wachirathan Waterfall", "Mae Kampong", "Doi Suthep-Pui National Park"],
            "วัฒนธรรม": ["Doi Suthep Temple", "Wat Chedi Luang", "Chiang Mai Museum", "Walking Street"],
            "ผจญภัย": ["Flight of the Gibbon Zipline", "Mae Taeng River Rafting", "Crazy Horse Climbing"],
            "ผ่อนคลาย": ["Spa and traditional Thai massage", "Nimman cafes", "Night Bazaar shopping"],
            "ครอบครัว": ["Chiang Mai Night Safari", "Elephant Nature Park", "Thai cooking class"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Doi Suthep Temple + Doi Pui", "afternoon": "Old City – Wat Chedi Luang, Wat Phra Singh", "evening": "Sunday Walking Street + Night Bazaar"},
            {"day": 2, "morning": "Doi Inthanon (early start)", "afternoon": "Wachirathan & Mae Klang Waterfalls", "evening": "Local restaurant in Nimman"},
            {"day": 3, "morning": "Warorot Market – souvenir shopping", "afternoon": "2-hour spa and massage", "evening": "Scenic dinner + Warm Up Cafe"},
        ]
    },

    "ภูเก็ต": {
        "activities": [
            "Patong, Kata, Karon, Bang Tao beaches",
            "Koh Phi Phi – snorkelling and diving",
            "Lard Yai Night Market",
            "Phuket Old Town heritage walk",
            "Big Buddha viewpoint",
            "Phang Nga Bay boat tour",
            "James Bond Island",
            "Similan Islands diving (day trip)",
            "ATV mountain ride",
            "Tiger Kingdom",
        ],
        "must_eat": [
            "Moo Hong (braised pork belly over rice)",
            "Phuket-style Pad Thai",
            "O-Tao (Phuket-style rice salad)",
            "Gaeng Tai Pla (fish organ curry)",
            "Kuay Teow Nam Tok (waterfall noodle soup)",
            "Khanom Jin with green fish curry",
            "Kanom Krok (coconut rice pancakes)",
            "Durian in syrup (Thurian Loy Gaew)",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight: 1.5 hours, THB 900–4,000",
                "Bus: 12–14 hours, THB 500–900"
            ],
            "In the city": [
                "Grab: THB 100–400 depending on distance",
                "Metered taxi (rare) / negotiate with local drivers",
                "Scooter rental: THB 200–350 per day",
                "Car rental: THB 800–1,500 per day",
                "Songthaew (route bus): THB 30–50"
            ]
        },
        "budget_per_day": {
            "budget": "THB 700–1,200 (bungalow + market food)",
            "mid": "THB 2,000–3,500 (3-star hotel + restaurant meals)",
            "luxury": "THB 6,000–15,000+ (5-star pool villa)"
        },
        "accommodation": [
            "Lub d Hostel Phuket (Patong, budget-friendly)",
            "Avista Hideaway (Nai Harn, mid-range)",
            "Trisara Phuket (ultra-luxury pool villa)",
            "YAMA Hotel (Old Town, boutique)",
            "Banyan Tree Phuket (luxury, Laguna)",
        ],
        "pantip_tips": [
            "Kata Noi beach is much quieter than Patong — clearer water, better surf for beginners",
            "Walk Phuket Old Town in the morning or late afternoon for the best photos without crowds",
            "Phi Phi Island tours booked at the hotel are more expensive — negotiate with tour sellers on the beach",
            "Grab in Phuket is much cheaper than taxis but can be scarce, especially in the rain",
            "Beachfront restaurants are 2–3 times more expensive than eating in town — try the local market instead",
        ],
        "nearby_attractions": ["Koh Phi Phi", "Koh Racha", "Phang Nga Bay", "Similan Islands", "Phang Nga town"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Similan Islands", "Phi Phi diving", "Phang Nga Bay", "Kata beach"],
            "วัฒนธรรม": ["Phuket Old Town", "Wat Chalong", "Phuket Museum", "Night market"],
            "ผจญภัย": ["Hanuman Zipline", "ATV on the hills", "Surfing at Kata", "Kitesurfing at Bang Tao"],
            "ผ่อนคลาย": ["Luxury spa", "Private Surin beach", "Seaside dinner"],
            "ครอบครัว": ["Phuket Aquarium", "Splash Jungle Waterpark", "Tiger Kingdom"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Phuket Old Town + Rang Hill viewpoint", "afternoon": "Big Buddha + Wat Chalong", "evening": "Lard Yai Night Market"},
            {"day": 2, "morning": "Phi Phi Island tour (early departure)", "afternoon": "Snorkelling at Maya Bay", "evening": "Rest at accommodation"},
            {"day": 3, "morning": "Patong beach / Kata beach", "afternoon": "Scooter ride around the island for views", "evening": "Bangla Road nightlife"},
        ]
    },

    "กระบี่": {
        "activities": [
            "Railay Beach (longtail boat access only)",
            "Koh Phi Phi – snorkelling and diving",
            "Four Island Tour",
            "Rock climbing at Railay",
            "Kayaking in Thalen Bay",
            "Ao Nang Beach",
            "Tiger Cave Temple – panoramic views",
            "Koh Lanta",
        ],
        "must_eat": [
            "Stir-fried crab with curry powder",
            "Oyster omelette (Hoi Tod)",
            "Papaya salad with fermented fish (Som Tam Pla Ra)",
            "Grilled river prawns",
            "Seafood congee",
            "Fresh coconut water",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight (Krabi Airport): 1.5 hours, THB 900–3,500",
                "Flight + ferry via Phuket or Surat Thani",
                "Bus + ferry: 12–15 hours"
            ],
            "In the area": [
                "Longtail boat: THB 50–150 per person",
                "Grab: available in Krabi Town",
                "Scooter rental: THB 200–300 per day",
                "Ferry to Koh Lanta: THB 100–200"
            ]
        },
        "budget_per_day": {
            "budget": "THB 600–1,000",
            "mid": "THB 1,800–3,000",
            "luxury": "THB 5,000–12,000+"
        },
        "accommodation": [
            "Pak-Up Hostel (Krabi Town, budget)",
            "Anyavee Tubkaek Beach Resort (mid-range)",
            "Rayavadee (Railay, luxury)",
            "The Tubkaek Tropical Beach Resort",
        ],
        "pantip_tips": [
            "Railay Beach is only accessible by boat — travel is comfortable only when the sea is calm",
            "When booking island tours, ask whether the boat is a speedboat or longtail — prices differ significantly",
            "Kayaking in Thalen Bay is only possible at high tide — check times before going",
            "Tiger Cave Temple has 1,237 steps — exhausting, but the view is absolutely worth it; go early in the morning",
            "Fresh seafood at Krabi new market is much cheaper than at the beach restaurants",
        ],
        "nearby_attractions": ["Koh Lanta", "Koh Phi Phi", "Railay", "Hong Islands", "Hot Springs Waterfall"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Koh Phi Phi", "Railay nature", "Hot Springs Waterfall Krabi"],
            "วัฒนธรรม": ["Tiger Cave Temple", "Old Krabi Town"],
            "ผจญภัย": ["Rock climbing at Railay", "Cave kayaking", "Four Island diving"],
            "ผ่อนคลาย": ["Railay beach", "Seaside spa", "Sunset at Ao Nang"],
            "ครอบครัว": ["Four Island Tour (large boat)", "Kata shallow beach", "Snorkelling and fish spotting"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Tiger Cave Temple + city views", "afternoon": "Ao Nang Beach – check in", "evening": "Krabi night market"},
            {"day": 2, "morning": "Full-day Four Island Tour", "afternoon": "Coral reef snorkelling", "evening": "Relax – Sunset Cruise"},
            {"day": 3, "morning": "Boat to Railay + rock climbing", "afternoon": "Swimming at Emerald Cave", "evening": "Seafood dinner"},
        ]
    },

    "เกาะสมุย": {
        "activities": [
            "Chaweng, Lamai, and Bo Phut beaches",
            "Big Buddha Samui",
            "Ang Thong Marine Park snorkelling",
            "Sunset Cruise",
            "ATV ride around the island",
            "Na Mueang Waterfall",
            "Fisherman's Village Friday Night Market",
        ],
        "must_eat": [
            "Crab fried rice",
            "Tom Yum Goong (spicy prawn soup)",
            "Stir-fried seafood with chilli (Pad Cha)",
            "Shrimp paste with crispy fish (Ka Pi Tod)",
            "Na Tan snack (local sweet)",
            "Shrimp paste chilli dip with vegetables",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight (Samui Airport): 1.5 hours, THB 2,000–6,000 (Bangkok Airways)",
                "Flight + ferry via Surat Thani: cheaper option, THB 1,200–2,500 + THB 150 ferry",
                "Bus + ferry: 12–15 hours"
            ],
            "On the island": [
                "Scooter rental: THB 200–300 per day",
                "Taxi / Grab: THB 150–500",
                "Car rental: THB 900–1,500 per day"
            ]
        },
        "budget_per_day": {
            "budget": "THB 800–1,500",
            "mid": "THB 2,500–4,000",
            "luxury": "THB 7,000–20,000+"
        },
        "accommodation": [
            "Samui Backpacker (budget)",
            "Baan Samui Resort (mid, Chaweng)",
            "Four Seasons Koh Samui (luxury)",
            "Conrad Koh Samui (luxury)",
        ],
        "pantip_tips": [
            "Bo Phut beach is much quieter than Chaweng — clearer water, better for those who dislike crowds",
            "Samui flights are expensive — if on a tight budget, fly to Surat Thani and take the ferry to save over 50%",
            "Fisherman's Village has a market every Friday night — a relaxed stroll with fresh seafood",
            "Do not rent a scooter if you are not an experienced rider — some Samui roads are steep and slippery",
            "Ang Thong Marine Park tour is best visited at high tide for the most impressive views",
        ],
        "nearby_attractions": ["Koh Phangan", "Koh Tao", "Ang Thong Marine Park", "Thong Sai Bay"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Ang Thong Marine Park", "Na Mueang Waterfall", "Lamai Beach"],
            "วัฒนธรรม": ["Big Buddha", "Wat Phra Yai", "Fisherman's Village"],
            "ผจญภัย": ["Koh Tao diving (day trip)", "ATV", "Jet Ski"],
            "ผ่อนคลาย": ["Chaweng Beach", "Luxury spa", "Sunset Cruise"],
            "ครอบครัว": ["Glass-bottom boat – coral viewing", "Quiet Bo Phut beach", "Waterfall"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Check in + Chaweng Beach", "afternoon": "Big Buddha + Na Mueang Waterfall", "evening": "Fisherman's Village Night Market"},
            {"day": 2, "morning": "Ang Thong Marine Park tour (full day)", "afternoon": "Snorkelling", "evening": "Sunset Cruise"},
            {"day": 3, "morning": "Bo Phut Beach – swimming", "afternoon": "Massage and spa", "evening": "Seaside dinner"},
        ]
    },

    "เกาะพะงัน": {
        "activities": [
            "Full Moon Party (on the full moon night)",
            "Haad Rin and Thong Nai Pan beaches",
            "Koh Tao diving (day trip)",
            "Yoga Retreat",
            "Motorbike ride around the island",
            "Natural Pool (jungle swimming hole)",
        ],
        "must_eat": [
            "Pineapple fried rice",
            "Seafood papaya salad",
            "Grilled squid",
            "Fresh young coconut",
            "Smoothie Bowl",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight to Samui + ferry: THB 2,500–4,000",
                "Flight to Surat Thani + ferry: THB 1,500–2,500",
                "Bus + ferry: THB 800–1,200"
            ],
            "On the island": [
                "Scooter rental: THB 200–300 per day",
                "Local taxi: THB 200–500",
                "Longtail boat to other beaches: THB 50–150"
            ]
        },
        "budget_per_day": {
            "budget": "THB 700–1,200",
            "mid": "THB 2,000–3,500",
            "luxury": "THB 5,000–12,000+"
        },
        "accommodation": [
            "Haad Rin Guesthouse (budget, near Full Moon Party)",
            "Anantara Rasananda (luxury)",
            "Cocohut Village (mid-range)",
        ],
        "pantip_tips": [
            "Full Moon Party is extremely crowded — belongings are often stolen on the beach; watch your valuables",
            "Half Moon Party and Black Moon Party are quieter alternatives",
            "Thong Nai Pan beach is very peaceful — ideal for Yoga Retreat, not suitable for party-lovers",
            "The roads around the island are very steep — do not rent a scooter at night if you are not experienced",
            "Seafood in Thongsala town is fairer priced than at Haad Rin beach",
        ],
        "nearby_attractions": ["Koh Tao", "Koh Samui", "Mae Haad Bay", "Koh Makao"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Natural Pool", "Thong Nai Pan beach", "Jungle greenery"],
            "วัฒนธรรม": ["Thongsala Temple", "Thongsala morning market"],
            "ผจญภัย": ["Koh Tao diving", "Mountain motorbike ride", "Rope Swing"],
            "ผ่อนคลาย": ["Yoga Retreat", "Hillside spa", "Private beach"],
            "ครอบครัว": ["Quiet beach", "Glass-bottom boat", "Coral snorkelling"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Check in + Haad Rin beach", "afternoon": "Motorbike ride around the island", "evening": "Sunset + dinner"},
            {"day": 2, "morning": "Koh Tao diving tour", "afternoon": "Snorkelling", "evening": "Return to Koh Phangan"},
            {"day": 3, "morning": "Morning Yoga Class", "afternoon": "Natural Pool + waterfall", "evening": "Full Moon / Half Moon Party"},
        ]
    },

    "น่าน": {
        "activities": [
            "Wat Phumin (famous murals)",
            "Wat Phra That Khao Noi – city viewpoint",
            "Bua Tong fields (October–November)",
            "Scenic drive on Route 1081",
            "Pha Nam Yoi Waterfall",
            "Ban Thai Lue village at Nong Bua",
            "Nan morning market",
            "Nan Museum",
        ],
        "must_eat": [
            "Nan Khao Soi (thinner noodles, different from Chiang Mai style)",
            "Gaeng Ho (mixed curry stew)",
            "Nan-style crispy pork",
            "Khao Pun (Nan-style rice noodles)",
            "Nam Ngiao (spiced pork and tomato broth)",
            "Kanom Tom Nam (boiled coconut dumplings)",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight (Nok Air direct to Nan): 1.5 hours, THB 800–2,500",
                "Bus: 8–10 hours, THB 400–700",
                "Train to Den Chai + connecting bus: 10–13 hours"
            ],
            "In the city": [
                "Bicycle rental: THB 50–100 per day (ideal in town)",
                "Scooter rental: THB 150–250 per day",
                "Taxi / samlor (three-wheeler): negotiate fare"
            ]
        },
        "budget_per_day": {
            "budget": "THB 400–700 (very affordable)",
            "mid": "THB 1,000–2,000",
            "luxury": "THB 2,500–5,000"
        },
        "accommodation": [
            "Cross Hostel Nan (budget, central)",
            "Nan Boutique Hotel (mid-range)",
            "Pukha Nanfa Hotel (mid-luxury)",
        ],
        "pantip_tips": [
            "Nan has no public buses — you need a rental or private driver; scooter recommended",
            "Wat Phumin requires modest dress; far fewer tourists than Chiang Mai",
            "Bua Tong fields at Doi Phu Kha in October–November are stunning but get crowded",
            "Nan is very affordable — meals around THB 40–60, good guesthouses under THB 500",
            "Nan's cafes are beautiful, great atmosphere, and reasonably priced",
        ],
        "nearby_attractions": ["Doi Phu Kha", "Ban Luang", "Pua District", "Wiang Sa"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Bua Tong fields", "Pha Nam Yoi Waterfall", "Doi Phu Kha"],
            "วัฒนธรรม": ["Wat Phumin", "Nan Museum", "Ban Thai Lue village"],
            "ผจญภัย": ["Nam Wa River rafting", "Mountain motorbike routes"],
            "ผ่อนคลาย": ["Morning market", "Riverside cafe", "Relaxing with mountain views"],
            "ครอบครัว": ["Temples in town", "Nan market", "Public park"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Wat Phumin + Wat Phra That Chang Kham", "afternoon": "Nan Museum + Old Town walk", "evening": "Evening market + local restaurant"},
            {"day": 2, "morning": "Wat Phra That Khao Noi – scenic viewpoint", "afternoon": "Nong Bua village – Ban Thai Lue", "evening": "Cafe with mountain views"},
            {"day": 3, "morning": "Doi Phu Kha / Bua Tong fields (if October)", "afternoon": "Pha Nam Yoi Waterfall", "evening": "Souvenir shopping"},
        ]
    },

    "เชียงราย": {
        "activities": [
            "Wat Rong Khun (White Temple)",
            "Wat Rong Suea Ten (Blue Temple)",
            "Doi Tung and Doi Tung Royal Villa",
            "Golden Triangle viewpoint",
            "Kad Luang Chiang Rai market",
            "Choui Fong tea plantation",
            "Baan Dam (Black House)",
            "Sunrise at Doi Chang",
        ],
        "must_eat": [
            "Chiang Rai Khao Soi",
            "Khao Pun (rice noodles)",
            "Crispy pork with garlic",
            "Laab Moo (spiced minced pork salad)",
            "Doi Chang coffee",
            "Chiang Rai pomelo",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight: 1.5 hours, THB 900–2,800",
                "Bus: 10–12 hours, THB 450–750"
            ],
            "In the city": [
                "Car / scooter rental: THB 200–1,000 per day",
                "Taxi / Grab",
                "Local songthaew: THB 20–40"
            ]
        },
        "budget_per_day": {
            "budget": "THB 500–900",
            "mid": "THB 1,500–2,500",
            "luxury": "THB 3,000–6,000+"
        },
        "accommodation": [
            "Baan Bua Guest House (budget)",
            "Le Meridien Chiang Rai (luxury)",
            "The Legend Chiang Rai (boutique riverside)",
        ],
        "pantip_tips": [
            "Check whether Wat Rong Khun is open before visiting — it occasionally closes for restoration",
            "Doi Tung requires a private vehicle to get there — no public transport",
            "The Golden Triangle viewpoint overlooks three countries (Thailand, Laos, Myanmar) but has become very commercialised",
            "Chiang Rai PM2.5 haze in March–April is very bad — avoid if possible",
            "Kad Luang market has cheap fresh produce and local food",
        ],
        "nearby_attractions": ["Mae Sai", "Chiang Saen", "Doi Mae Salong", "Chiang Khong"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Doi Tung", "Tea plantation", "Doi Mae Salong"],
            "วัฒนธรรม": ["White Temple", "Blue Temple", "Black House", "Golden Triangle"],
            "ผจญภัย": ["Cycling", "Mekong River cruise"],
            "ผ่อนคลาย": ["Chiang Rai cafes", "Doi Chang tea garden"],
            "ครอบครัว": ["White Temple", "Black House", "Evening market"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Wat Rong Khun (White Temple)", "afternoon": "Baan Dam + Wat Rong Suea Ten", "evening": "Chiang Rai Night Bazaar"},
            {"day": 2, "morning": "Doi Tung + Royal Villa", "afternoon": "Golden Triangle + Chiang Saen", "evening": "By the Mekong River"},
            {"day": 3, "morning": "Doi Chang tea plantation", "afternoon": "Kad Luang market – souvenir shopping", "evening": "Local dinner"},
        ]
    },

    "หัวหิน": {
        "activities": [
            "Hua Hin Beach (5 km long)",
            "Cicada Night Market",
            "Marigold Flower Field",
            "Black Mountain Water Park",
            "Horseback riding on the beach",
            "Hua Hin Hills Vineyard",
            "Kaeng Krachan National Park (nearby)",
            "Golf – several top-ranked courses",
        ],
        "must_eat": [
            "Grilled river prawns – Hua Hin specialty",
            "Fresh seafood at the lower market",
            "Large blue swimmer crab",
            "Hua Hin-style rice salad",
            "Old-fashioned handmade ice cream",
            "Fresh-squeezed limeade",
        ],
        "transportation": {
            "From Bangkok": [
                "Private car: 3–4 hours (expressway + Route 35)",
                "Bus: 4–5 hours, THB 150–250",
                "Train: 4–5 hours, THB 50–300"
            ],
            "In the city": [
                "Metered taxi / Grab",
                "Scooter rental: THB 150–250 per day",
                "Samlor (three-wheeler): THB 50–150"
            ]
        },
        "budget_per_day": {
            "budget": "THB 600–1,000",
            "mid": "THB 1,800–3,000",
            "luxury": "THB 5,000–15,000+ (luxury beachfront hotel)"
        },
        "accommodation": [
            "Baan Talay Hostel (budget)",
            "Anantara Hua Hin Resort (mid-luxury)",
            "Rosewood Hua Hin (ultra luxury)",
            "Intercontinental Hua Hin (luxury)",
        ],
        "pantip_tips": [
            "Hua Hin beach is very long — the far end is much quieter than the main town section",
            "On weekends, Bangkok visitors flock here — heavy traffic; leave before 6 am",
            "Cicada Night Market is open Thursday to Sunday only",
            "The lower market in Hua Hin has cheap, fresh seafood — far better value than hotel restaurants",
            "Best season: November–May; the sea is murky during the rainy season",
        ],
        "nearby_attractions": ["Khao Takiap", "Kaeng Krachan Waterfall", "Phetchaburi", "Cha-am"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Kaeng Krachan", "Khao Takiap", "Khao Takiap beach"],
            "วัฒนธรรม": ["Klai Kangwon Palace", "Mrigadayavan Palace"],
            "ผจญภัย": ["Golf", "Black Mountain Water Park", "Horseback riding on the beach"],
            "ผ่อนคลาย": ["Hotel spa", "Beach sunset", "Wine bar"],
            "ครอบครัว": ["Black Mountain Water Park", "Horseback riding", "Marigold Field"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Hua Hin Beach + horseback riding", "afternoon": "Khao Takiap – scenic viewpoint", "evening": "Cicada Night Market"},
            {"day": 2, "morning": "Marigold Field / flower farm", "afternoon": "Mrigadayavan Palace", "evening": "Fresh seafood at the lower market"},
        ]
    },

    "ตรัง": {
        "activities": [
            "Koh Kradan (one of Thailand's clearest seas)",
            "Koh Mook – Emerald Cave",
            "Koh Cheuk and Koh Waen",
            "Trang island group snorkelling and diving",
            "Cave kayaking",
            "Chao Mai Beach",
            "Trang morning market",
            "Trang Museum",
        ],
        "must_eat": [
            "Trang-style rice porridge (with crispy pork)",
            "Trang roast pork (Moo Yang Trang)",
            "Trang roti (fresh, soft flatbread)",
            "Traditional Trang coffee",
            "Trang-style steamed cake",
            "Pa Thong Ko (Chinese fried dough)",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight: 1.5 hours, THB 900–2,500 (Nok Air, Thai AirAsia)",
                "Bus + ferry: 12–15 hours"
            ],
            "In the area": [
                "Longtail boat / speedboat to islands: THB 100–300",
                "Local taxi",
                "Scooter rental: THB 150–250 per day"
            ]
        },
        "budget_per_day": {
            "budget": "THB 500–900 (very affordable)",
            "mid": "THB 1,500–2,500",
            "luxury": "THB 3,500–8,000+"
        },
        "accommodation": [
            "Koh Ngai Resort (on the island, mid-range)",
            "Anantara Si Kao (luxury)",
            "Trang Hotel (budget, in town)",
        ],
        "pantip_tips": [
            "Koh Kradan has the clearest water in Thailand — only visit November–May",
            "The Emerald Cave at Koh Mook is only accessible at low tide — you must swim through a dark tunnel; a guided tour is required",
            "Trang is still under the radar — far fewer tourists than Krabi or Phuket, and significantly cheaper",
            "Traditional Trang coffee is delicious — famous shops open early and fill up fast",
            "Trang roast pork is considered the best in the south — a must-try!",
        ],
        "nearby_attractions": ["Koh Kradan", "Emerald Cave", "Trang island group", "Trang city"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Koh Kradan", "Emerald Cave", "Trang island diving"],
            "วัฒนธรรม": ["Trang morning market", "Museum", "Ancient temples"],
            "ผจญภัย": ["Cave kayaking", "Deep sea diving", "Swimming through Emerald Cave"],
            "ผ่อนคลาย": ["Private beach on Koh Kradan", "Sunset at Chao Mai Beach"],
            "ครอบครัว": ["Koh Cheuk snorkelling", "Sandy beach", "Local food market"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Trang morning market + traditional coffee", "afternoon": "Pier + travel to island", "evening": "Dinner – Trang roast pork"},
            {"day": 2, "morning": "Koh Kradan (full day)", "afternoon": "Snorkelling", "evening": "Bonfire on the beach"},
            {"day": 3, "morning": "Emerald Cave at Koh Mook", "afternoon": "Cave kayaking", "evening": "Return to town"},
        ]
    },

    "พัทยา": {
        "activities": [
            "Coral Island (Koh Larn)",
            "Water sports on the beach",
            "Pattaya Floating Market",
            "Sanctuary of Truth",
            "Walking Street nightlife",
            "Nong Nooch Tropical Garden",
            "Shopping at Central Pattaya",
            "Koh Larn diving",
        ],
        "must_eat": [
            "Fresh seafood by the sea",
            "Soy sauce marinated crab roe",
            "Deep-fried fish balls",
            "International food Pattaya-style",
        ],
        "transportation": {
            "From Bangkok": [
                "Car: 2–3 hours via expressway",
                "Bus: 3–4 hours, THB 100–200",
                "Train: available but very slow"
            ],
            "In Pattaya": [
                "Baht Bus (songthaew): THB 10 within city",
                "Grab: THB 80–300",
                "Ferry to Koh Larn: THB 30–50"
            ]
        },
        "budget_per_day": {
            "budget": "THB 600–1,000",
            "mid": "THB 2,000–3,500",
            "luxury": "THB 5,000–15,000+"
        },
        "accommodation": [
            "Inn Residence (budget)",
            "Holiday Inn Pattaya (mid)",
            "Hilton Pattaya (luxury, great sea view)",
        ],
        "pantip_tips": [
            "Koh Larn should not be visited on public holidays — extremely crowded, murky water; weekdays are far better",
            "Baht Bus costs THB 10 throughout its route but you need to know the stops",
            "Walking Street is not suitable for families with young children — it is an adult nightlife district",
            "Sanctuary of Truth is beautiful — visit in the morning for the best light and cooler temperature",
            "Seafood at the Pattaya night market is better value than beachside restaurants",
        ],
        "nearby_attractions": ["Koh Larn", "Khao Chi Chan", "Ancient City", "Sattahip"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Koh Larn", "Nong Nooch Garden"],
            "วัฒนธรรม": ["Sanctuary of Truth", "Floating Market"],
            "ผจญภัย": ["Parasailing", "Jet Ski", "Diving"],
            "ผ่อนคลาย": ["Spa", "Beach massage", "Rooftop dinner"],
            "ครอบครัว": ["Nong Nooch Tropical Garden", "Pattaya Elephant Village", "Ramayana Water Park"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Koh Larn (early departure)", "afternoon": "Snorkelling", "evening": "Walking Street"},
            {"day": 2, "morning": "Sanctuary of Truth", "afternoon": "Nong Nooch Garden", "evening": "Seafood dinner"},
        ]
    },

    "แม่ฮ่องสอน": {
        "activities": [
            "Jong Kham Lake",
            "Wat Jong Kham and Wat Jong Klang",
            "Doi Kiew Lom – sea of mist viewpoint",
            "Ban Rak Thai (Yunnan Chinese village)",
            "Tham Pla – Nam Lot Cave",
            "Hill tribe village (long-neck Karen)",
            "Pai (60 km away)",
        ],
        "must_eat": [
            "Mae Hong Son Khao Soi (Shan-style, with thinner noodles)",
            "Khanom Jin Nam Ngiao (rice noodles in pork-tomato broth)",
            "Gaeng Tai Pla (fish organ curry)",
            "Sticky rice with Shan sausage",
            "Ban Rak Thai coffee",
        ],
        "transportation": {
            "From Bangkok": [
                "Flight (via Chiang Mai): 1.5–3 hours, THB 1,500–4,000",
                "Car from Chiang Mai: 4–6 hours (Route 108, 1,864 curves)",
                "Bus from Chiang Mai: 5–7 hours, THB 150–250"
            ],
            "In the city": [
                "Scooter rental: THB 150–250 per day",
                "Car rental: THB 800–1,200 per day"
            ]
        },
        "budget_per_day": {
            "budget": "THB 400–700 (very affordable)",
            "mid": "THB 1,000–2,000",
            "luxury": "THB 2,500–5,000"
        },
        "accommodation": [
            "Johnnie House (budget, central)",
            "Maehongson Mountain Inn (mid)",
            "Imperial Mae Hong Son Resort (mid-luxury)",
        ],
        "pantip_tips": [
            "Mae Hong Son is remote — the 1,864-curve road can cause motion sickness; consider flying instead",
            "Sea of mist at Doi Kiew Lom: leave before 6 am",
            "Ban Rak Thai requires a hired vehicle or 4WD — no public transport",
            "If driving yourself, the Chiang Mai–Mae Hong Son route has stunning scenery but requires careful driving",
            "Mae Hong Son in March–April has very heavy PM2.5 haze — not recommended",
        ],
        "nearby_attractions": ["Pai", "Tham Pla Cave", "Pai Hot Springs", "Pai Memorial Bridge"],
        "best_activities_by_type": {
            "ธรรมชาติ": ["Doi Kiew Lom sea of mist", "Tham Pla – Nam Lot Cave", "Hot springs"],
            "วัฒนธรรม": ["Wat Jong Kham – Wat Jong Klang", "Hill tribe village", "Ban Rak Thai"],
            "ผจญภัย": ["Drive the 1,864-curve route", "River rafting", "Jungle trekking"],
            "ผ่อนคลาย": ["Jong Kham Lake", "Cafe with mountain views"],
            "ครอบครัว": ["Morning market", "Temples in town", "Jong Kham Lake"]
        },
        "schedule_suggestions": [
            {"day": 1, "morning": "Doi Kiew Lom – sea of mist (depart 5 am)", "afternoon": "Mae Hong Son town – Wat Jong Kham", "evening": "Jong Kham Lake sunset"},
            {"day": 2, "morning": "Tham Pla – Nam Lot Cave", "afternoon": "Long-neck Karen hill tribe village", "evening": "Morning-to-evening market"},
            {"day": 3, "morning": "Ban Rak Thai + mountain scenery", "afternoon": "Drive back via Pai", "evening": "One night in Pai"},
        ]
    },
}

# Default for destinations not in the database
DEFAULT_TRAVEL_INFO = {
    "activities": ["Walk around the town", "Visit temples and historic sites", "Local market", "Local cuisine"],
    "must_eat": ["Local regional food", "Fresh fruit", "Seafood (if on the coast)"],
    "transportation": {
        "General": ["Public transport", "Scooter rental", "Taxi"]
    },
    "budget_per_day": {
        "budget": "THB 400–800",
        "mid": "THB 1,200–2,500",
        "luxury": "THB 3,000–8,000+"
    },
    "pantip_tips": [
        "Search travel forums and community groups for the latest tips before visiting",
        "Book accommodation in advance for public holidays",
        "Carry plenty of water, especially in hot season",
    ]
}


def _normalize_location(location: str) -> str:
    if not location:
        return None
    location = location.strip()
    if location in TRAVEL_KNOWLEDGE_BASE:
        return location
    for dest in TRAVEL_KNOWLEDGE_BASE:
        if dest in location or location in dest:
            return dest
    keywords = {
        "chiang mai": "เชียงใหม่",
        "พะงัน": "เกาะพะงัน",
        "phangan": "เกาะพะงัน",
        "koh phangan": "เกาะพะงัน",
        "สมุย": "เกาะสมุย",
        "koh samui": "เกาะสมุย",
        "เลย": "เลย",
        "กทม": "กรุงเทพ",
        "bangkok": "กรุงเทพ",
        "phuket": "ภูเก็ต",
        "chiangmai": "เชียงใหม่",
        "krabi": "กระบี่",
        "pattaya": "พัทยา",
        "samui": "เกาะสมุย",
        "chiang rai": "เชียงราย",
        "chiangrai": "เชียงราย",
        "hua hin": "หัวหิน",
        "huahin": "หัวหิน",
        "trang": "ตรัง",
        "nan": "น่าน",
        "mae hong son": "แม่ฮ่องสอน",
        "maehongson": "แม่ฮ่องสอน",
        "prachuap": "ประจวบคีรีขันธ์",
        "prachuap khiri khan": "ประจวบคีรีขันธ์",
        "loei": "เลย",
        "khon kaen": "ขอนแก่น",
        "ayutthaya": "อยุธยา",
        "sukhothai": "สุโขทัย",
        "phu kradueng": "ภูกระดึง",
    }
    lower = location.lower()
    for kw, dest in keywords.items():
        if kw in lower:
            return dest
    return None


def _filter_by_activity_type(data: dict, activity_type: str) -> list:
    if not activity_type:
        return data.get("activities", [])
    activity_aliases = {
        "nature": "ธรรมชาติ",
        "culture": "วัฒนธรรม",
        "adventure": "ผจญภัย",
        "relaxation": "ผ่อนคลาย",
        "relax": "ผ่อนคลาย",
        "family": "ครอบครัว",
    }
    normalized_activity = activity_aliases.get(activity_type.lower(), activity_type)
    by_type = data.get("best_activities_by_type", {})
    for key in by_type:
        if normalized_activity in key or key in normalized_activity:
            return by_type[key]
    return data.get("activities", [])


def _filter_by_budget(data: dict, budget: str) -> str:
    budget_guide = data.get("budget_per_day", DEFAULT_TRAVEL_INFO["budget_per_day"])
    if budget == "budget":
        return f"Budget: {budget_guide.get('budget', 'N/A')}"
    elif budget == "luxury":
        return f"Luxury: {budget_guide.get('luxury', 'N/A')}"
    else:
        return f"Mid-range: {budget_guide.get('mid', 'N/A')}"


def search_travel_info(
    query: str,
    location: str = None,
    activity_type: str = None,
    budget: str = None
) -> dict:
    """
    Search for travel information from the Thai tourism knowledge base.

    Args:
        query: Search query
        location: Destination or province
        activity_type: Activity type (ธรรมชาติ/วัฒนธรรม/ผจญภัย/ผ่อนคลาย/ครอบครัว)
        budget: Budget level (budget/mid/luxury)

    Returns:
        dict: Comprehensive travel information
    """
    normalized = _normalize_location(location) if location else None

    if normalized and normalized in TRAVEL_KNOWLEDGE_BASE:
        data = TRAVEL_KNOWLEDGE_BASE[normalized]
    else:
        # Try searching from the query
        for dest_name, dest_data in TRAVEL_KNOWLEDGE_BASE.items():
            if dest_name in query:
                normalized = dest_name
                data = dest_data
                break
        else:
            data = DEFAULT_TRAVEL_INFO
            normalized = location or "Unknown"

    activities = _filter_by_activity_type(data, activity_type)
    budget_info = _filter_by_budget(data, budget)

    return {
        "location": normalized,
        "original_location": location,
        "query": query,
        "activity_type_filter": activity_type,
        "budget_filter": budget,
        "results": {
            "activities": activities,
            "all_activities_by_type": data.get("best_activities_by_type", {}),
            "food": data.get("must_eat", DEFAULT_TRAVEL_INFO["must_eat"]),
            "transportation": data.get("transportation", DEFAULT_TRAVEL_INFO["transportation"]),
            "budget_guide": {
                "selected": budget_info,
                "all": data.get("budget_per_day", DEFAULT_TRAVEL_INFO["budget_per_day"])
            },
            "accommodation": data.get("accommodation", []),
            "tips": data.get("pantip_tips", DEFAULT_TRAVEL_INFO["pantip_tips"]),
            "nearby_attractions": data.get("nearby_attractions", []),
            "schedule_suggestions": data.get("schedule_suggestions", []),
        },
        "source": "Thai Tourism Knowledge Base (community travel blogs)",
        "disclaimer": "Prices and information may change seasonally — please verify before travelling"
    }
