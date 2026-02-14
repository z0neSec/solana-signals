/**
 * API client for communicating with the backend.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Types
export interface Period {
  start: string;
  end: string;
  label: string;
}

export interface DashboardSummary {
  total_narratives: number;
  new_narratives: number;
  accelerating: number;
  total_signals: number;
  total_build_ideas: number;
  data_sources?: number;
}

export interface BuildIdea {
  title: string;
  description?: string | null;
  problem?: string | null;
  solution?: string | null;
  business_model?: string | null;
  effort?: string | null;
  market_size?: string | null;
}

export interface EntitySet {
  programs: string[];
  repos: string[];
  kols?: string[];
}

export interface Evidence {
  domain: string;
  signal_id?: string;
  description?: string;
  signal?: string;
  metric?: string;
  trend?: string;
  url?: string;
  link?: string;
}

export interface NarrativeScores {
  domain_breakdown: Record<string, number>;
  freshness: number;
  novelty_bonus: number;
  base_score: number;
  final_score: number;
}

export interface Narrative {
  id: string;
  rank: number;
  label: string;
  status: string;
  confidence: number;
  summary: string;
  signal_count: number;
  domains: string[];
  domain_counts: Record<string, number>;
  first_seen: string;
  last_seen: string;
  scores?: NarrativeScores;
  build_ideas: BuildIdea[];
  entities?: EntitySet;
  evidence?: Evidence[];
  why_now?: string;
  comparable_precedent?: string;
  keywords?: string[];
}

export interface DashboardResponse {
  period: Period;
  narratives: Narrative[];
  summary: DashboardSummary;
  last_updated: string;
}

export interface NarrativeListResponse {
  narratives: Narrative[];
  total: number;
  filters_applied: Record<string, unknown>;
}

export interface Signal {
  id: string;
  domain: string;
  type: string;
  description: string;
  author?: string;
  source?: string;
  url?: string;
  timestamp: string;
  credibility_score: number;
  relevance_score?: number;
  narrative_id?: string;
  narratives?: { label: string };
}

export interface SignalListResponse {
  signals: Signal[];
  total: number;
  filters_applied: Record<string, unknown>;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  database?: string;
  mode?: string;
}

// API Client class
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options?.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Health check
  async health(): Promise<HealthResponse> {
    return this.fetch<HealthResponse>("/health");
  }

  // Dashboard
  async getDashboard(): Promise<DashboardResponse> {
    return this.fetch<DashboardResponse>("/dashboard");
  }

  // Narratives
  async getNarratives(params?: {
    status?: string;
    min_confidence?: number;
    limit?: number;
    offset?: number;
  }): Promise<NarrativeListResponse> {
    const searchParams = new URLSearchParams();
    if (params?.status) searchParams.set("status", params.status);
    if (params?.min_confidence) searchParams.set("min_confidence", params.min_confidence.toString());
    if (params?.limit) searchParams.set("limit", params.limit.toString());
    if (params?.offset) searchParams.set("offset", params.offset.toString());
    
    const query = searchParams.toString();
    return this.fetch<NarrativeListResponse>(`/narratives${query ? `?${query}` : ""}`);
  }

  async getNarrative(id: string): Promise<Narrative> {
    return this.fetch<Narrative>(`/narratives/${id}`);
  }

  // Signals
  async getSignals(params?: {
    domain?: string;
    narrative_id?: string;
    limit?: number;
    offset?: number;
  }): Promise<SignalListResponse> {
    const searchParams = new URLSearchParams();
    if (params?.domain) searchParams.set("domain", params.domain);
    if (params?.narrative_id) searchParams.set("narrative_id", params.narrative_id);
    if (params?.limit) searchParams.set("limit", params.limit.toString());
    if (params?.offset) searchParams.set("offset", params.offset.toString());
    
    const query = searchParams.toString();
    return this.fetch<SignalListResponse>(`/signals${query ? `?${query}` : ""}`);
  }

  // Export
  async exportMarkdown(): Promise<{ markdown: string; generated_at: string }> {
    return this.fetch<{ markdown: string; generated_at: string }>("/export/markdown");
  }
}

// Singleton instance
export const api = new ApiClient();

// Helper hooks for data fetching
export async function fetchDashboard(): Promise<DashboardResponse> {
  return api.getDashboard();
}

export async function fetchNarratives(params?: {
  status?: string;
  min_confidence?: number;
  limit?: number;
}): Promise<NarrativeListResponse> {
  return api.getNarratives(params);
}

export async function fetchNarrative(id: string): Promise<Narrative> {
  return api.getNarrative(id);
}

export async function fetchSignals(params?: {
  domain?: string;
  narrative_id?: string;
  limit?: number;
}): Promise<SignalListResponse> {
  return api.getSignals(params);
}
