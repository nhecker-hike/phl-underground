import { Calendar, MapPin, Ticket } from "lucide-react";
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
  if (dateStr.startsWith("Through ")) {
    const d = new Date(dateStr.replace("Through ", "") + "T12:00:00");
    if (!isNaN(d.getTime())) {
      return `Through ${d.toLocaleDateString("en-US", { month: "short" })} ${d.getDate()}`;
    }
    return dateStr;
  }
  const parts = dateStr.split(/ to | and /);
  const rawFirst = parts[0].trim();
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

/** Shorten long price strings */
function formatPrice(price: string) {
  if (price.length > 18) {
    // e.g. "$15 - $20 (advance tickets recommended)" → "$15 - $20"
    const m = price.match(/^\$[\d,.]+ ?[-–] ?\$[\d,.]+/);
    if (m) return m[0];
    const m2 = price.match(/^(?:Free|\$[\d,.]+\+?)/i);
    if (m2) return m2[0];
  }
  return price;
}

export function EventCard({ event, onClick, compact }: Props) {
  const hasTicket = !!findTicketLink(event.name);

  return (
    <button
      onClick={onClick}
      className={`text-left w-full h-full group rounded-xl border border-border/50 bg-card hover:bg-white/[0.04] transition-all duration-200 overflow-hidden flex flex-col ${
        event.isInsider ? "insider-glow" : ""
      } ${compact ? "p-3.5" : "p-4"}`}
      data-testid={`card-event-${event.id}`}
    >
      {/* Date + Price row */}
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-1.5 min-w-0">
          <Calendar size={12} className="text-primary flex-shrink-0" />
          <span className="text-xs font-medium text-primary truncate">{formatDate(event.date)}</span>
          {hasTicket && (
            <Ticket size={11} className="text-primary/60 flex-shrink-0" data-testid={`ticket-indicator-${event.id}`} />
          )}
        </div>
        <span className="text-[11px] font-medium text-muted-foreground flex-shrink-0 text-right max-w-[40%] truncate">
          {formatPrice(event.price)}
        </span>
      </div>

      {/* Title — clamped to 2 lines */}
      <h3 className={`font-display font-semibold text-foreground group-hover:text-primary transition-colors leading-snug line-clamp-2 mb-1.5 ${
        compact ? "text-sm" : "text-[15px]"
      }`}>
        {event.name}
      </h3>

      {/* Venue + neighborhood */}
      <div className="flex items-center gap-1.5 mb-auto">
        <MapPin size={11} className="text-muted-foreground flex-shrink-0" />
        <span className="text-xs text-muted-foreground truncate">
          {event.venue} · {event.neighborhood}
        </span>
      </div>

      {/* Badges row — pushed to bottom */}
      <div className="flex items-center gap-1.5 mt-3 flex-wrap">
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
    </button>
  );
}
