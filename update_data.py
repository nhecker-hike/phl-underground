#!/usr/bin/env python3
"""
PHL Underground Nightly Data Refresh #9
- Add new events (not already in data)
- Remove past events
- Add new hotspots (not already in data)
- Run hotspot lifecycle management
- Update influencer recentPicks
- Deduplicate all entries
"""

import re
import json
from datetime import datetime, timedelta

TODAY = "2026-03-26"
TODAY_DT = datetime.strptime(TODAY, "%Y-%m-%d")
NEXT_EVENT_ID = 131
NEXT_SPOT_ID = 85

with open("client/src/data/philly-data.ts", "r") as f:
    content = f.read()

# ── Helper: get existing names (case-insensitive) ──
def get_existing_names(section_content):
    return set(n.lower() for n in re.findall(r'name: "([^"]+)"', section_content))

# ── Section boundaries ──
ev_start = content.find("export const events")
hs_start = content.find("export const hotspots")
inf_start = content.find("export const influencers")

events_section = content[ev_start:hs_start]
hotspots_section = content[hs_start:inf_start]
influencers_section = content[inf_start:]

existing_event_names = get_existing_names(events_section)
existing_hotspot_names = get_existing_names(hotspots_section)

print(f"Current events: {len(re.findall(r'id: \"event-', events_section))}")
print(f"Current hotspots: {len(re.findall(r'id: \"spot-', hotspots_section))}")
print(f"Existing event names: {len(existing_event_names)}")
print(f"Existing hotspot names: {len(existing_hotspot_names)}")

# ══════════════════════════════════════════════
# 1. NEW EVENTS TO ADD
# ══════════════════════════════════════════════
new_events = [
    {
        "name": "Lily Allen at The Met",
        "date": "2026-04-17",
        "time": "8:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N Broad St, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "London-native Lily Allen brings her critically acclaimed album West End Girl to The Met. The pop star channels her life story into her biggest tour yet, performing the full album live.",
        "price": "$45+",
        "vibeTag": "trending",
        "source": "visitphilly.com",
        "lat": 39.9726,
        "lng": -75.1590,
        "isInsider": False,
    },
    {
        "name": "Monster Jam at Lincoln Financial Field",
        "date": "2026-04-18",
        "time": "7:00 PM",
        "venue": "Lincoln Financial Field",
        "address": "1 Lincoln Financial Field Way, Philadelphia, PA 19148",
        "neighborhood": "South Philly Sports Complex",
        "category": "sports",
        "description": "Monster trucks take over the Linc for one explosive night. Watch massive trucks like Grave Digger and El Toro Loco crush cars and pull off insane stunts in the stadium.",
        "price": "$30+",
        "vibeTag": "family-friendly",
        "source": "lincolnfinancialfield.com",
        "lat": 39.9008,
        "lng": -75.1675,
        "isInsider": False,
    },
    {
        "name": "Sleepers Awake at Academy of Music",
        "date": "2026-04-22 to 2026-04-26",
        "time": "Various",
        "venue": "Academy of Music",
        "address": "240 S Broad St, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "performing-arts",
        "description": "A multi-night performance series at the stunning Academy of Music featuring orchestral works and contemporary compositions. An immersive classical music experience in one of America's most beautiful concert halls.",
        "price": "$30+",
        "vibeTag": "after-dark",
        "source": "ensembleartsphilly.org",
        "lat": 39.9470,
        "lng": -75.1653,
        "isInsider": True,
    },
    {
        "name": "KPop Flea Market",
        "date": "2026-04-11",
        "time": "10:00 AM",
        "venue": "Various",
        "address": "Philadelphia, PA",
        "neighborhood": "Center City",
        "category": "market",
        "description": "KPop fans unite at this flea market featuring photocards, albums, merch, fan art, and more from your favorite groups. A niche pop culture marketplace that draws collectors from across the region.",
        "price": "Free entry",
        "vibeTag": "underground",
        "source": "phillyfestivals.org",
        "lat": 39.9530,
        "lng": -75.1630,
        "isInsider": True,
    },
    {
        "name": "Punk Rock Flea Market",
        "date": "2026-04-17 to 2026-04-19",
        "time": "10:00 AM",
        "venue": "Various",
        "address": "Philadelphia, PA",
        "neighborhood": "Fishtown",
        "category": "market",
        "description": "The legendary Punk Rock Flea Market returns with three days of vintage finds, handmade goods, vinyl records, zines, art prints, and DIY everything. Vendors from across the Northeast bring the best of punk and alternative culture.",
        "price": "Free entry",
        "vibeTag": "underground",
        "source": "phillyfestivals.org",
        "lat": 39.9740,
        "lng": -75.1350,
        "isInsider": True,
    },
    {
        "name": "SpringFest Philadelphia",
        "date": "2026-04-17 to 2026-04-23",
        "time": "Various",
        "venue": "Various Locations",
        "address": "Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "festival",
        "description": "A week-long celebration of spring across Philadelphia featuring outdoor events, pop-up markets, live music, food vendors, and community gatherings at parks and plazas throughout the city.",
        "price": "Free - Varies",
        "vibeTag": "trending",
        "source": "phillyfestivals.org",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": False,
    },
    {
        "name": "Penn Relays at Franklin Field",
        "date": "2026-04-23 to 2026-04-25",
        "time": "9:00 AM",
        "venue": "Franklin Field",
        "address": "235 S 33rd St, Philadelphia, PA 19104",
        "neighborhood": "University City",
        "category": "sports",
        "description": "The oldest and largest track and field competition in the United States returns to Penn's historic Franklin Field. Three days of elite athletes, high school stars, and college competitors in America's greatest relay carnival.",
        "price": "$15+",
        "vibeTag": "local-favorite",
        "source": "phillyfestivals.org",
        "lat": 39.9502,
        "lng": -75.1930,
        "isInsider": False,
    },
    {
        "name": "Philly Black Pride",
        "date": "2026-04-23 to 2026-04-26",
        "time": "Various",
        "venue": "Various Locations",
        "address": "Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "cultural",
        "description": "Philadelphia's annual celebration of Black LGBTQ+ culture with four days of parties, panels, performances, and community events. One of the largest Black Pride celebrations on the East Coast.",
        "price": "Free - Varies",
        "vibeTag": "underground",
        "source": "phillyfestivals.org",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": True,
    },
    {
        "name": "Greater Philadelphia Cheesesteak Festival",
        "date": "2026-04-26",
        "time": "11:00 AM",
        "venue": "Dilworth Park",
        "address": "1 S 15th St, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "food",
        "description": "The ultimate showdown of Philly's most iconic food. Local cheesesteak shops compete for bragging rights while you taste your way through the city's best offerings. Live music, beer gardens, and all the whiz you can handle.",
        "price": "$20+",
        "vibeTag": "local-favorite",
        "source": "phillyfestivals.org",
        "lat": 39.9527,
        "lng": -75.1653,
        "isInsider": False,
    },
    {
        "name": "Fairmount Arts Crawl",
        "date": "2026-04-26",
        "time": "12:00 PM",
        "venue": "Fairmount Avenue",
        "address": "Fairmount Ave, Philadelphia, PA",
        "neighborhood": "Fairmount",
        "category": "art",
        "description": "A neighborhood-wide arts crawl along Fairmount Avenue featuring open studios, gallery exhibitions, live art demos, pop-up shops, and street performances. The perfect Sunday afternoon exploring one of Philly's most charming neighborhoods.",
        "price": "Free",
        "vibeTag": "underground",
        "source": "phillyfestivals.org",
        "lat": 39.9657,
        "lng": -75.1700,
        "isInsider": True,
    },
    {
        "name": "Booze Fest Philadelphia",
        "date": "2026-04-26",
        "time": "1:00 PM",
        "venue": "Various Locations",
        "address": "Philadelphia, PA",
        "neighborhood": "Center City",
        "category": "food",
        "description": "An adults-only festival celebrating craft cocktails, local distilleries, and mixology. Sample specialty drinks from Philly's best bars and discover new spirits from regional distillers.",
        "price": "$40+",
        "vibeTag": "after-dark",
        "source": "phillyfestivals.org",
        "lat": 39.9500,
        "lng": -75.1630,
        "isInsider": True,
    },
    {
        "name": "Good Kid at The Fillmore — Can We Hang Out? Tour",
        "date": "2026-04-20",
        "time": "8:00 PM",
        "venue": "The Fillmore Philadelphia",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Toronto indie-rock band Good Kid brings their infectious, high-energy live show to The Fillmore on their Can We Hang Out? Tour. Known for viral TikTok hits and a dedicated fanbase, this is one of the buzziest up-and-coming bands on the scene.",
        "price": "$25+",
        "vibeTag": "trending",
        "source": "thefillmorephilly.com",
        "lat": 39.9680,
        "lng": -75.1340,
        "isInsider": False,
    },
    {
        "name": "David & Tamela Mann at The Met",
        "date": "2026-04-26",
        "time": "8:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N Broad St, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "Gospel power couple David and Tamela Mann bring their Love & Relationship tour to The Met. An evening of faith, storytelling, and soul-stirring performances featuring hits like Take Me to the King.",
        "price": "$50+",
        "vibeTag": "local-favorite",
        "source": "themetphilly.com",
        "lat": 39.9726,
        "lng": -75.1590,
        "isInsider": False,
    },
    {
        "name": "Market East Pop-Up Block — Philly 250",
        "date": "2026-05-01 to 2026-09-30",
        "time": "Various",
        "venue": "900 Block of Market Street",
        "address": "900 Market St, Philadelphia, PA 19107",
        "neighborhood": "Center City East",
        "category": "market",
        "description": "Eight new pop-up businesses are taking over vacant storefronts on Market East ahead of the FIFA World Cup and Philly 250 celebrations. All small, homegrown, diverse local businesses — expect unique food, retail, and experiences.",
        "price": "Free entry",
        "vibeTag": "underground",
        "source": "inquirer.com",
        "lat": 39.9514,
        "lng": -75.1540,
        "isInsider": True,
    },
    {
        "name": "Open Streets: West Walnut — Sundays",
        "date": "2026-04-05 to 2026-05-17",
        "time": "8:00 AM - 1:00 PM",
        "venue": "West Walnut Street",
        "address": "Walnut St, Philadelphia, PA",
        "neighborhood": "West Philadelphia",
        "category": "outdoor",
        "description": "Every Sunday, car-free streets come alive with walkers, joggers, cyclists, and neighbors. West Walnut transforms into a community promenade with pop-up fitness classes, street vendors, and good vibes.",
        "price": "Free",
        "vibeTag": "local-favorite",
        "source": "phillyfestivals.org",
        "lat": 39.9528,
        "lng": -75.2050,
        "isInsider": True,
    },
]

# ══════════════════════════════════════════════
# 2. NEW HOTSPOTS TO ADD
# ══════════════════════════════════════════════
new_hotspots = [
    {
        "name": "Rhythm & Spirits",
        "type": "Restaurant / Bar",
        "address": "Center City, Philadelphia, PA",
        "neighborhood": "Center City",
        "description": "A vibrant Italian-Spanish fusion restaurant with live music nightly. The cocktail program pulls from Mediterranean influences while DJs and live bands keep the energy up after dinner service.",
        "vibeTag": "after-dark",
        "priceRange": "$$$",
        "cuisine": "Italian-Spanish Fusion",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9520,
        "lng": -75.1650,
        "source": "phillymag.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Scusi Pizza",
        "type": "Restaurant",
        "address": "Northern Liberties, Philadelphia, PA",
        "neighborhood": "Northern Liberties",
        "description": "Michelin-starred chef's casual pizza joint serving Neapolitan-style pies with premium toppings and house-made mozzarella. A low-key neighborhood spot that punches way above its weight class.",
        "vibeTag": "local-favorite",
        "priceRange": "$$",
        "cuisine": "Pizza / Italian",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9650,
        "lng": -75.1430,
        "source": "phillymag.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Sweet 4",
        "type": "Bar / Dessert",
        "address": "Kensington, Philadelphia, PA",
        "neighborhood": "Kensington",
        "description": "Part ice cream shop, part DJ-driven nightlife spot. By day it's chill scoops and sundaes; by night it transforms into a vibes-heavy lounge with guest DJs and themed party nights. A true Kensington original.",
        "vibeTag": "underground",
        "priceRange": "$$",
        "cuisine": "Desserts / Cocktails",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9780,
        "lng": -75.1280,
        "source": "phillymag.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Casa Oui",
        "type": "Cafe / Restaurant",
        "address": "705 S 5th St, Philadelphia, PA 19147",
        "neighborhood": "Queen Village",
        "description": "An all-day cafe bridging French and Mexican flavors. Mornings bring pastries, beignets, and breakfast sandwiches; evenings shift to steak, ceviche, and cocktails. A cozy corner spot with serious culinary range.",
        "vibeTag": "trending",
        "priceRange": "$$",
        "cuisine": "French-Mexican Fusion",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9401,
        "lng": -75.1490,
        "source": "visitphilly.com",
        "addedDate": TODAY,
        "trendingScore": 60,
    },
    {
        "name": "Poison Heart",
        "type": "Bar",
        "address": "931 Spring Garden St, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "description": "The best post-show bar on Spring Garden. Neon-lit, punk-influenced cocktail den with glowing lights, rum-heavy drinks, and free herbs de Provence popcorn. An 80s pop-punk band designed a bar — this is what you get.",
        "vibeTag": "underground",
        "priceRange": "$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 39.9613,
        "lng": -75.1540,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Grace & Proper",
        "type": "Bar",
        "address": "941 S 8th St, Philadelphia, PA 19147",
        "neighborhood": "Bella Vista",
        "description": "A tiny Portuguese-ish corner bar with paint-chipped ceilings and chalkboard menus. So small you'll graze elbows with strangers. Cava, potato chips with salami, and a crowd that gets rowdier the later it gets. Pure neighborhood vibes.",
        "vibeTag": "underground",
        "priceRange": "$",
        "cuisine": "Portuguese Tapas",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9388,
        "lng": -75.1570,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
]

# ══════════════════════════════════════════════
# 3. INFLUENCER UPDATES
# ══════════════════════════════════════════════
influencer_updates = {
    "@wooder_ice": {
        "name": "Wooder Ice x Philly 250",
        "type": "culture",
        "neighborhood": "Citywide",
        "quote": "Philly 250 is bringing the heat this spring. Pop-ups on Market East, new restaurants everywhere, and the city is buzzing before FIFA rolls in. This summer is going to be legendary.",
        "date": "2026-03-25",
    },
    "@josheatsphilly": {
        "name": "Side Eye Restaurant Review",
        "type": "restaurant",
        "neighborhood": "Queen Village",
        "quote": "Side Eye is the real deal — Philly French bistro vibes with a green peppercorn burger that slaps. The beef tartare is chef's kiss. Queen Village just got a serious upgrade.",
        "date": "2026-03-25",
    },
    "@fueledonphilly": {
        "name": "Pine Street Grill First Look",
        "type": "restaurant",
        "neighborhood": "Fitler Square",
        "quote": "The Her Supper Club team opened Pine Street Grill in Fitler Square and it's already a neighborhood staple. Michelin-quality cooking in a chill grill setting. Don't sleep on this one.",
        "date": "2026-03-24",
    },
    "@koryaversa": {
        "name": "R&B Only Live at The Fillmore",
        "type": "event",
        "neighborhood": "Fishtown",
        "quote": "R&B Only Live is coming to The Fillmore April 4th. If you know, you know — the best R&B party in the country is hitting Philly and tickets are going fast.",
        "date": "2026-03-24",
    },
    "@feedingtimetv": {
        "name": "Mi Vida Center City Tour",
        "type": "restaurant",
        "neighborhood": "Center City",
        "quote": "Mi Vida just opened on Ludlow and it's gorgeous. James Beard chef Roberto Santibañez brought his DC hit to Philly with upscale Mexican food in an enchanted forest setting. The moles are unreal.",
        "date": "2026-03-25",
    },
    "@thephillyfoodfanatic": {
        "name": "Piccolina Old City Date Night",
        "type": "restaurant",
        "neighborhood": "Old City",
        "quote": "Piccolina in Old City is your new date night spot. Oysters, housemade pasta, Neapolitan pizza — plus an all-Italian wine list and killer Negroni menu. South Philly roots, Old City vibes.",
        "date": "2026-03-24",
    },
    "@phillyfoodladies": {
        "name": "Casa Oui Brunch Spot",
        "type": "restaurant",
        "neighborhood": "Queen Village",
        "quote": "Casa Oui is doing French-Mexican all day and we are here for it. Beignets for breakfast, steak for dinner, and the Casa Oui Burger is already in our top 5. Queen Village keeps winning.",
        "date": "2026-03-25",
    },
    "@djour.philly": {
        "name": "Southeast Asian Market Opening",
        "type": "event",
        "neighborhood": "South Philly",
        "quote": "The Southeast Asian Market opens at FDR Park April 4th — fresh produce, street food vendors, and authentic Southeast Asian goods. This is going to be a weekly must-visit all spring and summer.",
        "date": "2026-03-25",
    },
    "@swagfoodphilly": {
        "name": "Banshee on South Street",
        "type": "restaurant",
        "neighborhood": "South Street",
        "quote": "Banshee from the Cheu Noodle Bar guys is Euro-fusion on South Street and it hits different. Spanish mackerel, roast chicken, and the Tropical Contact High cocktail is fire. New go-to.",
        "date": "2026-03-24",
    },
    "@cass_andthecity": {
        "name": "PHS Pop-Up Garden Manayunk Opening",
        "type": "event",
        "neighborhood": "Manayunk",
        "quote": "PHS Pop-Up Gardens are officially open for the season in Manayunk and South Street. Spring drinks, live music, string lights — Philly's favorite outdoor hangs are back.",
        "date": "2026-03-25",
    },
}

# ══════════════════════════════════════════════
# STEP 1: REMOVE PAST EVENTS
# ══════════════════════════════════════════════
print("\n=== REMOVING PAST EVENTS ===")

# Find and remove events with dates before today
# We need to find each event block and check its date
event_blocks = re.findall(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', events_section, re.DOTALL)
past_removed = 0
for block in event_blocks:
    date_match = re.search(r'date: "(\d{4}-\d{2}-\d{2})"', block)
    if date_match:
        event_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        if event_date < TODAY_DT:
            name_match = re.search(r'name: "([^"]+)"', block)
            name = name_match.group(1) if name_match else "unknown"
            print(f"  Removing past event: {name} ({date_match.group(1)})")
            # Remove the block plus trailing comma/whitespace
            # Find and remove more carefully to avoid leaving bare commas
            idx = content.find(block)
            if idx >= 0:
                # Check for trailing comma and whitespace
                end_idx = idx + len(block)
                after = content[end_idx:end_idx+20]
                if after.lstrip().startswith(','):
                    # Remove block + comma
                    comma_offset = after.index(',')
                    content = content[:idx] + content[end_idx + comma_offset + 1:]
                elif content[idx-5:idx].rstrip().endswith(','):
                    # Remove preceding comma + block
                    pre = content[:idx]
                    last_comma = pre.rstrip().rfind(',')
                    content = content[:last_comma] + content[end_idx:]
                else:
                    content = content[:idx] + content[end_idx:]
                past_removed += 1

print(f"  Removed {past_removed} past events")

# ══════════════════════════════════════════════
# STEP 2: ADD NEW EVENTS
# ══════════════════════════════════════════════
print("\n=== ADDING NEW EVENTS ===")

# Refresh existing names after removals
ev_end = content.find("export const hotspots")
existing_event_names = get_existing_names(content[:ev_end])

events_added = 0
event_id = NEXT_EVENT_ID

# Find insertion point (before the closing ];)
events_end_marker = content[:content.find("export const hotspots")].rfind("},")
if events_end_marker < 0:
    events_end_marker = content[:content.find("export const hotspots")].rfind("}")

insert_after = events_end_marker + 2  # after "},"

new_event_entries = []
for ev in new_events:
    if ev["name"].lower() in existing_event_names:
        print(f"  Skipping duplicate event: {ev['name']}")
        continue
    
    escaped_name = ev["name"].replace("'", "\\'").replace('"', '\\"')
    escaped_desc = ev["description"].replace("'", "\\'").replace('"', '\\"')
    
    entry = f"""  {{
    id: "event-{event_id}",
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
    isInsider: {"true" if ev["isInsider"] else "false"},
  }}"""
    new_event_entries.append(entry)
    existing_event_names.add(ev["name"].lower())
    events_added += 1
    event_id += 1
    print(f"  Adding event: {ev['name']}")

if new_event_entries:
    # Find the last }; of events array before hotspots
    hs_marker = content.find("export const hotspots")
    events_closing = content[:hs_marker].rfind("];")
    last_brace = content[:events_closing].rfind("}")
    
    # Insert new events after last entry
    insertion = ",\n" + ",\n".join(new_event_entries) + ",\n"
    content = content[:last_brace+1] + insertion + content[last_brace+1:]

print(f"  Added {events_added} new events")

# ══════════════════════════════════════════════
# STEP 3: ADD NEW HOTSPOTS
# ══════════════════════════════════════════════
print("\n=== ADDING NEW HOTSPOTS ===")

# Refresh section boundaries
hs_start = content.find("export const hotspots")
inf_start = content.find("export const influencers")
existing_hotspot_names = get_existing_names(content[hs_start:inf_start])

spots_added = 0
spot_id = NEXT_SPOT_ID

new_spot_entries = []
for spot in new_hotspots:
    if spot["name"].lower() in existing_hotspot_names:
        print(f"  Skipping duplicate hotspot: {spot['name']}")
        continue
    
    escaped_name = spot["name"].replace("'", "\\'").replace('"', '\\"')
    escaped_desc = spot["description"].replace("'", "\\'").replace('"', '\\"')
    cuisine_val = f'"{spot["cuisine"]}"' if spot["cuisine"] else "null"
    
    entry = f"""  {{
    id: "spot-{spot_id}",
    name: "{escaped_name}",
    type: "{spot['type']}",
    address: "{spot['address']}",
    neighborhood: "{spot['neighborhood']}",
    description: "{escaped_desc}",
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
    spot_id += 1
    print(f"  Adding hotspot: {spot['name']}")

if new_spot_entries:
    # Find the last }; of hotspots array before influencers
    inf_marker = content.find("export const influencers")
    hotspots_closing = content[:inf_marker].rfind("];")
    last_brace = content[:hotspots_closing].rfind("}")
    
    insertion = ",\n" + ",\n".join(new_spot_entries) + ",\n"
    content = content[:last_brace+1] + insertion + content[last_brace+1:]

print(f"  Added {spots_added} new hotspots")

# ══════════════════════════════════════════════
# STEP 4: HOTSPOT LIFECYCLE MANAGEMENT
# ══════════════════════════════════════════════
print("\n=== HOTSPOT LIFECYCLE MANAGEMENT ===")

# Refresh boundaries
hs_start = content.find("export const hotspots")
inf_start = content.find("export const influencers")
hs_section = content[hs_start:inf_start]

# Count hotspots
spot_count = len(re.findall(r'id: "spot-', hs_section))
print(f"  Total hotspots before lifecycle: {spot_count}")

# Find all hotspot blocks with their addedDate and trendingScore
spot_blocks = list(re.finditer(
    r'(\{[^{}]*?id: "spot-\d+"[^{}]*?\})',
    hs_section, re.DOTALL
))

pruned = 0
decayed = 0
unmarked_new = 0

for match in reversed(spot_blocks):  # reverse to not mess up indices
    block = match.group(1)
    
    # Extract fields
    added_match = re.search(r'addedDate: "(\d{4}-\d{2}-\d{2})"', block)
    score_match = re.search(r'trendingScore: (\d+)', block)
    insider_match = re.search(r'isInsider: (true|false)', block)
    is_new_match = re.search(r'isNew: (true|false)', block)
    name_match = re.search(r'name: "([^"]+)"', block)
    
    if not added_match or not score_match:
        continue
    
    added_date = datetime.strptime(added_match.group(1), "%Y-%m-%d")
    score = int(score_match.group(1))
    is_insider = insider_match and insider_match.group(1) == "true"
    is_new = is_new_match and is_new_match.group(1) == "true"
    name = name_match.group(1) if name_match else "unknown"
    days_old = (TODAY_DT - added_date).days
    
    # Pruning rules (only if over 60 total)
    should_prune = False
    if spot_count > 60:
        if days_old > 21 and score < 50:
            should_prune = True
        if days_old > 30 and not is_insider:
            should_prune = True
    
    if should_prune and spot_count > 40:
        print(f"  Pruning: {name} (added {added_match.group(1)}, score {score}, {days_old} days old)")
        # Find this block in the full content and remove it
        abs_start = hs_start + match.start()
        abs_end = hs_start + match.end()
        
        # Handle comma before or after
        after = content[abs_end:abs_end+20]
        before = content[max(0,abs_start-20):abs_start]
        
        if after.lstrip().startswith(','):
            comma_offset = after.index(',')
            content = content[:abs_start] + content[abs_end + comma_offset + 1:]
        elif before.rstrip().endswith(','):
            pre = content[:abs_start]
            last_comma = pre.rstrip().rfind(',')
            content = content[:last_comma] + content[abs_end:]
        else:
            content = content[:abs_start] + content[abs_end:]
        
        pruned += 1
        spot_count -= 1
        
        # Refresh section boundaries after each removal
        hs_start = content.find("export const hotspots")
        inf_start = content.find("export const influencers")
        continue
    
    # Decay scores for spots older than 7 days
    if days_old > 7 and score > 5:
        new_score = max(5, score - 5)
        new_block = block.replace(f"trendingScore: {score}", f"trendingScore: {new_score}")
        abs_start = hs_start + match.start()
        abs_end = hs_start + match.end()
        content = content[:abs_start] + new_block + content[abs_end:]
        decayed += 1
        
        # Refresh section boundaries
        hs_start = content.find("export const hotspots")
        inf_start = content.find("export const influencers")
    
    # Set isNew: false for spots older than 14 days
    if days_old > 14 and is_new:
        hs_start = content.find("export const hotspots")
        inf_start = content.find("export const influencers")
        hs_section = content[hs_start:inf_start]
        
        # Re-find the block in updated content
        block_match = re.search(re.escape(name_match.group(0)), hs_section)
        if block_match:
            # Find the isNew: true near this name
            name_pos = hs_start + block_match.start()
            # Search within ~500 chars after name
            search_zone = content[name_pos:name_pos+500]
            new_match = re.search(r'isNew: true', search_zone)
            if new_match:
                abs_pos = name_pos + new_match.start()
                content = content[:abs_pos] + "isNew: false" + content[abs_pos + len("isNew: true"):]
                unmarked_new += 1
                print(f"  Unmarked isNew: {name} ({days_old} days old)")

print(f"  Pruned: {pruned} hotspots")
print(f"  Decayed scores: {decayed} hotspots")
print(f"  Unmarked isNew: {unmarked_new} hotspots")

# Refresh final count
hs_start = content.find("export const hotspots")
inf_start = content.find("export const influencers")
final_spot_count = len(re.findall(r'id: "spot-', content[hs_start:inf_start]))
print(f"  Final hotspot count: {final_spot_count}")

# ══════════════════════════════════════════════
# STEP 5: UPDATE INFLUENCER RECENT PICKS
# ══════════════════════════════════════════════
print("\n=== UPDATING INFLUENCER PICKS ===")

influencer_updates_count = 0
for handle, pick in influencer_updates.items():
    # Find the influencer's recentPicks array
    handle_idx = content.find(f'handle: "{handle}"')
    if handle_idx < 0:
        print(f"  Handle not found: {handle}")
        continue
    
    picks_idx = content.find("recentPicks: [", handle_idx)
    if picks_idx < 0 or picks_idx > handle_idx + 2000:
        print(f"  recentPicks not found for {handle}")
        continue
    
    # Insert new pick at the beginning of the array
    picks_open = picks_idx + len("recentPicks: [")
    
    escaped_name = pick["name"].replace('"', '\\"')
    escaped_quote = pick["quote"].replace('"', '\\"')
    
    new_pick = f"""
      {{
        name: "{escaped_name}",
        type: "{pick['type']}",
        neighborhood: "{pick['neighborhood']}",
        quote: "{escaped_quote}",
        date: "{pick['date']}",
      }},"""
    
    content = content[:picks_open] + new_pick + content[picks_open:]
    influencer_updates_count += 1
    print(f"  Updated {handle}: {pick['name']}")

print(f"  Updated {influencer_updates_count} influencers")

# ══════════════════════════════════════════════
# STEP 6: DEDUPLICATION
# ══════════════════════════════════════════════
print("\n=== DEDUPLICATION ===")

# Check for duplicate event names
ev_end = content.find("export const hotspots")
ev_section = content[:ev_end]
event_names = re.findall(r'name: "([^"]+)"', ev_section)
event_name_lower = [n.lower() for n in event_names]

dupes_found = 0
seen = set()
for name in event_name_lower:
    if name in seen:
        dupes_found += 1
        print(f"  Duplicate event found: {name}")
    seen.add(name)

# Check for duplicate hotspot names
hs_start = content.find("export const hotspots")
inf_start = content.find("export const influencers")
hs_section = content[hs_start:inf_start]
spot_names = re.findall(r'name: "([^"]+)"', hs_section)
spot_name_lower = [n.lower() for n in spot_names]

seen = set()
for name in spot_name_lower:
    if name in seen:
        dupes_found += 1
        print(f"  Duplicate hotspot found: {name}")
    seen.add(name)

# Check for duplicate IDs
all_ids = re.findall(r'id: "([^"]+)"', content)
seen_ids = set()
for id_val in all_ids:
    if id_val in seen_ids:
        dupes_found += 1
        print(f"  Duplicate ID found: {id_val}")
    seen_ids.add(id_val)

if dupes_found == 0:
    print("  No duplicates found!")
else:
    print(f"  Found {dupes_found} duplicates - removing...")
    # Remove duplicate events (keep the one with longer description)
    # Process events
    ev_section = content[:content.find("export const hotspots")]
    event_blocks = re.findall(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', ev_section, re.DOTALL)
    
    name_to_blocks = {}
    for block in event_blocks:
        name_match = re.search(r'name: "([^"]+)"', block)
        if name_match:
            name = name_match.group(1).lower()
            if name not in name_to_blocks:
                name_to_blocks[name] = []
            name_to_blocks[name].append(block)
    
    for name, blocks in name_to_blocks.items():
        if len(blocks) > 1:
            # Keep the longest (most detailed)
            blocks.sort(key=len, reverse=True)
            for dup_block in blocks[1:]:
                idx = content.find(dup_block)
                if idx >= 0:
                    end_idx = idx + len(dup_block)
                    after = content[end_idx:end_idx+20]
                    before = content[max(0,idx-20):idx]
                    if after.lstrip().startswith(','):
                        comma_offset = after.index(',')
                        content = content[:idx] + content[end_idx + comma_offset + 1:]
                    elif before.rstrip().endswith(','):
                        pre = content[:idx]
                        last_comma = pre.rstrip().rfind(',')
                        content = content[:last_comma] + content[end_idx:]
                    else:
                        content = content[:idx] + content[end_idx:]
                    print(f"  Removed duplicate: {name}")

print(f"  Deduplication complete. Duplicates removed: {dupes_found}")

# ══════════════════════════════════════════════
# STEP 7: CLEAN UP bare commas and formatting
# ══════════════════════════════════════════════
print("\n=== CLEANUP ===")

# Remove any bare commas on their own line (creates undefined entries)
before_len = len(content)
content = re.sub(r'\n\s*,\s*\n', '\n', content)
# Remove double blank lines
content = re.sub(r'\n{3,}', '\n\n', content)
# Remove trailing commas before ]
content = re.sub(r',\s*\n(\s*\];)', r'\n\1', content)
after_len = len(content)
print(f"  Cleanup: removed {before_len - after_len} chars of formatting artifacts")

# ══════════════════════════════════════════════
# FINAL COUNTS
# ══════════════════════════════════════════════
final_events = len(re.findall(r'id: "event-', content))
final_spots = len(re.findall(r'id: "spot-', content))
print(f"\n=== FINAL COUNTS ===")
print(f"  Events: {final_events}")
print(f"  Hotspots: {final_spots}")
print(f"  Past events removed: {past_removed}")
print(f"  New events added: {events_added}")
print(f"  New hotspots added: {spots_added}")
print(f"  Influencers updated: {influencer_updates_count}")
print(f"  Hotspots pruned: {pruned}")
print(f"  Scores decayed: {decayed}")
print(f"  Duplicates removed: {dupes_found}")

# Write the updated file
with open("client/src/data/philly-data.ts", "w") as f:
    f.write(content)

print("\n✅ Data file updated successfully!")

# Save summary for notification
summary = {
    "past_events_removed": past_removed,
    "new_events_added": events_added,
    "new_hotspots_added": spots_added,
    "influencers_updated": influencer_updates_count,
    "hotspots_pruned": pruned,
    "scores_decayed": decayed,
    "isNew_unmarked": unmarked_new,
    "duplicates_removed": dupes_found,
    "final_events": final_events,
    "final_hotspots": final_spots,
}
with open("/tmp/update_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
