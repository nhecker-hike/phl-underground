import { useState, useMemo } from "react";
import { MapView } from "@/components/MapView";
import { EventCard } from "@/components/EventCard";
import { SpotCard } from "@/components/SpotCard";
import { EventDrawer, SpotDrawer } from "@/components/DetailDrawer";
import { FilterChips } from "@/components/FilterChips";
import {
  events,
  hotspots,
  influencers,
  type PhillyEvent,
  type HotSpot,
  type Influencer,
} from "@/data/philly-data";
import { Sparkles, TrendingUp } from "lucide-react";

const categories = ["All", "Events", "Food", "Nightlife", "Music", "Arts", "Outdoor", "Insider Picks"] as const;

function getInitials(name: string) {
  return name.split(/\s+/).map((w) => w[0]).slice(0, 2).join("").toUpperCase();
}

/** Short display name for the influencer picker */
function getShortName(name: string): string {
  // Remove parenthetical parts
  const clean = name.replace(/\s*\(.*\)\s*/, "").trim();
  // Known short mappings
  const map: Record<string, string> = {
    "Wooder Ice": "Wooder",
    "FeedingTimeTV": "FeedingTime",
    "The Philly Food Fanatic": "Fanatic",
    "Josh Moore": "Josh",
    "Cass Matthews": "Cass",
    "Philly Food Ladies": "FoodLadies",
    "Fueled on Philly": "Fueled",
    "Kory Aversa": "Kory",
    "Djour Philly": "Djour",
    "SwagFoodPhilly": "SwagFood",
  };
  return map[clean] ?? clean.split(/\s/)[0];
}

/** Check if an influencer has posted in March 2026 (i.e. "recent") */
function hasRecentPost(influencer: Influencer): boolean {
  return influencer.recentPicks.some((pick) => {
    const d = pick.date.toLowerCase();
    return d.includes("march") && d.includes("2026");
  });
}

/** Match influencer picks against events and hotspots by name */
function getInfluencerMatches(influencer: Influencer) {
  const pickNames = influencer.recentPicks.map((p: { name: string }) => p.name.toLowerCase());
  const matchedEvents = events.filter((e: PhillyEvent) =>
    pickNames.some((pn: string) => e.name.toLowerCase().includes(pn) || pn.includes(e.name.toLowerCase()))
  );
  const matchedSpots = hotspots.filter((s: HotSpot) =>
    pickNames.some((pn: string) => s.name.toLowerCase().includes(pn) || pn.includes(s.name.toLowerCase()))
  );
  return { events: matchedEvents, spots: matchedSpots };
}

export function ExplorePage() {
  const [category, setCategory] = useState<string>("All");
  const [selectedEvent, setSelectedEvent] = useState<PhillyEvent | null>(null);
  const [selectedSpot, setSelectedSpot] = useState<HotSpot | null>(null);
  const [selectedInfluencer, setSelectedInfluencer] = useState<Influencer | null>(null);

  const influencerMatches = useMemo(() => {
    if (!selectedInfluencer) return null;
    return getInfluencerMatches(selectedInfluencer);
  }, [selectedInfluencer]);

  const filteredMapEvents = useMemo(() => {
    if (influencerMatches) return influencerMatches.events;
    return undefined;
  }, [influencerMatches]);

  const filteredMapSpots = useMemo(() => {
    if (influencerMatches) return influencerMatches.spots;
    return undefined;
  }, [influencerMatches]);

  const feedItems = useMemo(() => {
    let items: Array<{ type: "event"; data: PhillyEvent } | { type: "spot"; data: HotSpot }> = [];

    if (selectedInfluencer && influencerMatches) {
      const eItems = influencerMatches.events.map((e) => ({ type: "event" as const, data: e }));
      const sItems = influencerMatches.spots.map((h) => ({ type: "spot" as const, data: h }));
      const combined: typeof items = [];
      const max = Math.max(eItems.length, sItems.length);
      for (let i = 0; i < max; i++) {
        if (eItems[i]) combined.push(eItems[i]);
        if (sItems[i]) combined.push(sItems[i]);
      }
      return combined.length > 0 ? combined : [
        ...events.slice(0, 4).map((e) => ({ type: "event" as const, data: e })),
      ];
    }

    if (category === "All" || category === "Events") {
      items.push(...events.map((e) => ({ type: "event" as const, data: e })));
    }
    if (category === "All" || category === "Food") {
      items.push(...events.filter((e) => e.category === "food").map((e) => ({ type: "event" as const, data: e })));
      items.push(...hotspots.filter((h) => h.type === "restaurant" || h.type === "cafe").map((h) => ({ type: "spot" as const, data: h })));
    }
    if (category === "Nightlife") {
      items.push(...events.filter((e) => e.category === "nightlife").map((e) => ({ type: "event" as const, data: e })));
      items.push(...hotspots.filter((h) => h.type === "bar" || h.type === "venue").map((h) => ({ type: "spot" as const, data: h })));
    }
    if (category === "Music") {
      items.push(...events.filter((e) => e.category === "music").map((e) => ({ type: "event" as const, data: e })));
      items.push(...hotspots.filter((h) => h.type === "venue").map((h) => ({ type: "spot" as const, data: h })));
    }
    if (category === "Arts") {
      items.push(...events.filter((e) => e.category === "arts").map((e) => ({ type: "event" as const, data: e })));
    }
    if (category === "Outdoor") {
      items.push(...events.filter((e) => e.category === "outdoor").map((e) => ({ type: "event" as const, data: e })));
    }
    if (category === "Insider Picks") {
      items.push(...events.filter((e) => e.isInsider).map((e) => ({ type: "event" as const, data: e })));
      items.push(...hotspots.filter((h) => h.isInsider).map((h) => ({ type: "spot" as const, data: h })));
    }

    if (category !== "All" && category !== "Events") {
      const seen = new Set<string>();
      items = items.filter((item) => {
        const key = item.type + (item.type === "event" ? (item.data as PhillyEvent).name : (item.data as HotSpot).name);
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }

    if (category === "All") {
      const eventItems = events.slice(0, 10).map((e) => ({ type: "event" as const, data: e }));
      const spotItems = hotspots.slice(0, 10).map((h) => ({ type: "spot" as const, data: h }));
      items = [];
      const max = Math.max(eventItems.length, spotItems.length);
      for (let i = 0; i < max; i++) {
        if (eventItems[i]) items.push(eventItems[i]);
        if (spotItems[i]) items.push(spotItems[i]);
      }
    }

    return items;
  }, [category, selectedInfluencer, influencerMatches]);

  return (
    <div className="min-h-screen" data-testid="page-explore">
      {/* Influencer Picker */}
      <div className="px-4 sm:px-6 lg:px-8 pt-5 pb-2 max-w-7xl mx-auto">
        <div
          className="flex items-start gap-3 sm:gap-4 overflow-x-auto pb-3 pt-2 px-2 scrollbar-hide justify-center"
          data-testid="influencer-picker"
        >
          {/* All button */}
          <button
            onClick={() => setSelectedInfluencer(null)}
            className={`flex flex-col items-center gap-1.5 flex-shrink-0 transition-all ${
              !selectedInfluencer ? "opacity-100" : "opacity-50 hover:opacity-80"
            }`}
            data-testid="influencer-all"
          >
            <div className="relative">
              <div
                className={`w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                  !selectedInfluencer
                    ? "bg-primary/20 text-primary ring-2 ring-primary ring-offset-2 ring-offset-background"
                    : "bg-white/10 text-muted-foreground"
                }`}
              >
                All
              </div>
            </div>
            <span className={`text-[10px] text-center leading-tight ${!selectedInfluencer ? "text-primary font-semibold" : "text-muted-foreground"}`}>
              All
            </span>
          </button>

          {influencers.map((inf) => {
            const isRecent = hasRecentPost(inf);
            const isSelected = selectedInfluencer?.id === inf.id;
            return (
              <button
                key={inf.id}
                onClick={() => setSelectedInfluencer(isSelected ? null : inf)}
                className={`flex flex-col items-center gap-1.5 flex-shrink-0 transition-all ${
                  isSelected ? "opacity-100" : "opacity-60 hover:opacity-90"
                }`}
                data-testid={`influencer-pick-${inf.id}`}
              >
                <div className="relative">
                  {/* Pulse ring for recent posters */}
                  {isRecent && !isSelected && (
                    <div className="absolute inset-0 rounded-full influencer-pulse" />
                  )}
                  {/* Active dot indicator */}
                  {isRecent && (
                    <div className="absolute -top-0.5 -right-0.5 z-10">
                      <div className="w-3 h-3 rounded-full bg-emerald-400 border-2 border-background pulse-dot" />
                    </div>
                  )}
                  <div
                    className={`w-12 h-12 sm:w-14 sm:h-14 rounded-full overflow-hidden transition-all ${
                      isSelected
                        ? "ring-2 ring-primary ring-offset-2 ring-offset-background"
                        : isRecent
                          ? "ring-2 ring-primary/40"
                          : ""
                    }`}
                  >
                    {inf.avatar ? (
                      <img
                        src={`${import.meta.env.BASE_URL}${inf.avatar.replace('./', '')}`}
                        alt={inf.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.style.display = "none";
                          const fallback = target.nextElementSibling as HTMLElement;
                          if (fallback) fallback.style.display = "flex";
                        }}
                      />
                    ) : null}
                    <div
                      className={`w-full h-full items-center justify-center text-[11px] font-bold ${
                        isSelected
                          ? "bg-primary/20 text-primary"
                          : "bg-white/10 text-muted-foreground"
                      }`}
                      style={{ display: inf.avatar ? "none" : "flex" }}
                    >
                      {getInitials(inf.name)}
                    </div>
                  </div>
                </div>
                <span
                  className={`text-[10px] max-w-[72px] truncate text-center leading-tight ${
                    isSelected ? "text-primary font-semibold" : "text-muted-foreground"
                  }`}
                >
                  {getShortName(inf.name)}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Map */}
      <div className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <MapView
          height="50vh"
          onEventClick={setSelectedEvent}
          onSpotClick={setSelectedSpot}
          filteredEvents={filteredMapEvents}
          filteredSpots={filteredMapSpots}
          showSports={!selectedInfluencer}
        />
      </div>

      {/* What's Hot Feed — VERTICAL GRID, no horizontal scroll */}
      <div className="px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp size={18} className="text-primary" />
          <h2 className="font-display font-bold text-lg text-foreground">
            {selectedInfluencer ? `${selectedInfluencer.name}'s Picks` : "What's Hot Right Now"}
          </h2>
        </div>

        {/* Filter chips — hide when influencer is selected */}
        {!selectedInfluencer && (
          <div className="mb-5">
            <FilterChips options={categories} selected={category} onChange={setCategory} />
          </div>
        )}

        {/* VERTICAL responsive grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {feedItems.map((item, i) => (
            <div key={`${item.type}-${i}`}>
              {item.type === "event" ? (
                <EventCard
                  event={item.data as PhillyEvent}
                  onClick={() => setSelectedEvent(item.data as PhillyEvent)}
                />
              ) : (
                <SpotCard
                  spot={item.data as HotSpot}
                  onClick={() => setSelectedSpot(item.data as HotSpot)}
                />
              )}
            </div>
          ))}
        </div>

        {/* Featured Insider Section */}
        {!selectedInfluencer && (
          <div className="mt-10">
            <div className="flex items-center gap-2 mb-5">
              <Sparkles size={18} className="text-primary" />
              <h2 className="font-display font-bold text-lg text-foreground">Insider Picks</h2>
              <span className="text-xs text-primary bg-primary/10 px-2 py-0.5 rounded-full font-medium">
                Curated
              </span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[...events.filter((e) => e.isInsider).slice(0, 3), ...hotspots.filter((h) => h.isInsider).slice(0, 3)].map((item, i) => (
                <div key={i}>
                  {"venue" in item ? (
                    <EventCard
                      event={item as PhillyEvent}
                      onClick={() => setSelectedEvent(item as PhillyEvent)}
                    />
                  ) : (
                    <SpotCard
                      spot={item as HotSpot}
                      onClick={() => setSelectedSpot(item as HotSpot)}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Drawers */}
      {selectedEvent && (
        <EventDrawer event={selectedEvent} onClose={() => setSelectedEvent(null)} />
      )}
      {selectedSpot && (
        <SpotDrawer spot={selectedSpot} onClose={() => setSelectedSpot(null)} />
      )}
    </div>
  );
}
