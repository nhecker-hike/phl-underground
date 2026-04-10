#!/usr/bin/env python3
"""PHL Underground Weekly Refresh #13 (2026-04-10)"""
import re, json
from datetime import datetime

TODAY = "2026-04-10"
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

# ═══════════════════════════════════════
# STEP 1: REMOVE PAST EVENTS
# ═══════════════════════════════════════
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
print(f"  Removed {past_removed}")

# ═══════════════════════════════════════
# STEP 2: ADD NEW EVENTS
# ═══════════════════════════════════════
print("\n=== ADDING NEW EVENTS ===")
hs_start, _ = bounds()
existing_ev = get_names(content[:hs_start])

new_events = [
    {
        "name": "The Wonder Years with Pool Kids at TLA",
        "date": "2026-04-10",
        "time": "7:00 PM",
        "venue": "Theatre of Living Arts",
        "address": "334 South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "concert",
        "description": "Philly's own emo-pop-punk heroes The Wonder Years bring their cathartic, anthemic live show to the TLA with Pool Kids opening. A hometown show from one of the city's most beloved bands -- expect singalongs, crowd surfs, and raw emotion.",
        "price": "$30+",
        "vibeTag": "local-favorite",
        "source": "seatgeek.com",
        "lat": 39.9427, "lng": -75.1487,
        "isInsider": False,
    },
    {
        "name": "Bob Moses with Cannons at The Fillmore",
        "date": "2026-04-10",
        "time": "7:30 PM",
        "venue": "The Fillmore Philadelphia",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Electronic duo Bob Moses brings their deep, moody house music to The Fillmore with synth-pop act Cannons opening. Dark beats, immersive visuals, and a packed dance floor -- a perfect Friday night for electronic music fans.",
        "price": "$35+",
        "vibeTag": "after-dark",
        "source": "seatgeek.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": False,
    },
    {
        "name": "Floetry with Raheem DeVaughn at The Met",
        "date": "2026-04-10",
        "time": "8:00 PM",
        "venue": "The Met Philadelphia",
        "address": "858 N Broad St, Philadelphia, PA 19130",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "Neo-soul legends Floetry bring their lush harmonies and spoken-word poetry to The Met with R&B crooner Raheem DeVaughn opening. Say Yes to a Friday night of pure vibes in one of Philly's most gorgeous venues.",
        "price": "$55+",
        "vibeTag": "after-dark",
        "source": "seatgeek.com",
        "lat": 39.9726, "lng": -75.1590,
        "isInsider": False,
    },
    {
        "name": "Snow Tha Product at Union Transfer",
        "date": "2026-04-10",
        "time": "8:00 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden St, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "concert",
        "description": "Bilingual rapper Snow Tha Product brings her fiery flow and viral energy to Union Transfer. One of the most dynamic live performers in hip-hop -- expect rapid-fire bars in English and Spanish and a crowd that matches her energy.",
        "price": "$30+",
        "vibeTag": "trending",
        "source": "seatgeek.com",
        "lat": 39.9614, "lng": -75.1543,
        "isInsider": False,
    },
    {
        "name": "Trey Songz at Liacouras Center",
        "date": "2026-04-10",
        "time": "8:00 PM",
        "venue": "The Liacouras Center",
        "address": "1776 N Broad St, Philadelphia, PA 19121",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "R&B hitmaker Trey Songz brings smooth vocals and an energetic stage show to the Liacouras Center. Heart Attack, Slow Motion, and a catalog of bedroom anthems in a big arena setting.",
        "price": "$50+",
        "vibeTag": "trending",
        "source": "seatgeek.com",
        "lat": 39.9812, "lng": -75.1565,
        "isInsider": False,
    },
    {
        "name": "Happy Landing at The Foundry",
        "date": "2026-04-10",
        "time": "8:00 PM",
        "venue": "The Foundry at The Fillmore",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Indie-rock act Happy Landing plays the intimate Foundry stage. A smaller, sweatier room for a louder, more personal show -- the kind of Friday night Fishtown was built for.",
        "price": "$15+",
        "vibeTag": "underground",
        "source": "seatgeek.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": True,
    },
    {
        "name": "A Nation of Artists at Philadelphia Museum of Art",
        "date": "2026-04-12 to 2027-07-05",
        "time": "Various",
        "venue": "Philadelphia Museum of Art",
        "address": "2600 Benjamin Franklin Pkwy, Philadelphia, PA 19130",
        "neighborhood": "Fairmount",
        "category": "art",
        "description": "A landmark exhibition uniting three extraordinary collections -- the PMA, PAFA, and the Middleton Family Collection -- to celebrate America's 250th anniversary. Over 1,000 works of American art spanning centuries, from colonial portraiture to contemporary sculpture. A once-in-a-lifetime show exclusive to Philadelphia.",
        "price": "$25+",
        "vibeTag": "trending",
        "source": "philamuseum.org",
        "lat": 39.9656, "lng": -75.1810,
        "isInsider": False,
    },
    {
        "name": "South 9th Street Italian Market Festival",
        "date": "2026-05-16 to 2026-05-17",
        "time": "10:00 AM - 5:00 PM",
        "venue": "South 9th Street Italian Market",
        "address": "S 9th St, Philadelphia, PA 19147",
        "neighborhood": "Italian Market",
        "category": "festival",
        "description": "One of Philadelphia's most iconic events -- seven blocks of South 9th Street transform into a massive block party celebrating the nation's oldest outdoor market. Over 100 vendors, live music, food from every corner of the globe, local art and crafts. A quintessential Philly day out.",
        "price": "Free entry",
        "vibeTag": "local-favorite",
        "source": "italianmarketphilly.org",
        "lat": 39.9370, "lng": -75.1580,
        "isInsider": False,
    },
    {
        "name": "Independent Fridays at PMA",
        "date": "2026-04-10 to 2026-06-26",
        "time": "5:00 PM - 8:45 PM",
        "venue": "Philadelphia Museum of Art",
        "address": "2600 Benjamin Franklin Pkwy, Philadelphia, PA 19130",
        "neighborhood": "Fairmount",
        "category": "art",
        "description": "Starting April 10, the PMA stays open late every Friday evening with live music, cocktails, and after-hours gallery access. A completely different vibe from daytime visits -- stroll among masterworks at golden hour with a drink in hand. The insider Friday night move.",
        "price": "$25+",
        "vibeTag": "after-dark",
        "source": "civicamag.com",
        "lat": 39.9656, "lng": -75.1810,
        "isInsider": True,
    },
    {
        "name": "Josh Wink at The Barbary",
        "date": "2026-04-25",
        "time": "10:00 PM",
        "venue": "The Barbary",
        "address": "951 Frankford Ave, Philadelphia, PA 19125",
        "neighborhood": "Fishtown",
        "category": "nightlife",
        "description": "Philly-born techno and house legend Josh Wink brings his iconic sets to The Barbary. One of the original architects of the 90s rave scene, Wink's deep, hypnotic DJ sets are the real deal. A late-night insider pick for dance music lovers.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "songkick.com",
        "lat": 39.9710, "lng": -75.1352,
        "isInsider": True,
    },
    {
        "name": "Hayley Williams at Franklin Music Hall",
        "date": "2026-04-12",
        "time": "8:00 PM",
        "venue": "Franklin Music Hall",
        "address": "421 N 7th St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "concert",
        "description": "Paramore frontwoman Hayley Williams brings her solo material to Franklin Music Hall. Her solo work trades in a more introspective, new wave-influenced sound -- a must-see for fans of her evolution as an artist.",
        "price": "$45+",
        "vibeTag": "trending",
        "source": "songkick.com",
        "lat": 39.9618, "lng": -75.1480,
        "isInsider": False,
    },
    {
        "name": "Subhumans with La Pobreska at Warehouse on Watts",
        "date": "2026-04-10",
        "time": "8:00 PM",
        "venue": "Warehouse on Watts (WoW)",
        "address": "923 N Watts St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "concert",
        "description": "UK anarcho-punk legends Subhumans play the DIY Warehouse on Watts with La Pobreska, The Brood, and the venomous pinks. An all-ages punk show in a raw warehouse space -- this is underground Philly at its purest.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "songkick.com",
        "lat": 39.9640, "lng": -75.1420,
        "isInsider": True,
    },
    {
        "name": "Water From Your Eyes at Franklin Music Hall",
        "date": "2026-04-11",
        "time": "8:00 PM",
        "venue": "Franklin Music Hall",
        "address": "421 N 7th St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "concert",
        "description": "Brooklyn experimental-pop duo Water From Your Eyes brings their glitchy, genre-defying sound to Franklin Music Hall. One of the most critically acclaimed acts in indie music right now -- angular beats, wry humor, and hypnotic live energy.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "songkick.com",
        "lat": 39.9618, "lng": -75.1480,
        "isInsider": True,
    },
    {
        "name": "Sacco and Vanzetti at Maas Building",
        "date": "2026-04-12",
        "time": "8:00 PM",
        "venue": "Maas Building",
        "address": "4740 Baltimore Ave, Philadelphia, PA 19143",
        "neighborhood": "West Philadelphia",
        "category": "performing-arts",
        "description": "A commedia dell'arte retelling of the infamous Sacco and Vanzetti trial -- blending absurdist comedy with political tragedy in an intimate West Philly venue. Experimental theater at its most daring.",
        "price": "$15+",
        "vibeTag": "underground",
        "source": "metrophiladelphia.com",
        "lat": 39.9480, "lng": -75.2190,
        "isInsider": True,
    },
    {
        "name": "Foo Fighters with Queens of the Stone Age at Lincoln Financial Field",
        "date": "2026-08-13",
        "time": "5:30 PM",
        "venue": "Lincoln Financial Field",
        "address": "1 Lincoln Financial Field Way, Philadelphia, PA 19148",
        "neighborhood": "South Philly Sports Complex",
        "category": "concert",
        "description": "Two-time Rock Hall inductees Foo Fighters headline the Linc with Queens of the Stone Age, Mannequin Pussy, and Gouge Away. The biggest rock show of the summer in a stadium setting -- Everlong singalongs guaranteed.",
        "price": "$75+",
        "vibeTag": "trending",
        "source": "visitphilly.com",
        "lat": 39.9008, "lng": -75.1675,
        "isInsider": False,
    },
]

added_events = 0
eid = next_eid
entries = []
for ev in new_events:
    if ev["name"].lower() in existing_ev:
        print(f"  Skip: {ev['name']}"); continue
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
    added_events += 1; eid += 1
    print(f"  Adding: {ev['name']}")

if entries:
    hs_start, _ = bounds()
    ec = content[:hs_start].rfind("];")
    lb = content[:ec].rfind("}")
    content = content[:lb+1] + ",\n" + ",\n".join(entries) + ",\n" + content[lb+1:]
print(f"  Added {added_events}")

# ═══════════════════════════════════════
# STEP 3: ADD NEW HOTSPOTS
# ═══════════════════════════════════════
print("\n=== ADDING NEW HOTSPOTS ===")
hs_start, inf_start = bounds()
existing_hs = get_names(content[hs_start:inf_start])

new_hotspots = [
    {
        "name": "Ranstead Room",
        "type": "Speakeasy / Cocktail Bar",
        "address": "1715 Schubert Alley, Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse Square",
        "description": "One of Philly's best-kept secrets for 15+ years. Hidden behind an unmarked black door in an alley behind El Rey, the Ranstead Room is a dark, moody, 1930s-style speakeasy with leather booths, some of the city's best cocktails, and the kind of atmosphere you can't manufacture. If you haven't found it, you haven't tried.",
        "vibeTag": "underground",
        "priceRange": "$$$",
        "cuisine": "Cocktails",
        "isNew": False,
        "isInsider": True,
        "lat": 39.9508, "lng": -75.1693,
        "source": "tastingtable.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Behind the Red Door at Vita",
        "type": "Speakeasy / Restaurant",
        "address": "261 S 17th St, Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse Square",
        "description": "A full speakeasy restaurant hidden behind a bright red refrigerator door inside Vita gelato shop. Handmade pasta, bistecca alla Fiorentina, Italian wines, and a secret garden -- Narnia but with carbonara. Reservation only via Resy.",
        "vibeTag": "underground",
        "priceRange": "$$$",
        "cuisine": "Italian",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9490, "lng": -75.1720,
        "source": "visitphilly.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Corio",
        "type": "Restaurant",
        "address": "University City, Philadelphia, PA",
        "neighborhood": "University City",
        "description": "A new pizza and pasta spot in University City offering NYC-style pies, wings, and hearty Italian-American dishes for both lunch and dinner. Casual, buzzy, and already drawing crowds from the Penn and Drexel campuses.",
        "vibeTag": "trending",
        "priceRange": "$$",
        "cuisine": "Pizza / Italian",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9530, "lng": -75.1930,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 60,
    },
    {
        "name": "Kendo Sushi",
        "type": "Restaurant",
        "address": "1521 Spring Garden St, Philadelphia, PA 19130",
        "neighborhood": "Spring Garden",
        "description": "A sleek new sushi spot on Spring Garden serving fresh nigiri, creative rolls, and Japanese small plates. Already generating word-of-mouth buzz as a serious contender in the Philly sushi scene.",
        "vibeTag": "trending",
        "priceRange": "$$$",
        "cuisine": "Japanese / Sushi",
        "isNew": True,
        "isInsider": False,
        "lat": 39.9614, "lng": -75.1600,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 60,
    },
]

added_spots = 0
sid = next_sid
spot_entries = []
for sp in new_hotspots:
    if sp["name"].lower() in existing_hs:
        print(f"  Skip: {sp['name']}"); continue
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
    added_spots += 1; sid += 1
    print(f"  Adding: {sp['name']}")

if spot_entries:
    _, inf_start = bounds()
    hc = content[:inf_start].rfind("];")
    lb = content[:hc].rfind("}")
    content = content[:lb+1] + ",\n" + ",\n".join(spot_entries) + ",\n" + content[lb+1:]
print(f"  Added {added_spots}")

# ═══════════════════════════════════════
# STEP 4: HOTSPOT LIFECYCLE
# ═══════════════════════════════════════
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
    sc = int(sm.group(1)); insider = im and im.group(1) == "true"
    isnew = nm and nm.group(1) == "true"
    name = name_m.group(1) if name_m else "?"; age = (TODAY_DT - ad).days

    do_prune = False
    if spot_count > 60:
        if age > 21 and sc < 50: do_prune = True
        if age > 30 and not insider: do_prune = True
    if do_prune and spot_count > 40:
        print(f"  Pruning: {name} (age {age}d, score {sc})")
        a_s = hs_start + m.start(); a_e = hs_start + m.end()
        after = content[a_e:a_e+20]; before = content[max(0,a_s-20):a_s]
        if after.lstrip().startswith(','):
            content = content[:a_s] + content[a_e + after.index(',') + 1:]
        elif before.rstrip().endswith(','):
            lc = content[:a_s].rstrip().rfind(',')
            content = content[:lc] + content[a_e:]
        else: content = content[:a_s] + content[a_e:]
        pruned += 1; spot_count -= 1; hs_start, inf_start = bounds(); continue

    if age > 7 and sc > 5:
        ns = max(5, sc - 5)
        nb = b.replace(f"trendingScore: {sc}", f"trendingScore: {ns}")
        a_s = hs_start + m.start(); a_e = hs_start + m.end()
        content = content[:a_s] + nb + content[a_e:]
        decayed += 1; hs_start, inf_start = bounds()

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
                unmarked += 1; print(f"  Unmarked: {name} ({age}d)")

hs_start, inf_start = bounds()
final_spots = len(re.findall(r'id: "spot-', content[hs_start:inf_start]))
print(f"  Pruned: {pruned}, Decayed: {decayed}, Unmarked: {unmarked}, Final: {final_spots}")

# ═══════════════════════════════════════
# STEP 5: INFLUENCER UPDATES
# ═══════════════════════════════════════
print("\n=== INFLUENCER UPDATES ===")
picks = {
    "@wooder_ice": {
        "name": "A Nation of Artists at PMA",
        "type": "art",
        "neighborhood": "Fairmount",
        "quote": "A Nation of Artists opens at the Philadelphia Museum of Art this Sunday -- 1,000+ works of American art celebrating the 250th. PMA, PAFA, and the Middleton Collection all together. Once-in-a-lifetime exhibition and it is only here in Philly.",
        "date": TODAY,
    },
    "@feedingtimetv": {
        "name": "Emilia Pasta Night in Fishtown",
        "type": "restaurant",
        "neighborhood": "Fishtown",
        "quote": "Greg Vernick's Emilia in Fishtown is turning out incredible pasta. The cacio e pepe is textbook, the ragus are rich and complex, and the Frankford Ave vibe is exactly right. James Beard nominee doing casual Italian at its finest.",
        "date": TODAY,
    },
    "@josheatsphilly": {
        "name": "Behind the Red Door at Vita",
        "type": "restaurant",
        "neighborhood": "Rittenhouse Square",
        "quote": "Found a speakeasy behind a red refrigerator door inside Vita gelato in Rittenhouse. Full Italian restaurant -- handmade pasta, bistecca, wine -- hidden behind a gelato shop. Book on Resy, this is the coolest dinner in Philly right now.",
        "date": TODAY,
    },
    "@thephillyfoodfanatic": {
        "name": "Manong Filipino Fare on Fairmount",
        "type": "restaurant",
        "neighborhood": "Fairmount",
        "quote": "Manong on Fairmount Ave is doing beautiful Filipino food. The lumpia are crispy perfection, the chicken adobo is rich and tangy, and the whole experience feels like a warm hug. Philly needed this.",
        "date": TODAY,
    },
    "@cass_andthecity": {
        "name": "Independent Fridays at PMA",
        "type": "event",
        "neighborhood": "Fairmount",
        "quote": "New Friday night move: Independent Fridays at the PMA. Galleries stay open late with cocktails and live music starting tonight. Walking through American art with a drink at golden hour is a vibe I did not know I needed.",
        "date": TODAY,
    },
    "@phillyfoodladies": {
        "name": "Corio University City Pizza",
        "type": "restaurant",
        "neighborhood": "University City",
        "quote": "Corio in University City just opened and the NYC-style pizza is legit. Thin crust, great sauce, and they do wings too. Perfect lunch spot for the UCity crowd. Already packed.",
        "date": TODAY,
    },
    "@fueledonphilly": {
        "name": "Wonder Years Hometown TLA Show",
        "type": "event",
        "neighborhood": "South Street",
        "quote": "The Wonder Years at TLA tonight with Pool Kids. A hometown emo show from Philly's finest. If you grew up on Soupy's lyrics, this is a mandatory Friday night. Expect tears and crowd surfs.",
        "date": TODAY,
    },
    "@koryaversa": {
        "name": "StrEAT Food Festival Final Countdown",
        "type": "event",
        "neighborhood": "Manayunk",
        "quote": "Nine days until StrEAT Food Festival takes over Main Street Manayunk. 85+ food trucks, live music, new family area this year. April 19, 11am to 5pm. Free entry. This is the biggest food event of the spring, do not miss it.",
        "date": TODAY,
    },
    "@djour.philly": {
        "name": "Subhumans at Warehouse on Watts",
        "type": "event",
        "neighborhood": "Northern Liberties",
        "quote": "UK anarcho-punk legends Subhumans are playing Warehouse on Watts tonight. DIY venue, all ages, raw punk energy. This is the underground Philly show of the week. La Pobreska, The Brood, and the venomous pinks opening.",
        "date": TODAY,
    },
    "@swagfoodphilly": {
        "name": "Kendo Sushi Spring Garden",
        "type": "restaurant",
        "neighborhood": "Spring Garden",
        "quote": "Kendo Sushi on Spring Garden is a sleeper hit. Fresh nigiri, creative rolls, and the omakase is surprisingly affordable for the quality. Philly's sushi scene just got a serious upgrade.",
        "date": TODAY,
    },
}

inf_count = 0
for handle, pick in picks.items():
    hi = content.find(f'handle: "{handle}"')
    if hi < 0: print(f"  Not found: {handle}"); continue
    pi = content.find("recentPicks: [", hi)
    if pi < 0 or pi > hi + 2000: print(f"  No picks: {handle}"); continue
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
    inf_count += 1; print(f"  Updated {handle}: {pick['name']}")
print(f"  Updated {inf_count}")

# ═══════════════════════════════════════
# STEP 6: DEDUP
# ═══════════════════════════════════════
print("\n=== DEDUP ===")
dupes = 0
hs_start, _ = bounds()
en = [n.lower() for n in re.findall(r'name: "([^"]+)"', content[:hs_start])]
seen = set()
for n in en:
    if n in seen: dupes += 1; print(f"  Dup event: {n}")
    seen.add(n)
_, inf_start = bounds(); hs_start, _ = bounds()
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
                    else: content = content[:idx] + content[ei:]
else:
    print("  No duplicates")

# ═══════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════
print("\n=== CLEANUP ===")
bl = len(content)
content = re.sub(r'\n\s*,\s*\n', '\n', content)
content = re.sub(r'\n{3,}', '\n\n', content)
content = re.sub(r',\s*\n(\s*\];)', r'\n\1', content)
print(f"  Cleaned {bl - len(content)} chars")

# FINAL
fe = len(re.findall(r'id: "event-', content))
fs = len(re.findall(r'id: "spot-', content))
print(f"\n=== DONE ===")
print(f"  Events: {fe}, Hotspots: {fs}")
print(f"  Removed: {past_removed}, Added events: {added_events}, Added spots: {added_spots}")
print(f"  Influencers: {inf_count}, Pruned: {pruned}, Decayed: {decayed}, Dupes: {dupes}")

with open("client/src/data/philly-data.ts", "w") as f:
    f.write(content)

json.dump({
    "past_removed": past_removed, "events_added": added_events,
    "spots_added": added_spots, "influencers": inf_count,
    "pruned": pruned, "decayed": decayed, "unmarked": unmarked,
    "dupes": dupes, "final_events": fe, "final_spots": fs,
}, open("/tmp/run13_summary.json","w"), indent=2)
print("File saved!")
