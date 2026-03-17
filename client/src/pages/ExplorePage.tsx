import { useState, useMemo } from "react";
import { MapView } from "@/components/MapView";
import { EventCard } from "@/components/EventCard";
import { SpotCard } from "@/components/SpotCard";
import { InfluencerPickCard } from "@/components/InfluencerPickCard";
import { EventDrawer, SpotDrawer } from "@/components/DetailDrawer";
import { FilterChips } from "@/components/FilterChips";
import {
  events,
  hotspots,
  influencers,
  type PhillyEvent,
  type HotSpot,
  type Influencer,
  type InfluencerPick,
} from "@/data/philly-data";
import { Sparkles, TrendingUp, Play, ExternalLink } from "lucide-react";
import { EmailCapture } from "@/components/EmailCapture";

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
    "FeedingTimeTV": "Feeding",
    "The Philly Food Fanatic": "Fanatic",
    "Josh Moore": "Josh",
    "Cass Matthews": "Cass",
    "Philly Food Ladies": "FoodLadies",
    "Fueled on Philly": "Fueled",
    "Kory Aversa": "Kory",
    "Djour Philly": "Djour",
    "SwagFoodPhilly": "SwagFood",
    "Visit Philly": "VisitPhilly",
    "Farah Stacy": "Farah",
  };
  return map[clean] ?? clean.split(/\s/)[0];
}

/** Check if an influencer has posted in March 2026 (i.e. "recent") */
function hasRecentPost(influencer: Influencer): boolean {
  return influencer.recentPicks.some((pick) => {
    const d = String(pick.date || "").toLowerCase();
    return d.includes("march") && d.includes("2026");
  });
}

/** Match influencer picks against events and hotspots by name */
function getInfluencerMatches(influencer: Influencer) {
  const pickNames = influencer.recentPicks.map((p) => String(p.name || "").toLowerCase()).filter(Boolean);
  const matchedEvents = events.filter((e) => {
    const en = String(e.name || "").toLowerCase();
    return pickNames.some((pn) => en.includes(pn) || pn.includes(en));
  });
  const matchedSpots = hotspots.filter((s) => {
    const sn = String(s.name || "").toLowerCase();
    return pickNames.some((pn) => sn.includes(pn) || pn.includes(sn));
  });
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

  /** All picks for the selected influencer, sorted newest first */
  const influencerPicks = useMemo(() => {
    if (!selectedInfluencer) return [];
    return [...selectedInfluencer.recentPicks].sort((a, b) => {
      const months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];
      const getScore = (d: string | undefined) => {
        const dl = String(d || "").toLowerCase();
        if (dl.includes("2026")) {
          const mi = months.findIndex((m) => dl.includes(m));
          return mi >= 0 ? 2000 + mi * 30 : 1900;
        }
        if (dl.includes("2025")) {
          const mi = months.findIndex((m) => dl.includes(m));
          return mi >= 0 ? 1000 + mi * 30 : 900;
        }
        return 0;
      };
      return getScore(b.date) - getScore(a.date);
    });
  }, [selectedInfluencer]);

  const feedItems = useMemo(() => {
    let items: Array<{ type: "event"; data: PhillyEvent } | { type: "spot"; data: HotSpot }> = [];

    // If influencer selected, skip feed items — we'll show influencer picks instead
    if (selectedInfluencer) return [];

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
  }, [category, selectedInfluencer]);

  // Count picks that have a reel
  const reelCount = selectedInfluencer
    ? selectedInfluencer.recentPicks.filter((p) => p.reelUrl).length
    : 0;

  return (
    <div className="min-h-screen" data-testid="page-explore">
      {/* Influencer Picker */}
      <div className="px-3 sm:px-6 lg:px-8 pt-5 pb-2 max-w-7xl mx-auto">
        <div
          className="flex items-start gap-3 sm:gap-4 overflow-x-auto pb-3 pt-2 px-1 scrollbar-hide sm:justify-center"
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
                className={`w-14 h-14 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                  !selectedInfluencer
                    ? "bg-primary/20 text-primary ring-[2.5px] ring-primary shadow-[0_0_12px_hsl(45,100%,60%,0.35)]"
                    : "bg-white/10 text-muted-foreground ring-1 ring-white/10"
                }`}
              >
                All
              </div>
            </div>
            <span className={`text-[10px] min-w-[60px] text-center leading-tight ${!selectedInfluencer ? "text-primary font-semibold" : "text-muted-foreground"}`}>
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
                  isSelected
                    ? "opacity-100"
                    : selectedInfluencer
                      ? "opacity-40 hover:opacity-70"
                      : "opacity-80 hover:opacity-100"
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
                    className={`w-14 h-14 rounded-full overflow-hidden transition-all ${
                      isSelected
                        ? "ring-[2.5px] ring-primary shadow-[0_0_12px_hsl(45,100%,60%,0.35)]"
                        : isRecent
                          ? "ring-2 ring-primary/40"
                          : "ring-1 ring-white/10"
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
                  className={`text-[10px] min-w-[60px] max-w-[72px] truncate text-center leading-tight ${
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
      <div className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <MapView
          height="40vh"
          desktopHeight="50vh"
          onEventClick={setSelectedEvent}
          onSpotClick={setSelectedSpot}
          filteredEvents={filteredMapEvents}
          filteredSpots={filteredMapSpots}
          showSports={!selectedInfluencer}
        />
      </div>

      {/* INFLUENCER TRACKER VIEW — shown when an influencer is selected */}
      {selectedInfluencer && (
        <div className="px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto">
          {/* Influencer header */}
          <div className="flex items-center gap-3 mb-2">
            {selectedInfluencer.avatar ? (
              <img
                src={`${import.meta.env.BASE_URL}${selectedInfluencer.avatar.replace("./", "")}`}
                alt={selectedInfluencer.name}
                className="w-10 h-10 rounded-full object-cover border-2 border-primary/40"
              />
            ) : null}
            <div>
              <h2 className="font-display font-bold text-lg text-foreground">
                {selectedInfluencer.name.replace(/\s*\(.*\)\s*/, "")}'s Tracker
              </h2>
              <p className="text-xs text-muted-foreground">
                {selectedInfluencer.recentPicks.length} picks &middot; {selectedInfluencer.followers}
              </p>
            </div>
          </div>

          {/* Stats row */}
          <div className="flex items-center gap-3 mb-5">
            <span className="text-[11px] px-2.5 py-1 rounded-full bg-primary/10 text-primary font-medium">
              {influencerPicks.filter((p) => p.date.toLowerCase().includes("march") && p.date.includes("2026")).length} this month
            </span>
            {reelCount > 0 && (
              <span className="flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-full bg-pink-500/10 text-pink-400 font-medium">
                <Play size={10} className="fill-current" />
                {reelCount} reel{reelCount !== 1 ? "s" : ""}
              </span>
            )}
            <a
              href={selectedInfluencer.socialLinks?.Instagram || "#"}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-full bg-white/5 text-muted-foreground hover:text-foreground font-medium transition-colors ml-auto"
            >
              Follow {selectedInfluencer.handle}
              <ExternalLink size={10} />
            </a>
          </div>

          {/* Matched events/spots from main arrays (clickable detail cards) */}
          {influencerMatches && (influencerMatches.events.length > 0 || influencerMatches.spots.length > 0) && (
            <div className="mb-6">
              <h3 className="font-display font-semibold text-sm text-foreground mb-3 flex items-center gap-2">
                <TrendingUp size={14} className="text-primary" />
                On the Map
                <span className="text-[10px] font-normal text-muted-foreground">
                  &mdash; matched to events &amp; hot spots
                </span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {influencerMatches.events.map((e, i) => (
                  <EventCard
                    key={`map-event-${i}`}
                    event={e}
                    onClick={() => setSelectedEvent(e)}
                  />
                ))}
                {influencerMatches.spots.map((s, i) => (
                  <SpotCard
                    key={`map-spot-${i}`}
                    spot={s}
                    onClick={() => setSelectedSpot(s)}
                  />
                ))}
              </div>
            </div>
          )}

          {/* ALL influencer picks — the full tracker */}
          <div>
            <h3 className="font-display font-semibold text-sm text-foreground mb-3 flex items-center gap-2">
              <Sparkles size={14} className="text-primary" />
              All Recent Picks
              <span className="text-[10px] font-normal text-muted-foreground">
                &mdash; everything they're posting about
              </span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {influencerPicks.map((pick, i) => (
                <InfluencerPickCard
                  key={`pick-${i}`}
                  pick={pick}
                  influencer={selectedInfluencer}
                />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* What's Hot Feed — ONLY shown when no influencer selected */}
      {!selectedInfluencer && (
        <div className="px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={18} className="text-primary" />
            <h2 className="font-display font-bold text-lg text-foreground">
              What's Hot Right Now
            </h2>
          </div>

          {/* Filter chips */}
          <div className="mb-5">
            <FilterChips options={categories} selected={category} onChange={setCategory} />
          </div>

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
        </div>
      )}

      {/* Email Capture */}
      <div className="px-4 sm:px-6 lg:px-8 pb-6 max-w-7xl mx-auto">
        <EmailCapture />
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
