import { useLocation, Link } from "wouter";
import { Compass, CalendarDays, MapPin, Trophy, Users } from "lucide-react";

const tabs = [
  { href: "/", label: "Explore", icon: Compass },
  { href: "/events", label: "Events", icon: CalendarDays },
  { href: "/spots", label: "Spots", icon: MapPin },
  { href: "/sports", label: "Sports", icon: Trophy },
  { href: "/influencers", label: "Crew", icon: Users },
];

export function BottomNav() {
  const [location] = useLocation();

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-50 md:hidden border-t border-border/50 backdrop-blur-xl safe-area-bottom"
      style={{ backgroundColor: "hsl(220 15% 6% / 0.95)" }}
      data-testid="bottom-nav"
    >
      <div className="flex items-center justify-around h-14">
        {tabs.map((tab) => {
          const isActive =
            tab.href === "/"
              ? location === "/" || location === ""
              : location.startsWith(tab.href);
          const Icon = tab.icon;
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={`flex flex-col items-center justify-center gap-0.5 flex-1 h-full no-underline transition-colors ${
                isActive
                  ? "text-primary"
                  : "text-muted-foreground active:text-foreground"
              }`}
              data-testid={`bottomnav-${tab.label.toLowerCase()}`}
            >
              <Icon size={20} strokeWidth={isActive ? 2.25 : 1.75} />
              <span className={`text-[10px] leading-none ${isActive ? "font-semibold" : "font-medium"}`}>
                {tab.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
