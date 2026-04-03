#!/usr/bin/env python3
"""
PHL Underground Weekly Data Refresh #12 (2026-04-03)
First weekly run - bigger update since last push was Mar 28.
"""
import re, json
from datetime import datetime

TODAY = "2026-04-03"
TODAY_DT = datetime.strptime(TODAY, "%Y-%m-%d")

with open("client/src/data/philly-data.ts", "r") as f:
    content = f.read()

def get_names(sec): return set(n.lower() for n in re.findall(r'name: "([^"]+)"', sec))
def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"')
def bounds(): return content.find("export const hotspots"), content.find("export const influencers")

hs_start, inf_start = bounds()
ev_ids = [int(x) for x in re.findall(r'id: "event-(\d+)"', content)]
sp_ids = [int(x) for x in re.findall(r'id: "spot-(\d+)"', content)]
next_eid = max(ev_ids) + 1
next_sid = max(sp_ids) + 1
print(f"Start: {len(ev_ids)} events (max event-{max(ev_ids)}), {len(sp_ids)} hotspots (max spot-{max(sp_ids)})")

# ══════════════════════════════════════
# STEP 1: REMOVE PAST EVENTS
# ══════════════════════════════════════
print("\n=== REMOVING PAST EVENTS ===")
hs_start, _ = bounds()
ev_sec = content[:hs_start]
blocks = list(re.finditer(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', ev_sec, re.DOTALL))
past_removed = 0

for m in reversed(blocks):
    b = m.group(1)
    dm = re.search(r'date: "(\d{4}-\d{2}-\d{2})"', b)
    if dm and datetime.strptime(dm.group(1), "%Y-%m-%d") < TODAY_DT:
        nm = re.search(r'name: "([^"]+)"', b)
        print(f"  Removing: {nm.group(1) if nm else '?'} ({dm.group(1)})")
        s, e = m.start(), m.end()
        after = ev_sec[e:e+20]; before = ev_sec[max(0,s-20):s]
        if after.lstrip().startswith(','):
            ev_sec = ev_sec[:s] + ev_sec[e + after.index(',') + 1:]
        elif before.rstrip().endswith(','):
            lc = ev_sec[:s].rstrip().rfind(',')
            ev_sec = ev_sec[:lc] + ev_sec[e:]
        else:
            ev_sec = ev_sec[:s] + ev_sec[e:]
        past_removed += 1

content = ev_sec + content[hs_start:]
print(f"  Removed {past_removed} past events")

# ══════════════════════════════════════
# STEP 2: ADD NEW EVENTS
# ══════════════════════════════════════
print("\n=== ADDING NEW EVENTS ===")
hs_start, _ = bounds()
existing_ev = get_names(content[:hs_start])

new_events = [
    {
        "name": "The Old 97s at Underground Arts",
        "date": "2026-04-03",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19107",
        "neighborhood": "Callowhill",
        "category": "concert",
        "description": "Alt-country legends The Old 97s bring their sharp songwriting and rowdy live energy to Underground Arts. Two decades of Texas twang meets punk rock spirit in one of Philly's best mid-size rooms.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9583, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "Sports. at Underground Arts",
        "date": "2026-04-04",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19107",
        "neighborhood": "Callowhill",
        "category": "concert",
        "description": "Portland dream-pop band Sports. delivers shimmering, reverb-drenched grooves at Underground Arts. A laid-back, feel-good Saturday night show perfect for indie heads.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9583, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "Robert Plant with Saving Grace at The Met",
        "date": "2026-04-04",
        "time": "7:30 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N Broad St, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "Led Zeppelin legend Robert Plant and his band Saving Grace perform an intimate evening of Americana, folk, and roots music at the gorgeous Met Philadelphia. A once-in-a-lifetime show from a rock icon in an acoustic setting.",
        "price": "$75+",
        "vibeTag": "trending",
        "source": "visitphilly.com",
        "lat": 39.9726, "lng": -75.1590,
        "isInsider": False,
    },
    {
        "name": "Thievery Corporation at Franklin Music Hall",
        "date": "2026-04-04",
        "time": "8:00 PM",
        "venue": "Franklin Music Hall",
        "address": "421 N 7th St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "concert",
        "description": "Electronic/world music pioneers Thievery Corporation bring their eclectic, groove-heavy DJ set to Franklin Music Hall. Downtempo beats, bossa nova, and dub reggae -- a vibe-heavy Saturday night.",
        "price": "$40+",
        "vibeTag": "after-dark",
        "source": "concertfix.com",
        "lat": 39.9618, "lng": -75.1480,
        "isInsider": False,
    },
    {
        "name": "Circle Jerks & Gorilla Biscuits at TLA",
        "date": "2026-04-04",
        "time": "8:00 PM",
        "venue": "Theatre of Living Arts",
        "address": "334 South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "concert",
        "description": "Hardcore punk legends Circle Jerks and Gorilla Biscuits co-headline the TLA. A rare double bill of 80s punk royalty -- expect mosh pits, crowd surfs, and absolute chaos. Essential for punk fans.",
        "price": "$35+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9427, "lng": -75.1487,
        "isInsider": True,
    },
    {
        "name": "South Street Easter Promenade",
        "date": "2026-04-05",
        "time": "12:00 PM - 3:30 PM",
        "venue": "South Street",
        "address": "S 5th St & South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "cultural",
        "description": "Philadelphia's beloved Easter tradition returns to South Street with a festive promenade featuring live music, street performers, bonnet contests, and family-friendly activities. A colorful, community-driven celebration.",
        "price": "Free",
        "vibeTag": "local-favorite",
        "source": "phila.gov",
        "lat": 39.9428, "lng": -75.1480,
        "isInsider": False,
    },
    {
        "name": "Philly Photo Day at Love Park",
        "date": "2026-04-06",
        "time": "1:00 PM - 2:00 PM",
        "venue": "JFK Plaza (Love Park)",
        "address": "1501 John F Kennedy Blvd, Philadelphia, PA 19102",
        "neighborhood": "Center City",
        "category": "cultural",
        "description": "Philly Photo Day invites the entire city to gather at Love Park for a massive group photo capturing the spirit of Philadelphia. A fun, free community event -- bring your friends and be part of the snapshot.",
        "price": "Free",
        "vibeTag": "local-favorite",
        "source": "phila.gov",
        "lat": 39.9543, "lng": -75.1654,
        "isInsider": False,
    },
    {
        "name": "Voxtrot at The Foundry",
        "date": "2026-04-08",
        "time": "8:00 PM",
        "venue": "The Foundry at The Fillmore",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Austin indie-pop darlings Voxtrot reunite at The Foundry for a rare club show. Literate, jangly pop with big hooks -- one of the most beloved reunions in indie rock right now. Small venue, big energy.",
        "price": "$30+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": True,
    },
    {
        "name": "Odumodublvck at Underground Arts",
        "date": "2026-04-08",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19107",
        "neighborhood": "Callowhill",
        "category": "concert",
        "description": "Nigerian Afrobeats/hip-hop star Odumodublvck brings his viral energy to Underground Arts. Known for the global smash Declan Rice, he is one of the most exciting new voices in African music. A packed, high-energy Wednesday night.",
        "price": "$25+",
        "vibeTag": "trending",
        "source": "concertfix.com",
        "lat": 39.9583, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "McLusky at Underground Arts",
        "date": "2026-04-10",
        "time": "9:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19107",
        "neighborhood": "Callowhill",
        "category": "concert",
        "description": "Welsh noise-rock cult heroes McLusky return from the dead for a rare US show. Abrasive, funny, and impossibly loud -- this is one of the most anticipated underground rock shows of the spring.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9583, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "Poison The Well & Converge at The Fillmore",
        "date": "2026-04-11",
        "time": "7:00 PM",
        "venue": "The Fillmore Philadelphia",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Metalcore and post-hardcore legends Poison The Well and Converge co-headline The Fillmore with Spy and Balmora opening. A stacked bill of heavy music that will absolutely level the room.",
        "price": "$35+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": True,
    },
    {
        "name": "Black Label Society at The Fillmore",
        "date": "2026-04-07",
        "time": "7:30 PM",
        "venue": "The Fillmore Philadelphia",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Zakk Wylde and Black Label Society bring their crushing riffs and legendary guitar shredding to The Fillmore. A must for metal fans -- expect a wall of sound and epic solos all night.",
        "price": "$45+",
        "vibeTag": "trending",
        "source": "concertfix.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": False,
    },
    {
        "name": "Lewis Capaldi at The Liacouras Center",
        "date": "2026-04-15",
        "time": "7:30 PM",
        "venue": "The Liacouras Center",
        "address": "1776 N Broad St, Philadelphia, PA 19121",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "Scottish singer-songwriter Lewis Capaldi returns to the stage with his heart-on-sleeve ballads and disarming humor. An arena show that feels intimate -- expect tears, laughter, and massive singalongs.",
        "price": "$50+",
        "vibeTag": "trending",
        "source": "visitphilly.com",
        "lat": 39.9812, "lng": -75.1565,
        "isInsider": False,
    },
    {
        "name": "Tigers Jaw at Union Transfer",
        "date": "2026-04-16",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden St, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "concert",
        "description": "Scranton emo/indie-rock favorites Tigers Jaw play a hometown-adjacent show at Union Transfer. Their emotionally resonant songs and tight live performances make this an essential night for the Philly emo scene.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9614, "lng": -75.1543,
        "isInsider": True,
    },
    {
        "name": "Cut Worms at Underground Arts",
        "date": "2026-04-16",
        "time": "8:30 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19107",
        "neighborhood": "Callowhill",
        "category": "concert",
        "description": "Brooklyn retro-pop crooner Cut Worms brings his warm, vintage sound to Underground Arts. Think 60s doo-wop meets indie songwriting -- a dreamy, lo-fi evening for fans of classic pop melodies.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9583, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "1776: The Musical at Walnut Street Theatre",
        "date": "2026-04-14 to 2026-05-31",
        "time": "Various",
        "venue": "Walnut Street Theatre",
        "address": "825 Walnut St, Philadelphia, PA 19107",
        "neighborhood": "Washington Square",
        "category": "performing-arts",
        "description": "In a Semiquincentennial year, the Walnut Street Theatre presents a new production of the 1969 Broadway classic about the signing of the Declaration of Independence. History comes alive in the nation's oldest theater, steps from where it all happened.",
        "price": "$30+",
        "vibeTag": "local-favorite",
        "source": "visitphilly.com",
        "lat": 39.9488, "lng": -75.1520,
        "isInsider": False,
    },
    {
        "name": "Calum Scott at The Fillmore",
        "date": "2026-04-22",
        "time": "8:00 PM",
        "venue": "The Fillmore Philadelphia",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "The Dancing on My Own singer and honorary Philadelphian Calum Scott performs at The Fillmore with selections from his new album Avenoir. Pop ballads in an intimate setting.",
        "price": "$35+",
        "vibeTag": "trending",
        "source": "visitphilly.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": False,
    },
    {
        "name": "Germantown Jazz Festival",
        "date": "2026-04-24 to 2026-04-26",
        "time": "Various",
        "venue": "Various Germantown Venues",
        "address": "Germantown, Philadelphia, PA",
        "neighborhood": "Germantown",
        "category": "festival",
        "description": "Three days of jazz concerts, master classes, and performances across historic Germantown venues. Opening night at Attic Brewery features Philly's top jazz artists, Saturday brings trumpeter Terell Stafford, and Sunday closes with a Big Band Jazz Battle and late-night jam. A deep insider pick.",
        "price": "$15 - $50",
        "vibeTag": "underground",
        "source": "germantownjazzfestival.com",
        "lat": 40.0340, "lng": -75.1760,
        "isInsider": True,
    },
    {
        "name": "Festival of Colors at Philadelphia Zoo",
        "date": "2026-04-25",
        "time": "11:30 AM - 3:30 PM",
        "venue": "Philadelphia Zoo",
        "address": "3400 W Girard Ave, Philadelphia, PA 19104",
        "neighborhood": "West Philadelphia",
        "category": "cultural",
        "description": "The Philadelphia Zoo celebrates spring with a joyful Festival of Colors in partnership with the Council of Indian Organizations. Indian music, dancing, kids activities, food, art, and a color-throwing ceremony. Free with zoo admission.",
        "price": "$20-$34 (zoo admission)",
        "vibeTag": "family-friendly",
        "source": "visitphilly.com",
        "lat": 39.9714, "lng": -75.1955,
        "isInsider": False,
    },
    {
        "name": "Rising Up: Rocky and the Making of Monuments at PMA",
        "date": "2026-04-25 to 2026-08-02",
        "time": "Various",
        "venue": "Philadelphia Museum of Art",
        "address": "2600 Benjamin Franklin Pkwy, Philadelphia, PA 19130",
        "neighborhood": "Fairmount",
        "category": "art",
        "description": "Inspired by the iconic Rocky Statue, this new exhibition at the PMA explores why we make monuments, who gets memorialized, and what monuments mean to communities. A timely, thought-provoking show opening during the city's 250th anniversary celebrations.",
        "price": "$25+",
        "vibeTag": "trending",
        "source": "visitphilly.com",
        "lat": 39.9656, "lng": -75.1810,
        "isInsider": False,
    },
    {
        "name": "Spring Fest at Bartram's Garden",
        "date": "2026-04-18",
        "time": "TBD",
        "venue": "Bartram's Garden",
        "address": "5400 Lindbergh Blvd, Philadelphia, PA 19143",
        "neighborhood": "Southwest Philadelphia",
        "category": "outdoor",
        "description": "A free, family-friendly spring festival at historic Bartram's Garden featuring workshops, garden tours, keynotes, local vendors, and a nursery sale. A hidden gem event in one of America's oldest botanic gardens.",
        "price": "Free",
        "vibeTag": "underground",
        "source": "inquirer.com",
        "lat": 39.9320, "lng": -75.2130,
        "isInsider": True,
    },
    {
        "name": "The Growlers at Union Transfer",
        "date": "2026-04-21",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden St, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "concert",
        "description": "Beach goth originators The Growlers bring their psychedelic surf-rock to Union Transfer. Known for hazy, sun-soaked live shows that feel like a party at the end of the world.",
        "price": "$30+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9614, "lng": -75.1543,
        "isInsider": True,
    },
    {
        "name": "Broncho at Underground Arts",
        "date": "2026-04-23",
        "time": "8:00 PM",
        "venue": "Underground Arts",
        "address": "1200 Callowhill St, Philadelphia, PA 19107",
        "neighborhood": "Callowhill",
        "category": "concert",
        "description": "Oklahoma garage-rock band Broncho delivers catchy, buzzsaw pop-punk at Underground Arts. Their tight, energetic sets are pure fun -- a great midweek show for indie rock fans.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "concertfix.com",
        "lat": 39.9583, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "Brauhaus Schmitz Maifest",
        "date": "2026-05-02",
        "time": "12:00 PM - 8:00 PM",
        "venue": "Brauhaus Schmitz",
        "address": "718 South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "festival",
        "description": "One of the largest German Maifest celebrations in Pennsylvania. Flower crowns, maypole dancing, a liter lift competition, live music, authentic German eats, beer, and an actual pig roast. A full day of Bavarian revelry on South Street.",
        "price": "Free entry, pay for food/beer",
        "vibeTag": "local-favorite",
        "source": "inquirer.com",
        "lat": 39.9432, "lng": -75.1588,
        "isInsider": False,
    },
]

added_events = 0
eid = next_eid
entries = []
for ev in new_events:
    if ev["name"].lower() in existing_ev:
        print(f"  Skipping: {ev['name']}")
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
    entries.append(entry)
    existing_ev.add(ev["name"].lower())
    added_events += 1
    eid += 1
    print(f"  Adding: {ev['name']}")

if entries:
    hs_start, _ = bounds()
    ec = content[:hs_start].rfind("];")
    lb = content[:ec].rfind("}")
    content = content[:lb+1] + ",\n" + ",\n".join(entries) + ",\n" + content[lb+1:]

print(f"  Added {added_events} events")

# ══════════════════════════════════════
# STEP 3: ADD NEW HOTSPOTS
# ══════════════════════════════════════
print("\n=== ADDING NEW HOTSPOTS ===")
hs_start, inf_start = bounds()
existing_hs = get_names(content[hs_start:inf_start])

new_hotspots = [
    {
        "name": "The Grape",
        "type": "Bar / Music Venue",
        "address": "105 Grape St, Philadelphia, PA 19127",
        "neighborhood": "Manayunk",
        "description": "The beloved Grape Room returns reborn as just The Grape -- a two-floor indie music venue and dive bar off Manayunk's Main Street. Open mic nights, stand-up comedy, indie bands, beer on both floors, and the kitchen is coming soon. A Northwest Philly institution rises again.",
        "vibeTag": "underground",
        "priceRange": "$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 40.0260, "lng": -75.2280,
        "source": "visitphilly.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Known Associates",
        "type": "Cocktail Bar",
        "address": "941 Spruce St, Philadelphia, PA 19107",
        "neighborhood": "Washington Square West",
        "description": "Forsythia chef Christopher Kearse teams with PS & Daughters to create a Euro-style cocktail bar in the former Varga Bar space. Expect elegant cocktails, moody design, and the kind of grown-up nightlife that makes you feel like you're in Paris. The most anticipated bar opening of spring 2026.",
        "vibeTag": "trending",
        "priceRange": "$$$",
        "cuisine": "Cocktails / Small Plates",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9450, "lng": -75.1573,
        "source": "phillymag.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Savu",
        "type": "Restaurant",
        "address": "208 S 13th St, Philadelphia, PA 19107",
        "neighborhood": "Midtown Village",
        "description": "A refined new restaurant on 13th Street offering seasonal, ingredient-driven cuisine in a sleek, modern space. Already generating buzz as one of the most reservation-worthy new spots in the city.",
        "vibeTag": "trending",
        "priceRange": "$$$",
        "cuisine": "New American",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9480, "lng": -75.1613,
        "source": "visitphilly.com",
        "addedDate": TODAY,
        "trendingScore": 60,
    },
    {
        "name": "LynUp Cafe & Lounge",
        "type": "Restaurant / BYOB",
        "address": "7803 Frankford Ave, Philadelphia, PA",
        "neighborhood": "Far Northeast",
        "description": "A fashionable West African BYOB bringing bold flavors to Frankford Avenue. Jollof rice, suya, fufu, and puff-puff alongside a lounge vibe with music and community events. A rare gem representing Nigerian and Ghanaian cuisine in the Northeast.",
        "vibeTag": "underground",
        "priceRange": "$$",
        "cuisine": "West African",
        "isNew": True,
        "isInsider": True,
        "lat": 40.0630, "lng": -75.0530,
        "source": "visitphilly.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
]

added_spots = 0
sid = next_sid
spot_entries = []
for sp in new_hotspots:
    if sp["name"].lower() in existing_hs:
        print(f"  Skipping: {sp['name']}")
        continue
    cv = f'"{sp["cuisine"]}"' if sp["cuisine"] else "null"
    entry = f"""  {{
    id: "spot-{sid}",
    name: "{esc(sp['name'])}",
    type: "{sp['type']}",
    address: "{esc(sp['address'])}",
    neighborhood: "{sp['neighborhood']}",
    description: "{esc(sp['description'])}",
    vibeTag: "{sp['vibeTag']}",
    priceRange: "{sp['priceRange']}",
    cuisine: {cv},
    isNew: {"true" if sp["isNew"] else "false"},
    isInsider: {"true" if sp["isInsider"] else "false"},
    lat: {sp['lat']},
    lng: {sp['lng']},
    source: "{sp['source']}",
    addedDate: "{sp['addedDate']}",
    trendingScore: {sp['trendingScore']},
  }}"""
    spot_entries.append(entry)
    existing_hs.add(sp["name"].lower())
    added_spots += 1
    sid += 1
    print(f"  Adding: {sp['name']}")

if spot_entries:
    _, inf_start = bounds()
    hc = content[:inf_start].rfind("];")
    lb = content[:hc].rfind("}")
    content = content[:lb+1] + ",\n" + ",\n".join(spot_entries) + ",\n" + content[lb+1:]

print(f"  Added {added_spots} hotspots")

# ══════════════════════════════════════
# STEP 4: HOTSPOT LIFECYCLE
# ══════════════════════════════════════
print("\n=== HOTSPOT LIFECYCLE ===")
hs_start, inf_start = bounds()
hs_sec = content[hs_start:inf_start]
spot_count = len(re.findall(r'id: "spot-', hs_sec))
print(f"  Total: {spot_count}")

sblocks = list(re.finditer(r'(\{[^{}]*?id: "spot-\d+"[^{}]*?\})', hs_sec, re.DOTALL))
pruned = decayed = unmarked = 0

for m in reversed(sblocks):
    b = m.group(1)
    am = re.search(r'addedDate: "(\d{4}-\d{2}-\d{2})"', b)
    sm = re.search(r'trendingScore: (\d+)', b)
    im = re.search(r'isInsider: (true|false)', b)
    nm = re.search(r'isNew: (true|false)', b)
    name_m = re.search(r'name: "([^"]+)"', b)
    if not am or not sm: continue

    ad = datetime.strptime(am.group(1), "%Y-%m-%d")
    sc = int(sm.group(1))
    insider = im and im.group(1) == "true"
    isnew = nm and nm.group(1) == "true"
    name = name_m.group(1) if name_m else "?"
    age = (TODAY_DT - ad).days

    do_prune = False
    if spot_count > 60:
        if age > 21 and sc < 50: do_prune = True
        if age > 30 and not insider: do_prune = True

    if do_prune and spot_count > 40:
        print(f"  Pruning: {name} (age {age}d, score {sc})")
        a_s = hs_start + m.start()
        a_e = hs_start + m.end()
        after = content[a_e:a_e+20]
        before = content[max(0,a_s-20):a_s]
        if after.lstrip().startswith(','):
            content = content[:a_s] + content[a_e + after.index(',') + 1:]
        elif before.rstrip().endswith(','):
            lc = content[:a_s].rstrip().rfind(',')
            content = content[:lc] + content[a_e:]
        else:
            content = content[:a_s] + content[a_e:]
        pruned += 1; spot_count -= 1
        hs_start, inf_start = bounds()
        continue

    if age > 7 and sc > 5:
        ns = max(5, sc - 5)
        nb = b.replace(f"trendingScore: {sc}", f"trendingScore: {ns}")
        a_s = hs_start + m.start()
        a_e = hs_start + m.end()
        content = content[:a_s] + nb + content[a_e:]
        decayed += 1
        hs_start, inf_start = bounds()

    if age > 14 and isnew:
        hs_start, inf_start = bounds()
        hs_sec2 = content[hs_start:inf_start]
        bm2 = re.search(re.escape(name_m.group(0)), hs_sec2)
        if bm2:
            np2 = hs_start + bm2.start()
            sz = content[np2:np2+500]
            nm2 = re.search(r'isNew: true', sz)
            if nm2:
                ap = np2 + nm2.start()
                content = content[:ap] + "isNew: false" + content[ap+len("isNew: true"):]
                unmarked += 1
                print(f"  Unmarked isNew: {name} ({age}d)")

hs_start, inf_start = bounds()
final_spots = len(re.findall(r'id: "spot-', content[hs_start:inf_start]))
print(f"  Pruned: {pruned}, Decayed: {decayed}, Unmarked: {unmarked}, Final: {final_spots}")

# ══════════════════════════════════════
# STEP 5: INFLUENCER UPDATES
# ══════════════════════════════════════
print("\n=== INFLUENCER UPDATES ===")
picks = {
    "@wooder_ice": {
        "name": "Philly 250 Spring Kickoff",
        "type": "culture",
        "neighborhood": "Citywide",
        "quote": "Philly 250 is in full swing -- Market East pop-ups are live, 1776 The Musical opens at Walnut Street Theatre, and the city is buzzing. This is going to be the biggest year in Philly history. Get outside and enjoy it.",
        "date": TODAY,
    },
    "@feedingtimetv": {
        "name": "The Grape is Back in Manayunk",
        "type": "bar",
        "neighborhood": "Manayunk",
        "quote": "The Grape is officially back! The legendary Manayunk dive and music venue reopened with a new name and the same energy. Two floors, cold beer, indie bands, and open mic nights. Philly needed this.",
        "date": TODAY,
    },
    "@josheatsphilly": {
        "name": "Savu Midtown Village Dinner",
        "type": "restaurant",
        "neighborhood": "Midtown Village",
        "quote": "First dinner at Savu on 13th Street and it lived up to the hype. Seasonal menu, beautiful plating, and a chef who clearly knows what they are doing. This is fine dining without the attitude. Book now.",
        "date": TODAY,
    },
    "@thephillyfoodfanatic": {
        "name": "Southeast Asian Market Opening Day",
        "type": "market",
        "neighborhood": "South Philly",
        "quote": "The Southeast Asian Market is officially open at FDR Park for the season! Fresh produce, incredible street food, and the most authentic Southeast Asian flavors in the city. Every weekend through the fall.",
        "date": TODAY,
    },
    "@cass_andthecity": {
        "name": "Open Streets West Walnut Sundays",
        "type": "event",
        "neighborhood": "West Philadelphia",
        "quote": "Open Streets West Walnut kicked off this weekend and it was perfect. Car-free blocks, acoustic music, and the best of Walnut Street shopping and dining. Every Sunday through May 17.",
        "date": TODAY,
    },
    "@phillyfoodladies": {
        "name": "LynUp Cafe West African BYOB",
        "type": "restaurant",
        "neighborhood": "Far Northeast",
        "quote": "LynUp Cafe on Frankford Ave is doing incredible West African food -- jollof rice, suya, puff-puff, and the lounge vibes are on point. BYOB means you can bring your own palm wine. A hidden gem.",
        "date": TODAY,
    },
    "@fueledonphilly": {
        "name": "Circle Jerks & Gorilla Biscuits Hype",
        "type": "event",
        "neighborhood": "South Street",
        "quote": "Circle Jerks AND Gorilla Biscuits at TLA tomorrow night. If you care about punk rock even a little, this double bill is unmissable. Hardcore legends in a legendary venue. See you in the pit.",
        "date": TODAY,
    },
    "@koryaversa": {
        "name": "Robert Plant at The Met Preview",
        "type": "event",
        "neighborhood": "North Broad",
        "quote": "Robert Plant with Saving Grace at The Met tomorrow. A Led Zeppelin legend playing acoustic Americana in one of the most beautiful venues in America. This is a bucket list night. Limited tickets remain.",
        "date": TODAY,
    },
    "@djour.philly": {
        "name": "Germantown Jazz Festival Announcement",
        "type": "event",
        "neighborhood": "Germantown",
        "quote": "Mark your calendars -- Germantown Jazz Festival runs April 24-26. Three days of concerts at Attic Brewery, Germantown Settlement, and more. Terell Stafford headlines Saturday. This is the real jazz scene.",
        "date": TODAY,
    },
    "@swagfoodphilly": {
        "name": "Known Associates Bar Opening",
        "type": "bar",
        "neighborhood": "Washington Square West",
        "quote": "Known Associates from Forsythia's Chris Kearse is opening in the old Varga Bar space and it looks incredible. Euro-style cocktails, moody vibes, and PS & Daughters design. Spring's most anticipated bar.",
        "date": TODAY,
    },
}

inf_count = 0
for handle, pick in picks.items():
    hi = content.find(f'handle: "{handle}"')
    if hi < 0:
        print(f"  Not found: {handle}"); continue
    pi = content.find("recentPicks: [", hi)
    if pi < 0 or pi > hi + 2000:
        print(f"  No picks: {handle}"); continue
    po = pi + len("recentPicks: [")
    np_str = f"""
      {{
        name: "{esc(pick['name'])}",
        type: "{pick['type']}",
        neighborhood: "{pick['neighborhood']}",
        quote: "{esc(pick['quote'])}",
        date: "{pick['date']}",
      }},"""
    content = content[:po] + np_str + content[po:]
    inf_count += 1
    print(f"  Updated {handle}: {pick['name']}")

print(f"  Updated {inf_count} influencers")

# ══════════════════════════════════════
# STEP 6: DEDUP
# ══════════════════════════════════════
print("\n=== DEDUP ===")
dupes = 0
hs_start, _ = bounds()
en = [n.lower() for n in re.findall(r'name: "([^"]+)"', content[:hs_start])]
seen = set()
for n in en:
    if n in seen: dupes += 1; print(f"  Dup event: {n}")
    seen.add(n)

_, inf_start = bounds()
hs_start, _ = bounds()
sn = [n.lower() for n in re.findall(r'name: "([^"]+)"', content[hs_start:inf_start])]
seen = set()
for n in sn:
    if n in seen: dupes += 1; print(f"  Dup hotspot: {n}")
    seen.add(n)

aids = re.findall(r'id: "([^"]+)"', content)
seen_ids = set()
for i in aids:
    if i in seen_ids: dupes += 1; print(f"  Dup ID: {i}")
    seen_ids.add(i)

if dupes > 0:
    print(f"  Removing {dupes}...")
    hs_start, _ = bounds()
    eblocks = re.findall(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', content[:hs_start], re.DOTALL)
    nmap = {}
    for bl in eblocks:
        nm_match = re.search(r'name: "([^"]+)"', bl)
        if nm_match:
            k = nm_match.group(1).lower()
            nmap.setdefault(k, []).append(bl)
    for k, bls in nmap.items():
        if len(bls) > 1:
            bls.sort(key=len, reverse=True)
            for d in bls[1:]:
                idx = content.find(d)
                if idx >= 0:
                    ei = idx + len(d)
                    af = content[ei:ei+20]; bf = content[max(0,idx-20):idx]
                    if af.lstrip().startswith(','):
                        content = content[:idx] + content[ei+af.index(',')+1:]
                    elif bf.rstrip().endswith(','):
                        lc2 = content[:idx].rstrip().rfind(',')
                        content = content[:lc2] + content[ei:]
                    else:
                        content = content[:idx] + content[ei:]
else:
    print("  No duplicates")

# ══════════════════════════════════════
# STEP 7: CLEANUP
# ══════════════════════════════════════
print("\n=== CLEANUP ===")
bl = len(content)
content = re.sub(r'\n\s*,\s*\n', '\n', content)
content = re.sub(r'\n{3,}', '\n\n', content)
content = re.sub(r',\s*\n(\s*\];)', r'\n\1', content)
print(f"  Cleaned {bl - len(content)} chars")

# ══════════════════════════════════════
# FINAL
# ══════════════════════════════════════
fe = len(re.findall(r'id: "event-', content))
fs = len(re.findall(r'id: "spot-', content))
print(f"\n=== DONE ===")
print(f"  Events: {fe}, Hotspots: {fs}")
print(f"  Removed past: {past_removed}, Added events: {added_events}, Added spots: {added_spots}")
print(f"  Influencers: {inf_count}, Pruned: {pruned}, Decayed: {decayed}, Dupes: {dupes}")

with open("client/src/data/philly-data.ts", "w") as f:
    f.write(content)

json.dump({
    "past_removed": past_removed, "events_added": added_events,
    "spots_added": added_spots, "influencers": inf_count,
    "pruned": pruned, "decayed": decayed, "unmarked": unmarked,
    "dupes": dupes, "final_events": fe, "final_spots": fs,
}, open("/tmp/run12_summary.json","w"), indent=2)
print("File saved!")
