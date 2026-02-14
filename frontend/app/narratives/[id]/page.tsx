"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { StatusBadge, ConfidenceBar } from "@/components/DataDisplay";
import { SkeletonCard } from "@/components/Skeleton";
import { ErrorState } from "@/components/States";
import { AnimateOnScroll } from "@/hooks/useScrollAnimation";
import { fetchNarrative, Narrative } from "@/lib/api";
import { formatTimeAgo } from "@/lib/utils";
import { ScoreBreakdownChart } from "@/components/Charts";

const domainColors: Record<string, string> = {
  onchain: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
  github: "bg-violet-500/10 text-violet-500 border-violet-500/20",
  social: "bg-sky-500/10 text-sky-500 border-sky-500/20",
};

const trendIcon = (trend: string) => {
  if (trend.includes("↑")) return "text-success";
  if (trend.includes("↓")) return "text-red-500";
  return "text-text-tertiary";
};

export default function NarrativeDetailPage() {
  const params = useParams();
  const [narrative, setNarrative] = useState<Narrative | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const id = params.id as string;
        const data = await fetchNarrative(id);
        setNarrative(data);
      } catch (err) {
        console.error("Narrative fetch error:", err);
        setError("Failed to load narrative details. Is the backend running?");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [params.id]);

  if (loading) {
    return (
      <div className="space-y-8">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  if (error || !narrative) {
    return <ErrorState description={error || "Narrative not found"} retry={() => window.location.reload()} />;
  }

  const confidencePct = Math.round(narrative.confidence);

  return (
    <div className="space-y-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-text-tertiary" aria-label="Breadcrumb">
        <Link href="/narratives" className="hover:text-text-primary transition-colors">
          Narratives
        </Link>
        <span className="mx-2">/</span>
        <span className="text-text-primary">{narrative.label}</span>
      </nav>

      {/* Header */}
      <AnimateOnScroll>
        <header className="card p-6">
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <StatusBadge status={narrative.status} />
                <span className="text-xs text-text-tertiary font-mono">#{narrative.rank}</span>
              </div>
              <h1 className="font-serif text-2xl lg:text-3xl tracking-tight">
                {narrative.label}
              </h1>
              <p className="text-text-secondary max-w-2xl">
                {narrative.summary}
              </p>
            </div>

            <div className="flex flex-col gap-4 lg:items-end lg:min-w-[200px]">
              <div className="w-full lg:w-48">
                <ConfidenceBar value={confidencePct} label="Confidence" />
              </div>
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-text-tertiary">Signals: </span>
                  <span className="metric-value">{narrative.signal_count}</span>
                </div>
                <div>
                  <span className="text-text-tertiary">Last seen: </span>
                  <span>{formatTimeAgo(narrative.last_seen)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Domain Tags */}
          <div className="mt-6 pt-4 border-t">
            <div className="flex flex-wrap gap-2">
              {narrative.domains.map((domain) => (
                <span
                  key={domain}
                  className={`text-xs px-3 py-1.5 rounded-full border font-medium ${domainColors[domain] || "bg-border-subtle text-text-secondary"}`}
                >
                  {domain} ({narrative.domain_counts[domain] || 0})
                </span>
              ))}
            </div>
          </div>
        </header>
      </AnimateOnScroll>

      {/* Why Now */}
      {narrative.why_now && (
        <AnimateOnScroll delay={50}>
          <section>
            <h2 className="font-serif text-xl mb-4">Why Now?</h2>
            <div className="card p-6">
              <p className="text-text-secondary leading-relaxed">{narrative.why_now}</p>
            </div>
          </section>
        </AnimateOnScroll>
      )}

      {/* Comparable Precedent */}
      {narrative.comparable_precedent && (
        <AnimateOnScroll delay={100}>
          <section>
            <h2 className="font-serif text-xl mb-4">Historical Precedent</h2>
            <div className="card p-6 border-l-4 border-accent">
              <p className="text-text-secondary leading-relaxed italic">{narrative.comparable_precedent}</p>
            </div>
          </section>
        </AnimateOnScroll>
      )}

      {/* Evidence */}
      {narrative.evidence && narrative.evidence.length > 0 && (
        <AnimateOnScroll delay={150}>
          <section>
            <h2 className="font-serif text-xl mb-4">Evidence</h2>
            <div className="grid gap-3">
              {narrative.evidence.map((ev: any, i: number) => (
                <div key={i} className="card p-4 flex flex-col sm:flex-row sm:items-center gap-3">
                  <span className={`text-xs px-2.5 py-1 rounded-full border font-medium shrink-0 ${domainColors[ev.domain] || "bg-border-subtle text-text-secondary"}`}>
                    {ev.domain}
                  </span>
                  <span className="text-sm text-text-primary flex-1">{ev.description || ev.signal || "—"}</span>
                  {(ev.url || ev.link) && (
                    <a href={ev.url || ev.link} target="_blank" rel="noopener noreferrer" className="text-accent hover:text-accent/80 transition-colors shrink-0">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  )}
                </div>
              ))}
            </div>
          </section>
        </AnimateOnScroll>
      )}

      {/* Scoring Breakdown */}
      {narrative.scores && (
        <AnimateOnScroll delay={200}>
          <section>
            <h2 className="font-serif text-xl mb-4">Scoring Breakdown</h2>
            <div className="card p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                <div>
                  <p className="text-xs text-text-tertiary uppercase tracking-wide mb-1">Base Score</p>
                  <p className="metric-value text-xl">{(narrative.scores.base_score * 100).toFixed(0)}%</p>
                </div>
                <div>
                  <p className="text-xs text-text-tertiary uppercase tracking-wide mb-1">Freshness</p>
                  <p className="metric-value text-xl">{(narrative.scores.freshness * 100).toFixed(0)}%</p>
                </div>
                <div>
                  <p className="text-xs text-text-tertiary uppercase tracking-wide mb-1">Novelty Bonus</p>
                  <p className="metric-value text-xl">{narrative.scores.novelty_bonus.toFixed(1)}x</p>
                </div>
                <div>
                  <p className="text-xs text-text-tertiary uppercase tracking-wide mb-1">Final Score</p>
                  <p className="metric-value text-xl text-accent">{(narrative.scores.final_score * 100).toFixed(0)}%</p>
                </div>
              </div>
              <div className="pt-4 border-t">
                <p className="text-xs text-text-tertiary uppercase tracking-wide mb-3">Score Components</p>
                <ScoreBreakdownChart scores={narrative.scores} />
              </div>
            </div>
          </section>
        </AnimateOnScroll>
      )}

      {/* Key Entities */}
      {narrative.entities && (
        <AnimateOnScroll delay={250}>
          <section>
            <h2 className="font-serif text-xl mb-4">Key Entities</h2>
            <div className="grid md:grid-cols-3 gap-4">
              {narrative.entities.programs.length > 0 && (
                <div className="card p-5">
                  <h3 className="text-sm font-medium text-text-tertiary uppercase tracking-wide mb-3">Programs</h3>
                  <div className="space-y-2">
                    {narrative.entities.programs.map((p) => (
                      <p key={p} className="text-sm font-mono text-text-secondary truncate">{p}</p>
                    ))}
                  </div>
                </div>
              )}
              {narrative.entities.repos.length > 0 && (
                <div className="card p-5">
                  <h3 className="text-sm font-medium text-text-tertiary uppercase tracking-wide mb-3">Repositories</h3>
                  <div className="space-y-2">
                    {narrative.entities.repos.map((r) => (
                      <a key={r} href={`https://github.com/${r}`} target="_blank" rel="noopener noreferrer" className="block text-sm text-accent hover:text-accent/80 transition-colors truncate">
                        {r}
                      </a>
                    ))}
                  </div>
                </div>
              )}
              {(narrative.entities.kols?.length ?? 0) > 0 && (
                <div className="card p-5">
                  <h3 className="text-sm font-medium text-text-tertiary uppercase tracking-wide mb-3">Key Voices</h3>
                  <div className="space-y-2">
                    {narrative.entities.kols!.map((k) => (
                      <a key={k} href={`https://x.com/${k.replace("@", "")}`} target="_blank" rel="noopener noreferrer" className="block text-sm text-accent hover:text-accent/80 transition-colors">
                        {k}
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </section>
        </AnimateOnScroll>
      )}

      {/* Build Ideas */}
      {narrative.build_ideas && narrative.build_ideas.length > 0 && (
        <AnimateOnScroll delay={300}>
          <section>
            <h2 className="font-serif text-xl mb-4">
              Build Ideas
              <span className="ml-2 text-sm font-normal text-text-tertiary">({narrative.build_ideas.length})</span>
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              {narrative.build_ideas.map((idea: any, i: number) => (
                <div key={i} className="card p-5 space-y-3 hover:border-accent/30 transition-colors">
                  <div className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-7 h-7 flex items-center justify-center rounded-full bg-accent-muted text-accent text-xs font-bold">
                      {i + 1}
                    </span>
                    <h3 className="font-medium text-text-primary">{idea.title}</h3>
                  </div>
                  {(idea.description || idea.problem) && (
                    <p className="text-sm text-text-secondary">{idea.description || idea.problem}</p>
                  )}
                  {idea.solution && (
                    <div className="pt-3 border-t border-border-subtle">
                      <p className="text-sm text-text-secondary">
                        <span className="font-medium text-text-primary">Solution: </span>
                        {idea.solution}
                      </p>
                    </div>
                  )}
                  <div className="flex items-center gap-4 text-xs text-text-tertiary">
                    {idea.effort && <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-border-subtle rounded"><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" strokeWidth="2"/><polyline points="12 6 12 12 16 14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>{idea.effort}</span>}
                    {idea.business_model && <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-border-subtle rounded"><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23" strokeWidth="2"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>{idea.business_model}</span>}
                  </div>
                  {idea.market_size && (
                    <p className="text-xs text-text-tertiary italic">Market: {idea.market_size}</p>
                  )}
                </div>
              ))}
            </div>
          </section>
        </AnimateOnScroll>
      )}

      {/* Actions */}
      <div className="flex gap-4 no-print">
        <Link href="/report" className="btn btn-secondary px-4 py-2 text-sm">
          Export Report
        </Link>
        <Link href="/signals" className="btn btn-secondary px-4 py-2 text-sm">
          View All Signals
        </Link>
      </div>
    </div>
  );
}
