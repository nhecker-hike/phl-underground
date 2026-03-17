import { useState } from "react";
import { apiRequest } from "@/lib/queryClient";
import { Mail, ArrowRight, Check, Zap } from "lucide-react";

type Status = "idle" | "loading" | "success" | "error" | "duplicate";

export function EmailCapture() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email.trim() || status === "loading") return;

    setStatus("loading");
    try {
      const res = await apiRequest("POST", "/api/subscribe", { email: email.trim() });
      const data = await res.json();

      if (data.message === "You're already on the list") {
        setStatus("duplicate");
        setMessage("You're already on the list — we got you.");
      } else {
        setStatus("success");
        setMessage("You're in. Welcome to the underground.");
      }
      setEmail("");
    } catch (err: any) {
      setStatus("error");
      setMessage("Something went wrong. Try again.");
    }
  }

  const showForm = status === "idle" || status === "error";

  return (
    <div className="relative overflow-hidden" data-testid="email-capture">
      {/* Subtle gradient backdrop */}
      <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-transparent to-primary/5 rounded-2xl" />
      <div
        className="relative border border-border/40 rounded-2xl p-6 sm:p-8"
        style={{ backgroundColor: "hsl(220 12% 8%)" }}
      >
        <div className="max-w-xl mx-auto text-center">
          {/* Icon + heading */}
          <div className="flex items-center justify-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
              <Zap size={16} className="text-primary" />
            </div>
          </div>

          <h3
            className="font-display font-bold text-lg sm:text-xl text-foreground mb-1.5"
            style={{ fontFamily: "var(--font-display)" }}
          >
            Stay plugged in
          </h3>
          <p className="text-sm text-muted-foreground mb-5 leading-relaxed">
            Get the latest events, new spots, and insider picks — straight to your inbox.
          </p>

          {showForm ? (
            <form
              onSubmit={handleSubmit}
              className="flex flex-col sm:flex-row items-center gap-3"
              data-testid="email-capture-form"
            >
              <div className="relative flex-1 w-full">
                <Mail
                  size={16}
                  className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground/60 pointer-events-none"
                />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (status === "error") setStatus("idle");
                  }}
                  placeholder="your@email.com"
                  required
                  className="w-full pl-10 pr-4 py-3 text-sm bg-white/5 border border-border/50 rounded-xl text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary/50 transition-all"
                  data-testid="input-email"
                />
              </div>
              <button
                type="submit"
                disabled={status === "loading" || !email.trim()}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3 text-sm font-semibold rounded-xl bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                data-testid="button-subscribe"
              >
                {status === "loading" ? (
                  <div className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                ) : (
                  <>
                    Get Updates
                    <ArrowRight size={14} />
                  </>
                )}
              </button>
            </form>
          ) : (
            <div
              className="flex items-center justify-center gap-2 py-3 animate-fade-in-up"
              data-testid="email-capture-result"
            >
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center ${
                  status === "success" || status === "duplicate"
                    ? "bg-emerald-500/20 text-emerald-400"
                    : "bg-destructive/20 text-destructive"
                }`}
              >
                <Check size={14} />
              </div>
              <span
                className={`text-sm font-medium ${
                  status === "success" || status === "duplicate"
                    ? "text-emerald-400"
                    : "text-destructive"
                }`}
              >
                {message}
              </span>
            </div>
          )}

          {status === "error" && (
            <p className="text-xs text-destructive mt-2">{message}</p>
          )}

          <p className="text-[11px] text-muted-foreground/40 mt-4">
            No spam. Just the best of Philly. Unsubscribe anytime.
          </p>
        </div>
      </div>
    </div>
  );
}
