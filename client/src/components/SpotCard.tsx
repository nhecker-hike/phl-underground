import { MapPin } from "lucide-react";
import type { HotSpot } from "@/data/philly-data";

interface Props {
  spot: HotSpot;
  onClick?: () => void;
}

const vibeBadgeColors: Record<string, string> = {
  upscale: "bg-amber-500/15 text-amber-300",
  trendy: "bg-pink-500/15 text-pink-300",
  casual: "bg-blue-500/15 text-blue-300",
  dive: "bg-red-500/15 text-red-300",
  lively: "bg-orange-500/15 text-orange-300",
  romantic: "bg-rose-500/15 text-rose-300",
};

const typeBadgeColors: Record<string, string> = {
  restaurant: "bg-emerald-500/15 text-emerald-300",
  bar: "bg-violet-500/15 text-violet-300",
  cafe: "bg-cyan-500/15 text-cyan-300",
  venue: "bg-yellow-500/15 text-yellow-300",
  neighborhood: "bg-teal-500/15 text-teal-300",
};

function PriceDots({ range }: { range: string }) {
  const count = range.length;
  return (
    <span className="text-xs font-medium tracking-wider">
      {Array.from({ length: 4 }).map((_, i) => (
        <span key={i} className={i < count ? "text-primary" : "text-muted-foreground/30"}>$</span>
      ))}
    </span>
  );
}

export function SpotCard({ spot, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className={`text-left w-full h-full group rounded-xl border border-border/50 bg-card hover:bg-white/[0.04] transition-all duration-200 p-4 flex flex-col ${
        spot.isInsider ? "insider-glow" : ""
      }`}
      data-testid={`card-spot-${spot.id}`}
    >
      {/* Title row */}
      <div className="flex items-center gap-2 mb-1">
        <h3 className="font-display font-semibold text-[15px] text-foreground group-hover:text-primary transition-colors leading-snug line-clamp-2">
          {spot.name}
        </h3>
        {spot.isNew && (
          <span className="flex-shrink-0 text-[9px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 uppercase tracking-wider">
            NEW
          </span>
        )}
      </div>

      {/* Location */}
      <div className="flex items-center gap-1.5 mb-2">
        <MapPin size={11} className="text-muted-foreground flex-shrink-0" />
        <span className="text-xs text-muted-foreground truncate">{spot.neighborhood}</span>
        <span className="text-muted-foreground/30 text-xs">·</span>
        <PriceDots range={spot.priceRange} />
      </div>

      {/* Description */}
      <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2 mb-auto">
        {spot.description}
      </p>

      {/* Badges — pushed to bottom */}
      <div className="flex items-center gap-1.5 mt-3 flex-wrap">
        <span className={`text-[10px] font-medium px-2 py-0.5 rounded capitalize ${typeBadgeColors[spot.type] || "bg-slate-500/15 text-slate-300"}`}>
          {spot.type}
        </span>
        <span className={`text-[10px] font-medium px-2 py-0.5 rounded ${vibeBadgeColors[spot.vibeTag] || "bg-slate-500/15 text-slate-300"}`}>
          {spot.vibeTag}
        </span>
        {spot.cuisine && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-white/5 text-muted-foreground">
            {spot.cuisine}
          </span>
        )}
        {spot.isInsider && (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-primary/20 text-primary">
            INSIDER
          </span>
        )}
      </div>
    </button>
  );
}
