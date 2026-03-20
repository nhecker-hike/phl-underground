#!/usr/bin/env python3
"""PHL Underground Nightly Data Refresh -- Run #4 (March 20, 2026)"""

import re
import json

TODAY = "2026-03-20"
DATA_FILE = "client/src/data/philly-data.ts"

with open(DATA_FILE, "r") as f:
    content = f.read()

# ===================================================================
# 1. REMOVE EXPIRED EVENTS (last date strictly before today)
# ===================================================================

expired_ids = []
event_blocks = re.finditer(
    r'  \{\s*\n\s*id:\s*"(event-\d+)",\s*\n\s*name:\s*"([^"]+)",\s*\n\s*date:\s*"([^"]+)"',
    content
)

for match in event_blocks:
    eid, ename, raw_date = match.group(1), match.group(2), match.group(3)
    dates_found = re.findall(r'(\d{4}-\d{2}-\d{2})', raw_date)
    if dates_found:
        last_date = max(dates_found)
        if last_date < TODAY:
            expired_ids.append((eid, ename, raw_date))

print(f"Expired events to remove: {len(expired_ids)}")
for eid, ename, d in expired_ids:
    print(f"  - {eid}: {ename} ({d})")

for eid, ename, _ in expired_ids:
    pattern = re.compile(
        r'  \{\s*\n\s*id:\s*"' + re.escape(eid) + r'".*?\n\s*isInsider:\s*(?:true|false),?\s*\n\s*\},?\n',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        content = content[:m.start()] + content[m.end():]
        print(f"  Removed {eid}")
    else:
        print(f"  WARNING: Could not find block for {eid}")

# ===================================================================
# 2. ADD NEW EVENTS (starting from event-84)
# ===================================================================

new_events = [
    {
        "id": "event-84",
        "name": "Phillies Charities 5K at Citizens Bank Park",
        "date": "2026-03-21",
        "time": "9:00 AM",
        "venue": "Citizens Bank Park",
        "address": "1 Citizens Bank Way, Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "sports",
        "description": "The 16th annual Phillies Charities 5K loops through the Navy Yard and Citizens Bank Park. A Philly rite of spring with live music, fun surprises along the route, and four Phillies game tickets included with entry. Already sold out -- catch the energy as a spectator.",
        "price": "$65 (sold out)",
        "vibeTag": "mainstream",
        "source": "mlb.com/phillies",
        "lat": 39.9057,
        "lng": -75.1666,
        "isInsider": False,
    },
    {
        "id": "event-85",
        "name": "Robert Plant with Saving Grace at The Met Philadelphia",
        "date": "2026-04-04",
        "time": "7:30 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N. Broad Street, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "music",
        "description": "Led Zeppelin legend Robert Plant brings his intimate acoustic project Saving Grace to The Met, with Suzi Dian opening. A rare chance to hear one of rock\\'s greatest voices in a stripped-down, rootsy setting. This is bucket-list territory.",
        "price": "$65+",
        "vibeTag": "insider",
        "source": "ticketmaster.com / themetphilly.com",
        "lat": 39.9681,
        "lng": -75.1586,
        "isInsider": True,
    },
    {
        "id": "event-86",
        "name": "Boys Like Girls -- The Soundtrack Of Your Life Tour at The Met",
        "date": "2026-04-09",
        "time": "7:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N. Broad Street, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "music",
        "description": "2000s pop-punk favorites Boys Like Girls bring nostalgia and energy to The Met with iDKHOW and Arrows in Action supporting. If \\'The Great Escape\\' and \\'Thunder\\' still hit, this is your show.",
        "price": "$40+",
        "vibeTag": "mainstream",
        "source": "ticketmaster.com / livenation.com",
        "lat": 39.9681,
        "lng": -75.1586,
        "isInsider": False,
    },
    {
        "id": "event-87",
        "name": "Floetry Presents Say Yes The Tour at The Met",
        "date": "2026-04-10",
        "time": "8:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N. Broad Street, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "music",
        "description": "Neo-soul duo Floetry (Marsha Ambrosius and Natalie Stewart) bring their Say Yes Tour to The Met with Raheem DeVaughn. Grown-and-sexy vibes with \\'Say Yes,\\' \\'Floetic,\\' and spoken word poetry. A Philly must-see.",
        "price": "$55+",
        "vibeTag": "insider",
        "source": "themetphilly.com",
        "lat": 39.9681,
        "lng": -75.1586,
        "isInsider": True,
    },
    {
        "id": "event-88",
        "name": "Nick Offerman: Big Woodchuck at The Met Philadelphia",
        "date": "2026-04-12",
        "time": "7:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N. Broad Street, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "comedy",
        "description": "Ron Swanson himself brings his Big Woodchuck tour to The Met. Nick Offerman delivers deadpan humor, woodworking wisdom, and his signature mustachioed charm. An evening of laughs in one of Philly\\'s most stunning venues.",
        "price": "$45+",
        "vibeTag": "insider",
        "source": "ticketmaster.com / axs.com",
        "lat": 39.9681,
        "lng": -75.1586,
        "isInsider": True,
    },
    {
        "id": "event-89",
        "name": "In Bloom Spring Block Party at Piazza Alta",
        "date": "2026-04-18",
        "time": "10:00 AM",
        "venue": "Piazza Alta Courtyard",
        "address": "1099 Germantown Avenue, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "market",
        "description": "The Northern Liberties Farmers Market kicks off its 2026 season with the In Bloom Spring Block Party. Local vendors, food and drinks, wellness pop-ups, fitness classes, kid-friendly activities, and spring-inspired decor across the Piazza Alta courtyard. The neighborhood\\'s best free Saturday.",
        "price": "Free",
        "vibeTag": "chill",
        "source": "wooderice.com / blackbirdrsvp.com",
        "lat": 39.9650,
        "lng": -75.1425,
        "isInsider": True,
    },
    {
        "id": "event-90",
        "name": "RAYE -- This Tour May Contain New Music at The Met",
        "date": "2026-04-19",
        "time": "8:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N. Broad Street, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "music",
        "description": "British singer-songwriter RAYE brings her genre-bending sound to The Met. After her breakout album \\'My 21st Century Blues\\' swept the BRITs, she\\'s one of the most exciting live acts in the world right now -- raw vocals, orchestral arrangements, and electrifying energy.",
        "price": "$50+",
        "vibeTag": "buzzing",
        "source": "ticketmaster.com / livenation.com",
        "lat": 39.9681,
        "lng": -75.1586,
        "isInsider": True,
    },
    {
        "id": "event-91",
        "name": "Christian McBride & Edgar Meyer at Perelman Theater",
        "date": "2026-04-21",
        "time": "8:00 PM",
        "venue": "Perelman Theater at Kimmel Center",
        "address": "300 S. Broad Street, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "music",
        "description": "Philly\\'s own jazz bass legend Christian McBride teams up with genre-defying bassist Edgar Meyer for an intimate evening at Perelman Theater. Part of Ensemble Arts\\' acclaimed Jazz Series -- a night of virtuosity and improvisation between two masters.",
        "price": "$35+",
        "vibeTag": "insider",
        "source": "visitphilly.com / ensemblearts.org",
        "lat": 39.9468,
        "lng": -75.1657,
        "isInsider": True,
    },
]

# ===================================================================
# 3. ADD NEW HOTSPOTS (starting from spot-63)
# ===================================================================

new_hotspots = [
    {
        "id": "spot-63",
        "name": "Known Associates",
        "type": "bar",
        "address": "941 Spruce Street, Philadelphia, PA 19107",
        "neighborhood": "Washington Square West",
        "description": "Chef Christopher Kearse (Forsythia, Michelin-recommended) and designers PS & Daughters transform the former Varga Bar into a European-influenced cocktail bar where food plays a starring role. Expect technique-driven small plates and inventive drinks in a beautifully designed space.",
        "vibeTag": "exclusive",
        "priceRange": "$$$",
        "cuisine": "European",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9430,
        "lng": -75.1570,
        "source": "inquirer.com",
    },
    {
        "id": "spot-64",
        "name": "Bengaluru Cafe",
        "type": "restaurant",
        "address": "Northern Liberties, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "description": "South Indian cafe bringing dosas, idli, vada, and filter coffee to Northern Liberties. Casual counter-service spot that fills a gap in Philly\\'s Indian food landscape with authentic Bangalore street food flavors.",
        "vibeTag": "chill",
        "priceRange": "$",
        "cuisine": "South Indian",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9640,
        "lng": -75.1420,
        "source": "inquirer.com",
    },
    {
        "id": "spot-65",
        "name": "The Blue Warbler",
        "type": "restaurant",
        "address": "8001 Germantown Avenue, Philadelphia, PA 19118",
        "neighborhood": "Chestnut Hill",
        "description": "An all-day bakery-cafe-tavern serving edgy, eclectic comfort food on Germantown Avenue. Coffee in the morning, cocktails at night, and a crowd-sourced community vibe throughout. A welcome addition to Chestnut Hill\\'s dining scene.",
        "vibeTag": "chill",
        "priceRange": "$$",
        "cuisine": "American",
        "isNew": True,
        "isInsider": True,
        "lat": 40.0775,
        "lng": -75.2095,
        "source": "inquirer.com",
    },
    {
        "id": "spot-66",
        "name": "Taste Taco Bar",
        "type": "restaurant",
        "address": "300 South Street, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "description": "Indoor/outdoor taco bar from Hi-Def Hospitality on South Street. Occupying the former Jon\\'s Bar & Grille space with a lively patio, creative tacos, and frozen margaritas. A new anchor for the South Street strip.",
        "vibeTag": "buzzing",
        "priceRange": "$",
        "cuisine": "Mexican",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9406,
        "lng": -75.1490,
        "source": "inquirer.com",
    },
]

# ===================================================================
# 4. INSERT NEW DATA
# ===================================================================

def format_event(e):
    lines = ["  {"]
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
    lines = ["  {"]
    lines.append(f'    id: "{h["id"]}",')
    lines.append(f'    name: "{h["name"]}",')
    lines.append(f'    type: "{h["type"]}",')
    lines.append(f'    address: "{h["address"]}",')
    lines.append(f'    neighborhood: "{h["neighborhood"]}",')
    lines.append(f'    description: "{h["description"]}",')
    lines.append(f'    vibeTag: "{h["vibeTag"]}",')
    lines.append(f'    priceRange: "{h["priceRange"]}",')
    if h["cuisine"] is None:
        lines.append('    cuisine: null,')
    else:
        lines.append(f'    cuisine: "{h["cuisine"]}",')
    lines.append(f'    isNew: {"true" if h["isNew"] else "false"},')
    lines.append(f'    isInsider: {"true" if h["isInsider"] else "false"},')
    lines.append(f'    lat: {h["lat"]},')
    lines.append(f'    lng: {h["lng"]},')
    lines.append(f'    source: "{h["source"]}",')
    lines.append("  },")
    return "\n".join(lines)

events_end = "\n];\n\nexport const hotspots"
content = content.replace(events_end, "\n" + "\n".join(format_event(e) for e in new_events) + "\n" + events_end)
print(f"\nAdded {len(new_events)} new events (event-84 through event-91)")

hotspots_end = "\n];\n\nexport const influencers"
content = content.replace(hotspots_end, "\n" + "\n".join(format_hotspot(h) for h in new_hotspots) + "\n" + hotspots_end)
print(f"Added {len(new_hotspots)} new hotspots (spot-63 through spot-66)")

# ===================================================================
# 5. UPDATE INFLUENCER RECENT PICKS
# ===================================================================

def add_pick(content, handle, pick_text, label):
    marker = f'handle: "{handle}"'
    idx = content.find(marker)
    if idx != -1:
        rp_idx = content.find("recentPicks: [", idx)
        if rp_idx != -1:
            insert_at = rp_idx + len("recentPicks: [")
            content = content[:insert_at] + "\n" + pick_text + content[insert_at:]
            print(f"Updated {label}")
    else:
        print(f"WARNING: Could not find {handle}")
    return content

# Wooder Ice -- In Bloom Block Party coverage, NCAA March Madness in Philly
content = add_pick(content, "@wooder_ice",
    '      { name: "NCAA March Madness in Philly", type: "event", neighborhood: "South Philly", quote: "March Madness is HERE. Philly is hosting first and second round games at Xfinity Mobile Arena this weekend -- one of the most electric sports weekends of the year. The energy is unmatched.", date: "March 20, 2026" },',
    "Wooder Ice (NCAA March Madness)")

# FeedingTimeTV -- new restaurant coverage
content = add_pick(content, "@feedingtimetv",
    '      { name: "Bengaluru Cafe", type: "restaurant", neighborhood: "Northern Liberties", quote: "South Indian spot in NoLibs serving legit dosas, idli, and filter coffee. Fills a huge gap in the Philly food scene. The masala dosa is the move.", date: "March 19, 2026" },',
    "FeedingTimeTV (Bengaluru Cafe)")

# Josh Moore -- food content
content = add_pick(content, "@josheatsphilly",
    "      { name: \"Emilia\", type: \"restaurant\", neighborhood: \"Kensington\", quote: \"Greg Vernick's Italian spot in Kensington is living up to the hype. House-made pasta, live-fire cooking, and a neighborhood trattoria vibe that feels both elevated and approachable.\", date: \"March 19, 2026\" },",
    "Josh Moore (Emilia)")

# Kory Aversa -- scene coverage
content = add_pick(content, "@koryaversa",
    "      { name: \"Known Associates\", type: \"bar\", neighborhood: \"Washington Square West\", quote: \"The Forsythia team's new cocktail bar at the old Varga Bar space is stunning. European-influenced drinks, technique-driven food, gorgeous design. Washington Square just got a major upgrade.\", date: \"March 19, 2026\" },",
    "Kory Aversa (Known Associates)")

# SwagFoodPhilly -- food finds
content = add_pick(content, "@swagfoodphilly",
    '      { name: "Taste Taco Bar", type: "restaurant", neighborhood: "South Street", quote: "New taco spot on South Street with a solid patio. Creative tacos and frozen margs -- exactly what South Street needed.", date: "March 19, 2026" },',
    "SwagFoodPhilly (Taste Taco Bar)")

# ===================================================================
# 6. DEDUPLICATION CHECK
# ===================================================================

print("\n=== DEDUPLICATION CHECK ===")
dupes_removed = 0

# Event name dedup
event_entries = re.findall(r'id:\s*"(event-\d+)".*?name:\s*"([^"]+)"', content, re.DOTALL)
seen_events = {}
event_dupes = []
for eid, ename in event_entries:
    key = ename.lower().strip()
    if key in seen_events:
        event_dupes.append((eid, ename, seen_events[key]))
    else:
        seen_events[key] = (eid, ename)

print(f"Event name duplicates: {len(event_dupes)}")
for eid, ename, orig in event_dupes:
    print(f"  - {eid}: '{ename}' duplicates {orig}")
    pattern = re.compile(
        r'  \{\s*\n\s*id:\s*"' + re.escape(eid) + r'".*?\n\s*isInsider:\s*(?:true|false),?\s*\n\s*\},?\n',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        content = content[:m.start()] + content[m.end():]
        dupes_removed += 1
        print(f"  Removed {eid}")

# Hotspot name dedup
spot_entries = re.findall(r'id:\s*"(spot-\d+)".*?name:\s*"([^"]+)"', content, re.DOTALL)
seen_spots = {}
spot_dupes = []
for sid, sname in spot_entries:
    key = sname.lower().strip()
    if key in seen_spots:
        spot_dupes.append((sid, sname, seen_spots[key]))
    else:
        seen_spots[key] = (sid, sname)

print(f"Hotspot name duplicates: {len(spot_dupes)}")
for sid, sname, orig in spot_dupes:
    print(f"  - {sid}: '{sname}' duplicates {orig}")
    pattern = re.compile(
        r'  \{\s*\n\s*id:\s*"' + re.escape(sid) + r'".*?\n\s*source:\s*"[^"]*",?\s*\n\s*\},?\n',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        content = content[:m.start()] + content[m.end():]
        dupes_removed += 1
        print(f"  Removed {sid}")

# Verify unique IDs
all_ids = re.findall(r'id:\s*"([^"]+)"', content)
id_counts = {}
for i in all_ids:
    id_counts[i] = id_counts.get(i, 0) + 1
dup_ids = {k: v for k, v in id_counts.items() if v > 1}
if dup_ids:
    print(f"WARNING: Duplicate IDs: {dup_ids}")
else:
    print("All IDs unique -- passed")

print(f"\nTotal duplicates removed: {dupes_removed}")

# ===================================================================
# 7. WRITE FILE
# ===================================================================

with open(DATA_FILE, "w") as f:
    f.write(content)

final_events = len(re.findall(r'id:\s*"event-\d+"', content))
final_spots = len(re.findall(r'id:\s*"spot-\d+"', content))
final_inf = len(re.findall(r'id:\s*"influencer-\d+"', content))

print(f"\n=== FINAL COUNTS ===")
print(f"Events: {final_events}")
print(f"Hotspots: {final_spots}")
print(f"Influencers: {final_inf}")

summary = {
    "date": TODAY,
    "run_number": 4,
    "events_added": len(new_events),
    "hotspots_added": len(new_hotspots),
    "expired_removed": len(expired_ids),
    "duplicates_removed": dupes_removed,
    "influencer_updates": 5,
    "final_events": final_events,
    "final_hotspots": final_spots,
    "new_event_names": [e["name"] for e in new_events],
    "new_hotspot_names": [h["name"] for h in new_hotspots],
    "expired_names": [ename for _, ename, _ in expired_ids],
}
with open("update-summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("Summary written")
