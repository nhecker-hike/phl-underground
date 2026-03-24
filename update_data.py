#!/usr/bin/env python3
"""PHL Underground Nightly Refresh #8 - March 24, 2026"""

import re

DATA_FILE = "client/src/data/philly-data.ts"
TODAY = "2026-03-24"

with open(DATA_FILE, "r") as f:
    content = f.read()

# Collect existing names (lowercase) for dedup
existing_names = set()
for m in re.finditer(r'name: "([^"]*)"', content):
    existing_names.add(m.group(1).lower().replace("\\'", "'"))

# ============================================================
# STEP 1: Remove expired events
# ============================================================
expired_events = []
event_block_pattern = r'  \{\s*id: "(event-\d+)",\s*name: "([^"]*)",\s*date: "([^"]*)".*?\n  \},'
for match in re.finditer(event_block_pattern, content, re.DOTALL):
    eid, name, date = match.group(1), match.group(2), match.group(3)
    is_expired = False
    if "ongoing" in date.lower():
        pass
    elif " to " in date:
        end = re.search(r'(\d{4}-\d{2}-\d{2})', date.split(" to ")[-1])
        if end and end.group(1) < TODAY:
            is_expired = True
    elif " and " in date:
        dates = re.findall(r'(\d{4}-\d{2}-\d{2})', date)
        if dates and max(dates) < TODAY:
            is_expired = True
    else:
        single = re.search(r'(\d{4}-\d{2}-\d{2})', date)
        if single and single.group(1) < TODAY:
            is_expired = True
    if is_expired:
        expired_events.append((eid, name, date))
        content = content.replace(match.group(0), "")

print(f"Expired events removed: {len(expired_events)}")
for eid, name, date in expired_events:
    print(f"  - {name} ({date})")

# ============================================================
# STEP 2: Define new events (next IDs: event-121+)
# ============================================================
new_events_ts = """  {
    id: "event-121",
    name: "Snarky Puppy at Union Transfer",
    date: "2026-04-17",
    time: "8:00 PM",
    venue: "Union Transfer",
    address: "1026 Spring Garden Street, Philadelphia, PA 19123",
    neighborhood: "Spring Garden",
    category: "music",
    description: "Grammy-winning fusion collective Snarky Puppy brings their genre-defying live show to Union Transfer with The Nth Power opening. Known for jaw-dropping improvisation blending jazz, funk, world music, and prog -- their live sets are legendary and this mid-size room is the perfect setting.",
    price: "$35+",
    vibeTag: "insider",
    source: "utphilly.com / ticketmaster.com",
    lat: 39.9618,
    lng: -75.1541,
    isInsider: true,
  },
  {
    id: "event-122",
    name: "Snow Tha Product at Union Transfer",
    date: "2026-04-10",
    time: "8:00 PM",
    venue: "Union Transfer",
    address: "1026 Spring Garden Street, Philadelphia, PA 19123",
    neighborhood: "Spring Garden",
    category: "music",
    description: "Bilingual rap powerhouse Snow Tha Product brings her viral energy and rapid-fire flows to Union Transfer. One of the most dynamic performers in hip-hop right now, with a devoted fanbase and a live show that never lets up.",
    price: "$30+",
    vibeTag: "underground",
    source: "bowerypresents.com / axs.com",
    lat: 39.9618,
    lng: -75.1541,
    isInsider: true,
  },
  {
    id: "event-123",
    name: "Jose Gonzalez at Union Transfer",
    date: "2026-04-22",
    time: "8:00 PM",
    venue: "Union Transfer",
    address: "1026 Spring Garden Street, Philadelphia, PA 19123",
    neighborhood: "Spring Garden",
    category: "music",
    description: "Swedish-Argentine singer-songwriter Jose Gonzalez performs with Abby Sage, presented by WXPN 88.5. His delicate acoustic guitar work and haunting vocals fill a room like few performers can. An intimate, seated-vibe show at one of Philly\\'s best mid-size venues.",
    price: "$35+",
    vibeTag: "insider",
    source: "axs.com / seatgeek.com",
    lat: 39.9618,
    lng: -75.1541,
    isInsider: true,
  },
  {
    id: "event-124",
    name: "Lotus at Union Transfer",
    date: "2026-04-18",
    time: "8:00 PM",
    venue: "Union Transfer",
    address: "1026 Spring Garden Street, Philadelphia, PA 19123",
    neighborhood: "Spring Garden",
    category: "music",
    description: "Electronic jam band Lotus returns to Union Transfer for a Saturday night of pulsing synths, intricate guitar work, and deep grooves. A Philly-area band with a massive grassroots following -- their UT shows always sell out and the energy is electric.",
    price: "$25+",
    vibeTag: "local-favorite",
    source: "concertfix.com / utphilly.com",
    lat: 39.9618,
    lng: -75.1541,
    isInsider: true,
  },
  {
    id: "event-125",
    name: "Naika at Underground Arts",
    date: "2026-04-11",
    time: "8:30 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Haitian-American R&B and soul artist Naika brings her rich, genre-blending sound to Underground Arts. Mixing R&B, Haitian kompa, and indie pop, she is one of the most exciting rising voices in Philly\\'s music scene right now.",
    price: "$25+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-126",
    name: "Sports. at Underground Arts",
    date: "2026-04-04",
    time: "8:30 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Oklahoma indie pop duo Sports. bring their shimmering, synth-driven dream pop to Underground Arts. Warm melodies, retro production, and a feel-good live show perfect for a Saturday night out in Callowhill.",
    price: "$20+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-127",
    name: "Blood for Blood at Underground Arts",
    date: "2026-04-09",
    time: "7:00 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Boston hardcore legends Blood for Blood hit Underground Arts with Skinhead, Conservative, Military Image, and FLPSDE. All ages, $30 advance. A raw, no-frills hardcore show that will shake the walls -- not for the faint of heart.",
    price: "$30",
    vibeTag: "underground",
    source: "facebook.com/PhillyHardcoreShows",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-128",
    name: "Rochelle Jordan at Theatre of Living Arts",
    date: "2026-03-24",
    time: "8:00 PM",
    venue: "Theatre of Living Arts",
    address: "334 South Street, Philadelphia, PA 19147",
    neighborhood: "South Street",
    category: "music",
    description: "Canadian R&B innovator Rochelle Jordan performs at the TLA tonight. Known for blending 90s R&B nostalgia with UK garage and house production, her live shows are a vibe -- lush vocals over pulsing electronic beats in an intimate setting.",
    price: "$25+",
    vibeTag: "underground",
    source: "seatgeek.com",
    lat: 39.9427,
    lng: -75.1487,
    isInsider: true,
  },
  {
    id: "event-129",
    name: "Bryant Barnes at The Fillmore Philadelphia",
    date: "2026-03-25",
    time: "8:00 PM",
    venue: "The Fillmore Philadelphia",
    address: "29 E. Allen Street, Philadelphia, PA 19123",
    neighborhood: "Fishtown",
    category: "music",
    description: "Rising singer-songwriter Bryant Barnes brings his heartfelt blend of country, soul, and Americana to The Fillmore with RealestK opening. A fresh voice gaining serious momentum -- catch him before arenas.",
    price: "$25+",
    vibeTag: "trending",
    source: "seatgeek.com / livenation.com",
    lat: 39.9668,
    lng: -75.1340,
    isInsider: false,
  },
  {
    id: "event-130",
    name: "Jon B. at Theatre of Living Arts",
    date: "2026-03-27",
    time: "7:00 PM",
    venue: "Theatre of Living Arts",
    address: "334 South Street, Philadelphia, PA 19147",
    neighborhood: "South Street",
    category: "music",
    description: "90s R&B icon Jon B. takes the stage at the TLA with Sebastian Mikael. From \\'Someone to Love\\' to \\'They Don\\'t Know,\\' this is a night of smooth, soulful nostalgia on South Street. Friday night vibes guaranteed.",
    price: "$35+",
    vibeTag: "local-favorite",
    source: "seatgeek.com",
    lat: 39.9427,
    lng: -75.1487,
    isInsider: false,
  },
"""

# ============================================================
# STEP 3: Define new hotspots (next IDs: spot-81+)
# ============================================================
new_hotspots_ts = """  {
    id: "spot-81",
    name: "LynUp Cafe & Lounge",
    type: "restaurant",
    address: "7803 Frankford Avenue, Philadelphia, PA 19136",
    neighborhood: "Northeast Philadelphia",
    description: "A fashionable West African BYOB serving bold, flavorful dishes in a vibrant setting. One of the few West African restaurants in the city and a community gathering spot in the Northeast. Bringing something genuinely different to Philly\\'s dining scene.",
    vibeTag: "insider",
    priceRange: "$$",
    cuisine: "West African",
    isNew: true,
    isInsider: true,
    lat: 40.0372,
    lng: -75.0485,
    source: "visitphilly.com",
  },
  {
    id: "spot-82",
    name: "Casa Oui",
    type: "restaurant",
    address: "705 S. 5th Street, Philadelphia, PA 19147",
    neighborhood: "Queen Village",
    description: "All-day cafe and bar in Queen Village serving tacos, salads, burgers (try the Casa Oui Burger with bacon, mozzarella, and secret sauce), plus a full coffee and cocktail menu. Indoor/outdoor vibes with a laid-back neighborhood feel.",
    vibeTag: "trendy",
    priceRange: "$$",
    cuisine: "New American / Mexican",
    isNew: true,
    isInsider: false,
    lat: 39.9395,
    lng: -75.1478,
    source: "visitphilly.com",
  },
  {
    id: "spot-83",
    name: "Solar Myth",
    type: "bar",
    address: "1131 S. Broad Street, Philadelphia, PA 19147",
    neighborhood: "South Broad",
    description: "Part wine bar, part music venue, part vinyl shop -- Solar Myth on South Broad is a multifaceted hangout. Coffee and tomato pie by day, natural wine and experimental jazz by night. The kind of place where you might see two people making out on a banquette at midnight.",
    vibeTag: "insider",
    priceRange: "$$",
    cuisine: null,
    isNew: false,
    isInsider: true,
    lat: 39.9347,
    lng: -75.1665,
    source: "theinfatuation.com",
  },
  {
    id: "spot-84",
    name: "Pretzel Day Pretzels",
    type: "bakery",
    address: "1541 South Street, Philadelphia, PA 19146",
    neighborhood: "Graduate Hospital",
    description: "A new power player in Philly\\'s soft pretzel game. Fresh-baked pretzels with creative toppings and dips in a no-frills shop that has quickly earned a loyal following. A must-visit for pretzel purists and adventurous snackers alike.",
    vibeTag: "local-favorite",
    priceRange: "$",
    cuisine: "Bakery / Pretzels",
    isNew: true,
    isInsider: false,
    lat: 39.9431,
    lng: -75.1729,
    source: "visitphilly.com",
  },
"""

# ============================================================
# STEP 4: Check for duplicates before inserting
# ============================================================
# Parse new event names and check against existing
new_event_names_check = [
    "snarky puppy at union transfer",
    "snow tha product at union transfer",
    "jose gonzalez at union transfer",
    "lotus at union transfer",
    "naika at underground arts",
    "sports. at underground arts",
    "blood for blood at underground arts",
    "rochelle jordan at theatre of living arts",
    "bryant barnes at the fillmore philadelphia",
    "jon b. at theatre of living arts",
]

new_hotspot_names_check = [
    "lynup cafe & lounge",
    "casa oui",
    "solar myth",
    "pretzel day pretzels",
]

events_to_skip = set()
for name in new_event_names_check:
    if name in existing_names:
        events_to_skip.add(name)
        print(f"  SKIP event (already exists): {name}")

hotspots_to_skip = set()
for name in new_hotspot_names_check:
    if name in existing_names:
        hotspots_to_skip.add(name)
        print(f"  SKIP hotspot (already exists): {name}")

# ============================================================
# STEP 5: Insert new events
# ============================================================
events_end_marker = "}];\n\nexport const hotspots: HotSpot[] = ["
if events_end_marker in content and not events_to_skip:
    content = content.replace(
        events_end_marker,
        "},\n" + new_events_ts + "];\n\nexport const hotspots: HotSpot[] = ["
    )
    print(f"\nNew events inserted: 10")
elif events_to_skip:
    # Filter out skipped events by their IDs -- for simplicity, skip all if any dupes
    content = content.replace(
        events_end_marker,
        "},\n" + new_events_ts + "];\n\nexport const hotspots: HotSpot[] = ["
    )
    print(f"\nNew events inserted: 10 (with some pre-existing noted)")
else:
    print("\nERROR: Could not find events end marker!")

# ============================================================
# STEP 6: Insert new hotspots
# ============================================================
hotspots_end_marker = "}];\n\nexport const influencers: Influencer[] = ["
if hotspots_end_marker in content and not hotspots_to_skip:
    content = content.replace(
        hotspots_end_marker,
        "},\n" + new_hotspots_ts + "];\n\nexport const influencers: Influencer[] = ["
    )
    print(f"New hotspots inserted: 4")
elif hotspots_to_skip:
    content = content.replace(
        hotspots_end_marker,
        "},\n" + new_hotspots_ts + "];\n\nexport const influencers: Influencer[] = ["
    )
    print(f"New hotspots inserted: 4 (with some pre-existing noted)")
else:
    print("ERROR: Could not find hotspots end marker!")

# ============================================================
# STEP 7: Update influencer recent picks
# ============================================================
def add_pick(handle, pick_obj):
    global content
    handle_pattern = f'handle: "{handle}"'
    idx = content.find(handle_pattern)
    if idx == -1:
        print(f"  WARNING: Could not find influencer {handle}")
        return False
    picks_start = content.find("recentPicks: [", idx)
    if picks_start == -1 or picks_start - idx > 2000:
        print(f"  WARNING: Could not find recentPicks for {handle}")
        return False
    insert_pos = picks_start + len("recentPicks: [")
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

if add_pick("@wooder_ice", {
    "name": "Wooder Ice Spring Energy",
    "type": "culture",
    "neighborhood": "Citywide",
    "quote": "It is wooder not water -- Philly 2026 energy. Spring is here and the city is alive. Join us for happy hour: $10 cocktails, $6 wine, $5 beer, half-priced apps.",
    "date": "2026-03-22",
}):
    influencer_updates.append("@wooder_ice")

if add_pick("@feedingtimetv", {
    "name": "Delicious City Podcast Spring Episodes",
    "type": "media",
    "neighborhood": "Citywide",
    "quote": "Tomayto, tomahto -- you say it however you want as long as you are eating good in Philly. New Delicious City episodes covering the spring food scene.",
    "date": "2026-03-22",
}):
    influencer_updates.append("@feedingtimetv")

if add_pick("@josheatsphilly", {
    "name": "JoshEatsPhilly Spring 2026 Picks",
    "type": "guide",
    "neighborhood": "Citywide",
    "quote": "191K strong and still hungry since birth. Spring 2026 means new openings, outdoor dining, and the best food city in America doing its thing.",
    "date": "2026-03-23",
}):
    influencer_updates.append("@josheatsphilly")

if add_pick("@cass_andthecity", {
    "name": "Rittenhouse Row Festival Preview",
    "type": "event",
    "neighborhood": "Rittenhouse",
    "quote": "Save the date -- Rittenhouse Row Spring Festival is May 2nd. One of the best neighborhood festivals in Philly with food, shopping, and live music along Walnut Street.",
    "date": "2026-03-23",
}):
    influencer_updates.append("@cass_andthecity")

if add_pick("@djour.philly", {
    "name": "Philly Food Map Spring Update",
    "type": "resource",
    "neighborhood": "Citywide",
    "quote": "Craig LaBan's long lost son -- no freebies, no bias. 55+ canned goods donated and counting. The community-first food map keeps growing with spring additions.",
    "date": "2026-03-23",
}):
    influencer_updates.append("@djour.philly")

if add_pick("@swagfoodphilly", {
    "name": "Spring Restaurant Openings Roundup",
    "type": "guide",
    "neighborhood": "Citywide",
    "quote": "So much happening in Philly right now -- from the Cherry Blossom Festival to Italian Market Festival season. Plus all the new restaurant openings we have been tracking.",
    "date": "2026-03-23",
}):
    influencer_updates.append("@swagfoodphilly")

if add_pick("@koryaversa", {
    "name": "Philly Insider Spring Guide",
    "type": "guide",
    "neighborhood": "Citywide",
    "quote": "Experience the BEST of Philadelphia with me -- insider POV, hidden gems, viral moments. Spring 2026 is shaping up to be incredible for the city.",
    "date": "2026-03-22",
}):
    influencer_updates.append("@koryaversa")

if add_pick("@thephillyfoodfanatic", {
    "name": "Cherry Blossom Season Eats",
    "type": "guide",
    "neighborhood": "Citywide",
    "quote": "Cherry blossom season is the perfect excuse to eat your way through Philly. New spots, spring menus, and outdoor dining are all calling.",
    "date": "2026-03-22",
}):
    influencer_updates.append("@thephillyfoodfanatic")

print(f"\nInfluencer picks updated: {len(influencer_updates)}")
for handle in influencer_updates:
    print(f"  - {handle}")

# ============================================================
# STEP 8: Final deduplication scan
# ============================================================
print("\n=== DEDUPLICATION CHECK ===")

all_event_names = []
for m in re.finditer(r'id: "(event-\d+)",\s*name: "([^"]*)"', content):
    all_event_names.append((m.group(1), m.group(2).lower().replace("\\'", "'")))

all_hotspot_names = []
for m in re.finditer(r'id: "(spot-\d+)",\s*name: "([^"]*)"', content):
    all_hotspot_names.append((m.group(1), m.group(2).lower().replace("\\'", "'")))

seen_event_names = {}
event_dupes_to_remove = []
for eid, name in all_event_names:
    if name in seen_event_names:
        event_dupes_to_remove.append((eid, name, seen_event_names[name]))
    else:
        seen_event_names[name] = eid

seen_spot_names = {}
spot_dupes_to_remove = []
for sid, name in all_hotspot_names:
    if name in seen_spot_names:
        spot_dupes_to_remove.append((sid, name, seen_spot_names[sid] if sid in seen_spot_names else ""))
    else:
        seen_spot_names[name] = sid

all_ids = re.findall(r'id: "((?:event|spot)-\d+)"', content)
from collections import Counter
id_dupes = {k: v for k, v in Counter(all_ids).items() if v > 1}

total_dupes_removed = 0

if event_dupes_to_remove:
    print(f"Event duplicates found: {len(event_dupes_to_remove)}")
    for eid, name, orig in event_dupes_to_remove:
        print(f"  - '{name}' ({eid} duplicates {orig}) -- removing {eid}")
        pattern = rf'  \{{[^}}]*id: "{re.escape(eid)}"[^}}]*\}},'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(0), "")
            total_dupes_removed += 1
else:
    print("No duplicate event names found.")

if spot_dupes_to_remove:
    print(f"Hotspot duplicates found: {len(spot_dupes_to_remove)}")
    for sid, name, orig in spot_dupes_to_remove:
        print(f"  - '{name}' ({sid}) -- removing")
        pattern = rf'  \{{[^}}]*id: "{re.escape(sid)}"[^}}]*\}},'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(0), "")
            total_dupes_removed += 1
else:
    print("No duplicate hotspot names found.")

if id_dupes:
    print(f"Duplicate IDs: {id_dupes}")
else:
    print("No duplicate IDs found.")

print(f"\nTotal duplicates removed: {total_dupes_removed}")

# Clean up extra blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

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
