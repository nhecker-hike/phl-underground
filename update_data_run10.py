#!/usr/bin/env python3
"""
PHL Underground Nightly Data Refresh #10 (2026-03-27)
- Remove past events (before today)
- Add new events from research
- Add new hotspots
- Hotspot lifecycle management (decay scores, prune, unmark isNew)
- Update influencer recentPicks
- Deduplicate
"""

import re
import json
from datetime import datetime, timedelta

TODAY = "2026-03-27"
TODAY_DT = datetime.strptime(TODAY, "%Y-%m-%d")

with open("client/src/data/philly-data.ts", "r") as f:
    content = f.read()

# ── Helpers ──
def get_names(section):
    return set(n.lower() for n in re.findall(r'name: "([^"]+)"', section))

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")

# ── Section boundaries ──
def bounds():
    hs = content.find("export const hotspots")
    inf = content.find("export const influencers")
    return hs, inf

hs_start, inf_start = bounds()
existing_event_names = get_names(content[:hs_start])
existing_hotspot_names = get_names(content[hs_start:inf_start])

# Get max IDs
event_ids = [int(x) for x in re.findall(r'id: "event-(\d+)"', content)]
spot_ids = [int(x) for x in re.findall(r'id: "spot-(\d+)"', content)]
next_event_id = max(event_ids) + 1
next_spot_id = max(spot_ids) + 1

print(f"Starting state: {len(event_ids)} events (max event-{max(event_ids)}), {len(spot_ids)} hotspots (max spot-{max(spot_ids)})")

# ════════════════════════════════════════
# STEP 1: REMOVE PAST EVENTS
# ════════════════════════════════════════
print("\n=== REMOVING PAST EVENTS ===")
hs_start, _ = bounds()
ev_section = content[:hs_start]

# Find event blocks with simple dates that are in the past
event_blocks = list(re.finditer(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', ev_section, re.DOTALL))
past_removed = 0

for match in reversed(event_blocks):
    block = match.group(1)
    date_match = re.search(r'date: "(\d{4}-\d{2}-\d{2})"', block)
    if date_match:
        event_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        if event_date < TODAY_DT:
            name_match = re.search(r'name: "([^"]+)"', block)
            name = name_match.group(1) if name_match else "unknown"
            print(f"  Removing: {name} ({date_match.group(1)})")
            
            start = match.start()
            end = match.end()
            
            # Handle trailing comma
            after = ev_section[end:end+20]
            before = ev_section[max(0, start-20):start]
            
            if after.lstrip().startswith(','):
                comma_off = after.index(',')
                ev_section = ev_section[:start] + ev_section[end + comma_off + 1:]
            elif before.rstrip().endswith(','):
                pre = ev_section[:start]
                last_comma = pre.rstrip().rfind(',')
                ev_section = ev_section[:last_comma] + ev_section[end:]
            else:
                ev_section = ev_section[:start] + ev_section[end:]
            
            past_removed += 1

content = ev_section + content[hs_start:]
print(f"  Removed {past_removed} past events")

# ════════════════════════════════════════
# STEP 2: ADD NEW EVENTS
# ════════════════════════════════════════
print("\n=== ADDING NEW EVENTS ===")

# Refresh existing names
hs_start, _ = bounds()
existing_event_names = get_names(content[:hs_start])

new_events = [
    {
        "name": "CupcakKe: The Bakkery Album Release Tour at Brooklyn Bowl",
        "date": "2026-03-27",
        "time": "8:00 PM",
        "venue": "Brooklyn Bowl Philadelphia",
        "address": "1009 Canal St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "concert",
        "description": "CupcakKe brings her outrageous energy and the Bakkery Album Release Tour to Brooklyn Bowl. The provocative rapper is known for wild live shows and a fiercely loyal fanbase. 18+ event.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "seatgeek.com",
        "lat": 39.9630,
        "lng": -75.1390,
        "isInsider": True,
    },
    {
        "name": "Moonchild at Ardmore Music Hall",
        "date": "2026-04-03",
        "time": "8:00 PM",
        "venue": "Ardmore Music Hall",
        "address": "23 E Lancaster Ave, Ardmore, PA 19003",
        "neighborhood": "Main Line",
        "category": "concert",
        "description": "Neo-soul trio Moonchild brings their lush, jazzy sound to the intimate Ardmore Music Hall. One of the most underrated live acts in R&B/jazz fusion, with Brittney Carter opening. A true insider pick.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "jambase.com",
        "lat": 40.0067,
        "lng": -75.2878,
        "isInsider": True,
    },
    {
        "name": "Philly Film Society Spring Festival",
        "date": "2026-04-17 to 2026-04-23",
        "time": "Various",
        "venue": "Various Locations",
        "address": "Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "film",
        "description": "The Philadelphia Film Society's annual Spring Festival brings a curated lineup of independent films, documentaries, and shorts to theaters across the city. Q&As with filmmakers, opening night parties, and late-night screenings make this a week-long cultural highlight.",
        "price": "$15+",
        "vibeTag": "underground",
        "source": "phillyfestivals.org",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": True,
    },
    {
        "name": "Dinah Day Philadelphia",
        "date": "2026-04-18",
        "time": "12:00 PM",
        "venue": "Various Locations",
        "address": "Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "cultural",
        "description": "An all-day celebration and community gathering for women and femmes in Philadelphia. Music, vendors, wellness activities, and good vibes at various spots across the city.",
        "price": "Free - Varies",
        "vibeTag": "underground",
        "source": "phillyfestivals.org",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": True,
    },
    {
        "name": "Maker Faire Philadelphia",
        "date": "2026-04-19",
        "time": "10:00 AM",
        "venue": "Various",
        "address": "Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "market",
        "description": "Philly's annual celebration of DIY culture, invention, and creativity. Makers, hackers, artists, and tinkerers showcase everything from 3D printing to robotics to handcrafted goods. A family-friendly festival for the curious.",
        "price": "Free - $10",
        "vibeTag": "local-favorite",
        "source": "phillyfestivals.org",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": False,
    },
    {
        "name": "Chestnut Hill Clover Market",
        "date": "2026-04-12",
        "time": "10:00 AM - 4:00 PM",
        "venue": "Germantown Ave, Chestnut Hill",
        "address": "Germantown Ave, Philadelphia, PA 19118",
        "neighborhood": "Chestnut Hill",
        "category": "market",
        "description": "The Clover Market returns to Chestnut Hill with curated vendors selling vintage finds, handmade goods, artisan food, and local crafts along charming Germantown Avenue. A quintessential Philly Sunday.",
        "price": "Free entry",
        "vibeTag": "local-favorite",
        "source": "phillyfestivals.org",
        "lat": 40.0783,
        "lng": -75.2100,
        "isInsider": False,
    },
    {
        "name": "Mahler & Sorey with The Philadelphia Orchestra at Kimmel Center",
        "date": "2026-05-15 to 2026-05-16",
        "time": "8:00 PM",
        "venue": "Kimmel Center for the Performing Arts",
        "address": "300 S Broad St, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "performing-arts",
        "description": "Pianist Aaron Diehl and The Philadelphia Orchestra deliver Mahler's groundbreaking Symphony No. 5 -- described as a foaming, roaring, raging sea of sound -- alongside a new work from Pulitzer Prize-winning composer Tyshawn Sorey.",
        "price": "$30+",
        "vibeTag": "after-dark",
        "source": "visitphilly.com",
        "lat": 39.9464,
        "lng": -75.1660,
        "isInsider": True,
    },
]

events_added = 0
eid = next_event_id
new_event_entries = []

for ev in new_events:
    if ev["name"].lower() in existing_event_names:
        print(f"  Skipping (exists): {ev['name']}")
        continue
    
    entry = f"""  {{
    id: "event-{eid}",
    name: "{esc(ev['name'])}",
    date: "{ev['date']}",
    time: "{ev['time']}",
    venue: "{esc(ev['venue'])}",
    address: "{esc(ev['address'])}",
    neighborhood: "{ev['neighborhood']}",
    category: "{ev['category']}",
    description: "{esc(ev['description'])}",
    price: "{ev['price']}",
    vibeTag: "{ev['vibeTag']}",
    source: "{ev['source']}",
    lat: {ev['lat']},
    lng: {ev['lng']},
    isInsider: {"true" if ev["isInsider"] else "false"},
  }}"""
    new_event_entries.append(entry)
    existing_event_names.add(ev["name"].lower())
    events_added += 1
    eid += 1
    print(f"  Adding: {ev['name']}")

if new_event_entries:
    hs_start, _ = bounds()
    events_closing = content[:hs_start].rfind("];")
    last_brace = content[:events_closing].rfind("}")
    insertion = ",\n" + ",\n".join(new_event_entries) + ",\n"
    content = content[:last_brace+1] + insertion + content[last_brace+1:]

print(f"  Added {events_added} new events")

# ════════════════════════════════════════
# STEP 3: ADD NEW HOTSPOTS
# ════════════════════════════════════════
print("\n=== ADDING NEW HOTSPOTS ===")

hs_start, inf_start = bounds()
existing_hotspot_names = get_names(content[hs_start:inf_start])

new_hotspots = [
    {
        "name": "48 Record Bar",
        "type": "Bar / Vinyl Lounge",
        "address": "48 S 2nd St, Philadelphia, PA 19106",
        "neighborhood": "Old City",
        "description": "A vinyl-forward cocktail bar in Old City where the turntable is always spinning. Craft cocktails, rotating DJ nights, and a curated record collection for sale. The perfect late-night haunt for music heads.",
        "vibeTag": "underground",
        "priceRange": "$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 39.9489,
        "lng": -75.1456,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Manna Bakery Kensington",
        "type": "Bakery / Cafe",
        "address": "Kensington, Philadelphia, PA",
        "neighborhood": "Kensington",
        "description": "Farmers-market favorite Manna Bakery takes over the shuttered Essen's space in Kensington, bringing their beloved sourdough, pastries, and breakfast sandwiches to a permanent brick-and-mortar. A neighborhood game-changer.",
        "vibeTag": "local-favorite",
        "priceRange": "$",
        "cuisine": "Bakery",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9780,
        "lng": -75.1340,
        "source": "inquirer.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Jaffa Bar",
        "type": "Bar",
        "address": "1625 N Howard St, Philadelphia, PA 19122",
        "neighborhood": "Fishtown",
        "description": "A Middle Eastern-influenced cocktail bar in Fishtown with inventive drinks, small plates, and a moody, intimate atmosphere. Think arak-based cocktails, hummus with lamb, and late-night DJ sets on weekends.",
        "vibeTag": "underground",
        "priceRange": "$$",
        "cuisine": "Middle Eastern",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9752,
        "lng": -75.1352,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
]

spots_added = 0
sid = next_spot_id
new_spot_entries = []

for spot in new_hotspots:
    if spot["name"].lower() in existing_hotspot_names:
        print(f"  Skipping (exists): {spot['name']}")
        continue
    
    cuisine_val = f'"{spot["cuisine"]}"' if spot["cuisine"] else "null"
    
    entry = f"""  {{
    id: "spot-{sid}",
    name: "{esc(spot['name'])}",
    type: "{spot['type']}",
    address: "{esc(spot['address'])}",
    neighborhood: "{spot['neighborhood']}",
    description: "{esc(spot['description'])}",
    vibeTag: "{spot['vibeTag']}",
    priceRange: "{spot['priceRange']}",
    cuisine: {cuisine_val},
    isNew: {"true" if spot["isNew"] else "false"},
    isInsider: {"true" if spot["isInsider"] else "false"},
    lat: {spot['lat']},
    lng: {spot['lng']},
    source: "{spot['source']}",
    addedDate: "{spot['addedDate']}",
    trendingScore: {spot['trendingScore']},
  }}"""
    new_spot_entries.append(entry)
    existing_hotspot_names.add(spot["name"].lower())
    spots_added += 1
    sid += 1
    print(f"  Adding: {spot['name']}")

if new_spot_entries:
    _, inf_start = bounds()
    hotspots_closing = content[:inf_start].rfind("];")
    last_brace = content[:hotspots_closing].rfind("}")
    insertion = ",\n" + ",\n".join(new_spot_entries) + ",\n"
    content = content[:last_brace+1] + insertion + content[last_brace+1:]

print(f"  Added {spots_added} new hotspots")

# ════════════════════════════════════════
# STEP 4: HOTSPOT LIFECYCLE MANAGEMENT
# ════════════════════════════════════════
print("\n=== HOTSPOT LIFECYCLE ===")

hs_start, inf_start = bounds()
hs_section = content[hs_start:inf_start]
spot_count = len(re.findall(r'id: "spot-', hs_section))
print(f"  Total hotspots: {spot_count}")

spot_blocks = list(re.finditer(
    r'(\{[^{}]*?id: "spot-\d+"[^{}]*?\})', hs_section, re.DOTALL
))

pruned = 0
decayed = 0
unmarked_new = 0

for match in reversed(spot_blocks):
    block = match.group(1)
    added_m = re.search(r'addedDate: "(\d{4}-\d{2}-\d{2})"', block)
    score_m = re.search(r'trendingScore: (\d+)', block)
    insider_m = re.search(r'isInsider: (true|false)', block)
    isnew_m = re.search(r'isNew: (true|false)', block)
    name_m = re.search(r'name: "([^"]+)"', block)
    
    if not added_m or not score_m:
        continue
    
    added_date = datetime.strptime(added_m.group(1), "%Y-%m-%d")
    score = int(score_m.group(1))
    is_insider = insider_m and insider_m.group(1) == "true"
    is_new = isnew_m and isnew_m.group(1) == "true"
    name = name_m.group(1) if name_m else "unknown"
    days_old = (TODAY_DT - added_date).days
    
    # Pruning
    should_prune = False
    if spot_count > 60:
        if days_old > 21 and score < 50:
            should_prune = True
        if days_old > 30 and not is_insider:
            should_prune = True
    
    if should_prune and spot_count > 40:
        print(f"  Pruning: {name} (age {days_old}d, score {score})")
        abs_start = hs_start + match.start()
        abs_end = hs_start + match.end()
        after = content[abs_end:abs_end+20]
        before = content[max(0, abs_start-20):abs_start]
        
        if after.lstrip().startswith(','):
            comma_off = after.index(',')
            content = content[:abs_start] + content[abs_end + comma_off + 1:]
        elif before.rstrip().endswith(','):
            pre = content[:abs_start]
            lc = pre.rstrip().rfind(',')
            content = content[:lc] + content[abs_end:]
        else:
            content = content[:abs_start] + content[abs_end:]
        
        pruned += 1
        spot_count -= 1
        hs_start, inf_start = bounds()
        continue
    
    # Decay scores for spots older than 7 days
    if days_old > 7 and score > 5:
        new_score = max(5, score - 5)
        new_block = block.replace(f"trendingScore: {score}", f"trendingScore: {new_score}")
        abs_start = hs_start + match.start()
        abs_end = hs_start + match.end()
        content = content[:abs_start] + new_block + content[abs_end:]
        decayed += 1
        hs_start, inf_start = bounds()
    
    # Unmark isNew for spots older than 14 days
    if days_old > 14 and is_new:
        hs_start, inf_start = bounds()
        hs_section = content[hs_start:inf_start]
        block_match = re.search(re.escape(name_m.group(0)), hs_section)
        if block_match:
            name_pos = hs_start + block_match.start()
            search_zone = content[name_pos:name_pos+500]
            new_match = re.search(r'isNew: true', search_zone)
            if new_match:
                abs_pos = name_pos + new_match.start()
                content = content[:abs_pos] + "isNew: false" + content[abs_pos + len("isNew: true"):]
                unmarked_new += 1
                print(f"  Unmarked isNew: {name} ({days_old}d old)")

hs_start, inf_start = bounds()
final_spot_count = len(re.findall(r'id: "spot-', content[hs_start:inf_start]))
print(f"  Pruned: {pruned}, Decayed: {decayed}, Unmarked isNew: {unmarked_new}")
print(f"  Final hotspot count: {final_spot_count}")

# ════════════════════════════════════════
# STEP 5: UPDATE INFLUENCER PICKS
# ════════════════════════════════════════
print("\n=== UPDATING INFLUENCER PICKS ===")

influencer_updates = {
    "@wooder_ice": {
        "name": "Cherry Blossom Festival Preview",
        "type": "event",
        "neighborhood": "Fairmount Park",
        "quote": "Sakura Weekend is here -- the Cherry Blossom Festival hits Fairmount Park March 28-29. 100 years of cherry trees, live performances, food, and beer gardens. Early bird tickets end today, don't sleep.",
        "date": TODAY,
    },
    "@feedingtimetv": {
        "name": "Manayunk StrEAT Food Festival 2026",
        "type": "event",
        "neighborhood": "Manayunk",
        "quote": "StrEAT Food Festival is back April 19 and it's bigger than ever -- 85+ food trucks on Main Street Manayunk. New family area this year too. Mark your calendars, this is the one.",
        "date": TODAY,
    },
    "@josheatsphilly": {
        "name": "Emilia Fishtown Pasta Night",
        "type": "restaurant",
        "neighborhood": "Fishtown",
        "quote": "Emilia in Fishtown from Greg Vernick is exactly what Frankford Ave needed. Fresh pasta, killer sauces, and that Vernick attention to detail. The cacio e pepe is already in my top 5.",
        "date": TODAY,
    },
    "@thephillyfoodfanatic": {
        "name": "Banshee Late Night Bites",
        "type": "restaurant",
        "neighborhood": "South Street",
        "quote": "Late night at Banshee is elite. The euro-fusion small plates hit different after 10pm -- grilled Kyoto carrot, Barnstable oysters, and the Tropical Contact High cocktail. South Street has a new king.",
        "date": TODAY,
    },
    "@cass_andthecity": {
        "name": "Cherry Blossom Sakura Weekend",
        "type": "event",
        "neighborhood": "Fairmount Park",
        "quote": "Sakura Weekend tomorrow and Sunday! Tea ceremonies, taiko drumming, cosplay fashion show, and the cherry trees are at peak bloom. Fairmount Park is going to be gorgeous.",
        "date": TODAY,
    },
    "@phillyfoodladies": {
        "name": "New Food Hall at 3025",
        "type": "food-hall",
        "neighborhood": "University City",
        "quote": "New food hall alert at 3025 in University City -- multiple vendors, diverse cuisines, and a great casual hangout spot. Perfect for lunch runs or a quick dinner before a show.",
        "date": TODAY,
    },
    "@fueledonphilly": {
        "name": "Adda Kensington Opening",
        "type": "restaurant",
        "neighborhood": "Kensington",
        "quote": "Adda from Unapologetic Foods just opened on Frankford Ave and it's the real deal Indian food. The NYC team behind Michelin-starred Semma brought that same energy to Kensington. Go now before the wait gets crazy.",
        "date": TODAY,
    },
    "@koryaversa": {
        "name": "StrEAT Food Festival Planning",
        "type": "event",
        "neighborhood": "Manayunk",
        "quote": "Philly's biggest food festival is back! StrEAT Food takes over historic Main Street on Sunday, April 19. 70+ of the region's best food trucks. Save the date and come hungry.",
        "date": "2026-03-26",
    },
    "@djour.philly": {
        "name": "Drain at Union Transfer Tonight",
        "type": "event",
        "neighborhood": "Spring Garden",
        "quote": "Drain is hitting Union Transfer tonight with No Pressure, Haywire, and Secret World. Hardcore energy at its finest. If you know, you know -- this one is going to be wild.",
        "date": TODAY,
    },
    "@swagfoodphilly": {
        "name": "Side Eye Queen Village Weekend Visit",
        "type": "restaurant",
        "neighborhood": "Queen Village",
        "quote": "Weekend brunch energy at Side Eye in Queen Village. The Philly French bistro vibes are perfect -- housemade breads, pastries, and that green peppercorn brioche burger with Camembert. Neighborhood gem.",
        "date": TODAY,
    },
}

inf_updates_count = 0
for handle, pick in influencer_updates.items():
    handle_idx = content.find(f'handle: "{handle}"')
    if handle_idx < 0:
        print(f"  Handle not found: {handle}")
        continue
    
    picks_idx = content.find("recentPicks: [", handle_idx)
    if picks_idx < 0 or picks_idx > handle_idx + 2000:
        print(f"  recentPicks not found for {handle}")
        continue
    
    picks_open = picks_idx + len("recentPicks: [")
    
    new_pick = f"""
      {{
        name: "{esc(pick['name'])}",
        type: "{pick['type']}",
        neighborhood: "{pick['neighborhood']}",
        quote: "{esc(pick['quote'])}",
        date: "{pick['date']}",
      }},"""
    
    content = content[:picks_open] + new_pick + content[picks_open:]
    inf_updates_count += 1
    print(f"  Updated {handle}: {pick['name']}")

print(f"  Updated {inf_updates_count} influencers")

# ════════════════════════════════════════
# STEP 6: DEDUPLICATION
# ════════════════════════════════════════
print("\n=== DEDUPLICATION ===")

dupes_found = 0

# Check event names
hs_start, _ = bounds()
ev_names = [n.lower() for n in re.findall(r'name: "([^"]+)"', content[:hs_start])]
seen = set()
for n in ev_names:
    if n in seen:
        dupes_found += 1
        print(f"  Dup event: {n}")
    seen.add(n)

# Check hotspot names
_, inf_start = bounds()
hs_start, _ = bounds()
sp_names = [n.lower() for n in re.findall(r'name: "([^"]+)"', content[hs_start:inf_start])]
seen = set()
for n in sp_names:
    if n in seen:
        dupes_found += 1
        print(f"  Dup hotspot: {n}")
    seen.add(n)

# Check IDs
all_ids = re.findall(r'id: "([^"]+)"', content)
seen_ids = set()
for i in all_ids:
    if i in seen_ids:
        dupes_found += 1
        print(f"  Dup ID: {i}")
    seen_ids.add(i)

if dupes_found == 0:
    print("  No duplicates found")
else:
    print(f"  WARNING: {dupes_found} duplicates detected - removing...")
    # Remove duplicate events by keeping longer descriptions
    hs_start, _ = bounds()
    ev_section = content[:hs_start]
    ev_blocks = re.findall(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', ev_section, re.DOTALL)
    name_map = {}
    for block in ev_blocks:
        nm = re.search(r'name: "([^"]+)"', block)
        if nm:
            key = nm.group(1).lower()
            if key not in name_map:
                name_map[key] = []
            name_map[key].append(block)
    
    for key, blocks in name_map.items():
        if len(blocks) > 1:
            blocks.sort(key=len, reverse=True)
            for dup in blocks[1:]:
                idx = content.find(dup)
                if idx >= 0:
                    end_idx = idx + len(dup)
                    after = content[end_idx:end_idx+20]
                    before = content[max(0,idx-20):idx]
                    if after.lstrip().startswith(','):
                        co = after.index(',')
                        content = content[:idx] + content[end_idx+co+1:]
                    elif before.rstrip().endswith(','):
                        pre = content[:idx]
                        lc = pre.rstrip().rfind(',')
                        content = content[:lc] + content[end_idx:]
                    else:
                        content = content[:idx] + content[end_idx:]
                    print(f"  Removed dup: {key}")

print(f"  Total duplicates processed: {dupes_found}")

# ════════════════════════════════════════
# STEP 7: CLEANUP
# ════════════════════════════════════════
print("\n=== CLEANUP ===")
before_len = len(content)
content = re.sub(r'\n\s*,\s*\n', '\n', content)
content = re.sub(r'\n{3,}', '\n\n', content)
content = re.sub(r',\s*\n(\s*\];)', r'\n\1', content)
after_len = len(content)
print(f"  Cleaned {before_len - after_len} chars")

# ════════════════════════════════════════
# FINAL COUNTS
# ════════════════════════════════════════
final_events = len(re.findall(r'id: "event-', content))
final_spots = len(re.findall(r'id: "spot-', content))
print(f"\n=== FINAL ===")
print(f"  Events: {final_events}")
print(f"  Hotspots: {final_spots}")
print(f"  Past removed: {past_removed}")
print(f"  New events: {events_added}")
print(f"  New hotspots: {spots_added}")
print(f"  Influencers updated: {inf_updates_count}")
print(f"  Pruned: {pruned}")
print(f"  Scores decayed: {decayed}")
print(f"  Duplicates: {dupes_found}")

with open("client/src/data/philly-data.ts", "w") as f:
    f.write(content)

print("\nData file updated!")

# Save summary
summary = {
    "past_events_removed": past_removed,
    "new_events_added": events_added,
    "new_hotspots_added": spots_added,
    "influencers_updated": inf_updates_count,
    "hotspots_pruned": pruned,
    "scores_decayed": decayed,
    "isNew_unmarked": unmarked_new,
    "duplicates_removed": dupes_found,
    "final_events": final_events,
    "final_hotspots": final_spots,
}
with open("/tmp/run10_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
