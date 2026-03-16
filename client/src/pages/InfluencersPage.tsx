import { influencers } from "@/data/philly-data";
import { InfluencerCard } from "@/components/InfluencerCard";
import { Users } from "lucide-react";

export function InfluencersPage() {
  return (
    <div className="min-h-screen px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto" data-testid="page-influencers">
      {/* Header */}
      <div className="flex items-center gap-2.5 mb-2">
        <Users size={20} className="text-purple-400" />
        <h1 className="font-display font-bold text-xl text-foreground">Influencers</h1>
        <span className="text-xs text-muted-foreground bg-white/5 px-2 py-0.5 rounded-full">
          {influencers.length} tastemakers
        </span>
      </div>
      <p className="text-sm text-muted-foreground mb-8 max-w-xl leading-relaxed">
        The local voices shaping Philadelphia's food, nightlife, and culture scene. Explore their recent picks and follows.
      </p>

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {influencers.map((inf) => (
          <InfluencerCard key={inf.id} influencer={inf} />
        ))}
      </div>
    </div>
  );
}
