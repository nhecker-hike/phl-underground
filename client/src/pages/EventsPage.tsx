import { useState, useMemo } from "react";
import { events, eventCategories, vibeOptions, type PhillyEvent } from "@/data/philly-data";
import { EventCard } from "@/components/EventCard";
import { EventDrawer } from "@/components/DetailDrawer";
import { FilterChips, FilterToggle } from "@/components/FilterChips";
import { Calendar, SlidersHorizontal } from "lucide-react";

export function EventsPage() {
  const [selectedEvent, setSelectedEvent] = useState<PhillyEvent | null>(null);
  const [category, setCategory] = useState("All");
  const [vibe, setVibe] = useState("All");
  const [insiderOnly, setInsiderOnly] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  const filtered = useMemo(() => {
    return events.filter((e) => {
      if (category !== "All" && e.category.toLowerCase() !== category.toLowerCase()) return false;
      if (vibe !== "All" && e.vibeTag !== vibe) return false;
      if (insiderOnly && !e.isInsider) return false;
      return true;
    });
  }, [category, vibe, insiderOnly]);

  return (
    <div className="min-h-screen px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto" data-testid="page-events">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <Calendar size={20} className="text-primary" />
          <h1 className="font-display font-bold text-xl text-foreground">Events</h1>
          <span className="text-xs text-muted-foreground bg-white/5 px-2 py-0.5 rounded-full">
            {filtered.length} of {events.length}
          </span>
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg border transition ${
            showFilters ? "bg-primary/15 text-primary border-primary/30" : "text-muted-foreground border-border/50 hover:text-foreground"
          }`}
          data-testid="button-toggle-filters"
        >
          <SlidersHorizontal size={14} />
          Filters
        </button>
      </div>

      {/* Category chips — always visible */}
      <div className="mb-4">
        <FilterChips options={eventCategories} selected={category} onChange={setCategory} />
      </div>

      {/* Extended filters */}
      {showFilters && (
        <div className="mb-5 p-4 rounded-xl bg-card border border-border/50 space-y-3 animate-fade-in" data-testid="filters-panel">
          <div>
            <span className="text-xs font-medium text-muted-foreground mb-2 block">Vibe</span>
            <FilterChips options={vibeOptions} selected={vibe} onChange={setVibe} />
          </div>
          <div className="flex gap-2">
            <FilterToggle label="Insider Only" active={insiderOnly} onChange={setInsiderOnly} />
          </div>
        </div>
      )}

      {/* Event list */}
      {filtered.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-muted-foreground text-sm">No events match your filters.</p>
          <button
            onClick={() => { setCategory("All"); setVibe("All"); setInsiderOnly(false); }}
            className="mt-2 text-primary text-sm font-medium hover:underline"
          >
            Clear filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              onClick={() => setSelectedEvent(event)}
            />
          ))}
        </div>
      )}

      {/* Drawer */}
      {selectedEvent && (
        <EventDrawer event={selectedEvent} onClose={() => setSelectedEvent(null)} />
      )}
    </div>
  );
}
