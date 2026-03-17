import { MapPin, Calendar, Play, ExternalLink } from "lucide-react";
import type { InfluencerPick, Influencer } from "@/data/philly-data";

interface Props {
  pick: InfluencerPick;
  influencer: Influencer;
}

const typeColors: Record<string, string> = {
  restaurant: "bg-amber-500/15 text-amber-300",
  bar: "bg-purple-500/15 text-purple-300",
  cafe: "bg-orange-500/15 text-orange-300",
  event: "bg-cyan-500/15 text-cyan-300",
  spot: "bg-emerald-500/15 text-emerald-300",
};

export function InfluencerPickCard({ pick, influencer }: Props) {
  const typeStyle = typeColors[pick.type] || "bg-slate-500/15 text-slate-300";

  return (
    <div
      className="rounded-xl border border-border/50 bg-card overflow-hidden transition-all duration-200 hover:bg-white/[0.04] group"
      data-testid={`card-pick-${pick.name.replace(/\s+/g, "-").toLowerCase()}`}
    >
      <div className="p-4">
        {/* Header row: type badge + date */}
        <div className="flex items-center justify-between mb-2.5">
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded uppercase tracking-wide ${typeStyle}`}>
            {pick.type}
          </span>
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground/70">
            <Calendar size={10} />
            {pick.date}
          </span>
        </div>

        {/* Name */}
        <h3 className="font-display font-semibold text-sm text-foreground leading-tight mb-1.5">
          {pick.name}
        </h3>

        {/* Neighborhood */}
        <div className="flex items-center gap-1 text-[11px] text-muted-foreground mb-2.5">
          <MapPin size={10} className="text-primary/60 flex-shrink-0" />
          {pick.neighborhood}
        </div>

        {/* Quote */}
        <p className="text-xs text-muted-foreground/80 leading-relaxed line-clamp-3">
          "{pick.quote}"
        </p>

        {/* Footer: influencer attribution + reel link */}
        <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-border/30">
          <div className="flex items-center gap-2">
            {influencer.avatar ? (
              <img
                src={`${import.meta.env.BASE_URL}${influencer.avatar.replace("./", "")}`}
                alt={influencer.name}
                className="w-5 h-5 rounded-full object-cover border border-primary/30"
              />
            ) : (
              <div className="w-5 h-5 rounded-full bg-primary/20 flex items-center justify-center text-[8px] font-bold text-primary">
                {influencer.name.split(" ").map((w) => w[0]).join("").slice(0, 2)}
              </div>
            )}
            <span className="text-[10px] text-muted-foreground font-medium">
              {influencer.handle}
            </span>
          </div>

          {pick.reelUrl && (
            <a
              href={pick.reelUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] font-semibold text-pink-400 hover:text-pink-300 transition-colors"
              data-testid={`link-reel-${pick.name.replace(/\s+/g, "-").toLowerCase()}`}
            >
              <Play size={10} className="fill-current" />
              Watch Reel
              <ExternalLink size={8} className="opacity-60" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
