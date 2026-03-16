export function MapLegend() {
  return (
    <div
      className="absolute bottom-8 left-3 z-[400] rounded-lg border border-border/50 px-3 py-2.5"
      style={{ backgroundColor: "hsl(220 15% 6% / 0.85)", backdropFilter: "blur(8px)" }}
      data-testid="map-legend"
    >
      <div className="flex flex-col gap-1.5 text-[11px]">
        <div className="flex items-center gap-2">
          <span className="block w-2.5 h-2.5 rounded-full" style={{ background: "hsl(45, 100%, 60%)", boxShadow: "0 0 6px hsl(45 100% 60% / 0.5)" }} />
          <span className="text-muted-foreground">Events</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="block w-2.5 h-2.5 rounded-full" style={{ background: "hsl(190, 80%, 50%)", boxShadow: "0 0 6px hsl(190 80% 50% / 0.5)" }} />
          <span className="text-muted-foreground">Hot Spots</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="block w-2.5 h-2.5 rounded-full" style={{ background: "hsl(142, 71%, 45%)", boxShadow: "0 0 6px hsl(142 71% 45% / 0.5)" }} />
          <span className="text-muted-foreground">Sports Venues</span>
        </div>
      </div>
    </div>
  );
}
