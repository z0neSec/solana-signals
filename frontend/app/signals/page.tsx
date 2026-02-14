"use client";

import { useState, useEffect } from "react";
import { DataTable } from "@/components/DataDisplay";
import { SkeletonTable } from "@/components/Skeleton";
import { EmptyState, ErrorState } from "@/components/States";
import { AnimateOnScroll } from "@/hooks/useScrollAnimation";
import { fetchSignals, Signal } from "@/lib/api";

const sourceFilters = ["All", "helius", "github", "twitter"];
const typeFilters = ["All", "program_activity", "network_health", "repo_created", "commit_activity", "tweet"];

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

export default function SignalsPage() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sourceFilter, setSourceFilter] = useState("All");
  const [typeFilter, setTypeFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchSignals();
        setSignals(response.signals);
      } catch (err) {
        setError("Failed to load signals. Is the backend running?");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredSignals = signals
    .filter((s) => sourceFilter === "All" || s.source === sourceFilter)
    .filter((s) => typeFilter === "All" || s.type === typeFilter)
    .filter(
      (s) =>
        searchQuery === "" ||
        (s.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          s.author?.toLowerCase().includes(searchQuery.toLowerCase()))
    );

  const columns = [
    {
      key: "source",
      header: "Source",
      width: "100px",
      render: (value: unknown) => (
        <span className="text-xs font-medium uppercase tracking-wide text-text-tertiary">
          {String(value)}
        </span>
      ),
    },
    {
      key: "description",
      header: "Content",
      render: (value: unknown) => (
        <span className="text-sm line-clamp-2">{String(value)}</span>
      ),
    },
    {
      key: "author",
      header: "Author",
      width: "140px",
      render: (value: unknown) => (
        <span className="text-sm text-text-secondary font-mono text-xs">{String(value)}</span>
      ),
    },
    {
      key: "narratives",
      header: "Narrative",
      width: "160px",
      render: (value: any, row: Signal) => (
        row.narratives && row.narratives.label ? (
          <a
            href={`/narratives/${row.narrative_id}`}
            className="text-sm text-accent hover:text-accent/80 transition-colors"
          >
            {row.narratives.label}
          </a>
        ) : (
          <span className="text-xs text-text-tertiary">—</span>
        )
      ),
    },
    {
      key: "credibility_score",
      header: "Relevance",
      width: "90px",
      render: (value: unknown) => (
        <span className="metric-value text-sm">{Math.round(Number(value) * 100)}%</span>
      ),
    },
    {
      key: "timestamp",
      header: "Time",
      width: "100px",
      render: (value: unknown) => (
        <span className="text-xs text-text-tertiary">{formatTimeAgo(String(value))}</span>
      ),
    },
  ];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <AnimateOnScroll>
        <header className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-surface-raised rounded-full border border-border-subtle">
            <svg className="w-4 h-4 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span className="text-xs font-medium text-text-secondary">Real-time Feed</span>
          </div>
          <h1 className="font-serif text-3xl lg:text-4xl tracking-tight text-gradient">
            Signal Stream
          </h1>
          <p className="text-text-secondary max-w-2xl">
            Live signals from across the Solana ecosystem—social media, development activity, news, and community discussions.
          </p>
        </header>
      </AnimateOnScroll>

      {/* Filters */}
      <AnimateOnScroll delay={100}>
        <div className="card p-4 lg:p-5">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <label htmlFor="signal-search" className="sr-only">
                Search signals
              </label>
              <input
                id="signal-search"
                type="text"
                placeholder="Search content or author..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 text-sm bg-surface border border-border-subtle rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent placeholder:text-text-tertiary transition-shadow"
              />
            </div>

            {/* Source Filter */}
            <div>
              <label htmlFor="source-filter" className="sr-only">
                Filter by source
              </label>
              <select
                id="source-filter"
                value={sourceFilter}
                onChange={(e) => setSourceFilter(e.target.value)}
                className="px-4 py-2.5 text-sm bg-surface border border-border-subtle rounded-lg focus:outline-none focus:ring-2 focus:ring-accent cursor-pointer"
              >
                {sourceFilters.map((source) => {
                  const label: Record<string, string> = { helius: "Helius (Onchain)", github: "GitHub", twitter: "Twitter" };
                  return (
                    <option key={source} value={source}>
                      {source === "All" ? "All Sources" : label[source] || source}
                    </option>
                  );
                })}
              </select>
            </div>

            {/* Type Filter */}
            <div>
              <label htmlFor="type-filter" className="sr-only">
                Filter by type
              </label>
              <select
                id="type-filter"
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                className="px-4 py-2.5 text-sm bg-surface border border-border-subtle rounded-lg focus:outline-none focus:ring-2 focus:ring-accent cursor-pointer"
              >
                {typeFilters.map((type) => {
                  const label: Record<string, string> = { program_activity: "Program Activity", network_health: "Network Health", repo_created: "Repo Created", commit_activity: "Commit Activity", tweet: "Tweet" };
                  return (
                    <option key={type} value={type}>
                      {type === "All" ? "All Types" : label[type] || type}
                    </option>
                  );
                })}
              </select>
            </div>
          </div>
        </div>
      </AnimateOnScroll>

      {/* Error State */}
      {error && <ErrorState description={error} retry={() => window.location.reload()} />}

      {/* Results Count */}
      {!loading && !error && (
        <AnimateOnScroll delay={150}>
          <p className="text-sm text-text-tertiary flex items-center gap-2">
            <span className="font-medium text-text-primary">{filteredSignals.length}</span>
            of {signals.length} signals
            {(searchQuery || sourceFilter !== "All" || typeFilter !== "All") && (
              <span className="ml-2 px-2 py-0.5 bg-accent/10 text-accent text-xs rounded-full">
                Filtered
              </span>
            )}
          </p>
        </AnimateOnScroll>
      )}

      {/* Signals Table */}
      <AnimateOnScroll delay={200}>
        {loading ? (
          <SkeletonTable />
        ) : filteredSignals.length === 0 ? (
          <EmptyState
            title="No signals found"
            description={
              searchQuery || sourceFilter !== "All" || typeFilter !== "All"
                ? "Try adjusting your filters."
                : "Signals will appear here once ingested."
            }
            action={
              searchQuery || sourceFilter !== "All" || typeFilter !== "All"
                ? {
                    label: "Clear filters",
                    onClick: () => {
                      setSearchQuery("");
                      setSourceFilter("All");
                      setTypeFilter("All");
                    },
                  }
                : undefined
            }
          />
        ) : (
          <DataTable columns={columns} data={filteredSignals} keyField="id" />
        )}
      </AnimateOnScroll>
    </div>
  );
}
