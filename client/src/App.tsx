import { Switch, Route, Router } from "wouter";
import { useHashLocation } from "wouter/use-hash-location";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { NavBar } from "@/components/NavBar";
import { ExplorePage } from "@/pages/ExplorePage";
import { EventsPage } from "@/pages/EventsPage";
import { SpotsPage } from "@/pages/SpotsPage";
import { SportsPage } from "@/pages/SportsPage";
import { InfluencersPage } from "@/pages/InfluencersPage";
import { PerplexityAttribution } from "@/components/PerplexityAttribution";
import NotFound from "@/pages/not-found";
import { Analytics } from "@vercel/analytics/react";

function AppRouter() {
  return (
    <Switch>
      <Route path="/" component={ExplorePage} />
      <Route path="/events" component={EventsPage} />
      <Route path="/spots" component={SpotsPage} />
      <Route path="/sports" component={SportsPage} />
      <Route path="/influencers" component={InfluencersPage} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Router hook={useHashLocation}>
          <div className="min-h-screen bg-background text-foreground">
            <NavBar />
            <main>
              <AppRouter />
            </main>
            <footer className="border-t border-border/30 py-6 px-4 mt-8">
              <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
                <p className="text-xs text-muted-foreground/50">
                  PHL Underground — Philadelphia's insider city guide
                </p>
                <PerplexityAttribution />
              </div>
            </footer>
          </div>
        </Router>
        <Analytics />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
