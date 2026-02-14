import { ReactNode } from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  change?: {
    value: string;
    direction: "up" | "down" | "neutral";
  };
  subtext?: string;
}

export function MetricCard({ label, value, change, subtext }: MetricCardProps) {
  return (
    <div className="card-static p-5 lg:p-6 group relative overflow-hidden">
      {/* Gradient accent on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      <div className="relative">
        <div className="text-xs font-semibold text-text-tertiary uppercase tracking-wider mb-2">
          {label}
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-3xl lg:text-4xl font-bold metric-value">{value}</span>
          {change && (
            <span className={`text-sm font-semibold flex items-center gap-0.5 ${
              change.direction === "up" 
                ? "text-success" 
                : change.direction === "down" 
                  ? "text-error" 
                  : "text-text-tertiary"
            }`}>
              {change.direction === "up" && (
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 15l7-7 7 7" />
                </svg>
              )}
              {change.direction === "down" && (
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7" />
                </svg>
              )}
              {change.value}
            </span>
          )}
        </div>
        {subtext && (
          <div className="text-xs text-text-tertiary mt-2">{subtext}</div>
        )}
      </div>
    </div>
  );
}

interface ConfidenceBarProps {
  value: number; // 0-100
  label?: string;
  size?: "sm" | "md";
}

export function ConfidenceBar({ value, label, size = "md" }: ConfidenceBarProps) {
  const clampedValue = Math.max(0, Math.min(100, value));
  const height = size === "sm" ? "h-2" : "h-2.5";
  
  // Gradient based on confidence level
  let barClass = "bg-gradient-to-r from-gray-400 to-gray-500";
  if (clampedValue >= 80) barClass = "bg-gradient-to-r from-emerald-500 to-green-400";
  else if (clampedValue >= 60) barClass = "bg-gradient-to-r from-indigo-500 to-purple-500";
  else if (clampedValue >= 40) barClass = "bg-gradient-to-r from-amber-500 to-orange-400";
  else barClass = "bg-gradient-to-r from-red-500 to-rose-400";

  return (
    <div className="flex items-center gap-3">
      {label && (
        <span className="text-xs text-text-secondary min-w-[70px] font-medium">{label}</span>
      )}
      <div className={`flex-1 ${height} bg-border-subtle rounded-full overflow-hidden`}>
        <div 
          className={`${height} ${barClass} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${clampedValue}%` }}
          role="progressbar"
          aria-valuenow={clampedValue}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
      <span className="metric-value-plain text-sm min-w-[40px] text-right font-bold">
        {clampedValue}%
      </span>
    </div>
  );
}

type BadgeVariant = "new" | "accelerating" | "stable" | "declining" | "default";

interface StatusBadgeProps {
  status: string;
  variant?: BadgeVariant;
}

export function StatusBadge({ status, variant = "default" }: StatusBadgeProps) {
  const variantClasses: Record<BadgeVariant, string> = {
    new: "badge-new",
    accelerating: "badge-accelerating",
    stable: "badge-stable",
    declining: "bg-warning-muted text-warning",
    default: "bg-border-subtle text-text-secondary",
  };

  // Auto-detect variant from status if not provided
  let resolvedVariant = variant;
  if (variant === "default") {
    const statusLower = status.toLowerCase();
    if (statusLower.includes("new") || statusLower.includes("emerging")) {
      resolvedVariant = "new";
    } else if (statusLower.includes("accelerat") || statusLower.includes("growing")) {
      resolvedVariant = "accelerating";
    } else if (statusLower.includes("stable") || statusLower.includes("established")) {
      resolvedVariant = "stable";
    } else if (statusLower.includes("declin") || statusLower.includes("fading")) {
      resolvedVariant = "declining";
    }
  }

  return (
    <span className={`badge ${variantClasses[resolvedVariant]}`}>
      {status}
    </span>
  );
}

interface NarrativeCardProps {
  id: string;
  title: string;
  summary: string;
  status: string;
  confidence: number;
  signalCount: number;
  lastUpdated: string;
  keywords?: string[];
  href?: string;
}

export function NarrativeCard({
  id,
  title,
  summary,
  status,
  confidence,
  signalCount,
  lastUpdated,
  keywords = [],
  href,
}: NarrativeCardProps) {
  const content = (
    <article className="card p-6 group relative overflow-hidden">
      {/* Subtle gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      {/* Top accent line */}
      <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-accent via-purple-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative">
        <header className="flex items-start justify-between gap-4 mb-3">
          <div className="flex-1 min-w-0">
            <div className="text-xs text-text-tertiary mb-1.5 font-mono">
              {id}
            </div>
            <h3 className="font-serif text-lg lg:text-xl leading-snug group-hover:text-accent transition-colors duration-300">
              {title}
            </h3>
          </div>
          <StatusBadge status={status} />
        </header>

        <p className="text-sm text-text-secondary line-clamp-2 mb-4 leading-relaxed">
          {summary}
        </p>

        <div className="mb-4">
          <ConfidenceBar value={confidence} size="sm" />
        </div>

        {keywords.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {keywords.slice(0, 5).map((keyword) => (
              <span 
                key={keyword} 
                className="text-xs px-2.5 py-1 bg-surface-raised text-text-secondary rounded-full border border-border-subtle hover:border-accent/30 hover:text-accent transition-colors duration-200"
              >
                {keyword}
              </span>
            ))}
            {keywords.length > 5 && (
              <span className="text-xs px-2.5 py-1 text-text-tertiary">
                +{keywords.length - 5}
              </span>
            )}
          </div>
        )}

        <footer className="flex items-center justify-between text-xs text-text-tertiary pt-4 border-t border-border-subtle">
          <span className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            {signalCount} signals
          </span>
          <span className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {lastUpdated}
          </span>
        </footer>
      </div>
    </article>
  );

  if (href) {
    return (
      <a href={href} className="block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent rounded-lg">
        {content}
      </a>
    );
  }

  return content;
}

interface DataTableColumn<T> {
  key: keyof T | string;
  header: string;
  width?: string;
  render?: (value: unknown, row: T) => ReactNode;
}

interface DataTableProps<T> {
  columns: DataTableColumn<T>[];
  data: T[];
  keyField: keyof T;
  onRowClick?: (row: T) => void;
}

export function DataTable<T extends object>({ 
  columns, 
  data, 
  keyField,
  onRowClick 
}: DataTableProps<T>) {
  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border-subtle bg-gradient-to-r from-surface-raised to-surface">
              {columns.map((col) => (
                <th 
                  key={String(col.key)}
                  className="px-4 py-4 text-left font-medium text-text-secondary text-xs uppercase tracking-wider"
                  style={{ width: col.width }}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {data.map((row, idx) => (
              <tr 
                key={String((row as Record<string, unknown>)[keyField as string]) || idx}
                onClick={() => onRowClick?.(row)}
                className={`
                  transition-colors group
                  ${onRowClick ? "cursor-pointer" : ""}
                  hover:bg-surface-raised/50
                `}
              >
                {columns.map((col) => {
                  const value = (row as Record<string, unknown>)[col.key as string];
                  return (
                    <td key={String(col.key)} className="px-4 py-4 group-hover:text-text-primary transition-colors">
                      {col.render ? col.render(value, row) : String(value ?? "")}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
