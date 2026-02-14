/**
 * Shared utility functions.
 */

/** Format a timestamp string as relative time (e.g. "5m ago", "2h ago"). */
export function formatTimeAgo(dateString: string): string {
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

/** Domain color mapping for consistent styling. */
export function getDomainColor(domain: string): string {
  switch (domain) {
    case "onchain":
      return "#10b981"; // emerald
    case "github":
      return "#8b5cf6"; // violet
    case "social":
      return "#0ea5e9"; // sky
    default:
      return "#71717a"; // zinc
  }
}

/** Domain bg class for badges. */
export function getDomainBgClass(domain: string): string {
  switch (domain) {
    case "onchain":
      return "bg-emerald-500";
    case "github":
      return "bg-violet-500";
    case "social":
      return "bg-sky-500";
    default:
      return "bg-zinc-500";
  }
}
