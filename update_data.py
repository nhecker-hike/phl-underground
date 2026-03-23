#!/usr/bin/env python3
"""PHL Underground Nightly Refresh #7 - March 23, 2026"""

import re
import json

DATA_FILE = "client/src/data/philly-data.ts"
TODAY = "2026-03-23"

with open(DATA_FILE, "r") as f:
    content = f.read()

# ============================================================
# STEP 1: Remove expired events (single-day events before today)
# For date ranges, check if the END date has passed
# ============================================================
expired_events = []

def is_expired(date_str):
    """Check if an event date has fully passed."""
    date_str = date_str.strip()
    # Handle "ongoing" - never expires
    if "ongoing" in date_str.lower():
        return False
    # Handle ranges: "2026-03-18 to 2026-03-29"
    if " to " in date_str:
        end_part = date_str.split(" to ")[-1].strip()
        # Extract just the date portion (remove day names, parenthetical notes)
        end_date = re.search(r'(\d{4}-\d{2}-\d{2})', end_part)
        if end_date:
            return end_date.group(1) < TODAY
        return False
    # Handle "and" dates: "2026-03-20 and 2026-03-22"
    if " and " in date_str:
        dates = re.findall(r'(\d{4}-\d{2}-\d{2})', date_str)
        if dates:
            return max(dates) < TODAY
        return False
    # Single date
    single = re.search(r'(\d{4}-\d{2}-\d{2})', date_str)
    if single:
        return single.group(1) < TODAY
    return False

# Find and remove expired events
event_block_pattern = r'  \{\s*id: "(event-\d+)",\s*name: "([^"]*)",\s*date: "([^"]*)".*?\n  \},'
for match in re.finditer(event_block_pattern, content, re.DOTALL):
    eid = match.group(1)
    name = match.group(2)
    date = match.group(3)
    if is_expired(date):
        expired_events.append((eid, name, date))
        content = content.replace(match.group(0), "")

print(f"Expired events removed: {len(expired_events)}")
for eid, name, date in expired_events:
    print(f"  - {name} ({date})")

# ============================================================
# STEP 2: Add new events
# Next available ID: event-112
# ============================================================
new_events = [
    {
        "id": "event-112",
        "name": "Obscura at Underground Arts",
        "date": "2026-03-23",
        "time": "7:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "German progressive death metal legends Obscura bring their technically dazzling live show to Underground Arts. Known for jaw-dropping musicianship and cosmic themes, this is a must-see for anyone into heavy, cerebral music in an intimate basement venue.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "undergroundarts.org",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-113",
        "name": "Rebirth Brass Band at Underground Arts",
        "date": "2026-03-26",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "New Orleans brass royalty Rebirth Brass Band rolls into Underground Arts for a night of second-line grooves, funk, and pure party energy. Grammy winners known for turning any room into a Mardi Gras celebration -- standing room only, bring your dancing shoes.",
        "price": "$30+",
        "vibeTag": "local-favorite",
        "source": "undergroundarts.org",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-114",
        "name": "The Dirty Three at Underground Arts",
        "date": "2026-04-02",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Australian instrumental trio The Dirty Three -- violin, drums, guitar -- deliver sprawling, emotionally devastating sets that feel like watching a storm roll in. A rare Philly appearance for one of the most singular live bands on the planet. If you know, you know.",
        "price": "$35+",
        "vibeTag": "underground",
        "source": "undergroundarts.org / concertfix.com",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-115",
        "name": "The Old 97's at Underground Arts",
        "date": "2026-04-03",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Alt-country pioneers The Old 97s bring decades of raucous, whiskey-soaked anthems to Underground Arts. Rhett Miller and crew are known for high-energy shows that blur the line between punk and country -- perfect for a Friday night in the basement.",
        "price": "$30+",
        "vibeTag": "underground",
        "source": "undergroundarts.org / concertfix.com",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-116",
        "name": "Odumodublvck at Underground Arts",
        "date": "2026-04-08",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Nigerian Afrobeats and rap star Odumodublvck brings his viral energy to Underground Arts. Known for genre-blending tracks that mix Afrobeats, amapiano, and hip-hop, this is one of the most exciting young international acts hitting Philly this spring.",
        "price": "$30+",
        "vibeTag": "underground",
        "source": "undergroundarts.org",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-117",
        "name": "Riot Nerd: Beyonce and Lady Gaga Night at Underground Arts",
        "date": "2026-03-27",
        "time": "10:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "nightlife",
        "description": "A multi-room dance party celebrating the queens of pop -- Beyonce and Lady Gaga all night long. DJs spin deep cuts and hits across multiple rooms at Underground Arts. Late start, high energy, and costumes encouraged.",
        "price": "$15+",
        "vibeTag": "underground",
        "source": "undergroundarts.org / concertfix.com",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-118",
        "name": "Pablo Batista: Primera Primavera Latin Jazz Orchestra",
        "date": "2026-04-17",
        "time": "7:30 PM",
        "venue": "Perelman Theater",
        "address": "300 S. Broad Street, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "music",
        "description": "Grammy Award-winning percussionist Pablo Batista leads a 20-piece big band in vintage formal wear through legendary Latin jazz tunes. The inaugural Primera Primavera concert kicks off a new annual Latin jazz series at Perelman Theater -- an intimate, one-night-only affair.",
        "price": "$30+",
        "vibeTag": "insider",
        "source": "visitphilly.com",
        "lat": 39.9468,
        "lng": -75.1649,
        "isInsider": True,
    },
    {
        "id": "event-119",
        "name": "McLusky at Underground Arts",
        "date": "2026-04-10",
        "time": "9:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Welsh noise-rock cult heroes McLusky are back from the dead and louder than ever. If you missed them the first time around, this is your shot -- abrasive, witty, and absolutely ferocious in a small room. One of the most anticipated underground shows of spring.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "undergroundarts.org / concertfix.com",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-120",
        "name": "Cut Worms at Underground Arts",
        "date": "2026-04-16",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Brooklyn songwriter Cut Worms channels vintage AM radio gold -- lush harmonies, twangy guitars, and a dreamy nostalgia that sounds like it was beamed in from 1966. A beautiful mid-week show for fans of lo-fi pop and classic songwriting.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "undergroundarts.org / concertfix.com",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
    {
        "id": "event-121",
        "name": "Die Krupps at Underground Arts",
        "date": "2026-03-29",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill Street, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "German industrial pioneers Die Krupps bring four decades of crushing electronic body music to Underground Arts. Legends of the EBM/industrial scene, known for fusing metal riffs with pounding synths. A rare US date for hardcore fans of the genre.",
        "price": "$35+",
        "vibeTag": "underground",
        "source": "undergroundarts.org / concertfix.com",
        "lat": 39.9590,
        "lng": -75.1580,
        "isInsider": True,
    },
]

# Check which new events already exist (by name, case-insensitive)
existing_names = set()
for m in re.finditer(r'name: "([^"]*)"', content):
    existing_names.add(m.group(1).lower().replace("\\'", "'"))

events_to_add = []
events_skipped = []
for ev in new_events:
    name_lower = ev["name"].lower()
    # Check exact match and partial matches
    already_exists = False
    for existing in existing_names:
        if name_lower == existing:
            already_exists = True
            break
    if already_exists:
        events_skipped.append(ev["name"])
    else:
        events_to_add.append(ev)

print(f"\nNew events to add: {len(events_to_add)}")
print(f"Events skipped (already exist): {len(events_skipped)}")
for name in events_skipped:
    print(f"  - {name}")

# Insert new events before the closing of the events array
if events_to_add:
    events_insert = ""
    for ev in events_to_add:
        insider_str = "true" if ev["isInsider"] else "false"
        escaped_name = ev["name"].replace("'", "\\'")
        escaped_desc = ev["description"].replace("'", "\\'")
        events_insert += f"""  {{
    id: "{ev['id']}",
    name: "{escaped_name}",
    date: "{ev['date']}",
    time: "{ev['time']}",
    venue: "{ev['venue']}",
    address: "{ev['address']}",
    neighborhood: "{ev['neighborhood']}",
    category: "{ev['category']}",
    description: "{escaped_desc}",
    price: "{ev['price']}",
    vibeTag: "{ev['vibeTag']}",
    source: "{ev['source']}",
    lat: {ev['lat']},
    lng: {ev['lng']},
    isInsider: {insider_str},
  }},
"""
    # Find the end of the events array and insert before it
    content = content.replace(
        "\n];\n\nexport const hotspots: HotSpot[] = [",
        "\n" + events_insert + "];\n\nexport const hotspots: HotSpot[] = ["
    )

# ============================================================
# STEP 3: Add new hotspots
# Next available ID: spot-77
# ============================================================
new_hotspots = [
    {
        "id": "spot-77",
        "name": "Shibam Coffee",
        "type": "cafe",
        "address": "4700 Baltimore Avenue, Philadelphia, PA 19143",
        "neighborhood": "West Philadelphia",
        "description": "A rare Yemeni coffeeshop in West Philly, open until midnight on Fridays and Saturdays. Serving traditional Yemeni coffee alongside snacks in a cozy, community-driven space. One of the few late-night cafe options on the west side.",
        "vibeTag": "insider",
        "priceRange": "$",
        "cuisine": "Yemeni coffee",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9490,
        "lng": -75.2190,
        "source": "Philadelphia Inquirer",
    },
    {
        "id": "spot-78",
        "name": "Duo Restaurant & Bar",
        "type": "restaurant",
        "address": "112 S. 18th Street, Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse",
        "description": "A sleek new Center City addition offering a menu that pairs globally inspired small plates with an inventive cocktail program. Modern space with moody lighting, perfect for a date night or happy hour near Rittenhouse Square.",
        "vibeTag": "trendy",
        "priceRange": "$$",
        "cuisine": "New American",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9521,
        "lng": -75.1710,
        "source": "Philadelphia Inquirer",
    },
    {
        "id": "spot-79",
        "name": "Carmen\\'s Table",
        "type": "restaurant",
        "address": "1301 S. 9th Street, Philadelphia, PA 19147",
        "neighborhood": "South Philly",
        "description": "A new Italian-American spot on the edge of the Italian Market serving family-style classics with a modern touch. Homemade pasta, red sauce, and a warm neighborhood vibe that feels like Sunday dinner at nonna\\'s.",
        "vibeTag": "local-favorite",
        "priceRange": "$$",
        "cuisine": "Italian-American",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9337,
        "lng": -75.1589,
        "source": "Philadelphia Inquirer",
    },
    {
        "id": "spot-80",
        "name": "Ranstead Room",
        "type": "bar",
        "address": "2013 Ranstead Street, Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse",
        "description": "One of Philly\\'s best-kept secrets -- a hidden speakeasy behind El Rey, through a nondescript black door with mirrored R\\'s. Dark, moody 1930s vibes with leather booths and some of the city\\'s finest cocktails. If you have to ask where it is, you might not find it.",
        "vibeTag": "insider",
        "priceRange": "$$$",
        "cuisine": None,
        "isNew": False,
        "isInsider": True,
        "lat": 39.9530,
        "lng": -75.1744,
        "source": "Tasting Table / Visit Philly",
    },
]

hotspots_to_add = []
hotspots_skipped = []
for spot in new_hotspots:
    name_lower = spot["name"].lower().replace("\\'", "'")
    already_exists = False
    for existing in existing_names:
        if name_lower == existing:
            already_exists = True
            break
    if already_exists:
        hotspots_skipped.append(spot["name"])
    else:
        hotspots_to_add.append(spot)

print(f"\nNew hotspots to add: {len(hotspots_to_add)}")
print(f"Hotspots skipped (already exist): {len(hotspots_skipped)}")
for name in hotspots_skipped:
    print(f"  - {name}")

if hotspots_to_add:
    hotspots_insert = ""
    for spot in hotspots_to_add:
        insider_str = "true" if spot["isInsider"] else "false"
        new_str = "true" if spot["isNew"] else "false"
        cuisine_str = f'"{spot["cuisine"]}"' if spot["cuisine"] else "null"
        escaped_name = spot["name"].replace("'", "\\'")
        escaped_desc = spot["description"].replace("'", "\\'")
        hotspots_insert += f"""  {{
    id: "{spot['id']}",
    name: "{escaped_name}",
    type: "{spot['type']}",
    address: "{spot['address']}",
    neighborhood: "{spot['neighborhood']}",
    description: "{escaped_desc}",
    vibeTag: "{spot['vibeTag']}",
    priceRange: "{spot['priceRange']}",
    cuisine: {cuisine_str},
    isNew: {new_str},
    isInsider: {insider_str},
    lat: {spot['lat']},
    lng: {spot['lng']},
    source: "{spot['source']}",
  }},
"""
    # Find end of hotspots array
    content = content.replace(
        "\n];\n\nexport const influencers: Influencer[] = [",
        "\n" + hotspots_insert + "];\n\nexport const influencers: Influencer[] = ["
    )

# ============================================================
# STEP 4: Update influencer recent picks
# ============================================================
def add_pick(handle, pick_obj):
    """Add a new pick to an influencer's recentPicks array."""
    global content
    # Find the influencer block by handle
    handle_pattern = f'handle: "{handle}"'
    idx = content.find(handle_pattern)
    if idx == -1:
        print(f"  WARNING: Could not find influencer {handle}")
        return False
    
    # Find recentPicks array for this influencer
    picks_start = content.find("recentPicks: [", idx)
    if picks_start == -1 or picks_start - idx > 2000:
        print(f"  WARNING: Could not find recentPicks for {handle}")
        return False
    
    insert_pos = picks_start + len("recentPicks: [")
    
    # Build pick string
    reel_line = ""
    if pick_obj.get("reelUrl"):
        reel_line = f'\n        reelUrl: "{pick_obj["reelUrl"]}",'
    
    escaped_name = pick_obj["name"].replace("'", "\\'").replace('"', '\\"')
    escaped_quote = pick_obj["quote"].replace("'", "\\'").replace('"', '\\"')
    
    pick_str = f"""
      {{
        name: "{escaped_name}",
        type: "{pick_obj['type']}",
        neighborhood: "{pick_obj['neighborhood']}",
        quote: "{escaped_quote}",
        date: "{pick_obj['date']}",{reel_line}
      }},"""
    
    content = content[:insert_pos] + pick_str + content[insert_pos:]
    return True

influencer_updates = []

# @wooder_ice - posted about Gilda Cafe and Reading Terminal Market
if add_pick("@wooder_ice", {
    "name": "Reading Terminal Market Spring Visit",
    "type": "food-hall",
    "neighborhood": "Center City",
    "quote": "First day of spring and everyone was waiting for their Wooder Ice. Bright and early experiencing food in Reading Terminal -- great way to start the day.",
    "date": "2026-03-21",
}):
    influencer_updates.append("@wooder_ice")

# @feedingtimetv - Delicious City Podcast
if add_pick("@feedingtimetv", {
    "name": "Delicious City Philly Podcast",
    "type": "media",
    "neighborhood": "Citywide",
    "quote": "New episode of the Delicious City Philly Podcast dropping -- covering the best eats and drinks across the city this spring.",
    "date": "2026-03-20",
}):
    influencer_updates.append("@feedingtimetv")

# @josheatsphilly - gnocchi takeout window, 191K followers
if add_pick("@josheatsphilly", {
    "name": "Gnocchi Takeout Window",
    "type": "restaurant",
    "neighborhood": "Center City",
    "quote": "There is a gnocchi takeout window right across the street -- the kind of spot that makes Philly the best food city in America.",
    "date": "2026-03-22",
}):
    influencer_updates.append("@josheatsphilly")

# @cass_andthecity - Longwood Gardens Glow and travel content
if add_pick("@cass_andthecity", {
    "name": "Longwood Gardens Garden Glow",
    "type": "experience",
    "neighborhood": "Kennett Square (day trip)",
    "quote": "An after-hours experience that transforms the Gardens into a luminous dream. Now through March 8 -- SPARK installation, timed ticketed reservations required. Definitely worth adding to your list.",
    "date": "2026-03-18",
}):
    influencer_updates.append("@cass_andthecity")

# @djour.philly - community food map, 49K followers
if add_pick("@djour.philly", {
    "name": "Community-First Food Map Update",
    "type": "resource",
    "neighborhood": "Citywide",
    "quote": "No freebies, no bias -- updated the community-first food map with 55+ canned goods donated and counting. The best Philly food destinations all in one coded map.",
    "date": "2026-03-21",
}):
    influencer_updates.append("@djour.philly")

# @swagfoodphilly - Southeast Asian Market and new spots
if add_pick("@swagfoodphilly", {
    "name": "Southeast Asian Market at FDR Park",
    "type": "market",
    "neighborhood": "South Philly",
    "quote": "The Southeast Asian Market at FDR Park is back for the season -- one of the best hidden food markets in the city. Stock up on fresh produce and street food.",
    "date": "2026-03-22",
}):
    influencer_updates.append("@swagfoodphilly")

# @phillyfoodladies - spring dining picks
if add_pick("@phillyfoodladies", {
    "name": "Spring 2026 Philly Dining Guide",
    "type": "guide",
    "neighborhood": "Citywide",
    "quote": "Your guide to Philly's best food, drinks and fun this spring -- new openings, pop-ups, and the spots everyone is talking about right now.",
    "date": "2026-03-20",
}):
    influencer_updates.append("@phillyfoodladies")

# @fueledonphilly - food events and community
if add_pick("@fueledonphilly", {
    "name": "Mawn Philly Visit",
    "type": "restaurant",
    "neighborhood": "Fishtown",
    "quote": "Eat all night. Drink all night. Talk food all night. That is our vibe at Mawn -- incredible Southeast Asian flavors in Fishtown.",
    "date": "2026-03-19",
}):
    influencer_updates.append("@fueledonphilly")

print(f"\nInfluencer picks updated: {len(influencer_updates)}")
for handle in influencer_updates:
    print(f"  - {handle}")

# ============================================================
# STEP 5: DEDUPLICATION
# ============================================================
print("\n=== DEDUPLICATION CHECK ===")

# Collect all names by section
all_event_names = []
for m in re.finditer(r'id: "(event-\d+)",\s*name: "([^"]*)"', content):
    all_event_names.append((m.group(1), m.group(2).lower().replace("\\'", "'")))

all_hotspot_names = []
for m in re.finditer(r'id: "(spot-\d+)",\s*name: "([^"]*)"', content):
    all_hotspot_names.append((m.group(1), m.group(2).lower().replace("\\'", "'")))

# Check for duplicate event names
seen_event_names = {}
event_dupes = []
for eid, name in all_event_names:
    if name in seen_event_names:
        event_dupes.append((eid, name, seen_event_names[name]))
    else:
        seen_event_names[name] = eid

# Check for duplicate hotspot names
seen_spot_names = {}
spot_dupes = []
for sid, name in all_hotspot_names:
    if name in seen_spot_names:
        spot_dupes.append((sid, name, seen_spot_names[name]))
    else:
        seen_spot_names[name] = sid

# Check for duplicate IDs
all_ids = re.findall(r'id: "((?:event|spot)-\d+)"', content)
seen_ids = {}
id_dupes = []
for id_val in all_ids:
    if id_val in seen_ids:
        id_dupes.append(id_val)
    seen_ids[id_val] = seen_ids.get(id_val, 0) + 1

total_dupes_removed = 0

if event_dupes:
    print(f"Event name duplicates found: {len(event_dupes)}")
    for eid, name, original_id in event_dupes:
        print(f"  - '{name}' ({eid} duplicates {original_id})")
        # Remove the duplicate (keep the original)
        pattern = rf'  \{{[^}}]*id: "{re.escape(eid)}"[^}}]*\}},'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(0), "")
            total_dupes_removed += 1
else:
    print("No duplicate event names found.")

if spot_dupes:
    print(f"Hotspot name duplicates found: {len(spot_dupes)}")
    for sid, name, original_id in spot_dupes:
        print(f"  - '{name}' ({sid} duplicates {original_id})")
        pattern = rf'  \{{[^}}]*id: "{re.escape(sid)}"[^}}]*\}},'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(0), "")
            total_dupes_removed += 1
else:
    print("No duplicate hotspot names found.")

if id_dupes:
    print(f"Duplicate IDs found: {id_dupes}")
else:
    print("No duplicate IDs found.")

print(f"\nTotal duplicates removed: {total_dupes_removed}")

# Clean up any extra blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

# ============================================================
# STEP 6: Write updated file
# ============================================================
with open(DATA_FILE, "w") as f:
    f.write(content)

# Final counts
final_events = len(re.findall(r'id: "event-\d+"', content))
final_hotspots = len(re.findall(r'id: "spot-\d+"', content))
final_influencers = len(re.findall(r'handle: "@', content))

print(f"\n=== FINAL COUNTS ===")
print(f"Events: {final_events}")
print(f"Hotspots: {final_hotspots}")
print(f"Influencers: {final_influencers}")
print(f"\n=== SUMMARY ===")
print(f"Expired events removed: {len(expired_events)}")
print(f"New events added: {len(events_to_add)}")
print(f"New hotspots added: {len(hotspots_to_add)}")
print(f"Influencer picks updated: {len(influencer_updates)}")
print(f"Duplicates removed: {total_dupes_removed}")
