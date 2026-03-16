import { Calendar, MapPin, DollarSign, Star, Ticket } from "lucide-react";
import type { PhillyEvent } from "@/data/philly-data";
import { findTicketLink } from "@/data/philly-data";

interface Props {
  event: PhillyEvent;
  onClick?: () => void;
  compact?: boolean;
}

const vibeBadgeColors: Record<string, string> = {
  underground: "bg-purple-500/15 text-purple-300",
  upscale: "bg-amber-500/15 text-amber-300",
  trendy: "bg-pink-500/15 text-pink-300",
  chill: "bg-blue-500/15 text-blue-300",
  boozy: "bg-red-500/15 text-red-300",
  mainstream: "bg-slate-500/15 text-slate-300",
  "date-night": "bg-rose-500/15 text-rose-300",
  "family-friendly": "bg-green-500/15 text-green-300",
  lively: "bg-orange-500/15 text-orange-300",
};

function formatDate(dateStr: string) {
  // Handle "Through YYYY-MM-DD" prefix
  if (dateStr.startsWith("Through ")) {
    const d = new Date(dateStr.replace("Through ", "") + "T12:00:00");
    if (!isNaN(d.getTime())) {
      return `Through ${d.toLocaleDateString("en-US", { month: "short" })} ${d.getDate()}`;
    }
    return dateStr;
  }
  // Handle ranges: "to", "and", or separate dates
  const parts = dateStr.split(/ to | and /);
  const rawFirst = parts[0].trim();
  // Extract first date-like substring (YYYY-MM-DD)
  const dateMatch = rawFirst.match(/(\d{4}-\d{2}-\d{2})/);
  if (!dateMatch) return dateStr;
  const d = new Date(dateMatch[1] + "T12:00:00");
  if (isNaN(d.getTime())) return dateStr;
  const month = d.toLocaleDateString("en-US", { month: "short" });
  const day = d.getDate();
  if (parts.length > 1) {
    const rawSecond = parts[parts.length - 1].trim();
    const dateMatch2 = rawSecond.match(/(\d{4}-\d{2}-\d{2})/);
    if (dateMatch2) {
      const d2 = new Date(dateMatch2[1] + "T12:00:00");
      if (!isNaN(d2.getTime())) {
        const month2 = d2.toLocaleDateString("en-US", { month: "short" });
        const day2 = d2.getDate();
        return `${month} ${day} – ${month2} ${day2}`;
      }
    }
  }
  return `${month} ${day}`;
}

export function EventCard({ event, onClick, compact }: Props) {
  const hasTicket = !!findTicketLink(event.name);

  return (
    <button
      onClick={onClick}
      className={`text-left w-full group rounded-xl border border-border/50 bg-card hover:bg-white/[0.04] transition-all duration-200 overflow-hidden ${
        event.isInsider ? "insider-glow" : ""
      } ${compact ? "p-3.5" : "p-4"}`}
      data-testid={`card-event-${event.id}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          {/* Date row */}
          <div className="flex items-center gap-1.5 mb-1.5">
            <Calendar size={12} className="text-primary flex-shrink-0" />
            <span className="text-xs font-medium text-primary">{formatDate(event.date)}</span>
            {hasTicket && (
              <Ticket size={11} className="text-primary/60 flex-shrink-0" data-testid={`ticket-indicator-${event.id}`} />
            )}
          </div>

          {/* Title */}
          <h3 className={`font-display font-semibold text-foreground group-hover:text-primary transition-colors leading-tight ${
            compact ? "text-sm" : "text-[15px]"
          }`}>
            {event.name}
          </h3>

          {/* Venue + neighborhood */}
          <div className="flex items-center gap-1.5 mt-1.5">
            <MapPin size={11} className="text-muted-foreground flex-shrink-0" />
            <span className="text-xs text-muted-foreground truncate">
              {event.venue} · {event.neighborhood}
            </span>
          </div>

          {/* Badges row */}
          <div className="flex items-center gap-1.5 mt-2.5 flex-wrap">
            <span className="text-[10px] font-medium uppercase tracking-wider px-2 py-0.5 rounded bg-white/5 text-muted-foreground">
              {event.category}
            </span>
            <span className={`text-[10px] font-medium px-2 py-0.5 rounded ${vibeBadgeColors[event.vibeTag] || "bg-slate-500/15 text-slate-300"}`}>
              {event.vibeTag}
            </span>
            {event.isInsider && (
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-primary/20 text-primary">
                INSIDER
              </span>
            )}
          </div>
        </div>

        {/* Price */}
        <div className="flex-shrink-0 text-right">
          <span className="text-xs font-medium text-muted-foreground">{event.price}</span>
        </div>
      </div>
    </button>
  );
}
