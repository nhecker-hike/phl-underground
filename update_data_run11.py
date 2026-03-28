#!/usr/bin/env python3
"""
PHL Underground Nightly Data Refresh #11 (2026-03-28)
"""
import re, json
from datetime import datetime

TODAY = "2026-03-28"
TODAY_DT = datetime.strptime(TODAY, "%Y-%m-%d")

with open("client/src/data/philly-data.ts", "r") as f:
    content = f.read()

def get_names(section):
    return set(n.lower() for n in re.findall(r'name: "([^"]+)"', section))

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")

def bounds():
    return content.find("export const hotspots"), content.find("export const influencers")

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
ev_section = content[:hs_start]
blocks = list(re.finditer(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', ev_section, re.DOTALL))
past_removed = 0

for match in reversed(blocks):
    block = match.group(1)
    dm = re.search(r'date: "(\d{4}-\d{2}-\d{2})"', block)
    if dm and datetime.strptime(dm.group(1), "%Y-%m-%d") < TODAY_DT:
        nm = re.search(r'name: "([^"]+)"', block)
        print(f"  Removing: {nm.group(1) if nm else '?'} ({dm.group(1)})")
        s, e = match.start(), match.end()
        after = ev_section[e:e+20]
        before = ev_section[max(0,s-20):s]
        if after.lstrip().startswith(','):
            ev_section = ev_section[:s] + ev_section[e + after.index(',') + 1:]
        elif before.rstrip().endswith(','):
            lc = ev_section[:s].rstrip().rfind(',')
            ev_section = ev_section[:lc] + ev_section[e:]
        else:
            ev_section = ev_section[:s] + ev_section[e:]
        past_removed += 1

content = ev_section + content[hs_start:]
print(f"  Removed {past_removed} past events")

# ═══════════════════════════════════════
# STEP 2: ADD NEW EVENTS
# ═══════════════════════════════════════
print("\n=== ADDING NEW EVENTS ===")
hs_start, _ = bounds()
existing_ev = get_names(content[:hs_start])

new_events = [
    {
        "name": "The Format with Ben Kweller at Franklin Music Hall",
        "date": "2026-03-28",
        "time": "6:50 PM",
        "venue": "Franklin Music Hall",
        "address": "421 N 7th St, Philadelphia, PA 19123",
        "neighborhood": "Northern Liberties",
        "category": "concert",
        "description": "Indie-pop favorites The Format reunite at Franklin Music Hall with Ben Kweller and Adult Mom opening. The band is donating $1 from every ticket to fight food insecurity and fund local animal shelters. All ages.",
        "price": "$40+",
        "vibeTag": "trending",
        "source": "franklinmusichall.com",
        "lat": 39.9618, "lng": -75.1480,
        "isInsider": False,
    },
    {
        "name": "Sabrina Claudio: Fall In Love With Her Tour at TLA",
        "date": "2026-03-28",
        "time": "8:00 PM",
        "venue": "Theatre of Living Arts",
        "address": "334 South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "concert",
        "description": "R&B singer-songwriter Sabrina Claudio brings her sultry, intimate sound to the TLA on her Fall In Love With Her Tour. Dylan Sinclair opens. A vibe-heavy Saturday night for R&B lovers.",
        "price": "$50+",
        "vibeTag": "after-dark",
        "source": "ticketmaster.com",
        "lat": 39.9427, "lng": -75.1487,
        "isInsider": False,
    },
    {
        "name": "TobyMac Hits Deep Tour at The Liacouras Center",
        "date": "2026-03-28",
        "time": "7:00 PM",
        "venue": "The Liacouras Center",
        "address": "1776 N Broad St, Philadelphia, PA 19121",
        "neighborhood": "North Broad",
        "category": "concert",
        "description": "Christian music powerhouse TobyMac brings the Hits Deep Tour to The Liacouras Center with Crowder and Jeremy Camp. A massive production with uplifting energy and sing-along anthems.",
        "price": "$30+",
        "vibeTag": "family-friendly",
        "source": "nationaltoday.com",
        "lat": 39.9812, "lng": -75.1565,
        "isInsider": False,
    },
    {
        "name": "Whisper\\'s Wicked Cabaret at Velvet Whip",
        "date": "2026-04-11",
        "time": "9:00 PM",
        "venue": "Velvet Whip Arts & Social Club",
        "address": "Near 11th & Wood St, Philadelphia, PA 19107",
        "neighborhood": "Eraserhood / Callowhill",
        "category": "nightlife",
        "description": "The hottest performers on the East Coast set the stage ablaze with bewitching acts and sensational flair at this underground cabaret night. Velvet Whip is a hidden gem in the Eraserhood -- intimate, moody, and completely off the beaten path.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "velvetwhipphilly.com",
        "lat": 39.9580, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "City Wide Sessions Jazz Jam at Velvet Whip",
        "date": "2026-04-16",
        "time": "7:00 PM",
        "venue": "Velvet Whip Arts & Social Club",
        "address": "Near 11th & Wood St, Philadelphia, PA 19107",
        "neighborhood": "Eraserhood / Callowhill",
        "category": "nightlife",
        "description": "City Wide Sessions returns after 3 years -- an open jam night where Philly musicians show up, sit in, and create. A high-quality house band anchors the night while seasoned players and newcomers collaborate. The room is real, the energy is right.",
        "price": "$10",
        "vibeTag": "underground",
        "source": "velvetwhipphilly.com",
        "lat": 39.9580, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "Les Classiques: Erotic Burlesque Affair at Velvet Whip",
        "date": "2026-04-17",
        "time": "9:00 PM",
        "venue": "Velvet Whip Arts & Social Club",
        "address": "Near 11th & Wood St, Philadelphia, PA 19107",
        "neighborhood": "Eraserhood / Callowhill",
        "category": "nightlife",
        "description": "Burlesque Queen Goldi Fox hosts a birthday bash dipped in Southern heat and rhinestones at Philly\\'s most underground cabaret venue. Lowbrow lovers and cabaret connoisseurs unite for a night of boundary-pushing performance art.",
        "price": "$25+",
        "vibeTag": "underground",
        "source": "velvetwhipphilly.com",
        "lat": 39.9580, "lng": -75.1573,
        "isInsider": True,
    },
    {
        "name": "together PANGEA & The Red Pears at The Foundry",
        "date": "2026-04-19",
        "time": "8:00 PM",
        "venue": "The Foundry at The Fillmore",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "LA garage-rock favorites together PANGEA and The Red Pears bring raw, high-energy indie-punk to The Foundry. A smaller, sweatier room for a louder, more intimate show. This is the insider pick of the weekend.",
        "price": "$20+",
        "vibeTag": "underground",
        "source": "thefillmorephilly.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": True,
    },
    {
        "name": "Wallice at The Foundry",
        "date": "2026-04-20",
        "time": "8:00 PM",
        "venue": "The Foundry at The Fillmore",
        "address": "29 E Allen St, Philadelphia, PA 19123",
        "neighborhood": "Fishtown",
        "category": "concert",
        "description": "Rising indie-pop artist Wallice brings her quirky, genre-bending sound to The Foundry. Known for blending lo-fi bedroom pop with jazz influences, she is one of the most exciting emerging acts on the indie circuit.",
        "price": "$18+",
        "vibeTag": "trending",
        "source": "thefillmorephilly.com",
        "lat": 39.9680, "lng": -75.1340,
        "isInsider": True,
    },
    {
        "name": "Vincent Mason at Theatre of Living Arts",
        "date": "2026-04-25",
        "time": "8:00 PM",
        "venue": "Theatre of Living Arts",
        "address": "334 South St, Philadelphia, PA 19147",
        "neighborhood": "South Street",
        "category": "concert",
        "description": "Monster Energy Outbreak Tour presents Vincent Mason with his There I Go Tour. An emerging hip-hop and R&B voice bringing introspective bars and smooth production to the TLA stage.",
        "price": "$25+",
        "vibeTag": "trending",
        "source": "ticketmaster.com",
        "lat": 39.9427, "lng": -75.1487,
        "isInsider": False,
    },
    {
        "name": "Linvilla Orchards Food Truck Frenzy",
        "date": "2026-04-25 to 2026-04-26",
        "time": "11:00 AM - 5:00 PM",
        "venue": "Linvilla Orchards",
        "address": "137 W Knowlton Rd, Media, PA 19063",
        "neighborhood": "Delaware County",
        "category": "food",
        "description": "A weekend of food trucks, live music, and orchard vibes at Linvilla. Dozens of trucks park among the apple trees for a chill suburban food fest with family-friendly activities, hayrides, and local craft vendors.",
        "price": "Free entry, pay for food",
        "vibeTag": "family-friendly",
        "source": "phillyfestivals.org",
        "lat": 39.9100, "lng": -75.3880,
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

# ═══════════════════════════════════════
# STEP 3: ADD NEW HOTSPOTS
# ═══════════════════════════════════════
print("\n=== ADDING NEW HOTSPOTS ===")
hs_start, inf_start = bounds()
existing_hs = get_names(content[hs_start:inf_start])

new_hotspots = [
    {
        "name": "Velvet Whip Arts & Social Club",
        "type": "Bar / Venue",
        "address": "Near 11th & Wood St, Philadelphia, PA 19107",
        "neighborhood": "Eraserhood / Callowhill",
        "description": "A hidden cabaret and arts club in the Eraserhood near Chinatown. Live jazz every Tuesday, burlesque nights, whisky tastings, open mic jams, and the kind of underground programming that makes Philly nightlife special. Enter through a nondescript door -- if you know, you know.",
        "vibeTag": "underground",
        "priceRange": "$$",
        "cuisine": None,
        "isNew": True,
        "isInsider": True,
        "lat": 39.9580, "lng": -75.1573,
        "source": "velvetwhipphilly.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Supérette",
        "type": "Bar / Wine Bar",
        "address": "1538 E Passyunk Ave, Philadelphia, PA 19147",
        "neighborhood": "East Passyunk",
        "description": "A natural wine bar on East Passyunk with a rotating by-the-glass list, small plates, and a neighborhood vibe that feels like drinking at your coolest friend\\'s apartment. Buzzy and intimate.",
        "vibeTag": "trending",
        "priceRange": "$$",
        "cuisine": "Wine Bar / Small Plates",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9325, "lng": -75.1600,
        "source": "theinfatuation.com",
        "addedDate": TODAY,
        "trendingScore": 80,
    },
    {
        "name": "Bob & Barbara\\'s Lounge",
        "type": "Dive Bar",
        "address": "1509 South St, Philadelphia, PA 19146",
        "neighborhood": "South Street",
        "description": "The birthplace of the Citywide Special -- a shot of Jim Beam and a PBR tallboy for $6. Legendary South Street dive with live music, Thursday night drag shows, and a timeless Philly atmosphere. If you haven\\'t been, you haven\\'t really done Philly nightlife.",
        "vibeTag": "local-favorite",
        "priceRange": "$",
        "cuisine": None,
        "isNew": False,
        "isInsider": True,
        "lat": 39.9437, "lng": -75.1720,
        "source": "theinfatuation.com",
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
    nm_m = re.search(r'isNew: (true|false)', b)
    name_m = re.search(r'name: "([^"]+)"', b)
    if not am or not sm: continue

    ad = datetime.strptime(am.group(1), "%Y-%m-%d")
    sc = int(sm.group(1))
    insider = im and im.group(1) == "true"
    isnew = nm_m and nm_m.group(1) == "true"
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
        hs_sec = content[hs_start:inf_start]
        bm = re.search(re.escape(name_m.group(0)), hs_sec)
        if bm:
            np = hs_start + bm.start()
            sz = content[np:np+500]
            nm2 = re.search(r'isNew: true', sz)
            if nm2:
                ap = np + nm2.start()
                content = content[:ap] + "isNew: false" + content[ap+len("isNew: true"):]
                unmarked += 1
                print(f"  Unmarked isNew: {name} ({age}d)")

hs_start, inf_start = bounds()
final_spots = len(re.findall(r'id: "spot-', content[hs_start:inf_start]))
print(f"  Pruned: {pruned}, Decayed: {decayed}, Unmarked: {unmarked}, Final: {final_spots}")

# ═══════════════════════════════════════
# STEP 5: INFLUENCER UPDATES
# ═══════════════════════════════════════
print("\n=== INFLUENCER UPDATES ===")
picks = {
    "@wooder_ice": {
        "name": "Cherry Blossom Sakura Weekend",
        "type": "event",
        "neighborhood": "Fairmount Park",
        "quote": "Sakura Weekend is HERE. Cherry Blossom Festival in Fairmount Park today and tomorrow. Tea ceremonies, taiko drums, cosplay, karaoke, beer garden, and 100-year-old cherry trees at peak bloom. This is peak Philly spring.",
        "date": TODAY,
    },
    "@feedingtimetv": {
        "name": "Uchi Philadelphia Happy Hour",
        "type": "restaurant",
        "neighborhood": "Center City",
        "quote": "Uchi happy hour is an underrated Philly move. Half-price sashimi, creative cocktails, and that sleek Sansom St vibe. Get there early because the bar fills up fast.",
        "date": TODAY,
    },
    "@josheatsphilly": {
        "name": "Velvet Whip Jazz Night",
        "type": "nightlife",
        "neighborhood": "Eraserhood",
        "quote": "Found a hidden cabaret spot in the Eraserhood called Velvet Whip. Live jazz every Tuesday, whisky tastings, burlesque nights. You literally walk through a nondescript door. This is the underground Philly I live for.",
        "date": TODAY,
    },
    "@thephillyfoodfanatic": {
        "name": "Secondhand Ranch Fishtown",
        "type": "bar",
        "neighborhood": "Fishtown",
        "quote": "Secondhand Ranch in Fishtown is part cocktail bar, part vintage thrift shop. Sip a craft drink while browsing curated vintage. The aesthetic is immaculate and the drinks are seriously good.",
        "date": TODAY,
    },
    "@cass_andthecity": {
        "name": "The Format at Franklin Music Hall",
        "type": "event",
        "neighborhood": "Northern Liberties",
        "quote": "The Format reuniting at Franklin Music Hall tonight! Indie-pop nostalgia with Ben Kweller opening. They are donating $1 from every ticket to local food banks and animal shelters. Love that energy.",
        "date": TODAY,
    },
    "@phillyfoodladies": {
        "name": "Casa Oui All-Day Dining",
        "type": "restaurant",
        "neighborhood": "Queen Village",
        "quote": "Casa Oui in Queen Village does all-day so well. French-Mexican fusion that works morning to night. Beignets and breakfast tacos for brunch, steak and cocktails for dinner. New neighborhood staple.",
        "date": TODAY,
    },
    "@fueledonphilly": {
        "name": "Manna Bakery Kensington",
        "type": "restaurant",
        "neighborhood": "Kensington",
        "quote": "Manna Bakery finally has a permanent home in Kensington. Their sourdough and pastries were already legendary from farmers markets. Now you can get them any day of the week. Game changer.",
        "date": TODAY,
    },
    "@koryaversa": {
        "name": "Sabrina Claudio at TLA",
        "type": "event",
        "neighborhood": "South Street",
        "quote": "Sabrina Claudio at TLA tonight. Fall In Love With Her Tour. That venue plus her voice is going to be something special. South Street Saturday night done right.",
        "date": TODAY,
    },
    "@djour.philly": {
        "name": "Cherry Blossom Festival Day One",
        "type": "event",
        "neighborhood": "Fairmount Park",
        "quote": "Cherry Blossom Festival day one was beautiful. The trees are at peak bloom, the food vendors are amazing, and the cultural performances are next level. Day two is tomorrow -- do not miss it.",
        "date": TODAY,
    },
    "@swagfoodphilly": {
        "name": "Grace & Proper Bella Vista",
        "type": "bar",
        "neighborhood": "Bella Vista",
        "quote": "Grace & Proper in Bella Vista might be the tiniest bar in Philly but the vibes are massive. Portuguese tapas, cava, potato chips with salami, and a crowd that gets louder every hour. Perfect corner bar energy.",
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
    np = f"""
      {{
        name: "{esc(pick['name'])}",
        type: "{pick['type']}",
        neighborhood: "{pick['neighborhood']}",
        quote: "{esc(pick['quote'])}",
        date: "{pick['date']}",
      }},"""
    content = content[:po] + np + content[po:]
    inf_count += 1
    print(f"  Updated {handle}: {pick['name']}")

print(f"  Updated {inf_count} influencers")

# ═══════════════════════════════════════
# STEP 6: DEDUPLICATION
# ═══════════════════════════════════════
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
seen = set()
for i in aids:
    if i in seen: dupes += 1; print(f"  Dup ID: {i}")
    seen.add(i)

if dupes > 0:
    print(f"  Removing {dupes} duplicates...")
    hs_start, _ = bounds()
    eblocks = re.findall(r'(\{[^{}]*?id: "event-\d+"[^{}]*?\})', content[:hs_start], re.DOTALL)
    nmap = {}
    for bl in eblocks:
        nm = re.search(r'name: "([^"]+)"', bl)
        if nm:
            k = nm.group(1).lower()
            nmap.setdefault(k, []).append(bl)
    for k, bls in nmap.items():
        if len(bls) > 1:
            bls.sort(key=len, reverse=True)
            for d in bls[1:]:
                idx = content.find(d)
                if idx >= 0:
                    ei = idx + len(d)
                    af = content[ei:ei+20]
                    bf = content[max(0,idx-20):idx]
                    if af.lstrip().startswith(','):
                        content = content[:idx] + content[ei+af.index(',')+1:]
                    elif bf.rstrip().endswith(','):
                        lc = content[:idx].rstrip().rfind(',')
                        content = content[:lc] + content[ei:]
                    else:
                        content = content[:idx] + content[ei:]
else:
    print("  No duplicates")

print(f"  Total: {dupes}")

# ═══════════════════════════════════════
# STEP 7: CLEANUP
# ═══════════════════════════════════════
print("\n=== CLEANUP ===")
bl = len(content)
content = re.sub(r'\n\s*,\s*\n', '\n', content)
content = re.sub(r'\n{3,}', '\n\n', content)
content = re.sub(r',\s*\n(\s*\];)', r'\n\1', content)
print(f"  Cleaned {bl - len(content)} chars")

# ═══════════════════════════════════════
# FINAL
# ═══════════════════════════════════════
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
}, open("/tmp/run11_summary.json","w"), indent=2)
print("File saved!")
