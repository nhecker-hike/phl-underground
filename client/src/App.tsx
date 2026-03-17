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
import { BottomNav } from "@/components/BottomNav";
import NotFound from "@/pages/not-found";

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
            <main className="pb-16 md:pb-0">
              <AppRouter />
            </main>
            <BottomNav />
            <footer className="hidden md:block border-t border-border/30 py-6 px-4 mt-8">
              <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
                <p className="text-xs text-muted-foreground/50">
                  PHL Underground — Philadelphia's insider city guide
                </p>
                <PerplexityAttribution />
              </div>
            </footer>
          </div>
        </Router>
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
