import { X, Calendar, MapPin, Clock, DollarSign, Star, ExternalLink, Ticket, Music } from "lucide-react";
import type { PhillyEvent, HotSpot } from "@/data/philly-data";
import { findTicketLink, findMusicLink, findRestaurantLink } from "@/data/philly-data";

interface EventDrawerProps {
  event: PhillyEvent;
  onClose: () => void;
}

interface SpotDrawerProps {
  spot: HotSpot;
  onClose: () => void;
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
  casual: "bg-blue-400/15 text-blue-300",
  romantic: "bg-rose-400/15 text-rose-300",
  dive: "bg-red-400/15 text-red-300",
};

function DrawerShell({ onClose, children }: { onClose: () => void; children: React.ReactNode }) {
  return (
    <div
      className="fixed inset-0 z-[90] flex items-end justify-center"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
      data-testid="detail-drawer-backdrop"
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm animate-fade-in" onClick={onClose} />

      {/* Drawer */}
      <div className="relative w-full max-w-2xl max-h-[85vh] bg-card border-t border-x border-border rounded-t-2xl overflow-hidden animate-slide-up z-10">
        {/* Handle */}
        <div className="flex justify-center pt-3 pb-1">
          <div className="w-10 h-1 rounded-full bg-border" />
        </div>

        {/* Close */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 p-2 rounded-lg hover:bg-white/10 text-muted-foreground hover:text-foreground transition z-10"
          data-testid="button-close-drawer"
        >
          <X size={18} />
        </button>

        {/* Content */}
        <div className="overflow-y-auto px-5 pb-8 pt-2" style={{ maxHeight: "calc(85vh - 48px)" }}>
          {children}
        </div>
      </div>
    </div>
  );
}

export function EventDrawer({ event, onClose }: EventDrawerProps) {
  const ticket = findTicketLink(event.name);
  const music = event.category === "music" ? findMusicLink(event.name) : undefined;

  return (
    <DrawerShell onClose={onClose}>
      {/* Badges */}
      <div className="flex items-center gap-2 mb-3 flex-wrap">
        <span className="text-[11px] font-medium uppercase tracking-wider px-2.5 py-1 rounded bg-primary/15 text-primary">
          {event.category}
        </span>
        <span className={`text-[11px] font-medium px-2.5 py-1 rounded ${vibeBadgeColors[event.vibeTag] || "bg-slate-500/15 text-slate-300"}`}>
          {event.vibeTag}
        </span>
        {event.isInsider && (
          <span className="text-[11px] font-bold px-2.5 py-1 rounded bg-primary/25 text-primary">
            ★ INSIDER PICK
          </span>
        )}
      </div>

      {/* Title */}
      <h2 className="font-display font-bold text-xl text-foreground leading-tight mb-4">
        {event.name}
      </h2>

      {/* Meta */}
      <div className="space-y-2.5 mb-5">
        <div className="flex items-center gap-2.5 text-sm">
          <Calendar size={15} className="text-primary flex-shrink-0" />
          <span className="text-foreground">{event.date}</span>
        </div>
        <div className="flex items-center gap-2.5 text-sm">
          <Clock size={15} className="text-primary flex-shrink-0" />
          <span className="text-foreground">{event.time}</span>
        </div>
        <div className="flex items-center gap-2.5 text-sm">
          <MapPin size={15} className="text-primary flex-shrink-0" />
          <span className="text-foreground">{event.venue}</span>
        </div>
        <div className="flex items-start gap-2.5 text-sm">
          <span className="text-muted-foreground flex-shrink-0 ml-[27px]">{event.address}</span>
        </div>
        <div className="flex items-center gap-2.5 text-sm">
          <DollarSign size={15} className="text-primary flex-shrink-0" />
          <span className="text-foreground">{event.price}</span>
        </div>
      </div>

      {/* Action Links */}
      <div className="flex flex-wrap gap-2 mb-4">
        {ticket && (
          <a
            href={ticket.ticketUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm font-medium px-4 py-2 rounded-lg bg-primary/15 text-primary hover:bg-primary/25 transition"
            data-testid="link-get-tickets"
          >
            <Ticket size={14} />
            Get Tickets
            <ExternalLink size={11} />
          </a>
        )}
        {music && (
          <a
            href={music.spotifyUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm font-medium px-4 py-2 rounded-lg bg-emerald-500/15 text-emerald-300 hover:bg-emerald-500/25 transition"
            data-testid="link-spotify"
          >
            <Music size={14} />
            Listen on Spotify
            <ExternalLink size={11} />
          </a>
        )}
      </div>

      {/* Description */}
      <div className="border-t border-border/50 pt-4">
        <p className="text-sm text-muted-foreground leading-relaxed">{event.description}</p>
      </div>

      {/* Source */}
      <div className="mt-4 pt-3 border-t border-border/30">
        <span className="text-[11px] text-muted-foreground/50">Source: {event.source}</span>
      </div>
    </DrawerShell>
  );
}

export function SpotDrawer({ spot, onClose }: SpotDrawerProps) {
  const restaurant = findRestaurantLink(spot.name);

  return (
    <DrawerShell onClose={onClose}>
      {/* Badges */}
      <div className="flex items-center gap-2 mb-3 flex-wrap">
        <span className="text-[11px] font-medium capitalize px-2.5 py-1 rounded bg-cyan-500/15 text-cyan-300">
          {spot.type}
        </span>
        <span className={`text-[11px] font-medium px-2.5 py-1 rounded ${vibeBadgeColors[spot.vibeTag] || "bg-slate-500/15 text-slate-300"}`}>
          {spot.vibeTag}
        </span>
        {spot.isNew && (
          <span className="text-[11px] font-bold px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300">
            NEW
          </span>
        )}
        {spot.isInsider && (
          <span className="text-[11px] font-bold px-2.5 py-1 rounded bg-primary/25 text-primary">
            ★ INSIDER PICK
          </span>
        )}
      </div>

      {/* Title */}
      <h2 className="font-display font-bold text-xl text-foreground leading-tight mb-1">
        {spot.name}
      </h2>
      {spot.cuisine && (
        <p className="text-sm text-muted-foreground mb-4">{spot.cuisine}</p>
      )}

      {/* Meta */}
      <div className="space-y-2.5 mb-5">
        <div className="flex items-center gap-2.5 text-sm">
          <MapPin size={15} className="text-primary flex-shrink-0" />
          <span className="text-foreground">{spot.neighborhood}</span>
        </div>
        <div className="flex items-start gap-2.5 text-sm">
          <span className="text-muted-foreground flex-shrink-0 ml-[27px]">{spot.address}</span>
        </div>
        <div className="flex items-center gap-2.5 text-sm">
          <DollarSign size={15} className="text-primary flex-shrink-0" />
          <span className="text-foreground text-lg tracking-wider">
            {Array.from({ length: 4 }).map((_, i) => (
              <span key={i} className={i < spot.priceRange.length ? "text-primary" : "text-muted-foreground/20"}>$</span>
            ))}
          </span>
        </div>
      </div>

      {/* Action Links */}
      {restaurant && (
        <div className="flex flex-wrap gap-2 mb-4">
          {restaurant.resyUrl && (
            <a
              href={restaurant.resyUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-medium px-4 py-2 rounded-lg bg-primary/15 text-primary hover:bg-primary/25 transition"
              data-testid="link-resy"
            >
              Reserve on Resy
              <ExternalLink size={11} />
            </a>
          )}
          {restaurant.openTableUrl && (
            <a
              href={restaurant.openTableUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-medium px-4 py-2 rounded-lg bg-primary/15 text-primary hover:bg-primary/25 transition"
              data-testid="link-opentable"
            >
              Reserve on OpenTable
              <ExternalLink size={11} />
            </a>
          )}
          {!restaurant.resyUrl && !restaurant.openTableUrl && restaurant.websiteUrl && (
            <a
              href={restaurant.websiteUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-medium px-4 py-2 rounded-lg bg-white/5 text-foreground hover:bg-white/10 transition"
              data-testid="link-website"
            >
              Visit Website
              <ExternalLink size={11} />
            </a>
          )}
        </div>
      )}

      {/* Description */}
      <div className="border-t border-border/50 pt-4">
        <p className="text-sm text-muted-foreground leading-relaxed">{spot.description}</p>
      </div>

      {/* Source */}
      <div className="mt-4 pt-3 border-t border-border/30">
        <span className="text-[11px] text-muted-foreground/50">Source: {spot.source}</span>
      </div>
    </DrawerShell>
  );
}
