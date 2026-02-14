"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { MetricCard, NarrativeCard } from "@/components/DataDisplay";
import { SkeletonCard, SkeletonMetricCard } from "@/components/Skeleton";
import { EmptyState, ErrorState } from "@/components/States";
import { AnimateOnScroll } from "@/hooks/useScrollAnimation";
import { fetchDashboard, fetchSignals, Narrative, Signal } from "@/lib/api";

interface Stats {
  total_narratives: number;
  active_narratives: number;
  total_signals: number;
  avg_confidence: number;
  last_updated: string;
}

// Helper function to format timestamps as relative time
function formatTimeAgo(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return "just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [narratives, setNarratives] = useState<Narrative[]>([]);
  const [recentSignals, setRecentSignals] = useState<Signal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [data, signalData] = await Promise.all([
          fetchDashboard(),
          fetchSignals({ limit: 5 }),
        ]);
        
        // Compute active narratives (non-DECLINING)
        const activeCount = data.narratives.filter(
          (n) => n.status !== "DECLINING"
        ).length;
        
        // Compute average confidence (already 0-100)
        const avgConf = data.narratives.length > 0
          ? Math.round(
              data.narratives.reduce((sum, n) => sum + n.confidence, 0) /
                data.narratives.length
            )
          : 0;
        
        setStats({
          total_narratives: data.summary.total_narratives,
          active_narratives: activeCount,
          total_signals: data.summary.total_signals,
          avg_confidence: avgConf,
          last_updated: formatTimeAgo(data.last_updated),
        });
        
        setNarratives(data.narratives.slice(0, 4));
        setRecentSignals(signalData.signals || []);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
        setError("Failed to load dashboard data. Is the backend running?");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const retry = () => {
    setLoading(true);
    setError(null);
    window.location.reload();
  };

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <header className="relative py-8 lg:py-12">
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-indigo-500/10 via-purple-500/10 to-pink-500/10 rounded-full blur-3xl animate-float" />
        </div>
        <div className="text-center space-y-4">
          <h1 className="font-serif text-4xl lg:text-5xl tracking-tight">
            Discover <span className="text-gradient">Emerging Narratives</span>
          </h1>
          <p className="text-lg text-text-secondary max-w-2xl mx-auto">
            Real-time intelligence on the Solana ecosystem. Detect what matters before it becomes obvious.
          </p>
          {stats && (
            <p className="text-sm text-text-tertiary">
              Last updated {stats.last_updated}
            </p>
          )}
        </div>
      </header>

      {/* Error State */}
      {error && <ErrorState description={error} retry={retry} />}

      {/* Metrics Grid */}
      <AnimateOnScroll>
        <section aria-labelledby="metrics-heading">
          <h2 id="metrics-heading" className="sr-only">Key Metrics</h2>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            {loading ? (
              <>
                <SkeletonMetricCard />
                <SkeletonMetricCard />
                <SkeletonMetricCard />
                <SkeletonMetricCard />
              </>
            ) : stats ? (
              <>
                <div className="hover-lift">
                  <MetricCard
                    label="Total Narratives"
                    value={stats.total_narratives}
                    subtext="Detected this period"
                  />
                </div>
                <div className="hover-lift">
                  <MetricCard
                    label="Active"
                    value={stats.active_narratives}
                    subtext="Currently monitored"
                  />
                </div>
                <div className="hover-lift">
                  <MetricCard
                    label="Total Signals"
                    value={stats.total_signals}
                    subtext="Ingested signals"
                  />
                </div>
                <div className="hover-lift">
                  <MetricCard
                    label="Avg. Confidence"
                    value={`${stats.avg_confidence}%`}
                    subtext="Cross-narrative"
                  />
                </div>
              </>
            ) : null}
          </div>
        </section>
      </AnimateOnScroll>

      {/* Top Narratives */}
      <AnimateOnScroll delay={100}>
        <section aria-labelledby="narratives-heading">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 id="narratives-heading" className="font-serif text-2xl">
                Top Narratives
              </h2>
              <p className="text-sm text-text-tertiary mt-1">
                Most significant trends detected this period
              </p>
            </div>
            <Link
              href="/narratives"
              className="btn btn-secondary px-4 py-2 text-sm group"
            >
              View all
              <svg className="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>

          {loading ? (
            <div className="grid md:grid-cols-2 gap-6">
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </div>
          ) : narratives.length === 0 ? (
            <EmptyState
              title="No narratives detected"
              description="Narratives will appear here once signals are processed."
            />
          ) : (
            <div className="grid md:grid-cols-2 gap-6">
              {narratives.map((narrative, index) => (
                <div 
                  key={narrative.id} 
                  className="animate-on-scroll visible"
                  style={{ transitionDelay: `${index * 100}ms` }}
                >
                  <NarrativeCard
                    id={narrative.id}
                    title={narrative.label}
                    summary={narrative.summary}
                    status={narrative.status}
                    confidence={Math.round(narrative.confidence)}
                    signalCount={narrative.signal_count}
                    lastUpdated={formatTimeAgo(narrative.last_seen)}
                    keywords={narrative.domains}
                    href={`/narratives/${narrative.id}`}
                  />
                </div>
              ))}
            </div>
          )}
        </section>
      </AnimateOnScroll>

      {/* Signal Activity */}
      <AnimateOnScroll delay={200}>
        <section aria-labelledby="activity-heading">
          <h2 id="activity-heading" className="font-serif text-2xl mb-6">
            Recent Activity
          </h2>
          <div className="card-static p-6 lg:p-8">
            <div className="space-y-4">
              {loading ? (
                <div className="animate-pulse space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center gap-4">
                      <div className="skeleton h-3 w-3 rounded-full" />
                      <div className="skeleton h-4 w-3/4 rounded" />
                      <div className="skeleton h-4 w-16 rounded ml-auto" />
                    </div>
                  ))}
                </div>
              ) : recentSignals.length === 0 ? (
                <div className="text-center py-6 text-text-tertiary text-sm">
                  No recent signals yet. Run the ingestion pipeline to collect data.
                </div>
              ) : (
                recentSignals.map((signal, idx) => {
                  const domainColor = signal.domain === "onchain"
                    ? "bg-emerald-500"
                    : signal.domain === "github"
                    ? "bg-violet-500"
                    : "bg-sky-500";
                  
                  return (
                    <div key={signal.id || idx} className="flex items-center gap-4 p-3 rounded-lg hover:bg-surface transition-colors group cursor-pointer">
                      <span className={`h-3 w-3 rounded-full ${domainColor}`} />
                      <span className="text-text-secondary flex-1 group-hover:text-text-primary transition-colors text-sm">
                        <span className="font-medium text-text-primary capitalize">[{signal.domain}]</span>{" "}
                        {signal.description || "Signal detected"}
                      </span>
                      <span className="text-text-tertiary text-xs whitespace-nowrap">
                        {signal.timestamp ? formatTimeAgo(signal.timestamp) : ""}
                      </span>
                    </div>
                  );
                }))}
            </div>
            <div className="mt-6 pt-6 border-t flex items-center justify-between">
              <Link
                href="/signals"
                className="text-sm text-accent hover:text-accent/80 transition-colors font-medium"
              >
                View all signals
              </Link>
              <span className="text-xs text-text-tertiary">
                Refreshed every 30 seconds
              </span>
            </div>
          </div>
        </section>
      </AnimateOnScroll>

      {/* CTA Section */}
      <AnimateOnScroll delay={300}>
        <section className="relative overflow-hidden">
          <div className="gradient-border">
            <div className="relative p-8 lg:p-12 bg-gradient-brand-subtle rounded-[15px]">
              <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-accent/10 to-transparent rounded-full blur-3xl" />
              <div className="relative flex flex-col lg:flex-row items-center justify-between gap-6">
                <div className="text-center lg:text-left">
                  <h3 className="font-serif text-2xl mb-2">
                    Understand Our Analysis
                  </h3>
                  <p className="text-text-secondary max-w-xl">
                    Learn how we detect narratives using semantic clustering, 
                    temporal analysis, and cross-source validation.
                  </p>
                </div>
                <Link
                  href="/methodology"
                  className="btn btn-primary px-6 py-3 text-sm whitespace-nowrap"
                >
                  View Methodology
                </Link>
              </div>
            </div>
          </div>
        </section>
      </AnimateOnScroll>
    </div>
  );
}
