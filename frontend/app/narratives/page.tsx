"use client";

import { useState, useEffect } from "react";
import { NarrativeCard } from "@/components/DataDisplay";
import { SkeletonCard } from "@/components/Skeleton";
import { EmptyState, ErrorState } from "@/components/States";
import { AnimateOnScroll, StaggeredList } from "@/hooks/useScrollAnimation";
import { fetchNarratives, Narrative } from "@/lib/api";
import { formatTimeAgo } from "@/lib/utils";

const statusFilters = ["All", "NEW", "ACCELERATING", "STABLE", "DECLINING"];
const statusLabels: Record<string, string> = {
  All: "All",
  NEW: "New",
  ACCELERATING: "Accelerating",
  STABLE: "Stable",
  DECLINING: "Declining",
};

export default function NarrativesPage() {
  const [narratives, setNarratives] = useState<Narrative[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortBy, setSortBy] = useState<"confidence" | "recent">("confidence");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchNarratives({ limit: 50 });
        setNarratives(response.narratives);
      } catch (err) {
        console.error("Narratives fetch error:", err);
        setError("Failed to load narratives. Is the backend running?");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredNarratives = narratives
    .filter((n) => statusFilter === "All" || n.status === statusFilter)
    .filter(
      (n) =>
        searchQuery === "" ||
        n.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.domains.some((d) => d.toLowerCase().includes(searchQuery.toLowerCase()))
    )
    .sort((a, b) => {
      if (sortBy === "confidence") return b.confidence - a.confidence;
      return new Date(b.last_seen).getTime() - new Date(a.last_seen).getTime();
    });

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <AnimateOnScroll>
        <header className="space-y-3">
          <h1 className="font-serif text-3xl lg:text-4xl tracking-tight text-gradient">
            All Narratives
          </h1>
          <p className="text-text-secondary max-w-2xl">
            Explore all detected narratives in the current analysis period. Filter by status or search for specific topics.
          </p>
        </header>
      </AnimateOnScroll>

      {/* Filters */}
      <AnimateOnScroll delay={100}>
        <div className="flex flex-col sm:flex-row gap-4 p-4 bg-surface-raised/50 rounded-xl border border-border-subtle">
          <div className="flex-1 relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <label htmlFor="search" className="sr-only">Search narratives</label>
            <input
              id="search"
              type="text"
              placeholder="Search by name or domain..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 text-sm bg-surface border border-border-subtle rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent placeholder:text-text-tertiary transition-shadow"
            />
          </div>

          <div className="flex gap-1.5 p-1 bg-surface rounded-lg border border-border-subtle">
            {statusFilters.map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-all ${
                  statusFilter === status
                    ? "bg-gradient-to-r from-accent to-purple-500 text-white shadow-sm"
                    : "text-text-secondary hover:text-text-primary hover:bg-surface-raised"
                }`}
              >
                {statusLabels[status]}
              </button>
            ))}
          </div>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "confidence" | "recent")}
            className="px-4 py-2.5 text-sm bg-surface border border-border-subtle rounded-lg focus:outline-none focus:ring-2 focus:ring-accent cursor-pointer"
            aria-label="Sort by"
          >
            <option value="confidence">Sort by Confidence</option>
            <option value="recent">Sort by Recent</option>
          </select>
        </div>
      </AnimateOnScroll>

      {error && <ErrorState description={error} retry={() => window.location.reload()} />}

      {!loading && !error && (
        <AnimateOnScroll delay={150}>
          <p className="text-sm text-text-tertiary flex items-center gap-2">
            <span className="font-medium text-text-primary">{filteredNarratives.length}</span>
            of {narratives.length} narratives
            {searchQuery && (
              <span className="ml-2 px-2 py-0.5 bg-accent/10 text-accent text-xs rounded-full">Filtered</span>
            )}
          </p>
        </AnimateOnScroll>
      )}

      {loading ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : filteredNarratives.length === 0 ? (
        <EmptyState
          title="No narratives found"
          description={searchQuery ? "Try adjusting your search or filters." : "Narratives will appear here once detected."}
          action={searchQuery ? { label: "Clear search", onClick: () => setSearchQuery("") } : undefined}
        />
      ) : (
        <StaggeredList className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredNarratives.map((narrative) => (
            <NarrativeCard
              key={narrative.id}
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
          ))}
        </StaggeredList>
      )}
    </div>
  );
}
