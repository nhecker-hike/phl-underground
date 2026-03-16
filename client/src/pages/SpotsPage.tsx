import { useState, useMemo } from "react";
import { hotspots, spotTypes, vibeOptions, priceRanges, type HotSpot } from "@/data/philly-data";
import { SpotCard } from "@/components/SpotCard";
import { SpotDrawer } from "@/components/DetailDrawer";
import { FilterChips, FilterToggle } from "@/components/FilterChips";
import { MapPin, SlidersHorizontal } from "lucide-react";

export function SpotsPage() {
  const [selectedSpot, setSelectedSpot] = useState<HotSpot | null>(null);
  const [type, setType] = useState("All");
  const [vibe, setVibe] = useState("All");
  const [priceRange, setPriceRange] = useState("All");
  const [newOnly, setNewOnly] = useState(false);
  const [insiderOnly, setInsiderOnly] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  const filtered = useMemo(() => {
    return hotspots.filter((s) => {
      if (type !== "All" && s.type.toLowerCase() !== type.toLowerCase()) return false;
      if (vibe !== "All" && s.vibeTag !== vibe) return false;
      if (priceRange !== "All" && s.priceRange !== priceRange) return false;
      if (newOnly && !s.isNew) return false;
      if (insiderOnly && !s.isInsider) return false;
      return true;
    });
  }, [type, vibe, priceRange, newOnly, insiderOnly]);

  return (
    <div className="min-h-screen px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto" data-testid="page-spots">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <MapPin size={20} className="text-cyan-400" />
          <h1 className="font-display font-bold text-xl text-foreground">Hot Spots</h1>
          <span className="text-xs text-muted-foreground bg-white/5 px-2 py-0.5 rounded-full">
            {filtered.length} of {hotspots.length}
          </span>
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg border transition ${
            showFilters ? "bg-primary/15 text-primary border-primary/30" : "text-muted-foreground border-border/50 hover:text-foreground"
          }`}
          data-testid="button-toggle-spot-filters"
        >
          <SlidersHorizontal size={14} />
          Filters
        </button>
      </div>

      {/* Type chips */}
      <div className="mb-4">
        <FilterChips options={spotTypes} selected={type} onChange={setType} />
      </div>

      {/* Extended filters */}
      {showFilters && (
        <div className="mb-5 p-4 rounded-xl bg-card border border-border/50 space-y-3 animate-fade-in" data-testid="spot-filters-panel">
          <div>
            <span className="text-xs font-medium text-muted-foreground mb-2 block">Vibe</span>
            <FilterChips options={vibeOptions} selected={vibe} onChange={setVibe} />
          </div>
          <div>
            <span className="text-xs font-medium text-muted-foreground mb-2 block">Price Range</span>
            <FilterChips options={priceRanges} selected={priceRange} onChange={setPriceRange} />
          </div>
          <div className="flex gap-2">
            <FilterToggle label="New Only" active={newOnly} onChange={setNewOnly} />
            <FilterToggle label="Insider Only" active={insiderOnly} onChange={setInsiderOnly} />
          </div>
        </div>
      )}

      {/* Spot grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-muted-foreground text-sm">No spots match your filters.</p>
          <button
            onClick={() => { setType("All"); setVibe("All"); setPriceRange("All"); setNewOnly(false); setInsiderOnly(false); }}
            className="mt-2 text-primary text-sm font-medium hover:underline"
          >
            Clear filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((spot) => (
            <SpotCard
              key={spot.id}
              spot={spot}
              onClick={() => setSelectedSpot(spot)}
            />
          ))}
        </div>
      )}

      {/* Drawer */}
      {selectedSpot && (
        <SpotDrawer spot={selectedSpot} onClose={() => setSelectedSpot(null)} />
      )}
    </div>
  );
}
