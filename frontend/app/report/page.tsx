"use client";

import { useState, useEffect } from "react";
import { StatusBadge, ConfidenceBar } from "@/components/DataDisplay";
import { SkeletonCard } from "@/components/Skeleton";
import { EmptyState, ErrorState } from "@/components/States";
import { fetchDashboard, fetchNarratives, exportMarkdown, Narrative } from "@/lib/api";

export default function ReportPage() {
  const [narratives, setNarratives] = useState<Narrative[]>([]);
  const [period, setPeriod] = useState<string>("");
  const [totalSignals, setTotalSignals] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashboard, narrativeList] = await Promise.all([
          fetchDashboard(),
          fetchNarratives({ limit: 50 }),
        ]);

        setPeriod(dashboard.period.label);
        setTotalSignals(dashboard.summary.total_signals);
        setNarratives(narrativeList.narratives);
      } catch (err) {
        console.error("Report fetch error:", err);
        setError("Failed to load report data. Is the backend running?");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handlePrint = () => {
    window.print();
  };

  const handleExportMarkdown = async () => {
    try {
      const markdown = await exportMarkdown();
      const blob = new Blob([markdown], { type: "text/markdown" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `pulse-report-${new Date().toISOString().split("T")[0]}.md`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("Failed to export markdown. Is the backend running?");
    }
  };

  const generatedAt = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  if (loading) {
    return (
      <div className="space-y-8">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  if (error) {
    return <ErrorState description={error} retry={() => window.location.reload()} />;
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Print Controls */}
      <div className="mb-8 flex items-center justify-between no-print">
        <div>
          <h1 className="font-serif text-3xl tracking-tight">Export Report</h1>
          <p className="text-text-secondary">
            Print-ready narrative analysis report
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleExportMarkdown}
            className="btn btn-secondary px-6 py-2"
          >
            Download Markdown
          </button>
          <button
            onClick={handlePrint}
            className="btn btn-primary px-6 py-2"
          >
            Print / Save PDF
          </button>
        </div>
      </div>

      {/* Report Content */}
      <div className="space-y-8 print:space-y-6">
        {/* Report Header */}
        <header className="card p-8 print:border-0 print:shadow-none print:p-0">
          <div className="text-center mb-6">
            <h1 className="font-serif text-2xl lg:text-3xl tracking-tight mb-2">
              Solana Ecosystem Narrative Report
            </h1>
            <p className="text-text-secondary">
              Analysis Period: {period}
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4 text-center border-t border-b py-4">
            <div>
              <div className="metric-value text-2xl">{narratives.length}</div>
              <div className="text-xs text-text-tertiary uppercase tracking-wide">Narratives</div>
            </div>
            <div>
              <div className="metric-value text-2xl">{totalSignals}</div>
              <div className="text-xs text-text-tertiary uppercase tracking-wide">Signals</div>
            </div>
            <div>
              <div className="text-xs text-text-tertiary mt-2">Generated</div>
              <div className="text-sm">{generatedAt}</div>
            </div>
          </div>
        </header>

        {/* Executive Summary */}
        <section className="card p-6 print:border-0 print:shadow-none print:p-0 print:page-break-inside-avoid">
          <h2 className="font-serif text-xl mb-4">Executive Summary</h2>
          {narratives.length === 0 ? (
            <p className="text-text-secondary leading-relaxed">
              No narratives have been detected for this period. Run the ingestion pipeline to collect signals and generate narrative analysis.
            </p>
          ) : (
            <p className="text-text-secondary leading-relaxed">
              This report presents {narratives.length} detected narratives from
              the Solana ecosystem during {period}. Analysis is based on{" "}
              {totalSignals} signals collected from social media, developer
              activity, community channels, and on-chain data. Top narratives include{" "}
              {narratives.slice(0, 3).map((n, i) => (
                <span key={n.id}>
                  {i > 0 && (i === Math.min(narratives.length, 3) - 1 ? " and " : ", ")}
                  {n.label}
                </span>
              ))}.
            </p>
          )}
        </section>

        {/* Narratives */}
        {narratives.length === 0 ? (
          <EmptyState
            title="No narratives to report"
            description="Narratives will appear here once signals are processed."
          />
        ) : (
          narratives.map((narrative, index) => (
            <section
              key={narrative.id}
              className="card p-6 print:border-0 print:shadow-none print:p-0 print:border-t print:pt-6 print:page-break-inside-avoid"
            >
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <div className="text-xs text-text-tertiary mb-1">
                    Narrative {index + 1} of {narratives.length}
                  </div>
                  <h2 className="font-serif text-xl">{narrative.label}</h2>
                </div>
                <StatusBadge status={narrative.status} />
              </div>

              <p className="text-text-secondary mb-4">{narrative.summary}</p>

              <div className="mb-4">
                <ConfidenceBar value={Math.round(narrative.confidence)} label="Confidence" />
              </div>

              <div className="grid md:grid-cols-2 gap-4 mb-4">
                {narrative.entities && (
                  <div>
                    <h3 className="text-sm font-medium mb-2">Key Projects</h3>
                    <div className="flex flex-wrap gap-2">
                      {[
                        ...(narrative.entities.programs || []),
                        ...(narrative.entities.repos || []),
                      ].slice(0, 6).map((project) => (
                        <span key={project} className="text-xs px-2 py-1 bg-border-subtle rounded">
                          {project}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                <div>
                  <h3 className="text-sm font-medium mb-2">Domains</h3>
                  <div className="flex flex-wrap gap-2">
                    {narrative.domains.map((domain) => (
                      <span key={domain} className="text-xs px-2 py-1 bg-border-subtle rounded">
                        {domain}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {narrative.build_ideas && narrative.build_ideas.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium mb-2">Build Ideas</h3>
                  <ul className="space-y-1">
                    {narrative.build_ideas.map((idea: any, i: number) => (
                      <li key={i} className="text-sm text-text-secondary flex items-start gap-2">
                        <span className="text-accent">-</span>
                        {idea.title}{(idea.description || idea.problem) ? `: ${idea.description || idea.problem}` : ""}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="mt-4 pt-4 border-t flex gap-6 text-sm text-text-tertiary">
                <span>ID: {narrative.id}</span>
                <span>{narrative.signal_count} signals</span>
              </div>
            </section>
          ))
        )}

        {/* Footer */}
        <footer className="text-center text-sm text-text-tertiary pt-8 border-t print:mt-8">
          <p>Generated by Pulse - Solana Insights</p>
          <p className="mt-1">Solana Ecosystem Narrative Detection Tool</p>
        </footer>
      </div>
    </div>
  );
}
