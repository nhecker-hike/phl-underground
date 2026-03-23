#!/usr/bin/env python3
"""PHL Underground Nightly Refresh #7 - Fix insertions (March 23, 2026)"""

import re

DATA_FILE = "client/src/data/philly-data.ts"

with open(DATA_FILE, "r") as f:
    content = f.read()

# ============================================================
# Insert new events before the end of the events array
# Pattern: }]; before export const hotspots
# ============================================================
new_events_ts = """  {
    id: "event-113",
    name: "The Dirty Three at Underground Arts",
    date: "2026-04-02",
    time: "8:30 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Australian instrumental trio The Dirty Three -- violin, drums, guitar -- deliver sprawling, emotionally devastating sets that feel like watching a storm roll in. A rare Philly appearance for one of the most singular live bands on the planet. If you know, you know.",
    price: "$35+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-114",
    name: "The Old 97\\'s at Underground Arts",
    date: "2026-04-03",
    time: "8:30 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Alt-country pioneers The Old 97\\'s bring decades of raucous, whiskey-soaked anthems to Underground Arts. Rhett Miller and crew are known for high-energy shows that blur the line between punk and country -- perfect for a Friday night in the basement.",
    price: "$30+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-115",
    name: "Odumodublvck at Underground Arts",
    date: "2026-04-08",
    time: "8:00 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Nigerian Afrobeats and rap star Odumodublvck brings his viral energy to Underground Arts. Known for genre-blending tracks that mix Afrobeats, amapiano, and hip-hop, this is one of the most exciting young international acts hitting Philly this spring.",
    price: "$30+",
    vibeTag: "underground",
    source: "undergroundarts.org",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-116",
    name: "Riot Nerd: Beyonce and Lady Gaga Night at Underground Arts",
    date: "2026-03-27",
    time: "10:00 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "nightlife",
    description: "A multi-room dance party celebrating the queens of pop -- Beyonce and Lady Gaga all night long. DJs spin deep cuts and hits across multiple rooms at Underground Arts. Late start, high energy, and costumes encouraged.",
    price: "$15+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-117",
    name: "Pablo Batista: Primera Primavera Latin Jazz Orchestra",
    date: "2026-04-17",
    time: "7:30 PM",
    venue: "Perelman Theater",
    address: "300 S. Broad Street, Philadelphia, PA 19102",
    neighborhood: "Center City",
    category: "music",
    description: "Grammy Award-winning percussionist Pablo Batista leads a 20-piece big band in vintage formal wear through legendary Latin jazz tunes. The inaugural Primera Primavera concert kicks off a new annual Latin jazz series at Perelman Theater -- an intimate, one-night-only affair.",
    price: "$30+",
    vibeTag: "insider",
    source: "visitphilly.com",
    lat: 39.9468,
    lng: -75.1649,
    isInsider: true,
  },
  {
    id: "event-118",
    name: "McLusky at Underground Arts",
    date: "2026-04-10",
    time: "9:00 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Welsh noise-rock cult heroes McLusky are back from the dead and louder than ever. If you missed them the first time around, this is your shot -- abrasive, witty, and absolutely ferocious in a small room. One of the most anticipated underground shows of spring.",
    price: "$25+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-119",
    name: "Cut Worms at Underground Arts",
    date: "2026-04-16",
    time: "8:30 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "Brooklyn songwriter Cut Worms channels vintage AM radio gold -- lush harmonies, twangy guitars, and a dreamy nostalgia that sounds like it was beamed in from 1966. A beautiful mid-week show for fans of lo-fi pop and classic songwriting.",
    price: "$20+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
  {
    id: "event-120",
    name: "Die Krupps at Underground Arts",
    date: "2026-03-29",
    time: "8:00 PM",
    venue: "Underground Arts",
    address: "1200 Callowhill Street, Philadelphia, PA 19123",
    neighborhood: "Callowhill",
    category: "music",
    description: "German industrial pioneers Die Krupps bring four decades of crushing electronic body music to Underground Arts. Legends of the EBM/industrial scene, known for fusing metal riffs with pounding synths. A rare US date for hardcore fans of the genre.",
    price: "$35+",
    vibeTag: "underground",
    source: "undergroundarts.org / concertfix.com",
    lat: 39.9590,
    lng: -75.1580,
    isInsider: true,
  },
"""

# Insert before the end of events array (before hotspots section)
events_end_marker = "}];\n\nexport const hotspots: HotSpot[] = ["
if events_end_marker in content:
    content = content.replace(
        events_end_marker,
        "},\n" + new_events_ts + "];\n\nexport const hotspots: HotSpot[] = ["
    )
    print("Events inserted successfully.")
else:
    print("ERROR: Could not find events end marker!")

# ============================================================
# Insert new hotspots before the end of the hotspots array
# ============================================================
new_hotspots_ts = """  {
    id: "spot-77",
    name: "Shibam Coffee",
    type: "cafe",
    address: "4700 Baltimore Avenue, Philadelphia, PA 19143",
    neighborhood: "West Philadelphia",
    description: "A rare Yemeni coffeeshop in West Philly, open until midnight on Fridays and Saturdays. Serving traditional Yemeni coffee alongside snacks in a cozy, community-driven space. One of the few late-night cafe options on the west side.",
    vibeTag: "insider",
    priceRange: "$",
    cuisine: "Yemeni coffee",
    isNew: true,
    isInsider: true,
    lat: 39.9490,
    lng: -75.2190,
    source: "Philadelphia Inquirer",
  },
  {
    id: "spot-78",
    name: "Duo Restaurant & Bar",
    type: "restaurant",
    address: "112 S. 18th Street, Philadelphia, PA 19103",
    neighborhood: "Rittenhouse",
    description: "A sleek new Center City addition offering a menu that pairs globally inspired small plates with an inventive cocktail program. Modern space with moody lighting, perfect for a date night or happy hour near Rittenhouse Square.",
    vibeTag: "trendy",
    priceRange: "$$",
    cuisine: "New American",
    isNew: true,
    isInsider: false,
    lat: 39.9521,
    lng: -75.1710,
    source: "Philadelphia Inquirer",
  },
  {
    id: "spot-79",
    name: "Carmen\\'s Table",
    type: "restaurant",
    address: "1301 S. 9th Street, Philadelphia, PA 19147",
    neighborhood: "South Philly",
    description: "A new Italian-American spot on the edge of the Italian Market serving family-style classics with a modern touch. Homemade pasta, red sauce, and a warm neighborhood vibe that feels like Sunday dinner at nonna\\'s.",
    vibeTag: "local-favorite",
    priceRange: "$$",
    cuisine: "Italian-American",
    isNew: true,
    isInsider: false,
    lat: 39.9337,
    lng: -75.1589,
    source: "Philadelphia Inquirer",
  },
  {
    id: "spot-80",
    name: "Ranstead Room",
    type: "bar",
    address: "2013 Ranstead Street, Philadelphia, PA 19103",
    neighborhood: "Rittenhouse",
    description: "One of Philly\\'s best-kept secrets -- a hidden speakeasy behind El Rey, through a nondescript black door with mirrored R\\'s. Dark, moody 1930s vibes with leather booths and some of the city\\'s finest cocktails. If you have to ask where it is, you might not find it.",
    vibeTag: "insider",
    priceRange: "$$$",
    cuisine: null,
    isNew: false,
    isInsider: true,
    lat: 39.9530,
    lng: -75.1744,
    source: "Tasting Table / Visit Philly",
  },
"""

hotspots_end_marker = "}];\n\nexport const influencers: Influencer[] = ["
if hotspots_end_marker in content:
    content = content.replace(
        hotspots_end_marker,
        "},\n" + new_hotspots_ts + "];\n\nexport const influencers: Influencer[] = ["
    )
    print("Hotspots inserted successfully.")
else:
    print("ERROR: Could not find hotspots end marker!")

with open(DATA_FILE, "w") as f:
    f.write(content)

# Verify counts
final_events = len(re.findall(r'id: "event-\d+"', content))
final_hotspots = len(re.findall(r'id: "spot-\d+"', content))
print(f"\nFinal event count: {final_events}")
print(f"Final hotspot count: {final_hotspots}")
