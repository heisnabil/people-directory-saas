/**
 * ErrorState component.
 *
 * Shown when an API request fails. Provides a Retry action
 * and displays a user-friendly error message.
 */

import React from 'react';

interface ErrorStateProps {
  error: Error;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ error, onRetry }) => {
  const message =
    'status' in error && (error as { status: number }).status === 503
      ? 'The server is temporarily unavailable. Please try again in a moment.'
      : 'Something went wrong while fetching employees. Please check your connection and try again.';

  return (
    <div className="error-state" role="alert">
      <div className="error-state__icon" aria-hidden="true">
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
          <circle cx="12" cy="12" r="10" />
          <path d="M12 8v4" />
          <path d="M12 16h.01" />
        </svg>
      </div>

      <h3 className="error-state__title">Unable to load employees</h3>
      <p className="error-state__description">{message}</p>

      <button
        className="error-state__retry"
        onClick={onRetry}
        type="button"
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
          <path d="M3 3v5h5" />
          <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" />
          <path d="M16 16h5v5" />
        </svg>
        Try again
      </button>
    </div>
  );
};
