/**
 * EmptyState component.
 *
 * Shown when a search returns no results. Provides a clear action
 * to modify or clear the search.
 */

import React from 'react';

interface EmptyStateProps {
  searchTerm: string;
  onClear: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ searchTerm, onClear }) => {
  return (
    <div className="empty-state" role="status">
      <div className="empty-state__icon" aria-hidden="true">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
          <path d="M8 11h6" />
        </svg>
      </div>

      <h3 className="empty-state__title">No employees found</h3>
      <p className="empty-state__description">
        {searchTerm ? (
          <>
            No results match "<strong>{searchTerm}</strong>".
            Try a different name or department.
          </>
        ) : (
          'The employee directory is empty.'
        )}
      </p>

      {searchTerm && (
        <button
          className="empty-state__action"
          onClick={onClear}
          type="button"
        >
          Clear search
        </button>
      )}
    </div>
  );
};
