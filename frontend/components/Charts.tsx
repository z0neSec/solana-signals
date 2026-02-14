"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  CartesianGrid,
} from "recharts";
import { getDomainColor } from "@/lib/utils";

interface DomainDistributionProps {
  domainCounts: Record<string, number>;
}

export function DomainDistributionChart({ domainCounts }: DomainDistributionProps) {
  const data = Object.entries(domainCounts).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
    color: getDomainColor(name),
  }));

  if (data.length === 0) return null;

  return (
    <div className="w-full h-48">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={40}
            outerRadius={70}
            paddingAngle={3}
            dataKey="value"
            stroke="none"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--color-surface-elevated)",
              border: "1px solid var(--color-border)",
              borderRadius: "8px",
              color: "var(--color-text-primary)",
              fontSize: "12px",
            }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex items-center justify-center gap-4 -mt-2">
        {data.map((d) => (
          <div key={d.name} className="flex items-center gap-1.5 text-xs text-text-secondary">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: d.color }} />
            {d.name} ({d.value})
          </div>
        ))}
      </div>
    </div>
  );
}

interface NarrativeConfidenceChartProps {
  narratives: Array<{
    label: string;
    confidence: number;
    status: string;
  }>;
}

export function NarrativeConfidenceChart({ narratives }: NarrativeConfidenceChartProps) {
  const data = narratives.map((n) => ({
    name: n.label.length > 18 ? n.label.substring(0, 18) + "..." : n.label,
    confidence: Math.round(n.confidence),
    fill:
      n.status === "ACCELERATING"
        ? "#f59e0b"
        : n.status === "NEW"
        ? "#10b981"
        : n.status === "STABLE"
        ? "#71717a"
        : "#ef4444",
  }));

  if (data.length === 0) return null;

  return (
    <div className="w-full h-56">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ left: 8, right: 24, top: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" horizontal={false} />
          <XAxis
            type="number"
            domain={[0, 100]}
            tick={{ fontSize: 11, fill: "var(--color-text-tertiary)" }}
            tickFormatter={(v) => `${v}%`}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }}
            width={140}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--color-surface-elevated)",
              border: "1px solid var(--color-border)",
              borderRadius: "8px",
              color: "var(--color-text-primary)",
              fontSize: "12px",
            }}
            formatter={(value: number) => [`${value}%`, "Confidence"]}
          />
          <Bar dataKey="confidence" radius={[0, 4, 4, 0]} barSize={20}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface SignalTimelineProps {
  signals: Array<{
    timestamp: string;
    domain: string;
  }>;
}

export function SignalTimelineChart({ signals }: SignalTimelineProps) {
  // Bucket signals by day
  const buckets: Record<string, { onchain: number; github: number; social: number }> = {};

  signals.forEach((s) => {
    const day = new Date(s.timestamp).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
    if (!buckets[day]) buckets[day] = { onchain: 0, github: 0, social: 0 };
    const domain = s.domain as "onchain" | "github" | "social";
    if (buckets[day][domain] !== undefined) {
      buckets[day][domain]++;
    }
  });

  const data = Object.entries(buckets)
    .map(([day, counts]) => ({ day, ...counts }))
    .slice(-14); // Last 14 days max

  if (data.length === 0) return null;

  return (
    <div className="w-full h-48">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ left: 0, right: 8, top: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
          <XAxis
            dataKey="day"
            tick={{ fontSize: 10, fill: "var(--color-text-tertiary)" }}
          />
          <YAxis
            tick={{ fontSize: 10, fill: "var(--color-text-tertiary)" }}
            allowDecimals={false}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--color-surface-elevated)",
              border: "1px solid var(--color-border)",
              borderRadius: "8px",
              color: "var(--color-text-primary)",
              fontSize: "12px",
            }}
          />
          <Area
            type="monotone"
            dataKey="onchain"
            stackId="1"
            stroke="#10b981"
            fill="#10b981"
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="github"
            stackId="1"
            stroke="#8b5cf6"
            fill="#8b5cf6"
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="social"
            stackId="1"
            stroke="#0ea5e9"
            fill="#0ea5e9"
            fillOpacity={0.6}
          />
        </AreaChart>
      </ResponsiveContainer>
      <div className="flex items-center justify-center gap-4 mt-1">
        <div className="flex items-center gap-1.5 text-xs text-text-secondary">
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          Onchain
        </div>
        <div className="flex items-center gap-1.5 text-xs text-text-secondary">
          <span className="w-2 h-2 rounded-full bg-violet-500" />
          GitHub
        </div>
        <div className="flex items-center gap-1.5 text-xs text-text-secondary">
          <span className="w-2 h-2 rounded-full bg-sky-500" />
          Social
        </div>
      </div>
    </div>
  );
}

interface ScoreBreakdownChartProps {
  scores: {
    domain_breakdown: Record<string, number>;
    freshness: number;
    novelty_bonus: number;
    base_score: number;
    final_score: number;
  };
}

export function ScoreBreakdownChart({ scores }: ScoreBreakdownChartProps) {
  const data = [
    ...Object.entries(scores.domain_breakdown).map(([domain, score]) => ({
      name: domain.charAt(0).toUpperCase() + domain.slice(1),
      value: Math.round(score * 100),
      color: getDomainColor(domain),
    })),
    {
      name: "Freshness",
      value: Math.round(scores.freshness * 100),
      color: "#f59e0b",
    },
  ];

  return (
    <div className="w-full h-36">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ left: 0, right: 8, top: 4, bottom: 4 }}>
          <XAxis
            dataKey="name"
            tick={{ fontSize: 10, fill: "var(--color-text-tertiary)" }}
          />
          <YAxis
            tick={{ fontSize: 10, fill: "var(--color-text-tertiary)" }}
            tickFormatter={(v) => `${v}%`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--color-surface-elevated)",
              border: "1px solid var(--color-border)",
              borderRadius: "8px",
              color: "var(--color-text-primary)",
              fontSize: "12px",
            }}
            formatter={(value: number) => [`${value}%`, "Score"]}
          />
          <Bar dataKey="value" radius={[4, 4, 0, 0]} barSize={28}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
