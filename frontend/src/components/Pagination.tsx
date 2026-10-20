/**
 * Pagination component.
 *
 * Simple previous/next pagination with page info.
 * Receives all state through props – no internal data fetching.
 */

import React from 'react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  hasNext: boolean;
  hasPrev: boolean;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  hasNext,
  hasPrev,
}) => {
  if (totalPages <= 1) return null;

  return (
    <nav className="pagination" aria-label="Pagination">
      <button
        className="pagination__btn"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={!hasPrev}
        aria-label="Previous page"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="m15 18-6-6 6-6" />
        </svg>
        Previous
      </button>

      <span className="pagination__info">
        Page {currentPage + 1} of {totalPages}
      </span>

      <button
        className="pagination__btn"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!hasNext}
        aria-label="Next page"
      >
        Next
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="m9 18 6-6-6-6" />
        </svg>
      </button>
    </nav>
  );
};
