#!/usr/bin/env python3
"""PHL Underground nightly data refresh — Run #5 (March 21, 2026)"""

import re
import json
from datetime import datetime

TODAY = "2026-03-21"
DATA_FILE = "client/src/data/philly-data.ts"

with open(DATA_FILE, "r") as f:
    content = f.read()

# ────────────────────────────────────────────────
# 1. Remove expired events (last date < today)
# ────────────────────────────────────────────────
def get_last_date(date_str):
    dates = re.findall(r'(\d{4}-\d{2}-\d{2})', date_str)
    return max(dates) if dates else "9999-12-31"

events_match = re.search(r'(export const events: PhillyEvent\[\] = \[)(.*?)(\];)', content, re.DOTALL)
events_text = events_match.group(2)

# Split into individual event blocks
event_blocks = re.findall(r'(\s*\{[^{}]*?\})', events_text)
expired_count = 0
kept_events = []
for block in event_blocks:
    date_m = re.search(r'date:\s*"([^"]*)"', block)
    name_m = re.search(r'name:\s*"([^"]*)"', block)
    if date_m:
        last_date = get_last_date(date_m.group(1))
        if last_date < TODAY:
            print(f"REMOVING EXPIRED: {name_m.group(1) if name_m else '?'} (last date: {last_date})")
            expired_count += 1
            continue
    kept_events.append(block)

print(f"\nExpired events removed: {expired_count}")

# ────────────────────────────────────────────────
# 2. New events to add (starting at event-92)
# ────────────────────────────────────────────────
new_events = [
    {
        "id": "event-92",
        "name": "Natalie Jane at Underground Arts",
        "date": "2026-03-22",
        "time": "7:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Pop singer-songwriter Natalie Jane brings her rising catalog of viral hits to Underground Arts. Expect intimate vocals, confessional lyrics, and an energized crowd in one of Philly's best indie venues.",
        "price": "$25+",
        "vibeTag": "insider",
        "source": "undergroundarts.org / shazam.com",
        "lat": 39.9596,
        "lng": -75.1582,
        "isInsider": True,
    },
    {
        "id": "event-93",
        "name": "Hanabie at Theatre of Living Arts",
        "date": "2026-03-21",
        "time": "7:00 PM",
        "venue": "Theatre of Living Arts",
        "address": "334 South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "music",
        "description": "Japanese metalcore/kawaii-core sensation Hanabie brings their wildly energetic and genre-bending live show to South Street's iconic TLA. If you like mosh pits mixed with J-pop aesthetics, this is your night.",
        "price": "$25+",
        "vibeTag": "insider",
        "source": "seatgeek.com",
        "lat": 39.9424,
        "lng": -75.1491,
        "isInsider": True,
    },
    {
        "id": "event-94",
        "name": "Flannel 90s Night at Brooklyn Bowl Philadelphia",
        "date": "2026-03-21",
        "time": "8:00 PM",
        "venue": "Brooklyn Bowl Philadelphia",
        "address": "1009 Canal St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "nightlife",
        "description": "Flannel is a 21+ 90s tribute night with bowling, drinks, and all the grunge, alt-rock, and hip-hop of the decade. Perfect Saturday night out at Brooklyn Bowl — think Pearl Jam, Nirvana, TLC, and Biggie all in one set.",
        "price": "$15+",
        "vibeTag": "local-fav",
        "source": "seatgeek.com",
        "lat": 39.9646,
        "lng": -75.1377,
        "isInsider": False,
    },
    {
        "id": "event-95",
        "name": "PHS Pop-Up Garden Grand Opening — Manayunk & South Street",
        "date": "2026-03-27",
        "time": "All Day",
        "venue": "PHS Pop-Up Gardens",
        "address": "Manayunk & South Street locations, Philadelphia, PA",
        "neighborhood": "Manayunk / South Street",
        "category": "food-drink",
        "description": "The Pennsylvania Horticultural Society's beloved pop-up beer gardens kick off their 2026 season with a grand opening at both Manayunk and South Street. Expect boardwalk-style eats, frozen cocktails, and repurposed Flower Show plants. Manayunk features fried clams and the Gritty Margarita; South Street debuts sticky chai pretzel bites and Jamaican jerk wings.",
        "price": "Free entry",
        "vibeTag": "insider",
        "source": "axios.com / phs.org",
        "lat": 40.0264,
        "lng": -75.2255,
        "isInsider": True,
    },
    {
        "id": "event-96",
        "name": "Obscura at Underground Arts",
        "date": "2026-03-23",
        "time": "7:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "German technical death metal legends Obscura play Underground Arts on their 2026 tour. A must for metal heads — expect blistering guitar work, complex time signatures, and a packed underground crowd.",
        "price": "$25+",
        "vibeTag": "insider",
        "source": "undergroundarts.org",
        "lat": 39.9596,
        "lng": -75.1582,
        "isInsider": True,
    },
    {
        "id": "event-97",
        "name": "Rebirth Brass Band at Underground Arts",
        "date": "2026-03-26",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "New Orleans legends Rebirth Brass Band bring their Grammy-winning funk, jazz, and second-line grooves to Underground Arts. One of the most joyful live music experiences you'll find anywhere — guaranteed to make you move.",
        "price": "$30+",
        "vibeTag": "insider",
        "source": "undergroundarts.org",
        "lat": 39.9596,
        "lng": -75.1582,
        "isInsider": True,
    },
    {
        "id": "event-98",
        "name": "City Wide: A Refined Whiskey & Wine Experience at The Pyramid Club",
        "date": "2026-03-25",
        "time": "6:00 PM",
        "venue": "The Pyramid Club",
        "address": "1735 Market St, 52nd Floor, Philadelphia, PA 19103",
        "neighborhood": "Center City",
        "category": "food-drink",
        "description": "Sip premium whiskeys and curated wines 52 floors above Philadelphia at the Pyramid Club. An upscale tasting event with panoramic skyline views, live entertainment, and a dressed-up Philly crowd. Insider networking meets refined indulgence.",
        "price": "$65+",
        "vibeTag": "insider",
        "source": "eventbrite.com",
        "lat": 39.9536,
        "lng": -75.1689,
        "isInsider": True,
    },
    {
        "id": "event-99",
        "name": "Seeking Profit & Power at Independence Seaport Museum",
        "date": "2026-03-20 to 2027-01-01",
        "time": "10:00 AM - 5:00 PM",
        "venue": "Independence Seaport Museum",
        "address": "211 S Christopher Columbus Blvd, Philadelphia, PA 19106",
        "neighborhood": "Penn's Landing",
        "category": "culture",
        "description": "A brand-new exhibition exploring how America built its economy after the Revolution through trade with China. Features 150 rarely seen artifacts revealing how international commerce shaped the young nation into a global superpower. A Philly 250 Semiquincentennial highlight.",
        "price": "$18",
        "vibeTag": "local-fav",
        "source": "visitphilly.com",
        "lat": 39.9451,
        "lng": -75.1416,
        "isInsider": False,
    },
    {
        "id": "event-100",
        "name": "Manayunk StrEAT Food Festival",
        "date": "2026-04-19",
        "time": "11:00 AM - 5:00 PM",
        "venue": "Main Street Manayunk",
        "address": "Main Street, Manayunk, Philadelphia, PA 19127",
        "neighborhood": "Manayunk",
        "category": "food-drink",
        "description": "Philly's biggest food truck festival takes over historic Main Street in Manayunk with dozens of top vendors, live music on two stages, and all-day eating. Featuring Cousins Maine Lobster, Cactus Cantina, Aunt Dee's Pound Cake, and more. Rain or shine.",
        "price": "Free entry",
        "vibeTag": "local-fav",
        "source": "manayunk.com / seanelstone.com",
        "lat": 40.0259,
        "lng": -75.2257,
        "isInsider": False,
    },
    {
        "id": "event-101",
        "name": "Caiola at Underground Arts",
        "date": "2026-03-27",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19123",
        "neighborhood": "Callowhill",
        "category": "music",
        "description": "Rising indie artist Caiola performs at Underground Arts. A freshly announced show that's generating buzz in Philly's indie music scene — catch them before they blow up.",
        "price": "$20+",
        "vibeTag": "insider",
        "source": "undergroundarts.org",
        "lat": 39.9596,
        "lng": -75.1582,
        "isInsider": True,
    },
]

# Check for duplicates against existing event names
existing_event_names = set()
for block in kept_events:
    nm = re.search(r'name:\s*"([^"]*)"', block)
    if nm:
        existing_event_names.add(nm.group(1).lower().replace("\\'", "'"))

actually_new_events = []
for ev in new_events:
    if ev["name"].lower() in existing_event_names:
        print(f"SKIPPING DUPLICATE EVENT: {ev['name']}")
    else:
        actually_new_events.append(ev)

print(f"\nNew events to add: {len(actually_new_events)}")

# ────────────────────────────────────────────────
# 3. New hotspots to add (starting at spot-67)
# ────────────────────────────────────────────────
new_hotspots = [
    {
        "id": "spot-67",
        "name": "Liquorette",
        "type": "bar",
        "address": "255 S 16th St (above WineDive), Philadelphia, PA 19102",
        "neighborhood": "Rittenhouse",
        "description": "A luxury, European-style cocktail bar from the WineDive team (Heather Annechiarico & Chris Fetfatzes) opening above the beloved Rittenhouse wine bar. Expect refined cocktails, intimate vibes, and the same hospitality that made WineDive a neighborhood institution.",
        "vibeTag": "insider",
        "priceRange": "$$$",
        "cuisine": "cocktails",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9484,
        "lng": -75.1688,
        "source": "phillymag.com / seanelstone.com",
    },
    {
        "id": "spot-68",
        "name": "Pig & Khao",
        "type": "restaurant",
        "address": "Former Martha space, Kensington, Philadelphia, PA 19125",
        "neighborhood": "Kensington",
        "description": "NYC's acclaimed Thai-Filipino restaurant Pig & Khao is opening in the former Martha space in Kensington. Chef Leah Cohen brings bold Southeast Asian flavors — think lemongrass sausage, kare kare, and fish sauce wings — to one of Philly's hottest food corridors.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": "Thai-Filipino",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9747,
        "lng": -75.1318,
        "source": "phillymag.com",
    },
    {
        "id": "spot-69",
        "name": "Lucky Duck",
        "type": "restaurant",
        "address": "Rivermark Apartments, N. Columbus Blvd, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "description": "A new bar/restaurant overlooking the Delaware River from the Libertee Grounds team. American bar food, pizzas, and cocktails with waterfront views in NoLibs. Deliberately millennial-coded with a playful, social atmosphere perfect for group hangs.",
        "vibeTag": "local-fav",
        "priceRange": "$$",
        "cuisine": "American",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9680,
        "lng": -75.1339,
        "source": "phillymag.com",
    },
    {
        "id": "spot-70",
        "name": "Sacred Vice Brewing — Berks Taproom",
        "type": "bar",
        "address": "1027 N Berks St, Philadelphia, PA 19122",
        "neighborhood": "Kensington",
        "description": "Praised by Philly's top bartenders as one of the best new bars in the city. Great craft beer, beautiful mid-century modern decor, and a vinyl-only music selection with over 2,000 records. A chill, cozy neighborhood taproom that rewards repeat visits.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 39.9752,
        "lng": -75.1416,
        "source": "vinepair.com",
    },
    {
        "id": "spot-71",
        "name": "Next of Kin",
        "type": "bar",
        "address": "1300 N Front St, Philadelphia, PA 19122",
        "neighborhood": "Fishtown",
        "description": "One of Philly's best new cocktail bars according to industry insiders. Great cocktails, friendly staff, and a space that makes you want to stay. Named the top new bar pick by multiple Philly bartenders polled by VinePair.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": "cocktails",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9722,
        "lng": -75.1348,
        "source": "vinepair.com",
    },
    {
        "id": "spot-72",
        "name": "Amá",
        "type": "restaurant",
        "address": "Philadelphia, PA",
        "neighborhood": "Philadelphia",
        "description": "A buzzy new spot making culinary-style cocktails that lean into anti-waste ingredients. Beautiful, thoughtful drinks with a sustainability-forward approach. Cited by Philly bartenders as one of the most exciting new openings in the city.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": "cocktails / small plates",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9526,
        "lng": -75.1652,
        "source": "vinepair.com",
    },
]

# Check for duplicates against existing hotspot names
hotspots_match = re.search(r'(export const hotspots: HotSpot\[\] = \[)(.*?)(\];)', content, re.DOTALL)
hotspots_text = hotspots_match.group(2)
existing_spot_names = set()
for nm in re.findall(r'name:\s*"([^"]*)"', hotspots_text):
    existing_spot_names.add(nm.lower().replace("\\'", "'"))

actually_new_spots = []
for sp in new_hotspots:
    if sp["name"].lower() in existing_spot_names:
        print(f"SKIPPING DUPLICATE SPOT: {sp['name']}")
    else:
        actually_new_spots.append(sp)

print(f"New hotspots to add: {len(actually_new_spots)}")

# ────────────────────────────────────────────────
# 4. Influencer recentPicks updates
# ────────────────────────────────────────────────
influencer_updates = {
    "wooder_ice": [
        {
            "name": "PHS Pop-Up Garden Season",
            "type": "event",
            "neighborhood": "Manayunk / South Street",
            "quote": "The pop-up gardens are back with boardwalk-style eats, frozen drinks, and Flower Show plants getting a second life. Grand opening March 27!",
            "date": "2026-03-17",
        },
        {
            "name": "Diversitech 2026",
            "type": "event",
            "neighborhood": "Center City",
            "quote": "Diversitech 2026 returns March 19-21, bringing together leaders, innovators, founders, and emerging talent for one of the most dynamic events in Philly.",
            "date": "2026-02-26",
        },
    ],
    "josheatsphilly": [
        {
            "name": "5 New Center City Spots for 2026",
            "type": "spot",
            "neighborhood": "Center City",
            "quote": "From buzzy new cocktail bars and casual hangouts to late night food and intimate dining — these Center City spots are some of the most exciting in Philly right now.",
            "date": "2026-01-02",
        },
        {
            "name": "James Beard Award Semifinalists",
            "type": "spot",
            "neighborhood": "Philadelphia",
            "quote": "12 Philadelphia spots were named 2026 James Beard Award semifinalists, spanning Outstanding Restaurant, Best New Restaurant, and more. Philly stays winning.",
            "date": "2026-01-23",
        },
    ],
    "feedingtimetv": [
        {
            "name": "Best Wings in Philadelphia",
            "type": "spot",
            "neighborhood": "Philadelphia",
            "quote": "These are the best wings in Philadelphia coming into 2026. The crispy, saucy truth — DM me your favorites!",
            "date": "2026-02-17",
        },
    ],
    "phillyfoodladies": [
        {
            "name": "Spring Restaurant Week Picks",
            "type": "spot",
            "neighborhood": "Philadelphia",
            "quote": "Your guide to Philly's best food, drinks & fun this spring. We're hitting every new opening and pop-up we can find!",
            "date": "2026-03-10",
        },
    ],
    "fueledonphilly": [
        {
            "name": "Yards Brewing Eagles Watch Party",
            "type": "spot",
            "neighborhood": "Northern Liberties",
            "quote": "A great place to watch the Eagles game is Yards Brewing — host a watch party for 20 guests at $50/person with open bar and unlimited wings, pretzels, and hummus.",
            "date": "2026-03-10",
        },
    ],
    "koryaversa": [
        {
            "name": "Manayunk StrEAT Food Festival",
            "type": "event",
            "neighborhood": "Manayunk",
            "quote": "Philly's biggest food festival is back! StrEAT Food takes over historic Main Street on Sunday, April 19, 2026. Save the date & come hungry!",
            "date": "2026-03-15",
        },
    ],
}

# ────────────────────────────────────────────────
# 5. Build updated content
# ────────────────────────────────────────────────

def event_to_ts(ev):
    insider_str = "true" if ev["isInsider"] else "false"
    name_esc = ev["name"].replace("'", "\\'").replace('"', '\\"')
    desc_esc = ev["description"].replace("'", "\\'").replace('"', '\\"')
    venue_esc = ev["venue"].replace("'", "\\'").replace('"', '\\"')
    addr_esc = ev["address"].replace("'", "\\'").replace('"', '\\"')
    return f"""  {{
    id: "{ev['id']}",
    name: "{name_esc}",
    date: "{ev['date']}",
    time: "{ev['time']}",
    venue: "{venue_esc}",
    address: "{addr_esc}",
    neighborhood: "{ev['neighborhood']}",
    category: "{ev['category']}",
    description: "{desc_esc}",
    price: "{ev['price']}",
    vibeTag: "{ev['vibeTag']}",
    source: "{ev['source']}",
    lat: {ev['lat']},
    lng: {ev['lng']},
    isInsider: {insider_str},
  }}"""


def spot_to_ts(sp):
    insider_str = "true" if sp["isInsider"] else "false"
    new_str = "true" if sp["isNew"] else "false"
    cuisine_str = f'"{sp["cuisine"]}"' if sp["cuisine"] else "null"
    name_esc = sp["name"].replace("'", "\\'").replace('"', '\\"')
    desc_esc = sp["description"].replace("'", "\\'").replace('"', '\\"')
    addr_esc = sp["address"].replace("'", "\\'").replace('"', '\\"')
    return f"""  {{
    id: "{sp['id']}",
    name: "{name_esc}",
    type: "{sp['type']}",
    address: "{addr_esc}",
    neighborhood: "{sp['neighborhood']}",
    description: "{desc_esc}",
    vibeTag: "{sp['vibeTag']}",
    priceRange: "{sp['priceRange']}",
    cuisine: {cuisine_str},
    isNew: {new_str},
    isInsider: {insider_str},
    lat: {sp['lat']},
    lng: {sp['lng']},
    source: "{sp['source']}",
  }}"""


# Rebuild events array
new_events_ts = ",\n".join([event_to_ts(ev) for ev in actually_new_events])
rebuilt_events = ",".join(kept_events)
if actually_new_events:
    rebuilt_events += ",\n" + new_events_ts

content = content[:events_match.start(2)] + rebuilt_events + content[events_match.end(2):]

# Re-find hotspots match after content change
hotspots_match = re.search(r'(export const hotspots: HotSpot\[\] = \[)(.*?)(\];)', content, re.DOTALL)

# Rebuild hotspots array
new_spots_ts = ",\n".join([spot_to_ts(sp) for sp in actually_new_spots])
rebuilt_spots = hotspots_match.group(2)
if actually_new_spots:
    rebuilt_spots += ",\n" + new_spots_ts

content = content[:hotspots_match.start(2)] + rebuilt_spots + content[hotspots_match.end(2):]

# ────────────────────────────────────────────────
# 6. Update influencer recentPicks
# ────────────────────────────────────────────────
def add_pick(content, handle, pick):
    """Add a pick to an influencer's recentPicks array using string search"""
    quote_esc = pick["quote"].replace("'", "\\'").replace('"', '\\"')
    name_esc = pick["name"].replace("'", "\\'").replace('"', '\\"')
    new_pick = f"""      {{
        name: "{name_esc}",
        type: "{pick['type']}",
        neighborhood: "{pick['neighborhood']}",
        quote: "{quote_esc}",
        date: "{pick['date']}",
      }}"""

    # Find the influencer's recentPicks array
    handle_pos = content.find(f'handle: "@{handle}"')
    if handle_pos == -1:
        # Try without @ prefix
        handle_pos = content.find(f'handle: "{handle}"')
    if handle_pos == -1:
        print(f"  WARNING: Could not find handle {handle}")
        return content

    # Find recentPicks: [ after this handle
    picks_pos = content.find("recentPicks: [", handle_pos)
    if picks_pos == -1:
        print(f"  WARNING: Could not find recentPicks for {handle}")
        return content

    insert_pos = picks_pos + len("recentPicks: [")
    content = content[:insert_pos] + "\n" + new_pick + "," + content[insert_pos:]
    return content

influencer_update_count = 0
for handle, picks in influencer_updates.items():
    for pick in picks:
        content = add_pick(content, handle, pick)
        influencer_update_count += 1
        print(f"  Added pick for @{handle}: {pick['name']}")

print(f"\nInfluencer picks added: {influencer_update_count}")

# ────────────────────────────────────────────────
# 7. DEDUPLICATION
# ────────────────────────────────────────────────
print("\n--- DEDUPLICATION CHECK ---")

# Re-parse events for dedup
events_match2 = re.search(r'export const events: PhillyEvent\[\] = \[(.*?)\];', content, re.DOTALL)
event_blocks2 = re.findall(r'\s*\{[^{}]*?\}', events_match2.group(1))

# Check for duplicate event names (case-insensitive)
seen_event_names = {}
event_dupes = 0
deduped_events = []
for block in event_blocks2:
    nm = re.search(r'name:\s*"([^"]*)"', block)
    eid = re.search(r'id:\s*"([^"]*)"', block)
    if nm:
        key = nm.group(1).lower().replace("\\'", "'")
        if key in seen_event_names:
            # Keep the longer description
            existing_desc = re.search(r'description:\s*"([^"]*)"', seen_event_names[key])
            new_desc = re.search(r'description:\s*"([^"]*)"', block)
            if new_desc and existing_desc and len(new_desc.group(1)) > len(existing_desc.group(1)):
                # Replace existing with this one
                deduped_events = [b for b in deduped_events if b != seen_event_names[key]]
                deduped_events.append(block)
                seen_event_names[key] = block
                print(f"  DEDUP EVENT (keeping longer): {nm.group(1)}")
            else:
                print(f"  DEDUP EVENT (removing shorter): {nm.group(1)}")
            event_dupes += 1
        else:
            seen_event_names[key] = block
            deduped_events.append(block)
    else:
        deduped_events.append(block)

# Check for duplicate hotspot names
hotspots_match2 = re.search(r'export const hotspots: HotSpot\[\] = \[(.*?)\];', content, re.DOTALL)
spot_blocks2 = re.findall(r'\s*\{[^{}]*?\}', hotspots_match2.group(1))

seen_spot_names = {}
spot_dupes = 0
deduped_spots = []
for block in spot_blocks2:
    nm = re.search(r'name:\s*"([^"]*)"', block)
    if nm:
        key = nm.group(1).lower().replace("\\'", "'")
        if key in seen_spot_names:
            existing_desc = re.search(r'description:\s*"([^"]*)"', seen_spot_names[key])
            new_desc = re.search(r'description:\s*"([^"]*)"', block)
            if new_desc and existing_desc and len(new_desc.group(1)) > len(existing_desc.group(1)):
                deduped_spots = [b for b in deduped_spots if b != seen_spot_names[key]]
                deduped_spots.append(block)
                seen_spot_names[key] = block
                print(f"  DEDUP SPOT (keeping longer): {nm.group(1)}")
            else:
                print(f"  DEDUP SPOT (removing shorter): {nm.group(1)}")
            spot_dupes += 1
        else:
            seen_spot_names[key] = block
            deduped_spots.append(block)
    else:
        deduped_spots.append(block)

# Check for duplicate IDs
all_ids = []
for block in deduped_events + deduped_spots:
    id_m = re.search(r'id:\s*"([^"]*)"', block)
    if id_m:
        all_ids.append(id_m.group(1))

id_counts = {}
for i in all_ids:
    id_counts[i] = id_counts.get(i, 0) + 1

dup_ids = {k: v for k, v in id_counts.items() if v > 1}
if dup_ids:
    print(f"  WARNING: Duplicate IDs found: {dup_ids}")
else:
    print("  No duplicate IDs found.")

total_dupes = event_dupes + spot_dupes
print(f"\nTotal duplicates removed: {total_dupes} ({event_dupes} events, {spot_dupes} spots)")

# Rebuild if deduplication removed anything
if event_dupes > 0:
    rebuilt = ",".join(deduped_events)
    events_match3 = re.search(r'(export const events: PhillyEvent\[\] = \[)(.*?)(\];)', content, re.DOTALL)
    content = content[:events_match3.start(2)] + rebuilt + content[events_match3.end(2):]

if spot_dupes > 0:
    rebuilt = ",".join(deduped_spots)
    hotspots_match3 = re.search(r'(export const hotspots: HotSpot\[\] = \[)(.*?)(\];)', content, re.DOTALL)
    content = content[:hotspots_match3.start(2)] + rebuilt + content[hotspots_match3.end(2):]

# ────────────────────────────────────────────────
# 8. Write updated file
# ────────────────────────────────────────────────
with open(DATA_FILE, "w") as f:
    f.write(content)

# Final counts
final_events = len(re.findall(r'id: "event-', content))
final_spots = len(re.findall(r'id: "spot-', content))

print(f"\n=== FINAL SUMMARY ===")
print(f"Expired events removed: {expired_count}")
print(f"New events added: {len(actually_new_events)}")
print(f"New hotspots added: {len(actually_new_spots)}")
print(f"Influencer picks updated: {influencer_update_count}")
print(f"Duplicates removed: {total_dupes}")
print(f"Final event count: {final_events}")
print(f"Final hotspot count: {final_spots}")
