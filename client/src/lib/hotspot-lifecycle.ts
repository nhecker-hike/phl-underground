/**
 * Hotspot Lifecycle Management
 * 
 * Computes dynamic trending scores and filters hotspots/events
 * to keep the app feeling fresh and curated — not a dumping ground.
 */

import type { HotSpot, PhillyEvent } from "@/data/philly-data";

const TODAY = new Date().toISOString().slice(0, 10);

/** How many days ago a date string (YYYY-MM-DD) was */
function daysAgo(dateStr: string): number {
  const d = new Date(dateStr);
  const now = new Date(TODAY);
  return Math.max(0, Math.floor((now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24)));
}

/**
 * Compute a dynamic trending score for a hotspot.
 * Factors:
 * - Base trendingScore from data (set by cron)
 * - Recency bonus: newer spots score higher
 * - Insider bonus
 * - Decay: spots older than 10 days start losing points
 */
export function computeHotspotScore(spot: HotSpot): number {
  if (!spot) return 0;
  let score = spot.trendingScore ?? 50;
  
  const age = daysAgo(spot.addedDate || "2026-03-01");
  
  // Recency bonus: 0-3 days = +30, 4-7 days = +15, 8-14 days = +5
  if (age <= 3) score += 30;
  else if (age <= 7) score += 15;
  else if (age <= 14) score += 5;
  
  // Decay: after 10 days, lose 3 points per day
  if (age > 10) {
    score -= (age - 10) * 3;
  }
  
  // Insider bonus
  if (spot.isInsider) score += 15;
  
  // isNew bonus
  if (spot.isNew) score += 10;
  
  return Math.max(0, score);
}

/**
 * Get the top N hotspots by trending score.
 * Used for the map (capped at 25) and feed sections.
 */
export function getTopHotspots(spots: HotSpot[], limit: number = 25): HotSpot[] {
  return [...spots]
    .map(s => ({ spot: s, score: computeHotspotScore(s) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(({ spot }) => spot);
}

/**
 * Get all hotspots sorted by trending score (for SpotsPage listing).
 * No cap, but sorted so the hottest appear first.
 */
export function getSortedHotspots(spots: HotSpot[]): HotSpot[] {
  return [...spots]
    .map(s => ({ spot: s, score: computeHotspotScore(s) }))
    .sort((a, b) => b.score - a.score)
    .map(({ spot }) => spot);
}

/**
 * Parse an event date string and check if it has passed.
 * Handles formats like "2026-03-26", "2026-03-28 to 2026-03-29", etc.
 */
function getEventEndDate(dateStr: string): string {
  // If "to" format, get the end date
  const toMatch = dateStr.match(/to\s+(\d{4}-\d{2}-\d{2})/);
  if (toMatch) return toMatch[1];
  
  // Single date
  const singleMatch = dateStr.match(/(\d{4}-\d{2}-\d{2})/);
  if (singleMatch) return singleMatch[1];
  
  return dateStr;
}

/**
 * Check if an event is upcoming (not yet passed).
 */
export function isUpcoming(event: PhillyEvent): boolean {
  const endDate = getEventEndDate(event.date);
  return endDate >= TODAY;
}

/**
 * Get upcoming events sorted by date (soonest first).
 */
export function getUpcomingEvents(allEvents: PhillyEvent[]): PhillyEvent[] {
  return allEvents
    .filter(isUpcoming)
    .sort((a, b) => {
      const dateA = a.date.match(/\d{4}-\d{2}-\d{2}/)?.[0] || a.date;
      const dateB = b.date.match(/\d{4}-\d{2}-\d{2}/)?.[0] || b.date;
      return dateA.localeCompare(dateB);
    });
}

/**
 * Score events for the "What's Hot" feed.
 * Insider events and events happening sooner rank higher.
 */
export function getHottestEvents(allEvents: PhillyEvent[], limit: number = 15): PhillyEvent[] {
  const upcoming = getUpcomingEvents(allEvents);
  
  return upcoming
    .map(e => {
      let score = 50;
      const firstDate = e.date.match(/\d{4}-\d{2}-\d{2}/)?.[0] || e.date;
      const daysUntil = Math.max(0, -daysAgo(firstDate)); // negative daysAgo = future
      
      // Actually let's recalculate properly
      const eventDate = new Date(firstDate);
      const now = new Date(TODAY);
      const daysUntilEvent = Math.floor((eventDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
      
      // Happening very soon = higher score
      if (daysUntilEvent <= 2) score += 40;
      else if (daysUntilEvent <= 5) score += 25;
      else if (daysUntilEvent <= 10) score += 15;
      
      if (e.isInsider) score += 20;
      
      return { event: e, score };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(({ event }) => event);
}
