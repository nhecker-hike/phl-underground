import { useEffect, useRef } from "react";
import L from "leaflet";
import { events, hotspots, sportsTeams, type PhillyEvent, type HotSpot, type SportsTeam } from "@/data/philly-data";
import { MapLegend } from "./MapLegend";

// Custom marker icons
function createMarkerIcon(color: string) {
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="
      width: 14px; height: 14px;
      background: ${color};
      border: 2px solid rgba(255,255,255,0.8);
      border-radius: 50%;
      box-shadow: 0 0 8px ${color}80, 0 2px 4px rgba(0,0,0,0.5);
    "></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
    popupAnchor: [0, -10],
  });
}

const goldIcon = createMarkerIcon("hsl(45, 100%, 60%)");
const cyanIcon = createMarkerIcon("hsl(190, 80%, 50%)");
const greenIcon = createMarkerIcon("hsl(142, 71%, 45%)");

interface Props {
  height?: string;
  onEventClick?: (event: PhillyEvent) => void;
  onSpotClick?: (spot: HotSpot) => void;
  filteredEvents?: PhillyEvent[];
  filteredSpots?: HotSpot[];
  showEvents?: boolean;
  showSpots?: boolean;
  showSports?: boolean;
}

export function MapView({
  height = "60vh",
  onEventClick,
  onSpotClick,
  filteredEvents,
  filteredSpots,
  showEvents = true,
  showSpots = true,
  showSports = true,
}: Props) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return;

    const map = L.map(mapRef.current, {
      center: [39.9526, -75.1652],
      zoom: 13,
      zoomControl: true,
      attributionControl: true,
    });

    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 19,
    }).addTo(map);

    mapInstance.current = map;

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, []);

  // Update markers when filters change
  useEffect(() => {
    const map = mapInstance.current;
    if (!map) return;

    // Clear existing markers
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    const eventsToShow = showEvents ? (filteredEvents || events) : [];
    const spotsToShow = showSpots ? (filteredSpots || hotspots) : [];

    eventsToShow.forEach((event) => {
      const marker = L.marker([event.lat, event.lng], { icon: goldIcon }).addTo(map);
      const insiderBadge = event.isInsider
        ? '<span style="background:hsl(45,100%,60%);color:#000;padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600;">INSIDER</span>'
        : '';
      marker.bindPopup(`
        <div style="min-width:180px;font-family:General Sans,sans-serif;">
          <div style="font-size:13px;font-weight:600;margin-bottom:4px;line-height:1.3;">${event.name}</div>
          <div style="font-size:11px;color:hsl(220,5%,55%);margin-bottom:4px;">${event.venue}</div>
          <div style="display:flex;gap:4px;align-items:center;flex-wrap:wrap;">
            <span style="background:hsl(45,100%,60%,0.15);color:hsl(45,100%,60%);padding:1px 6px;border-radius:4px;font-size:10px;font-weight:500;">${event.category}</span>
            ${insiderBadge}
          </div>
        </div>
      `);
      marker.on("click", () => onEventClick?.(event));
    });

    spotsToShow.forEach((spot) => {
      const marker = L.marker([spot.lat, spot.lng], { icon: cyanIcon }).addTo(map);
      const insiderBadge = spot.isInsider
        ? '<span style="background:hsl(45,100%,60%);color:#000;padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600;">INSIDER</span>'
        : '';
      const newBadge = spot.isNew
        ? '<span style="background:hsl(150,60%,40%);color:#fff;padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600;">NEW</span>'
        : '';
      marker.bindPopup(`
        <div style="min-width:180px;font-family:General Sans,sans-serif;">
          <div style="font-size:13px;font-weight:600;margin-bottom:4px;line-height:1.3;">${spot.name}</div>
          <div style="font-size:11px;color:hsl(220,5%,55%);margin-bottom:4px;">${spot.neighborhood} · ${spot.priceRange}</div>
          <div style="display:flex;gap:4px;align-items:center;flex-wrap:wrap;">
            <span style="background:hsl(190,80%,50%,0.15);color:hsl(190,80%,50%);padding:1px 6px;border-radius:4px;font-size:10px;font-weight:500;">${spot.type}</span>
            ${newBadge}
            ${insiderBadge}
          </div>
        </div>
      `);
      marker.on("click", () => onSpotClick?.(spot));
    });

    // Sports venue markers
    if (showSports) {
      const venuesWithHomeGames = sportsTeams.filter(
        (t) => t.upcomingGames.some((g) => g.homeAway === "home" || g.homeAway === "neutral")
      );
      // Deduplicate by lat/lng (multiple teams share venues)
      const seen = new Set<string>();
      venuesWithHomeGames.forEach((team) => {
        const key = `${team.lat},${team.lng}`;
        if (seen.has(key)) return;
        seen.add(key);

        const teamsAtVenue = venuesWithHomeGames.filter((t) => t.lat === team.lat && t.lng === team.lng);
        const nextGame = teamsAtVenue
          .flatMap((t) => t.upcomingGames.filter((g) => g.homeAway === "home" || g.homeAway === "neutral"))
          .sort((a, b) => a.date.localeCompare(b.date))[0];

        const teamNames = teamsAtVenue.map((t) => t.team).join(", ");
        const marker = L.marker([team.lat, team.lng], { icon: greenIcon }).addTo(map);
        marker.bindPopup(`
          <div style="min-width:180px;font-family:General Sans,sans-serif;">
            <div style="font-size:13px;font-weight:600;margin-bottom:4px;line-height:1.3;">${teamNames}</div>
            <div style="font-size:11px;color:hsl(220,5%,55%);margin-bottom:4px;">${team.venue}</div>
            ${nextGame ? `<div style="font-size:11px;color:hsl(142,71%,45%);margin-top:2px;">Next: vs ${nextGame.opponent} · ${nextGame.date}</div>` : ""}
          </div>
        `);
      });
    }
  }, [filteredEvents, filteredSpots, showEvents, showSpots, showSports, onEventClick, onSpotClick]);

  return (
    <div className="relative" style={{ height, width: "100%" }}>
      <div
        ref={mapRef}
        style={{ height: "100%", width: "100%" }}
        className="rounded-xl overflow-hidden border border-border/50"
        data-testid="map-view"
      />
      <MapLegend />
    </div>
  );
}
