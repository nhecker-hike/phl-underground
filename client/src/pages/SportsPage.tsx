import { useState } from "react";
import {
  sportsTeams,
  watchBars,
  ncaaTournamentContext,
  findTeamPrediction,
  type SportsTeam,
  type WatchBar,
} from "@/data/philly-data";
import {
  Trophy,
  MapPin,
  Calendar,
  Clock,
  ChevronDown,
  ChevronUp,
  Ticket,
  TrendingUp,
  BarChart3,
  Tv,
  ExternalLink,
  Flame,
} from "lucide-react";

function formatGameDate(dateStr: string) {
  const d = new Date(dateStr + "T12:00:00");
  if (isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
}

function TeamCard({ team }: { team: SportsTeam }) {
  const [expanded, setExpanded] = useState(false);
  const prediction = findTeamPrediction(team.team);
  const isPro = team.level === "pro";
  const accent = isPro ? "primary" : "purple-400";
  const accentBg = isPro ? "bg-primary/15 text-primary" : "bg-purple-400/15 text-purple-300";
  const inSeason = team.season === "In Season";
  const homeGames = team.upcomingGames.filter((g) => g.homeAway === "home" || g.homeAway === "neutral");

  return (
    <div
      className="rounded-xl border border-border/50 bg-card overflow-hidden"
      data-testid={`card-team-${team.id}`}
    >
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div>
            <h3 className="font-display font-bold text-[15px] text-foreground leading-tight">
              {team.team}
            </h3>
            <p className="text-xs text-muted-foreground mt-0.5">
              {team.league} · {team.venue}
            </p>
          </div>
          <span
            className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full flex-shrink-0 ${
              inSeason ? "bg-emerald-500/20 text-emerald-300" : "bg-zinc-500/20 text-zinc-400"
            }`}
          >
            {team.season}
          </span>
        </div>

        {/* Record + prediction */}
        <div className="flex items-center gap-2 flex-wrap mb-2">
          <span className={`text-[10px] font-medium px-2 py-0.5 rounded ${accentBg}`}>
            {isPro ? "PRO" : "COLLEGE"}
          </span>
          {team.record && (
            <span className="text-xs text-muted-foreground">{team.record}</span>
          )}
          {prediction && (
            <a
              href={prediction.polymarketUrl || "#"}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] font-medium text-primary/80 hover:text-primary transition"
              data-testid={`prediction-${team.id}`}
            >
              <BarChart3 size={10} />
              {prediction.impliedProbability} title odds
              <ExternalLink size={8} />
            </a>
          )}
        </div>

        {/* Season note */}
        {team.seasonNote && (
          <p className="text-xs text-muted-foreground/80 leading-relaxed mb-3">
            {team.seasonNote}
          </p>
        )}

        {/* Upcoming games toggle */}
        {team.upcomingGames.length > 0 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1.5 text-xs font-medium text-foreground hover:text-primary transition w-full"
            data-testid={`toggle-games-${team.id}`}
          >
            <Calendar size={13} />
            {homeGames.length} home game{homeGames.length !== 1 ? "s" : ""} · {team.upcomingGames.length} total
            {expanded ? <ChevronUp size={13} className="ml-auto" /> : <ChevronDown size={13} className="ml-auto" />}
          </button>
        )}
      </div>

      {/* Games list */}
      {expanded && team.upcomingGames.length > 0 && (
        <div className="border-t border-border/30 divide-y divide-border/20">
          {team.upcomingGames.map((game, i) => (
            <div key={i} className="px-4 py-2.5 flex items-center gap-3" data-testid={`game-${team.id}-${i}`}>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="text-sm font-medium text-foreground truncate">
                    vs {game.opponent}
                  </span>
                  <span
                    className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
                      game.homeAway === "home"
                        ? "bg-emerald-500/15 text-emerald-300"
                        : game.homeAway === "away"
                        ? "bg-zinc-500/15 text-zinc-400"
                        : "bg-blue-500/15 text-blue-300"
                    }`}
                  >
                    {game.homeAway}
                  </span>
                  {game.isHot && (
                    <span className="flex items-center gap-0.5 text-[9px] font-bold uppercase px-1.5 py-0.5 rounded bg-orange-500/15 text-orange-300">
                      <Flame size={9} /> HOT
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-3 text-[11px] text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Calendar size={10} /> {formatGameDate(game.date)}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock size={10} /> {game.time}
                  </span>
                </div>
                {game.isHot && game.hotReason && (
                  <p className="text-[10px] text-orange-300/70 mt-1">{game.hotReason}</p>
                )}
              </div>
              <a
                href={game.ticketUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-shrink-0 flex items-center gap-1 text-[11px] font-medium text-primary hover:text-primary/80 transition px-2.5 py-1.5 rounded-lg bg-primary/10 hover:bg-primary/15"
                data-testid={`ticket-${team.id}-${i}`}
              >
                <Ticket size={12} />
                Tickets
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function WatchBarCard({ bar }: { bar: WatchBar }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className="rounded-xl border border-border/50 bg-card p-4"
      data-testid={`card-bar-${bar.id}`}
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <div>
          <h3 className="font-display font-semibold text-sm text-foreground">{bar.name}</h3>
          <p className="text-xs text-muted-foreground mt-0.5">{bar.neighborhood}</p>
        </div>
        <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-cyan-500/15 text-cyan-300 flex-shrink-0">
          {bar.vibeTag}
        </span>
      </div>

      <p className={`text-xs text-muted-foreground/80 leading-relaxed mb-2 ${!expanded ? "line-clamp-2" : ""}`}>
        {bar.description}
      </p>
      {bar.description.length > 120 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-[10px] text-primary hover:underline mb-2"
        >
          {expanded ? "Show less" : "Read more"}
        </button>
      )}

      {/* Team badges */}
      <div className="flex flex-wrap gap-1 mb-2">
        {bar.teams.map((t) => (
          <span key={t} className="text-[9px] font-medium uppercase px-1.5 py-0.5 rounded bg-white/5 text-muted-foreground">
            {t === "all" ? "All Teams" : t}
          </span>
        ))}
      </div>

      {bar.hasSpecials && bar.specialsNote && (
        <p className="text-[10px] text-emerald-300/80 leading-relaxed">
          🎉 {bar.specialsNote}
        </p>
      )}
    </div>
  );
}

export function SportsPage() {
  return (
    <div className="min-h-screen" data-testid="page-sports">
      {/* Hero Section */}
      <div className="px-4 sm:px-6 lg:px-8 pt-8 pb-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-3 mb-3">
          <Trophy size={24} className="text-emerald-400" />
          <h1 className="font-display font-bold text-2xl sm:text-3xl text-foreground">
            Philly Sports
          </h1>
        </div>
        <p className="text-sm text-muted-foreground max-w-2xl leading-relaxed">
          March Madness is here — the NCAA Tournament's First & Second Rounds come to Wells Fargo Center March 20–22.
          Plus: Phillies Opening Day on March 26, Sixers fighting for playoff positioning, and college hoops in full swing.
        </p>
      </div>

      {/* Team Cards Grid */}
      <div className="px-4 sm:px-6 lg:px-8 pb-8 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp size={16} className="text-emerald-400" />
          <h2 className="font-display font-bold text-lg text-foreground">Teams</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {sportsTeams.map((team) => (
            <TeamCard key={team.id} team={team} />
          ))}
        </div>
      </div>

      {/* March Madness Spotlight */}
      <div className="px-4 sm:px-6 lg:px-8 pb-8 max-w-7xl mx-auto">
        <div
          className="rounded-xl border border-purple-500/30 bg-purple-500/5 p-5"
          data-testid="march-madness-spotlight"
        >
          <div className="flex items-center gap-2 mb-3">
            <Trophy size={18} className="text-purple-400" />
            <h2 className="font-display font-bold text-lg text-foreground">March Madness in Philly</h2>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed mb-3">
            {ncaaTournamentContext.note}
          </p>
          <div className="space-y-1.5 text-xs text-muted-foreground mb-4">
            <div className="flex items-center gap-2">
              <MapPin size={12} className="text-purple-400" />
              {ncaaTournamentContext.localVenue}
            </div>
            <div className="flex items-center gap-2">
              <Calendar size={12} className="text-purple-400" />
              {ncaaTournamentContext.rounds}
            </div>
          </div>
          <div className="flex flex-wrap gap-2 mb-4">
            {sportsTeams
              .filter((t) => t.level === "college" && t.season === "In Season")
              .map((t) => (
                <span key={t.id} className="text-[11px] font-medium px-2.5 py-1 rounded bg-purple-400/15 text-purple-300">
                  {t.team} ({t.record})
                </span>
              ))}
          </div>
          <a
            href={ncaaTournamentContext.ticketUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-primary hover:text-primary/80 transition px-4 py-2 rounded-lg bg-primary/10 hover:bg-primary/15"
            data-testid="link-ncaa-tickets"
          >
            <Ticket size={14} />
            Get NCAA Tournament Tickets
            <ExternalLink size={12} />
          </a>
        </div>
      </div>

      {/* Where to Watch */}
      <div className="px-4 sm:px-6 lg:px-8 pb-12 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 mb-4">
          <Tv size={16} className="text-cyan-400" />
          <h2 className="font-display font-bold text-lg text-foreground">Where to Watch</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {watchBars.map((bar) => (
            <WatchBarCard key={bar.id} bar={bar} />
          ))}
        </div>
      </div>
    </div>
  );
}
