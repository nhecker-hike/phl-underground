import { useState } from "react";
import { Link, useLocation } from "wouter";
import { Search, X, Menu } from "lucide-react";
import { Logo } from "./Logo";
import { SearchOverlay } from "./SearchOverlay";

const navLinks = [
  { href: "/", label: "Explore" },
  { href: "/events", label: "Events" },
  { href: "/spots", label: "Hot Spots" },
  { href: "/sports", label: "Sports" },
  { href: "/influencers", label: "Influencers" },
];

export function NavBar() {
  const [location] = useLocation();
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      <nav
        className="sticky top-0 z-50 border-b border-border/50 backdrop-blur-xl"
        style={{ backgroundColor: "hsl(220 15% 6% / 0.9)" }}
        data-testid="navbar"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2.5 no-underline group" data-testid="link-home">
              <span className="text-primary">
                <Logo size={28} />
              </span>
              <span className="font-display font-bold text-lg tracking-tight text-foreground group-hover:text-primary transition-colors">
                PHL<span className="text-primary">Underground</span>
              </span>
            </Link>

            {/* Desktop Nav Links */}
            <div className="hidden md:flex items-center gap-1">
              {navLinks.map((link) => {
                const isActive = location === link.href || (link.href !== "/" && location.startsWith(link.href));
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`px-3.5 py-2 text-sm font-medium rounded-lg transition-all duration-200 no-underline ${
                      isActive
                        ? "text-primary bg-primary/10"
                        : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                    }`}
                    data-testid={`link-${link.label.toLowerCase().replace(' ', '-')}`}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </div>

            {/* Search + Mobile Toggle */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setSearchOpen(true)}
                className="flex items-center gap-2 px-3 py-1.5 text-sm text-muted-foreground bg-white/5 border border-border/50 rounded-lg hover:bg-white/10 hover:text-foreground transition-all"
                data-testid="button-search"
              >
                <Search size={15} />
                <span className="hidden sm:inline">Search</span>
                <kbd className="hidden lg:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono text-muted-foreground/60 bg-white/5 rounded">
                  ⌘K
                </kbd>
              </button>

              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 text-muted-foreground hover:text-foreground rounded-lg hover:bg-white/5 transition"
                data-testid="button-mobile-menu"
              >
                {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border/50 px-4 py-3 animate-fade-in" data-testid="mobile-menu">
            {navLinks.map((link) => {
              const isActive = location === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`block px-3 py-2.5 text-sm font-medium rounded-lg no-underline transition ${
                    isActive ? "text-primary bg-primary/10" : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </div>
        )}
      </nav>

      {searchOpen && <SearchOverlay onClose={() => setSearchOpen(false)} />}
    </>
  );
}
