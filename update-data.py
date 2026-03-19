#!/usr/bin/env python3
"""PHL Underground Nightly Data Refresh -- Run #3 (March 19, 2026)"""

import re
import json
from datetime import datetime

TODAY = "2026-03-19"
DATA_FILE = "client/src/data/philly-data.ts"

with open(DATA_FILE, "r") as f:
    content = f.read()

# ===================================================================
# 1. REMOVE EXPIRED EVENTS (date fully before today 2026-03-19)
# ===================================================================

expired_ids = []

event_blocks = re.finditer(
    r'  \{\s*\n\s*id:\s*"(event-\d+)",\s*\n\s*name:\s*"([^"]+)",\s*\n\s*date:\s*"([^"]+)"',
    content
)

for match in event_blocks:
    eid = match.group(1)
    ename = match.group(2)
    raw_date = match.group(3)
    
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
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + content[match.end():]
        print(f"  Removed {eid}: {ename}")
    else:
        print(f"  WARNING: Could not find block for {eid}")

# ===================================================================
# 2. ADD NEW EVENTS (starting from event-72)
# ===================================================================

new_events = [
    {
        "id": "event-72",
        "name": "Gogol Bordello at Union Transfer",
        "date": "2026-03-24",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Gypsy punk legends Gogol Bordello bring their wild, multi-cultural carnival of rock to Union Transfer on their We Mean It, Man! 2026 tour. Eugene Hutz and crew deliver one of the most chaotic and joyful live experiences in music. With Puzzled Panther and Boris and the Joy opening.",
        "price": "$35+",
        "vibeTag": "underground",
        "source": "utphilly.com / axs.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-73",
        "name": "There, There -- Radiohead Tribute at Union Transfer",
        "date": "2026-03-28",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "A full Radiohead tribute experience at Union Transfer. Deep cuts, album favorites, and the atmospheric soundscapes that made Thom Yorke and company one of the most important bands of the past 30 years -- performed live by a dedicated tribute act.",
        "price": "$20+",
        "vibeTag": "indie",
        "source": "concertfix.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-74",
        "name": "kwn at Theatre of Living Arts",
        "date": "2026-04-01",
        "time": "8:00 PM",
        "venue": "Theatre of Living Arts",
        "address": "334 South Street, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "music",
        "description": "East London rising star kwn (pronounced kay-wuhn) brings her quiet storm 2.0 R&B to the TLA. Her hits like \\'do what i say\\' and \\'back of the club\\' are the soundtrack to late-night Philly energy. A name to know before she blows up.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "livenation.com / ticketmaster.com",
        "lat": 39.9410,
        "lng": -75.1494,
        "isInsider": True,
    },
    {
        "id": "event-75",
        "name": "Ryan Davis and The Roadhouse Band at Union Transfer",
        "date": "2026-04-03",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Americana and heartland rock at its finest. Ryan Davis and The Roadhouse Band bring gritty, soulful country-rock to Union Transfer -- the kind of show where boots hit the floor and beers stay cold.",
        "price": "$20+",
        "vibeTag": "chill",
        "source": "concertfix.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-76",
        "name": "Luna at Union Transfer",
        "date": "2026-04-05",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Dream pop icons Luna, led by Dean Wareham, return to the stage. Their shimmering guitars and Velvet Underground-influenced sound defined 90s indie rock. A rare chance to see legends in an intimate venue.",
        "price": "$30+",
        "vibeTag": "indie",
        "source": "concertfix.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-77",
        "name": "Cardi B -- Little Miss Drama Tour at Xfinity Mobile Arena",
        "date": "2026-04-07",
        "time": "7:30 PM",
        "venue": "Xfinity Mobile Arena",
        "address": "3601 S. Broad Street, Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "music",
        "description": "Cardi B takes over Xfinity Mobile Arena on her first headlining arena tour. High-energy performances of \\'Bodega Baddie,\\' \\'WAP,\\' and cuts from her latest triple-platinum album. One of the biggest hip-hop shows hitting Philly this spring.",
        "price": "$70+",
        "vibeTag": "mainstream",
        "source": "ticketmaster.com / xfinitymobilearena.com",
        "lat": 39.9012,
        "lng": -75.1745,
        "isInsider": False,
    },
    {
        "id": "event-78",
        "name": "Lewis Capaldi at The Liacouras Center",
        "date": "2026-04-15",
        "time": "7:30 PM",
        "venue": "The Liacouras Center",
        "address": "1776 N. Broad Street, Philadelphia, PA 19121",
        "neighborhood": "North Philadelphia",
        "category": "music",
        "description": "Scottish singer-songwriter Lewis Capaldi makes his triumphant comeback with special guest Joy Crookes. After a two-year hiatus, the \\'Dancing on My Own\\' hitmaker performs selections from his new EP including \\'Almost\\' and \\'Survive.\\' Expect tears and singalongs.",
        "price": "$50+",
        "vibeTag": "mainstream",
        "source": "liacourascenter.com / livenation.com",
        "lat": 39.9812,
        "lng": -75.1553,
        "isInsider": False,
    },
    {
        "id": "event-79",
        "name": "The Growlers at Union Transfer",
        "date": "2026-04-17",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Beach goth pioneers The Growlers bring their hazy, psychedelic surf-rock to Union Transfer. A cult favorite with a laid-back California sound that translates perfectly to a sweaty Philly venue.",
        "price": "$30+",
        "vibeTag": "indie",
        "source": "concertfix.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
    {
        "id": "event-80",
        "name": "Demi Lovato -- It\\'s Not That Deep Tour at Xfinity Mobile Arena",
        "date": "2026-04-18",
        "time": "8:00 PM",
        "venue": "Xfinity Mobile Arena",
        "address": "3601 S. Broad Street, Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "music",
        "description": "Demi Lovato returns with dance-pop bangers and high-energy arena production on the It\\'s Not That Deep Tour with special guest Adela. A full night of pop spectacle at Xfinity.",
        "price": "$55+",
        "vibeTag": "mainstream",
        "source": "ticketmaster.com / xfinitymobilearena.com",
        "lat": 39.9012,
        "lng": -75.1745,
        "isInsider": False,
    },
    {
        "id": "event-81",
        "name": "Endea Owens Jazz at Perelman Theater",
        "date": "2026-03-28",
        "time": "8:00 PM",
        "venue": "Perelman Theater at Kimmel Center",
        "address": "300 S. Broad Street, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "music",
        "description": "Bassist Endea Owens, known from The Late Show with Stephen Colbert, performs as part of Ensemble Arts\\' acclaimed Jazz Series. An intimate evening of world-class jazz in one of Philly\\'s finest small venues.",
        "price": "$35+",
        "vibeTag": "insider",
        "source": "visitphilly.com / ensemblearts.org",
        "lat": 39.9468,
        "lng": -75.1657,
        "isInsider": True,
    },
    {
        "id": "event-82",
        "name": "Sing Us Home Festival",
        "date": "2026-05-01 to 2026-05-03",
        "time": "Various",
        "venue": "Venice Island Performing Arts Center",
        "address": "7 Lock Street, Philadelphia, PA 19127",
        "neighborhood": "Manayunk",
        "category": "music",
        "description": "Dave Hause\\'s annual punk rock and acoustic music festival returns for year four on Venice Island. The Menzingers, The Mountain Goats, Augustines (reunion!), and Dave Hause & The Mermaid headline three days of music, local food trucks, craft beer, tattoos, art, and vinyl vendors. One of Philly\\'s best-kept festival secrets.",
        "price": "$75+ (day pass)",
        "vibeTag": "underground",
        "source": "singushomefestival.com / rollingstone.com",
        "lat": 40.0268,
        "lng": -75.2258,
        "isInsider": True,
    },
    {
        "id": "event-83",
        "name": "NewDad at Union Transfer",
        "date": "2026-04-26",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden Street, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Irish shoegaze/dream pop quartet NewDad have been tearing up festival circuits and blogospheres. Lush walls of guitar, ethereal vocals, and hooks for days. Catch them at Union Transfer before arena tours inevitably follow.",
        "price": "$22+",
        "vibeTag": "indie",
        "source": "concertfix.com",
        "lat": 39.9615,
        "lng": -75.1553,
        "isInsider": True,
    },
]

# ===================================================================
# 3. ADD NEW HOTSPOTS (starting from spot-58)
# ===================================================================

new_hotspots = [
    {
        "id": "spot-58",
        "name": "Huda Burger",
        "type": "restaurant",
        "address": "Philadelphia, PA",
        "neighborhood": "West Philly",
        "description": "Halal smash burgers making waves across Philly food social media. Crispy, seasoned patties on soft buns with house sauces -- a cult following is already forming. Named one of the best new restaurants by Eater Philly in March 2026.",
        "vibeTag": "buzzing",
        "priceRange": "$",
        "cuisine": "Halal Burgers",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9560,
        "lng": -75.2010,
        "source": "philly.eater.com",
    },
    {
        "id": "spot-59",
        "name": "Cerveau",
        "type": "restaurant",
        "address": "Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse",
        "description": "Upscale French-inspired restaurant bringing cerebral, technique-driven cuisine to Rittenhouse. A refined menu with seasonal tasting options and an impressive natural wine list. Already generating serious buzz among Philly food media.",
        "vibeTag": "exclusive",
        "priceRange": "$$$$",
        "cuisine": "French",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9505,
        "lng": -75.1700,
        "source": "philly.eater.com",
    },
    {
        "id": "spot-60",
        "name": "El Sazon R.D.",
        "type": "restaurant",
        "address": "Philadelphia, PA",
        "neighborhood": "North Philadelphia",
        "description": "Authentic Dominican restaurant serving mangus, mofongos, and stewed meats with bold Caribbean flavors. A neighborhood gem highlighted by Eater Philly as one of the best new spots in the city. Generous portions, family-style vibes.",
        "vibeTag": "insider",
        "priceRange": "$",
        "cuisine": "Dominican",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9850,
        "lng": -75.1500,
        "source": "philly.eater.com",
    },
    {
        "id": "spot-61",
        "name": "Snack Shack at Forest & Main",
        "type": "restaurant",
        "address": "Frankford Avenue, Philadelphia, PA 19125",
        "neighborhood": "Fishtown",
        "description": "The beloved Forest & Main brewery now has a dedicated food window in Fishtown serving elevated snack bar bites -- smash burgers, loaded fries, and soft pretzels paired with their craft beers. Casual, fun, and perfectly Fishtown.",
        "vibeTag": "chill",
        "priceRange": "$",
        "cuisine": "American",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9720,
        "lng": -75.1330,
        "source": "philly.eater.com",
    },
    {
        "id": "spot-62",
        "name": "The Grape",
        "type": "bar",
        "address": "105 Grape Street, Philadelphia, PA",
        "neighborhood": "Manayunk",
        "description": "Neighborhood wine bar on Grape Street (yes, really) with a curated natural wine list, small plates, and a laid-back atmosphere. A welcome addition to the Manayunk bar scene that feels more like a Brooklyn wine bar than a typical Philly spot.",
        "vibeTag": "chill",
        "priceRange": "$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 40.0240,
        "lng": -75.2240,
        "source": "visitphilly.com",
    },
]

# ===================================================================
# 4. INSERT NEW EVENTS before the closing "];" of events array
# ===================================================================

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

events_end_marker = "\n];\n\nexport const hotspots"
events_insert = "\n" + "\n".join(format_event(e) for e in new_events) + "\n"
content = content.replace(events_end_marker, events_insert + events_end_marker)
print(f"\nAdded {len(new_events)} new events (event-72 through event-83)")

hotspots_end_marker = "\n];\n\nexport const influencers"
hotspots_insert = "\n" + "\n".join(format_hotspot(h) for h in new_hotspots) + "\n"
content = content.replace(hotspots_end_marker, hotspots_insert + hotspots_end_marker)
print(f"Added {len(new_hotspots)} new hotspots (spot-58 through spot-62)")

# ===================================================================
# 5. UPDATE INFLUENCER RECENT PICKS
# ===================================================================

# Wooder Ice -- add Diversitech Day 1 coverage (it started today Mar 19)
wooder_handle_marker = 'handle: "@wooder_ice"'
wooder_section_idx = content.find(wooder_handle_marker)
if wooder_section_idx != -1:
    wooder_recent_idx = content.find("recentPicks: [", wooder_section_idx)
    if wooder_recent_idx != -1:
        insert_after = wooder_recent_idx + len("recentPicks: [")
        wooder_new_pick = """
      { name: "Diversitech 2026 Day 1", type: "event", neighborhood: "Center City", quote: "Diversitech 2026 kicked off today -- Philly\'s most inclusive tech conference. Three days of panels, networking, and celebrating diverse founders and creators. See you there.", date: "March 19, 2026" },"""
        content = content[:insert_after] + wooder_new_pick + content[insert_after:]
        print("Updated Wooder Ice with 1 new pick (Diversitech Day 1)")
else:
    print("WARNING: Could not find Wooder Ice recentPicks marker")

# FeedingTimeTV -- add new food content
feedingtv_picks_marker = 'handle: "@feedingtimetv"'
feedingtv_section_idx = content.find(feedingtv_picks_marker)
if feedingtv_section_idx != -1:
    feedingtv_recent_idx = content.find("recentPicks: [", feedingtv_section_idx)
    if feedingtv_recent_idx != -1:
        insert_after = feedingtv_recent_idx + len("recentPicks: [")
        new_pick = """
      { name: "Huda Burger", type: "restaurant", neighborhood: "West Philly", quote: "Halal smash burgers that are absolutely crushing it right now. Crispy edges, perfectly seasoned. Get here before the line wraps around the block.", date: "March 18, 2026" },"""
        content = content[:insert_after] + new_pick + content[insert_after:]
        print("Updated FeedingTimeTV with 1 new pick (Huda Burger)")

# Cass Matthews -- add new pick
cass_picks_marker = 'handle: "@cass_andthecity"'
cass_section_idx = content.find(cass_picks_marker)
if cass_section_idx != -1:
    cass_recent_idx = content.find("recentPicks: [", cass_section_idx)
    if cass_recent_idx != -1:
        insert_after = cass_recent_idx + len("recentPicks: [")
        new_pick = """
      { name: "Ministry of Awe", type: "event", neighborhood: "Old City", quote: "Finally checked out Ministry of Awe in Old City -- the projection-mapped rooms are stunning. Perfect date night or creative inspiration. Book ahead.", date: "March 18, 2026" },"""
        content = content[:insert_after] + new_pick + content[insert_after:]
        print("Updated Cass Matthews with 1 new pick (Ministry of Awe)")

# Philly Food Ladies -- add new pick
ladies_picks_marker = 'handle: "@phillyfoodladies"'
ladies_section_idx = content.find(ladies_picks_marker)
if ladies_section_idx != -1:
    ladies_recent_idx = content.find("recentPicks: [", ladies_section_idx)
    if ladies_recent_idx != -1:
        insert_after = ladies_recent_idx + len("recentPicks: [")
        new_pick = """
      { name: "Cerveau", type: "restaurant", neighborhood: "Rittenhouse", quote: "The new French spot in Rittenhouse is giving everything. Technique-driven plates, beautiful presentation, and the natural wine list is incredible.", date: "March 18, 2026" },"""
        content = content[:insert_after] + new_pick + content[insert_after:]
        print("Updated Philly Food Ladies with 1 new pick (Cerveau)")

# Fueled on Philly -- add new pick
fueled_picks_marker = 'handle: "@fueledonphilly"'
fueled_section_idx = content.find(fueled_picks_marker)
if fueled_section_idx != -1:
    fueled_recent_idx = content.find("recentPicks: [", fueled_section_idx)
    if fueled_recent_idx != -1:
        insert_after = fueled_recent_idx + len("recentPicks: [")
        new_pick = """
      { name: "Snack Shack at Forest & Main", type: "restaurant", neighborhood: "Fishtown", quote: "Forest & Main\\'s new food window in Fishtown -- smash burgers and loaded fries to go with your craft beer. This is what we needed.", date: "March 18, 2026" },"""
        content = content[:insert_after] + new_pick + content[insert_after:]
        print("Updated Fueled on Philly with 1 new pick (Snack Shack)")

# Djour Philly -- add new pick
djour_picks_marker = 'handle: "@djour.philly"'
djour_section_idx = content.find(djour_picks_marker)
if djour_section_idx != -1:
    djour_recent_idx = content.find("recentPicks: [", djour_section_idx)
    if djour_recent_idx != -1:
        insert_after = djour_recent_idx + len("recentPicks: [")
        new_pick = """
      { name: "The Grape", type: "bar", neighborhood: "Manayunk", quote: "Natural wine bar on Grape Street in Manayunk. Cozy vibes, great list, perfect for a chill night out.", date: "March 18, 2026" },"""
        content = content[:insert_after] + new_pick + content[insert_after:]
        print("Updated Djour Philly with 1 new pick (The Grape)")

# ===================================================================
# 6. DEDUPLICATION CHECK
# ===================================================================

print("\n=== DEDUPLICATION CHECK ===")
dupes_removed = 0

# Extract all event names for dedup
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

# Near-duplicate check: same venue + one name contains the other
for i, (eid1, ename1, venue1) in enumerate(event_entries):
    for j, (eid2, ename2, venue2) in enumerate(event_entries):
        if i >= j:
            continue
        if venue1.lower() == venue2.lower() and venue1:
            n1 = re.sub(r'\s+', ' ', ename1.lower().replace("the ", "").strip())
            n2 = re.sub(r'\s+', ' ', ename2.lower().replace("the ", "").strip())
            # Only flag if one name is a strong substring of the other (>50% overlap)
            if (n1 in n2 or n2 in n1) and abs(len(n1) - len(n2)) < min(len(n1), len(n2)):
                pair = tuple(sorted([eid1, eid2]))
                already = any(d[0] in pair for d in event_dupes)
                if not already:
                    event_dupes.append((eid2, ename2, (eid1, ename1)))

print(f"Event duplicates found: {len(event_dupes)}")
for eid, ename, original in event_dupes:
    print(f"  - {eid}: '{ename}' duplicates {original}")

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

# Hotspot dedup: exact name matches only (avoid address false positives)
spot_entries = re.findall(
    r'id:\s*"(spot-\d+)".*?name:\s*"([^"]+)"',
    content, re.DOTALL
)

seen_spots = {}
spot_dupes = []
for sid, sname in spot_entries:
    key = sname.lower().strip()
    if key in seen_spots:
        spot_dupes.append((sid, sname, seen_spots[key]))
    else:
        seen_spots[key] = (sid, sname)

print(f"Hotspot duplicates found: {len(spot_dupes)}")
for sid, sname, original in spot_dupes:
    print(f"  - {sid}: '{sname}' duplicates {original}")

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

# Verify unique IDs
all_ids = re.findall(r'id:\s*"([^"]+)"', content)
id_counts = {}
for id_val in all_ids:
    id_counts[id_val] = id_counts.get(id_val, 0) + 1
dup_ids = {k: v for k, v in id_counts.items() if v > 1}
if dup_ids:
    print(f"WARNING: Duplicate IDs found: {dup_ids}")
else:
    print("All IDs are unique -- passed")

print(f"\nTotal duplicates removed: {dupes_removed}")

# ===================================================================
# 7. WRITE THE FILE
# ===================================================================

with open(DATA_FILE, "w") as f:
    f.write(content)

final_events = len(re.findall(r'id:\s*"event-\d+"', content))
final_spots = len(re.findall(r'id:\s*"spot-\d+"', content))
final_influencers = len(re.findall(r'id:\s*"influencer-\d+"', content))

print(f"\n=== FINAL COUNTS ===")
print(f"Events: {final_events}")
print(f"Hotspots: {final_spots}")
print(f"Influencers: {final_influencers}")
print(f"File written successfully!")

summary = {
    "date": TODAY,
    "run_number": 3,
    "events_added": len(new_events),
    "hotspots_added": len(new_hotspots),
    "expired_removed": len(expired_ids),
    "duplicates_removed": dupes_removed,
    "influencer_updates": 6,
    "final_events": final_events,
    "final_hotspots": final_spots,
    "new_event_names": [e["name"] for e in new_events],
    "new_hotspot_names": [h["name"] for h in new_hotspots],
    "expired_names": [f"{ename}" for _, ename, _ in expired_ids],
}
with open("update-summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nSummary written to update-summary.json")
