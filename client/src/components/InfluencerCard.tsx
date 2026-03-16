import { useState } from "react";
import { ChevronDown, ChevronUp, ExternalLink } from "lucide-react";
import type { Influencer } from "@/data/philly-data";
import { hotspots, events } from "@/data/philly-data";

interface Props {
  influencer: Influencer;
}

function getInitials(name: string) {
  return name.split(" ").map((w) => w[0]).join("").toUpperCase().slice(0, 2);
}

function hasRecentPost(influencer: Influencer): boolean {
  return influencer.recentPicks.some((pick) => {
    const d = pick.date.toLowerCase();
    return d.includes("march") && d.includes("2026");
  });
}

const platformColors: Record<string, string> = {
  Instagram: "bg-pink-500/15 text-pink-300",
  TikTok: "bg-cyan-500/15 text-cyan-300",
  Twitter: "bg-blue-500/15 text-blue-300",
  YouTube: "bg-red-500/15 text-red-300",
  Facebook: "bg-blue-600/15 text-blue-300",
  Website: "bg-emerald-500/15 text-emerald-300",
};

export function InfluencerCard({ influencer }: Props) {
  const [expanded, setExpanded] = useState(false);
  const platforms = influencer.platform.split(" | ").map((p) => p.trim());
  const focusTags = influencer.focus.split(" | ").map((f) => f.trim());
  const isRecent = hasRecentPost(influencer);

  return (
    <div
      className="rounded-xl border border-border/50 bg-card overflow-hidden transition-all duration-200 hover:bg-white/[0.04]"
      data-testid={`card-influencer-${influencer.id}`}
    >
      <div className="p-5">
        {/* Header — photo + centered info */}
        <div className="flex flex-col items-center text-center gap-3">
          {/* Avatar with pulse */}
          <div className="relative">
            {isRecent && (
              <div className="absolute inset-[-4px] rounded-full influencer-pulse" />
            )}
            {isRecent && (
              <div className="absolute -top-1 -right-1 z-10">
                <div className="w-3.5 h-3.5 rounded-full bg-emerald-400 border-2 border-card pulse-dot" />
              </div>
            )}
            {influencer.avatar ? (
              <img
                src={`${import.meta.env.BASE_URL}${influencer.avatar.replace('./', '')}`}
                alt={influencer.name}
                className={`w-16 h-16 rounded-full object-cover shadow-lg shadow-primary/10 ${
                  isRecent ? "border-2 border-primary/50" : "border-2 border-primary/30"
                }`}
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = "none";
                  const fallback = target.nextElementSibling as HTMLElement;
                  if (fallback) fallback.style.display = "flex";
                }}
              />
            ) : null}
            <div
              className="w-16 h-16 rounded-full bg-gradient-to-br from-primary/30 to-purple-500/30 items-center justify-center border-2 border-primary/30"
              style={{ display: influencer.avatar ? "none" : "flex" }}
            >
              <span className="font-display font-bold text-sm text-primary">{getInitials(influencer.name)}</span>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-center gap-1.5">
              <h3 className="font-display font-semibold text-[15px] text-foreground leading-tight">
                {influencer.name}
              </h3>
              {isRecent && (
                <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 uppercase tracking-wider">
                  Active
                </span>
              )}
            </div>
            <span className="text-xs text-primary font-medium">{influencer.handle}</span>
            <p className="text-xs text-muted-foreground mt-0.5">{influencer.followers}</p>
          </div>
        </div>

        {/* Platform badges — centered */}
        <div className="flex items-center justify-center gap-1.5 mt-4 flex-wrap">
          {platforms.map((p) => (
            <span
              key={p}
              className={`text-[10px] font-medium px-2 py-0.5 rounded ${platformColors[p] || "bg-slate-500/15 text-slate-300"}`}
            >
              {p}
            </span>
          ))}
          {focusTags.map((tag) => (
            <span
              key={tag}
              className="text-[10px] font-medium px-2 py-0.5 rounded bg-white/5 text-muted-foreground capitalize"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Bio */}
        <p className="text-xs text-muted-foreground leading-relaxed mt-4 line-clamp-2 text-center">
          {influencer.bio}
        </p>

        {/* Expand button — centered */}
        <div className="flex justify-center mt-4">
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 text-xs font-medium text-primary hover:text-primary/80 transition"
            data-testid={`button-expand-${influencer.id}`}
          >
            {expanded ? "Hide picks" : `View ${influencer.recentPicks.length} recent picks`}
            {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
        </div>
      </div>

      {/* Expanded picks */}
      {expanded && (
        <div className="border-t border-border/50 px-5 py-4 space-y-3 animate-fade-in bg-white/[0.02]">
          {influencer.recentPicks.map((pick, i) => {
            const matchedSpot = hotspots.find(
              (s) => s.name.toLowerCase() === pick.name.toLowerCase()
            );
            const matchedEvent = events.find(
              (e) => e.name.toLowerCase() === pick.name.toLowerCase()
            );

            return (
              <div key={i} className="flex items-start gap-2.5">
                <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold text-foreground">{pick.name}</span>
                    {(matchedSpot || matchedEvent) && (
                      <ExternalLink size={10} className="text-primary flex-shrink-0" />
                    )}
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed mt-0.5">
                    {pick.quote}
                  </p>
                  <span className="text-[10px] text-muted-foreground/60">{pick.date}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
