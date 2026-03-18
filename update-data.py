#!/usr/bin/env python3
"""PHL Underground Nightly Data Refresh — Run #2 (March 18, 2026)"""

import re
import json
from datetime import datetime

TODAY = "2026-03-18"
DATA_FILE = "client/src/data/philly-data.ts"

with open(DATA_FILE, "r") as f:
    content = f.read()

# ═══════════════════════════════════════════════════════════════
# 1. REMOVE EXPIRED EVENTS (date before today)
# ═══════════════════════════════════════════════════════════════

# Find event-35 (Sticky Fingers, Mar 17) — already passed
# We need to remove the entire object block for it
expired_ids = []

# Parse all event dates and check
event_blocks = re.finditer(
    r'  \{\s*\n\s*id:\s*"(event-\d+)",\s*\n\s*name:\s*"([^"]+)",\s*\n\s*date:\s*"([^"]+)"',
    content
)

for match in event_blocks:
    eid = match.group(1)
    ename = match.group(2)
    raw_date = match.group(3)
    
    # Handle multi-date formats
    # "2026-03-20 and 2026-03-22" -> use last date
    # "2026-03-28 to 2026-03-29" -> use last date
    # "2026-03-21 to 2026-04-25 (Saturdays)" -> use last date
    # "Through 2026-04-26" -> use that date
    # "2026-03-21 (recurring)" -> use that date
    
    dates_found = re.findall(r'(\d{4}-\d{2}-\d{2})', raw_date)
    if dates_found:
        last_date = max(dates_found)
        if last_date < TODAY:
            expired_ids.append((eid, ename, raw_date))

print(f"Expired events to remove: {len(expired_ids)}")
for eid, ename, d in expired_ids:
    print(f"  - {eid}: {ename} ({d})")

# Remove expired event blocks
for eid, ename, _ in expired_ids:
    # Find the block: from "  {" to "  },"
    pattern = re.compile(
        r'  \{\s*\n\s*id:\s*"' + re.escape(eid) + r'".*?\n\s*isInsider:\s*(?:true|false),?\s*\n\s*\},?\n',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + content[match.end():]
        print(f"  Removed {eid}: {ename}")
    else:
        print(f"  WARNING: Could not find block for {eid}")

# ═══════════════════════════════════════════════════════════════
# 2. ADD NEW EVENTS (starting from event-59)
# ═══════════════════════════════════════════════════════════════

new_events = [
    {
        "id": "event-59",
        "name": "Ministry of Awe — Immersive Art Experience",
        "date": "2026-03-18 to 2026-05-31",
        "time": "Various",
        "venue": "Ministry of Awe",
        "address": "36 S. 2nd Street, Philadelphia, PA 19106",
        "neighborhood": "Old City",
        "category": "art",
        "description": "Philadelphia\\'s newest immersive art destination has opened in Old City — a multi-room experience blending projection-mapped environments, interactive installations, and sensory storytelling. A must-visit for art lovers and Instagram content alike.",
        "price": "$30+",
        "vibeTag": "immersive",
        "source": "phillyvoice.com / uwishunu.com",
        "lat": 39.9476,
        "lng": -75.1462,
        "isInsider": True,
    },
    {
        "id": "event-60",
        "name": "Beyoncé + Gaga Night at Underground Arts",
        "date": "2026-03-27",
        "time": "9:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "nightlife",
        "description": "A full night dedicated to the queens of pop — DJ sets spinning Beyoncé and Lady Gaga all night. Dance party vibes with themed cocktails and costumes encouraged. One of Underground Arts\\' most anticipated themed nights.",
        "price": "$15-25",
        "vibeTag": "underground",
        "source": "undergroundarts.org",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-61",
        "name": "Florence + The Machine at Xfinity Mobile Arena",
        "date": "2026-04-25",
        "time": "8:00 PM",
        "venue": "Xfinity Mobile Arena",
        "address": "3601 S. Broad Street, Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "music",
        "description": "Florence Welch brings her ethereal, powerhouse vocals and theatrical stage presence to South Philly. One of the biggest arena shows this spring, following her acclaimed new album cycle.",
        "price": "$65+",
        "vibeTag": "mainstream",
        "source": "livenation.com",
        "lat": 39.9012,
        "lng": -75.1745,
        "isInsider": False,
    },
    {
        "id": "event-62",
        "name": "Snail Mail at The Fillmore Philadelphia",
        "date": "2026-04-16",
        "time": "8:00 PM",
        "venue": "The Fillmore Philadelphia",
        "address": "29 E Allen Street, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "music",
        "description": "Lindsey Jordan (Snail Mail) brings dreamy indie rock to The Fillmore. One of the defining voices of modern indie with emotionally charged songwriting and a devoted fanbase.",
        "price": "$35+",
        "vibeTag": "indie",
        "source": "thefillmorephilly.com",
        "lat": 39.9672,
        "lng": -75.1361,
        "isInsider": True,
    },
    {
        "id": "event-63",
        "name": "Waxahatchee at The Met Philadelphia",
        "date": "2026-04-18",
        "time": "8:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N. Broad Street, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "music",
        "description": "Katie Crutchfield\\'s acclaimed alt-country project takes the stage at The Met — one of Philly\\'s most stunning concert venues. Following the success of Tigers Blood, this is one of the most anticipated indie shows of the spring.",
        "price": "$40+",
        "vibeTag": "indie",
        "source": "themetphilly.com",
        "lat": 39.9681,
        "lng": -75.1586,
        "isInsider": True,
    },
    {
        "id": "event-64",
        "name": "Gary Numan at Keswick Theatre",
        "date": "2026-03-18",
        "time": "8:00 PM",
        "venue": "Keswick Theatre",
        "address": "291 N. Keswick Avenue, Glenside, PA 19038",
        "neighborhood": "Glenside",
        "category": "music",
        "description": "Synth-pop and industrial pioneer Gary Numan plays the intimate Keswick Theatre tonight. The \\'Cars\\' hitmaker continues to evolve with dark, atmospheric soundscapes that influenced generations of electronic and industrial artists.",
        "price": "$45+",
        "vibeTag": "underground",
        "source": "keswicktheatre.com",
        "lat": 40.1020,
        "lng": -75.1530,
        "isInsider": True,
    },
    {
        "id": "event-65",
        "name": "Drain at Union Transfer",
        "date": "2026-03-27",
        "time": "7:30 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Santa Cruz hardcore band Drain brings mosh-pit energy to Union Transfer. Known for their crossover thrash sound and high-octane live shows — expect crowd surfers and wall-to-wall energy.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "r5productions.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-66",
        "name": "The Brook & The Bluff at Union Transfer",
        "date": "2026-03-31",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Birmingham indie-pop quartet The Brook & The Bluff bring lush harmonies and feel-good energy to Union Transfer. A rising act with a sound somewhere between Hozier and Vance Joy.",
        "price": "$25+",
        "vibeTag": "indie",
        "source": "r5productions.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-67",
        "name": "Thursday at Union Transfer",
        "date": "2026-04-02",
        "time": "7:30 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Post-hardcore legends Thursday return to Philly. Geoff Rickly and crew helped define early 2000s emo and post-hardcore — if you know, you know. A cult favorite reunion show.",
        "price": "$35+",
        "vibeTag": "underground",
        "source": "r5productions.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-68",
        "name": "Sunn O))) at Union Transfer",
        "date": "2026-04-11",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Drone metal titans Sunn O))) deliver their signature wall of amplified sound and smoke at Union Transfer. A visceral, almost spiritual experience — wear earplugs and prepare to have your chest vibrate.",
        "price": "$30+",
        "vibeTag": "underground",
        "source": "r5productions.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-69",
        "name": "Alice Phoebe Lou at Union Transfer",
        "date": "2026-04-14",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "South African-born, Berlin-based singer-songwriter Alice Phoebe Lou brings her folk-tinged dream pop to Union Transfer. Started as a Berlin busker, now selling out venues worldwide with her intimate, hypnotic sound.",
        "price": "$30+",
        "vibeTag": "indie",
        "source": "r5productions.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-70",
        "name": "Tigers Jaw at Union Transfer",
        "date": "2026-04-16",
        "time": "7:30 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Scranton-born indie/emo heroes Tigers Jaw play a hometown-ish show at Union Transfer. A cornerstone of Pennsylvania\\'s indie rock scene with a catalog full of crowd singalongs.",
        "price": "$25+",
        "vibeTag": "indie",
        "source": "r5productions.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-71",
        "name": "Pancakes & Booze Art Show at Underground Arts",
        "date": "2026-04-04",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "art",
        "description": "A traveling art show featuring 100+ local and national artists, live body painting, a DJ, free all-you-can-eat pancakes, and a full bar. One of the most fun, casual ways to discover underground art and party at the same time.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "undergroundarts.org",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
]

# ═══════════════════════════════════════════════════════════════
# 3. ADD NEW HOTSPOTS (starting from spot-51)
# ═══════════════════════════════════════════════════════════════

new_hotspots = [
    {
        "id": "spot-51",
        "name": "Adda",
        "type": "restaurant",
        "address": "1811 Frankford Avenue, Philadelphia, PA 19125",
        "neighborhood": "Kensington",
        "description": "Modern Indian restaurant from chef Anup Joshi bringing creative takes on regional Indian cuisine to Frankford Ave. Inventive small plates, tandoori dishes, and craft cocktails with Indian-inspired flavors. One of 2026\\'s most buzzed-about new openings.",
        "vibeTag": "trendy",
        "priceRange": "$$$",
        "cuisine": "Indian",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9740,
        "lng": -75.1271,
        "source": "inquirer.com / phillymag.com",
    },
    {
        "id": "spot-52",
        "name": "Ayat",
        "type": "restaurant",
        "address": "1700 Sansom Street, Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse",
        "description": "Palestinian restaurant from celebrated Brooklyn chef Abdul Elenani, expanding from NYC to Philly. Known for musakhan rolls, lamb shank mansaf, and knafeh. A meaningful cultural dining experience with flavors you won\\'t find anywhere else in the city.",
        "vibeTag": "buzzing",
        "priceRange": "$$",
        "cuisine": "Palestinian",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9510,
        "lng": -75.1710,
        "source": "inquirer.com / eater.com",
    },
    {
        "id": "spot-53",
        "name": "7th Street Burger",
        "type": "restaurant",
        "address": "1100 Frankford Avenue, Philadelphia, PA 19125",
        "neighborhood": "Fishtown",
        "description": "NYC smash burger cult favorite expands to Fishtown. Thin, crispy-edged patties with melted American cheese, griddle-smashed to perfection. Simple menu, no frills, just one of the best burgers you\\'ll have. Cash and card.",
        "vibeTag": "buzzing",
        "priceRange": "$",
        "cuisine": "Burgers",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9690,
        "lng": -75.1335,
        "source": "phillymag.com / inquirer.com",
    },
    {
        "id": "spot-54",
        "name": "Terra Grill",
        "type": "restaurant",
        "address": "1004 N. 2nd Street, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "description": "Live-fire cooking restaurant in NoLibs featuring a wood-fired grill and rotisserie as centerpieces. Seasonal, locally sourced menu with charred vegetables, whole-roasted meats, and natural wines. An intimate, smoke-kissed dining experience.",
        "vibeTag": "trendy",
        "priceRange": "$$$",
        "cuisine": "American",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9630,
        "lng": -75.1425,
        "source": "inquirer.com",
    },
    {
        "id": "spot-55",
        "name": "Soufiane at the Morris",
        "type": "restaurant",
        "address": "225 S. 8th Street, Philadelphia, PA 19106",
        "neighborhood": "Washington Square West",
        "description": "Moroccan-French fine dining in the historic Morris House Hotel. Chef Soufiane Hachami brings tagines, couscous royale, and North African spices to a stunning setting with a courtyard garden. One of the most elegant new restaurants in the city.",
        "vibeTag": "exclusive",
        "priceRange": "$$$$",
        "cuisine": "Moroccan-French",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9468,
        "lng": -75.1535,
        "source": "inquirer.com / phillymag.com",
    },
    {
        "id": "spot-56",
        "name": "Bar Caviar",
        "type": "bar",
        "address": "1523 Walnut Street, Philadelphia, PA 19102",
        "neighborhood": "Rittenhouse",
        "description": "Upscale cocktail lounge and caviar bar on Walnut Street. Champagne flights, caviar bumps, oysters on the half shell, and meticulously crafted cocktails in a dimly lit, velvet-draped space. A glamorous new addition to Rittenhouse nightlife.",
        "vibeTag": "exclusive",
        "priceRange": "$$$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 39.9502,
        "lng": -75.1672,
        "source": "phillymag.com",
    },
    {
        "id": "spot-57",
        "name": "Lovechild",
        "type": "bar",
        "address": "901 N. 2nd Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "description": "The newest cocktail bar from the team behind Good King Tavern. Creative drinks program with rotating seasonal menus, vinyl DJ sets on weekends, and a cozy back patio. Already generating word-of-mouth buzz in the Spring Garden bar scene.",
        "vibeTag": "chill",
        "priceRange": "$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 39.9618,
        "lng": -75.1425,
        "source": "phillyvoice.com",
    },
]

# ═══════════════════════════════════════════════════════════════
# 4. INSERT NEW EVENTS before the closing "];" of events array
# ═══════════════════════════════════════════════════════════════

def format_event(e):
    lines = []
    lines.append("  {")
    lines.append(f'    id: "{e["id"]}",')
    lines.append(f'    name: "{e["name"]}",')
    lines.append(f'    date: "{e["date"]}",')
    lines.append(f'    time: "{e["time"]}",')
    lines.append(f'    venue: "{e["venue"]}",')
    lines.append(f'    address: "{e["address"]}",')
    lines.append(f'    neighborhood: "{e["neighborhood"]}",')
    lines.append(f'    category: "{e["category"]}",')
    lines.append(f'    description: "{e["description"]}",')
    lines.append(f'    price: "{e["price"]}",')
    lines.append(f'    vibeTag: "{e["vibeTag"]}",')
    lines.append(f'    source: "{e["source"]}",')
    lines.append(f'    lat: {e["lat"]},')
    lines.append(f'    lng: {e["lng"]},')
    lines.append(f'    isInsider: {"true" if e["isInsider"] else "false"},')
    lines.append("  },")
    return "\n".join(lines)

def format_hotspot(h):
    lines = []
    lines.append("  {")
    lines.append(f'    id: "{h["id"]}",')
    lines.append(f'    name: "{h["name"]}",')
    lines.append(f'    type: "{h["type"]}",')
    lines.append(f'    address: "{h["address"]}",')
    lines.append(f'    neighborhood: "{h["neighborhood"]}",')
    lines.append(f'    description: "{h["description"]}",')
    lines.append(f'    vibeTag: "{h["vibeTag"]}",')
    lines.append(f'    priceRange: "{h["priceRange"]}",')
    if h["cuisine"] is None:
        lines.append(f'    cuisine: null,')
    else:
        lines.append(f'    cuisine: "{h["cuisine"]}",')
    lines.append(f'    isNew: {"true" if h["isNew"] else "false"},')
    lines.append(f'    isInsider: {"true" if h["isInsider"] else "false"},')
    lines.append(f'    lat: {h["lat"]},')
    lines.append(f'    lng: {h["lng"]},')
    lines.append(f'    source: "{h["source"]}",')
    lines.append("  },")
    return "\n".join(lines)

# Insert new events before the end of events array
events_end_marker = "\n];\n\nexport const hotspots"
events_insert = "\n" + "\n".join(format_event(e) for e in new_events) + "\n"
content = content.replace(events_end_marker, events_insert + events_end_marker)
print(f"\nAdded {len(new_events)} new events (event-59 through event-71)")

# Insert new hotspots before the end of hotspots array
# Find the end of hotspots array — it ends with "];\n\nexport const influencers"
hotspots_end_marker = "\n];\n\nexport const influencers"
hotspots_insert = "\n" + "\n".join(format_hotspot(h) for h in new_hotspots) + "\n"
content = content.replace(hotspots_end_marker, hotspots_insert + hotspots_end_marker)
print(f"Added {len(new_hotspots)} new hotspots (spot-51 through spot-57)")

# ═══════════════════════════════════════════════════════════════
# 5. UPDATE INFLUENCER RECENT PICKS
# ═══════════════════════════════════════════════════════════════

# Wooder Ice — add new picks at the top of recentPicks
wooder_new_picks = """      { name: "Philadelphia\\'s Magic Gardens", type: "event", neighborhood: "South Street", quote: "Isaiah Zagar\\'s mosaic masterpiece on South Street — one of the most uniquely Philly experiences you can have. Always worth a visit with out-of-towners.", date: "March 17, 2026" },
      { name: "Battleship New Jersey", type: "event", neighborhood: "Camden Waterfront", quote: "Took the trip across the river to the Battleship NJ — massive warship museum with incredible views of the Philly skyline from the Delaware.", date: "March 17, 2026" },
      { name: "People\\'s Garden Philly", type: "event", neighborhood: "West Philly", quote: "Community garden spotlight — People\\'s Garden is one of the best examples of grassroots green space in the city. Support your local gardens.", date: "March 16, 2026" },"""

# Find Wooder Ice's recentPicks and add at the top
wooder_picks_marker = '    recentPicks: [\n      { name: "Diversitech 2026"'
if wooder_picks_marker in content:
    content = content.replace(
        wooder_picks_marker,
        '    recentPicks: [\n' + wooder_new_picks + '\n      { name: "Diversitech 2026"'
    )
    print("Updated Wooder Ice with 3 new picks")
else:
    print("WARNING: Could not find Wooder Ice recentPicks marker")

# Josh Moore — add new pick
josh_picks_marker = 'handle: "@josheatsphilly"'
josh_section_idx = content.find(josh_picks_marker)
if josh_section_idx != -1:
    josh_recent_idx = content.find("recentPicks: [", josh_section_idx)
    if josh_recent_idx != -1:
        insert_after = josh_recent_idx + len("recentPicks: [")
        josh_new_pick = """
      { name: "Dough Head Pizza Giveaway", type: "restaurant", neighborhood: "Fishtown", quote: "Running a giveaway with Dough Head Pizza — one of the best new pizza spots in Fishtown. Follow and tag a friend to win a pizza party for 4.", date: "March 17, 2026" },"""
        content = content[:insert_after] + josh_new_pick + content[insert_after:]
        print("Updated Josh Moore with 1 new pick")

# Kory Aversa — add new pick
kory_picks_marker = 'handle: "@koryaversa"'
kory_section_idx = content.find(kory_picks_marker)
if kory_section_idx != -1:
    kory_recent_idx = content.find("recentPicks: [", kory_section_idx)
    if kory_recent_idx != -1:
        insert_after = kory_recent_idx + len("recentPicks: [")
        kory_new_pick = """
      { name: "Adda", type: "restaurant", neighborhood: "Kensington", quote: "New Indian spot on Frankford Ave — creative small plates and tandoori that rival anything in NYC. Kensington keeps delivering.", date: "March 17, 2026" },"""
        content = content[:insert_after] + kory_new_pick + content[insert_after:]
        print("Updated Kory Aversa with 1 new pick")

# SwagFoodPhilly — add new pick
swag_picks_marker = 'handle: "@swagfoodphilly"'
swag_section_idx = content.find(swag_picks_marker)
if swag_section_idx != -1:
    swag_recent_idx = content.find("recentPicks: [", swag_section_idx)
    if swag_recent_idx != -1:
        insert_after = swag_recent_idx + len("recentPicks: [")
        swag_new_pick = """
      { name: "7th Street Burger", type: "restaurant", neighborhood: "Fishtown", quote: "NYC smash burger kings are now in Fishtown — crispy edges, melted cheese, simple menu. Go hungry.", date: "March 16, 2026" },"""
        content = content[:insert_after] + swag_new_pick + content[insert_after:]
        print("Updated SwagFoodPhilly with 1 new pick")

# PhillyFoodFanatic — add new pick
fanatic_picks_marker = 'handle: "@thephillyfoodfanatic"'
fanatic_section_idx = content.find(fanatic_picks_marker)
if fanatic_section_idx != -1:
    fanatic_recent_idx = content.find("recentPicks: [", fanatic_section_idx)
    if fanatic_recent_idx != -1:
        insert_after = fanatic_recent_idx + len("recentPicks: [")
        fanatic_new_pick = """
      { name: "Ayat", type: "restaurant", neighborhood: "Rittenhouse", quote: "Palestinian flavors from Brooklyn hitting Rittenhouse — musakhan rolls and lamb mansaf are incredible. A must-try new opening.", date: "March 17, 2026" },"""
        content = content[:insert_after] + fanatic_new_pick + content[insert_after:]
        print("Updated PhillyFoodFanatic with 1 new pick")

# ═══════════════════════════════════════════════════════════════
# 6. DEDUPLICATION CHECK
# ═══════════════════════════════════════════════════════════════

print("\n=== DEDUPLICATION CHECK ===")
dupes_removed = 0

# Extract all event names and IDs for dedup
event_entries = re.findall(
    r'id:\s*"(event-\d+)".*?name:\s*"([^"]+)".*?venue:\s*"([^"]*)"',
    content, re.DOTALL
)

# Check for duplicate event names (case-insensitive)
seen_events = {}
event_dupes = []
for eid, ename, venue in event_entries:
    key = ename.lower().strip()
    if key in seen_events:
        event_dupes.append((eid, ename, seen_events[key]))
    else:
        seen_events[key] = (eid, ename)

# Check for near-duplicates: same venue + very similar name
for i, (eid1, ename1, venue1) in enumerate(event_entries):
    for j, (eid2, ename2, venue2) in enumerate(event_entries):
        if i >= j:
            continue
        if venue1.lower() == venue2.lower() and venue1:
            # Same venue - check if names are very similar
            n1 = ename1.lower().replace("the ", "").strip()
            n2 = ename2.lower().replace("the ", "").strip()
            if n1 in n2 or n2 in n1:
                if (eid2, ename2, (eid1, ename1)) not in event_dupes and (eid1, ename1, (eid2, ename2)) not in event_dupes:
                    # Keep the one with longer description
                    event_dupes.append((eid2, ename2, (eid1, ename1)))

print(f"Event duplicates found: {len(event_dupes)}")
for eid, ename, original in event_dupes:
    print(f"  - {eid}: '{ename}' duplicates {original}")

# Remove event duplicates (keep the first/longer one)
for eid, ename, _ in event_dupes:
    pattern = re.compile(
        r'  \{\s*\n\s*id:\s*"' + re.escape(eid) + r'".*?\n\s*isInsider:\s*(?:true|false),?\s*\n\s*\},?\n',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + content[match.end():]
        dupes_removed += 1
        print(f"  Removed duplicate event: {eid}")

# Extract all hotspot names and IDs for dedup
spot_entries = re.findall(
    r'id:\s*"(spot-\d+)".*?name:\s*"([^"]+)".*?address:\s*"([^"]*)"',
    content, re.DOTALL
)

seen_spots = {}
spot_dupes = []
for sid, sname, addr in spot_entries:
    key = sname.lower().strip()
    if key in seen_spots:
        spot_dupes.append((sid, sname, seen_spots[key]))
    else:
        seen_spots[key] = (sid, sname)

# Check for near-duplicate hotspots: same address different name
for i, (sid1, sname1, addr1) in enumerate(spot_entries):
    for j, (sid2, sname2, addr2) in enumerate(spot_entries):
        if i >= j:
            continue
        if addr1.lower() == addr2.lower() and addr1:
            n1 = sname1.lower().strip()
            n2 = sname2.lower().strip()
            if n1 != n2:
                if (sid2, sname2, (sid1, sname1)) not in spot_dupes and (sid1, sname1, (sid2, sname2)) not in spot_dupes:
                    spot_dupes.append((sid2, sname2, (sid1, sname1)))

print(f"Hotspot duplicates found: {len(spot_dupes)}")
for sid, sname, original in spot_dupes:
    print(f"  - {sid}: '{sname}' duplicates {original}")

# Remove hotspot duplicates
for sid, sname, _ in spot_dupes:
    pattern = re.compile(
        r'  \{\s*\n\s*id:\s*"' + re.escape(sid) + r'".*?\n\s*source:\s*"[^"]*",?\s*\n\s*\},?\n',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + content[match.end():]
        dupes_removed += 1
        print(f"  Removed duplicate hotspot: {sid}")

# Check for duplicate IDs
all_ids = re.findall(r'id:\s*"([^"]+)"', content)
id_counts = {}
for id_val in all_ids:
    id_counts[id_val] = id_counts.get(id_val, 0) + 1
dup_ids = {k: v for k, v in id_counts.items() if v > 1}
if dup_ids:
    print(f"WARNING: Duplicate IDs found: {dup_ids}")
else:
    print("All IDs are unique ✓")

print(f"\nTotal duplicates removed: {dupes_removed}")

# ═══════════════════════════════════════════════════════════════
# 7. WRITE THE FILE
# ═══════════════════════════════════════════════════════════════

with open(DATA_FILE, "w") as f:
    f.write(content)

# Final count
final_events = len(re.findall(r'id:\s*"event-\d+"', content))
final_spots = len(re.findall(r'id:\s*"spot-\d+"', content))
final_influencers = len(re.findall(r'id:\s*"influencer-\d+"', content))

print(f"\n=== FINAL COUNTS ===")
print(f"Events: {final_events}")
print(f"Hotspots: {final_spots}")
print(f"Influencers: {final_influencers}")
print(f"File written successfully!")

# Write summary for notification
summary = {
    "date": TODAY,
    "events_added": len(new_events),
    "hotspots_added": len(new_hotspots),
    "expired_removed": len(expired_ids),
    "duplicates_removed": dupes_removed,
    "influencer_updates": 5,
    "final_events": final_events,
    "final_hotspots": final_spots,
    "new_event_names": [e["name"] for e in new_events],
    "new_hotspot_names": [h["name"] for h in new_hotspots],
    "expired_names": [f"{ename}" for _, ename, _ in expired_ids],
}
with open("update-summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nSummary written to update-summary.json")
