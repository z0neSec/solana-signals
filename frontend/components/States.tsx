interface EmptyStateProps {
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="card p-12 text-center">
      <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-border-subtle">
        <svg
          className="h-6 w-6 text-text-tertiary"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m6 4.125l2.25 2.25m0 0l2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z"
          />
        </svg>
      </div>
      <h3 className="mb-1 font-serif text-lg">{title}</h3>
      <p className="text-sm text-text-secondary mb-4">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="btn btn-secondary px-4 py-2 text-sm"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

interface ErrorStateProps {
  title?: string;
  description?: string;
  retry?: () => void;
}

export function ErrorState({ 
  title = "Something went wrong", 
  description = "We encountered an error loading this data. Please try again.",
  retry 
}: ErrorStateProps) {
  return (
    <div className="card border-error-muted p-12 text-center">
      <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-error-muted">
        <svg
          className="h-6 w-6 text-error"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
          />
        </svg>
      </div>
      <h3 className="mb-1 font-serif text-lg">{title}</h3>
      <p className="text-sm text-text-secondary mb-4">{description}</p>
      {retry && (
        <button
          onClick={retry}
          className="btn btn-secondary px-4 py-2 text-sm"
        >
          Try again
        </button>
      )}
    </div>
  );
}
