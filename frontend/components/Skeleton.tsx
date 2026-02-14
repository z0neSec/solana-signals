// Skeleton loading components

export function SkeletonCard() {
  return (
    <div className="card p-6 animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="space-y-2">
          <div className="skeleton h-4 w-24 rounded" />
          <div className="skeleton h-6 w-48 rounded" />
        </div>
        <div className="skeleton h-6 w-20 rounded" />
      </div>
      <div className="space-y-2 mb-4">
        <div className="skeleton h-4 w-full rounded" />
        <div className="skeleton h-4 w-3/4 rounded" />
      </div>
      <div className="flex items-center gap-4">
        <div className="skeleton h-4 w-32 rounded" />
        <div className="skeleton h-4 w-24 rounded" />
      </div>
    </div>
  );
}

export function SkeletonMetricCard() {
  return (
    <div className="card p-4 animate-pulse">
      <div className="skeleton h-3 w-20 mb-2 rounded" />
      <div className="skeleton h-8 w-16 rounded" />
    </div>
  );
}

export function SkeletonTable() {
  return (
    <div className="card overflow-hidden animate-pulse">
      <div className="border-b p-4">
        <div className="flex gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-4 w-24 rounded" />
          ))}
        </div>
      </div>
      {[1, 2, 3, 4, 5].map((row) => (
        <div key={row} className="border-b p-4 last:border-0">
          <div className="flex gap-4">
            {[1, 2, 3, 4].map((col) => (
              <div key={col} className="skeleton h-4 w-24 rounded" />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export function SkeletonChart() {
  return (
    <div className="card p-6 animate-pulse">
      <div className="skeleton h-4 w-32 mb-4 rounded" />
      <div className="skeleton h-48 w-full rounded" />
    </div>
  );
}
