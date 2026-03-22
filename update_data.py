#!/usr/bin/env python3
"""PHL Underground nightly data refresh -- Run #6 (March 22, 2026)"""

import re

TODAY = "2026-03-22"
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
# 2. New events (starting at event-102)
# ────────────────────────────────────────────────
new_events = [
    {
        "id": "event-102",
        "name": "76ers Homecoming Night vs. Chicago Bulls",
        "date": "2026-03-25",
        "time": "7:00 PM",
        "venue": "Xfinity Mobile Arena",
        "address": "3601 S. Broad Street, Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "sports",
        "description": "The 76ers celebrate Homecoming Night at Xfinity Mobile Arena against the Bulls as the playoff race heats up. Part of the 25th anniversary celebration of the 2001 Eastern Conference Champions, with the first 2,001 fans scoring free gear. One of the season's final themed nights.",
        "price": "$40+",
        "vibeTag": "mainstream",
        "source": "visitphilly.com / nba.com",
        "lat": 39.9012,
        "lng": -75.1745,
        "isInsider": False,
    },
    {
        "id": "event-103",
        "name": "Southeast Asian Market Opening Day at FDR Park",
        "date": "2026-04-04",
        "time": "10:00 AM - 5:00 PM",
        "venue": "FDR Park",
        "address": "Pattison Ave & S. Broad St, Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "food-drink",
        "description": "The nationally renowned Southeast Asian Market returns for its 2026 season with 80+ vendors serving the best Lao, Khmer, Thai, Vietnamese, and Indonesian cuisine in the city. Cash recommended (no ATM on-site). This outdoor market runs Sundays through fall and is an absolute Philly insider must-visit.",
        "price": "Free entry",
        "vibeTag": "insider",
        "source": "fdrseamarket.com / visitphilly.com",
        "lat": 39.9035,
        "lng": -75.1750,
        "isInsider": True,
    },
    {
        "id": "event-104",
        "name": "Dine Latino Restaurant Week: Spring Edition",
        "date": "2026-04-06 to 2026-04-12",
        "time": "Varies",
        "venue": "Participating restaurants citywide",
        "address": "Various locations, Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "food-drink",
        "description": "Dine Latino Restaurant Week celebrates Philadelphia's vibrant Latin food scene with special prix-fixe menus and promotions at participating restaurants across the city. Explore cuisines from Mexico, Puerto Rico, Colombia, Peru, and beyond at some of Philly's best Latin-owned eateries.",
        "price": "Varies",
        "vibeTag": "local-fav",
        "source": "visitphilly.com",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": False,
    },
    {
        "id": "event-105",
        "name": "Philly Otaku Fest at Pennsylvania Convention Center",
        "date": "2026-04-10 to 2026-04-12",
        "time": "10:00 AM - 6:00 PM",
        "venue": "Pennsylvania Convention Center",
        "address": "1101 Arch St, Philadelphia, PA 19107",
        "neighborhood": "Center City",
        "category": "culture",
        "description": "Philadelphia's anime, manga, and Japanese pop culture convention returns to the Convention Center. Cosplay contests, artist alley, vendor hall, panels, and screenings. A haven for the city's growing otaku community.",
        "price": "$30+",
        "vibeTag": "insider",
        "source": "phillyfestivals.org",
        "lat": 39.9543,
        "lng": -75.1596,
        "isInsider": True,
    },
    {
        "id": "event-106",
        "name": "Philly Cocktail Fest",
        "date": "2026-04-11",
        "time": "1:00 PM - 5:00 PM",
        "venue": "TBD",
        "address": "Philadelphia, PA",
        "neighborhood": "Philadelphia",
        "category": "food-drink",
        "description": "The city's premier cocktail festival showcasing Philadelphia's booming bar scene. Sample craft cocktails from the city's top bartenders, learn about spirits, and discover why Philly has become one of the East Coast's best drinking destinations.",
        "price": "$50+",
        "vibeTag": "insider",
        "source": "phillyfestivals.org",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": True,
    },
    {
        "id": "event-107",
        "name": "Flavors on the Avenue -- East Passyunk Spring Fest",
        "date": "2026-04-26",
        "time": "12:00 PM - 5:00 PM",
        "venue": "East Passyunk Avenue",
        "address": "East Passyunk Ave (Broad to Dickinson), Philadelphia, PA 19148",
        "neighborhood": "South Philly",
        "category": "food-drink",
        "description": "South Philly comes alive during the annual Flavors on the Avenue fest, bringing East Passyunk's top restaurants together for a five-block outdoor food extravaganza. Free to attend, pay-as-you-go eating from acclaimed neighborhood restaurants plus craft market, live music, seasonal cocktails, and kid-friendly activities.",
        "price": "Free entry",
        "vibeTag": "local-fav",
        "source": "visitphilly.com / audacy.com",
        "lat": 39.9271,
        "lng": -75.1614,
        "isInsider": False,
    },
    {
        "id": "event-108",
        "name": "Festival of Colors at Philadelphia Zoo",
        "date": "2026-04-25",
        "time": "11:30 AM - 3:30 PM",
        "venue": "Philadelphia Zoo",
        "address": "3400 W Girard Ave, Philadelphia, PA 19104",
        "neighborhood": "West Philly",
        "category": "culture",
        "description": "The nation's first zoo celebrates spring with the Festival of Colors, presented with the Council of Indian Organizations. A day of Indian music, dancing, kids activities, food, and art featuring artists from Philadelphia's Indian-American community. A unique cultural celebration in a beautiful setting.",
        "price": "Zoo admission",
        "vibeTag": "local-fav",
        "source": "visitphilly.com",
        "lat": 39.9710,
        "lng": -75.1955,
        "isInsider": False,
    },
    {
        "id": "event-109",
        "name": "Free Throw at Union Transfer",
        "date": "2026-04-18",
        "time": "7:30 PM",
        "venue": "Union Transfer",
        "address": "1026 Spring Garden St, Philadelphia, PA 19123",
        "neighborhood": "Spring Garden",
        "category": "music",
        "description": "Emo-punk favorites Free Throw bring their cathartic, sing-along anthems to Union Transfer. A perfect midsize venue show for fans of the Midwest emo revival scene. Expect crowd surfers, heartfelt lyrics, and a packed room.",
        "price": "$20+",
        "vibeTag": "insider",
        "source": "concertfix.com / utphilly.com",
        "lat": 39.9614,
        "lng": -75.1551,
        "isInsider": True,
    },
    {
        "id": "event-110",
        "name": "Dining Out for Life Philadelphia",
        "date": "2026-04-16",
        "time": "All Day",
        "venue": "Participating restaurants citywide",
        "address": "Various locations, Philadelphia, PA",
        "neighborhood": "Citywide",
        "category": "food-drink",
        "description": "Dine out and do good -- the 36th annual Dining Out for Life benefits Action Wellness with participating restaurants donating a portion of sales. Dozens of Philly eateries join in, including Good Dog Bar, Jack's Firehouse, Urban Village Brewing, and all 16 Stephen Starr restaurants. Eat well, support a great cause.",
        "price": "Varies",
        "vibeTag": "local-fav",
        "source": "visitphilly.com",
        "lat": 39.9526,
        "lng": -75.1652,
        "isInsider": False,
    },
    {
        "id": "event-111",
        "name": "South 9th Street Italian Market Festival",
        "date": "2026-05-16 to 2026-05-17",
        "time": "10:00 AM - 5:00 PM",
        "venue": "9th Street Italian Market",
        "address": "S 9th Street, Philadelphia, PA 19147",
        "neighborhood": "South Philly",
        "category": "food-drink",
        "description": "One of Philadelphia's most popular events: seven city blocks of the Italian Market transform into a celebration of culture, gastronomy, art, and music. Over 100 vendors showcase a range of cuisines and beverages, plus live music, local artists, and crafters. A true Philly institution.",
        "price": "Free entry",
        "vibeTag": "local-fav",
        "source": "italianmarketphilly.org",
        "lat": 39.9381,
        "lng": -75.1581,
        "isInsider": False,
    },
]

# Check for duplicates against existing
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
# 3. New hotspots (starting at spot-73)
# ────────────────────────────────────────────────
new_hotspots = [
    {
        "id": "spot-73",
        "name": "Fermentery Form",
        "type": "bar",
        "address": "1700 N Palethorp St, Philadelphia, PA 19122",
        "neighborhood": "Kensington",
        "description": "Tucked down an unassuming alley in Kensington, this unconventional microbrewery is one of Philly's most unique hidden gems. Wild-fermented beers, natural wines, and an intimate, off-the-grid atmosphere that feels like a well-kept secret. A true insider destination for craft beer devotees.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": "craft beer / natural wine",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9784,
        "lng": -75.1380,
        "source": "phillyprgirl.com / yelp.com",
    },
    {
        "id": "spot-74",
        "name": "Carolyn's Vietnamese",
        "type": "restaurant",
        "address": "Philadelphia, PA",
        "neighborhood": "Philadelphia",
        "description": "A buzzy new Vietnamese restaurant that's been generating attention from Philly's food influencer community. Part of a wave of exciting independent openings bringing diverse flavors to the city's constantly evolving dining scene.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": "Vietnamese",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9526,
        "lng": -75.1652,
        "source": "instagram.com / phillymag.com",
    },
    {
        "id": "spot-75",
        "name": "Schmaltz",
        "type": "restaurant",
        "address": "Philadelphia, PA",
        "neighborhood": "Philadelphia",
        "description": "A new concept specializing in Jewish comfort food with a focus on latkes and other classics. Part of the exciting 2026 wave of Philly openings from passionate local food entrepreneurs, generating strong social media buzz among Philly food creators.",
        "vibeTag": "insider",
        "priceRange": "$$",
        "cuisine": "Jewish deli / comfort food",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9526,
        "lng": -75.1652,
        "source": "instagram.com / inquirer.com",
    },
    {
        "id": "spot-76",
        "name": "O'Morrey's",
        "type": "bar",
        "address": "1720 Sansom St, Philadelphia, PA 19103",
        "neighborhood": "Rittenhouse",
        "description": "An upcoming cocktail bar from the Ripplewood/Izzy's team (Biff Gottehrer and Kenjiro Omori) in the former Genji space. The name is a playful rendering of Omori's surname. Expect the same polished cocktail craft that made Ripplewood a whiskey destination, now in Center City.",
        "vibeTag": "insider",
        "priceRange": "$$$",
        "cuisine": "cocktails",
        "isNew": True,
        "isInsider": True,
        "lat": 39.9505,
        "lng": -75.1700,
        "source": "inquirer.com / phillymag.com",
    },
]

# Check for dupes
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
    "@wooder_ice": [
        {
            "name": "Wooder Ice Happy Hour at Uchi",
            "type": "spot",
            "neighborhood": "Rittenhouse",
            "quote": "Philly food lovers, clear your calendars. Wooder Ice hosted a special Happy Hour at Uchi -- one of the hottest new sushi spots in the city. The vibes were immaculate.",
            "date": "2026-03-11",
        },
    ],
    "@josheatsphilly": [
        {
            "name": "Restaurant Turn-Ons and Turn-Offs",
            "type": "spot",
            "neighborhood": "Philadelphia",
            "quote": "Josh stopped by the Mike Late Show to share his top restaurant turn-ons and turn-offs in the Philly dining scene. The conversation every food lover needs to hear.",
            "date": "2026-03-06",
        },
    ],
    "@djour.philly": [
        {
            "name": "Manong in Fairmount",
            "type": "spot",
            "neighborhood": "Fairmount",
            "quote": "Big name chefs pivoting towards approachable and affordable. Money's tight and nostalgia always comforts. Manong in Fairmount -- for how much I spit venom on Fairmount, it's one of my favorite neighborhoods.",
            "date": "2026-01-15",
        },
    ],
    "@swagfoodphilly": [
        {
            "name": "Southeast Asian Market at FDR Park",
            "type": "event",
            "neighborhood": "South Philly",
            "quote": "PSA: the Southeast Asian Market is back at FDR Park on April 4th! With over 80+ vendors, this is one of the best outdoor food experiences in the city. Don't sleep on it.",
            "date": "2026-03-17",
        },
    ],
    "@thephillyfoodfanatic": [
        {
            "name": "Cherry Blossom Festival Preview",
            "type": "event",
            "neighborhood": "Fairmount Park",
            "quote": "The Cherry Blossom Festival is this weekend (March 28-29) at Fairmount Park. Food, performances, and the most beautiful spring blooms in the city. Get your tickets now!",
            "date": "2026-03-20",
        },
    ],
    "@cass_andthecity": [
        {
            "name": "Spring Dining in Philly",
            "type": "spot",
            "neighborhood": "Philadelphia",
            "quote": "The best vibe to catch in 2026? That Philly Pheeling. When you're ready to catch it, I'm here to get you there. Spring dining season is officially on.",
            "date": "2026-03-10",
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


# Rebuild events
new_events_ts = ",\n".join([event_to_ts(ev) for ev in actually_new_events])
rebuilt_events = ",".join(kept_events)
if actually_new_events:
    rebuilt_events += ",\n" + new_events_ts

content = content[:events_match.start(2)] + rebuilt_events + content[events_match.end(2):]

# Re-find hotspots match
hotspots_match = re.search(r'(export const hotspots: HotSpot\[\] = \[)(.*?)(\];)', content, re.DOTALL)

# Rebuild hotspots
new_spots_ts = ",\n".join([spot_to_ts(sp) for sp in actually_new_spots])
rebuilt_spots = hotspots_match.group(2)
if actually_new_spots:
    rebuilt_spots += ",\n" + new_spots_ts

content = content[:hotspots_match.start(2)] + rebuilt_spots + content[hotspots_match.end(2):]

# ────────────────────────────────────────────────
# 6. Update influencer recentPicks
# ────────────────────────────────────────────────
def add_pick(content, handle, pick):
    quote_esc = pick["quote"].replace("'", "\\'").replace('"', '\\"')
    name_esc = pick["name"].replace("'", "\\'").replace('"', '\\"')
    new_pick = f"""      {{
        name: "{name_esc}",
        type: "{pick['type']}",
        neighborhood: "{pick['neighborhood']}",
        quote: "{quote_esc}",
        date: "{pick['date']}",
      }}"""

    handle_pos = content.find(f'handle: "{handle}"')
    if handle_pos == -1:
        print(f"  WARNING: Could not find handle {handle}")
        return content

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
        print(f"  Added pick for {handle}: {pick['name']}")

print(f"\nInfluencer picks added: {influencer_update_count}")

# ────────────────────────────────────────────────
# 7. DEDUPLICATION
# ────────────────────────────────────────────────
print("\n--- DEDUPLICATION CHECK ---")

events_match2 = re.search(r'export const events: PhillyEvent\[\] = \[(.*?)\];', content, re.DOTALL)
event_blocks2 = re.findall(r'\s*\{[^{}]*?\}', events_match2.group(1))

seen_event_names = {}
event_dupes = 0
deduped_events = []
for block in event_blocks2:
    nm = re.search(r'name:\s*"([^"]*)"', block)
    if nm:
        key = nm.group(1).lower().replace("\\'", "'")
        if key in seen_event_names:
            existing_desc = re.search(r'description:\s*"([^"]*)"', seen_event_names[key])
            new_desc = re.search(r'description:\s*"([^"]*)"', block)
            if new_desc and existing_desc and len(new_desc.group(1)) > len(existing_desc.group(1)):
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
