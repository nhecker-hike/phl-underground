import { useState, useEffect, useRef } from "react";
import { Search, X, Calendar, MapPin, User, Trophy } from "lucide-react";
import { searchAll } from "@/data/philly-data";
import { useLocation } from "wouter";

interface Props {
  onClose: () => void;
}

export function SearchOverlay({ onClose }: Props) {
  const [query, setQuery] = useState("");
  const [, setLocation] = useLocation();
  const inputRef = useRef<HTMLInputElement>(null);
  const results = searchAll(query);
  const hasResults = results.events.length > 0 || results.spots.length > 0 || results.influencers.length > 0 || results.teams.length > 0;

  useEffect(() => {
    inputRef.current?.focus();
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-[100] bg-black/70 backdrop-blur-sm flex justify-center pt-[10vh] px-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
      data-testid="search-overlay"
    >
      <div className="w-full max-w-xl bg-card border border-border rounded-xl overflow-hidden animate-fade-in" style={{ maxHeight: '70vh' }}>
        {/* Search Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
          <Search size={18} className="text-muted-foreground flex-shrink-0" />
          <input
            ref={inputRef}
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search events, spots, sports, influencers..."
            className="flex-1 bg-transparent text-foreground text-sm outline-none placeholder:text-muted-foreground"
            data-testid="input-search"
          />
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground p-1" data-testid="button-close-search">
            <X size={16} />
          </button>
        </div>

        {/* Results */}
        <div className="overflow-y-auto" style={{ maxHeight: 'calc(70vh - 56px)' }}>
          {query.length > 0 && !hasResults && (
            <div className="px-4 py-8 text-center text-muted-foreground text-sm">
              No results for "{query}"
            </div>
          )}

          {results.events.length > 0 && (
            <div className="px-2 py-2">
              <div className="px-3 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Events
              </div>
              {results.events.slice(0, 5).map((event) => (
                <button
                  key={event.id}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition text-left"
                  onClick={() => { setLocation("/events"); onClose(); }}
                  data-testid={`search-result-${event.id}`}
                >
                  <Calendar size={15} className="text-primary flex-shrink-0" />
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-foreground truncate">{event.name}</div>
                    <div className="text-xs text-muted-foreground">{event.venue} · {event.neighborhood}</div>
                  </div>
                  {event.isInsider && (
                    <span className="ml-auto text-[10px] font-semibold text-primary bg-primary/10 px-1.5 py-0.5 rounded">
                      INSIDER
                    </span>
                  )}
                </button>
              ))}
            </div>
          )}

          {results.spots.length > 0 && (
            <div className="px-2 py-2">
              <div className="px-3 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Hot Spots
              </div>
              {results.spots.slice(0, 5).map((spot) => (
                <button
                  key={spot.id}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition text-left"
                  onClick={() => { setLocation("/spots"); onClose(); }}
                  data-testid={`search-result-${spot.id}`}
                >
                  <MapPin size={15} className="text-cyan-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-foreground truncate">{spot.name}</div>
                    <div className="text-xs text-muted-foreground">{spot.type} · {spot.neighborhood}</div>
                  </div>
                  {spot.isInsider && (
                    <span className="ml-auto text-[10px] font-semibold text-primary bg-primary/10 px-1.5 py-0.5 rounded">
                      INSIDER
                    </span>
                  )}
                </button>
              ))}
            </div>
          )}

          {results.teams.length > 0 && (
            <div className="px-2 py-2">
              <div className="px-3 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Sports Teams
              </div>
              {results.teams.slice(0, 5).map((team) => (
                <button
                  key={team.id}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition text-left"
                  onClick={() => { setLocation("/sports"); onClose(); }}
                  data-testid={`search-result-${team.id}`}
                >
                  <Trophy size={15} className="text-emerald-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-foreground truncate">{team.team}</div>
                    <div className="text-xs text-muted-foreground">{team.league} · {team.venue}</div>
                  </div>
                  <span className={`ml-auto text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                    team.season === "In Season" ? "text-emerald-300 bg-emerald-500/10" : "text-zinc-400 bg-zinc-500/10"
                  }`}>
                    {team.season === "In Season" ? "IN SEASON" : "OFF"}
                  </span>
                </button>
              ))}
            </div>
          )}

          {results.influencers.length > 0 && (
            <div className="px-2 py-2">
              <div className="px-3 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Influencers
              </div>
              {results.influencers.slice(0, 5).map((inf) => (
                <button
                  key={inf.id}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition text-left"
                  onClick={() => { setLocation("/influencers"); onClose(); }}
                  data-testid={`search-result-${inf.id}`}
                >
                  <User size={15} className="text-purple-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-foreground truncate">{inf.name}</div>
                    <div className="text-xs text-muted-foreground">{inf.handle}</div>
                  </div>
                </button>
              ))}
            </div>
          )}

          {!query && (
            <div className="px-4 py-8 text-center text-muted-foreground text-sm">
              Search across events, hot spots, sports, and influencers...
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
