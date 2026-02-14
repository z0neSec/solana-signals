"use client";

import Link from "next/link";
import { AnimateOnScroll } from "@/hooks/useScrollAnimation";

export default function MethodologyPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Page Header */}
      <AnimateOnScroll>
        <header className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-surface-raised rounded-full border border-border-subtle">
            <svg className="w-4 h-4 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span className="text-xs font-medium text-text-secondary">Documentation</span>
          </div>
          <h1 className="font-serif text-3xl lg:text-4xl tracking-tight text-gradient">
            Methodology
          </h1>
          <p className="text-text-secondary max-w-2xl">
            How we detect and analyze emerging narratives in the Solana ecosystem.
          </p>
        </header>
      </AnimateOnScroll>

      <div className="space-y-6">
        <AnimateOnScroll delay={50}>
          <section className="card p-6 lg:p-8 group relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <div className="relative">
              <h2 className="font-serif text-xl lg:text-2xl mb-4">Signal Collection</h2>
              <p className="text-text-secondary leading-relaxed mb-6">
                We continuously ingest signals from multiple sources across the Solana ecosystem:
              </p>
              <ul className="space-y-3 text-text-secondary">
                <li className="flex items-start gap-3 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="flex-shrink-0 w-2 h-2 rounded-full bg-gradient-to-r from-accent to-purple-500 mt-2" />
                  <span><strong className="text-text-primary">Social Media:</strong> Twitter/X posts from key accounts, trending hashtags, and engagement metrics</span>
                </li>
                <li className="flex items-start gap-3 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="flex-shrink-0 w-2 h-2 rounded-full bg-gradient-to-r from-accent to-purple-500 mt-2" />
                  <span><strong className="text-text-primary">Developer Activity:</strong> GitHub commits, new repositories, package releases</span>
                </li>
                <li className="flex items-start gap-3 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="flex-shrink-0 w-2 h-2 rounded-full bg-gradient-to-r from-accent to-purple-500 mt-2" />
                  <span><strong className="text-text-primary">Community Channels:</strong> Discord discussions, governance proposals, and forum activity</span>
                </li>
                <li className="flex items-start gap-3 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="flex-shrink-0 w-2 h-2 rounded-full bg-gradient-to-r from-accent to-purple-500 mt-2" />
                  <span><strong className="text-text-primary">News and Media:</strong> Press releases, blog posts, and industry publications</span>
                </li>
                <li className="flex items-start gap-3 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="flex-shrink-0 w-2 h-2 rounded-full bg-gradient-to-r from-accent to-purple-500 mt-2" />
                  <span><strong className="text-text-primary">On-Chain Data:</strong> Transaction patterns, smart contract deployments, and token movements</span>
                </li>
              </ul>
            </div>
          </section>
        </AnimateOnScroll>

        <AnimateOnScroll delay={100}>
          <section className="card p-6 lg:p-8 group relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <div className="relative">
              <h2 className="font-serif text-xl lg:text-2xl mb-4">Semantic Clustering</h2>
              <p className="text-text-secondary leading-relaxed mb-6">
                Raw signals are processed through a multi-stage pipeline:
              </p>
              <ol className="space-y-4 text-text-secondary">
                <li className="flex items-start gap-4 p-4 rounded-lg bg-surface-raised/50">
                  <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-gradient-to-br from-accent to-purple-500 text-white text-sm font-bold">1</span>
                  <div>
                    <strong className="text-text-primary">Embedding Generation</strong>
                    <p className="mt-1">Each signal is converted to a high-dimensional vector using OpenAI embeddings.</p>
                  </div>
                </li>
                <li className="flex items-start gap-4 p-4 rounded-lg bg-surface-raised/50">
                  <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-gradient-to-br from-accent to-purple-500 text-white text-sm font-bold">2</span>
                  <div>
                    <strong className="text-text-primary">Density-Based Clustering</strong>
                    <p className="mt-1">HDBSCAN algorithm groups semantically similar signals automatically.</p>
                  </div>
                </li>
                <li className="flex items-start gap-4 p-4 rounded-lg bg-surface-raised/50">
                  <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-gradient-to-br from-accent to-purple-500 text-white text-sm font-bold">3</span>
                  <div>
                    <strong className="text-text-primary">Narrative Synthesis</strong>
                    <p className="mt-1">LLM analysis synthesizes cluster contents into coherent narratives.</p>
                  </div>
                </li>
              </ol>
            </div>
          </section>
        </AnimateOnScroll>

        <AnimateOnScroll delay={150}>
          <section className="card p-6 lg:p-8 group relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <div className="relative">
              <h2 className="font-serif text-xl lg:text-2xl mb-4">Confidence Scoring</h2>
              <p className="text-text-secondary leading-relaxed mb-6">
                Each narrative receives a confidence score (0-100%) based on:
              </p>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 bg-surface-raised rounded-xl border border-border-subtle hover:border-accent/30 transition-colors">
                  <h3 className="font-medium mb-2">Signal Volume</h3>
                  <p className="text-sm text-text-secondary">Number of supporting signals relative to baseline.</p>
                </div>
                <div className="p-4 bg-surface-raised rounded-xl border border-border-subtle hover:border-accent/30 transition-colors">
                  <h3 className="font-medium mb-2">Source Diversity</h3>
                  <p className="text-sm text-text-secondary">Signals from multiple independent sources.</p>
                </div>
                <div className="p-4 bg-surface-raised rounded-xl border border-border-subtle hover:border-accent/30 transition-colors">
                  <h3 className="font-medium mb-2">Temporal Consistency</h3>
                  <p className="text-sm text-text-secondary">Sustained discussion over time.</p>
                </div>
                <div className="p-4 bg-surface-raised rounded-xl border border-border-subtle hover:border-accent/30 transition-colors">
                  <h3 className="font-medium mb-2">Cluster Cohesion</h3>
                  <p className="text-sm text-text-secondary">How tightly grouped signals are in semantic space.</p>
                </div>
              </div>
            </div>
          </section>
        </AnimateOnScroll>

        <AnimateOnScroll delay={200}>
          <section className="card p-6 lg:p-8 group relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <div className="relative">
              <h2 className="font-serif text-xl lg:text-2xl mb-4">Status Classification</h2>
              <p className="text-text-secondary leading-relaxed mb-6">
                Narratives are classified into lifecycle stages:
              </p>
              <div className="space-y-3">
                <div className="flex items-center gap-4 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="badge badge-new">New</span>
                  <span className="text-text-secondary">Recently detected, limited historical data</span>
                </div>
                <div className="flex items-center gap-4 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="badge badge-accelerating">Accelerating</span>
                  <span className="text-text-secondary">Growing signal volume and engagement</span>
                </div>
                <div className="flex items-center gap-4 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="badge badge-stable">Stable</span>
                  <span className="text-text-secondary">Consistent activity, established narrative</span>
                </div>
                <div className="flex items-center gap-4 p-3 rounded-lg hover:bg-surface-raised transition-colors">
                  <span className="badge bg-warning-muted text-warning">Declining</span>
                  <span className="text-text-secondary">Decreasing activity, waning interest</span>
                </div>
              </div>
            </div>
          </section>
        </AnimateOnScroll>
      </div>

      <AnimateOnScroll delay={250}>
        <div className="pt-4">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent/80 transition-colors group"
          >
            <svg className="w-4 h-4 transform group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Dashboard
          </Link>
        </div>
      </AnimateOnScroll>
    </div>
  );
}
