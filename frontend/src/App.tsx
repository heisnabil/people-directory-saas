/**
 * App — Root application component.
 *
 * Composes the People Directory page from reusable components.
 * Owns no data-fetching or API logic — delegates to useEmployeeSearch hook.
 */

import React, { useRef } from 'react';
import { gsap } from 'gsap';
import { useGSAP } from '@gsap/react';
import { useEmployeeSearch } from './hooks/useEmployeeSearch';
import { SearchBar } from './components/SearchBar';
import { EmployeeList } from './components/EmployeeList';
import { EmptyState } from './components/EmptyState';
import { ErrorState } from './components/ErrorState';
import { Pagination } from './components/Pagination';

gsap.registerPlugin(useGSAP);

const App: React.FC = () => {
  const {
    searchInput,
    setSearchInput,
    debouncedSearch,
    clearSearch,
    employees,
    total,
    isLoading,
    isFetching,
    isError,
    error,
    refetch,
    currentPage,
    totalPages,
    goToPage,
    hasNextPage,
    hasPrevPage,
  } = useEmployeeSearch();

  const appRef = useRef<HTMLDivElement>(null);

  // Restrained page entrance
  useGSAP(
    () => {
      const prefersReducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)',
      ).matches;

      if (prefersReducedMotion) return;

      const tl = gsap.timeline({ defaults: { ease: 'power2.out' } });

      tl.fromTo(
        '.page-intro',
        { opacity: 0, y: -6 },
        { opacity: 1, y: 0, duration: 0.35 },
      ).fromTo(
        '.search-bar',
        { opacity: 0, y: 6 },
        { opacity: 1, y: 0, duration: 0.3 },
        '-=0.12',
      );
    },
    { scope: appRef },
  );

  const showResults = !isLoading && !isError && employees.length > 0;
  const showEmpty = !isLoading && !isError && employees.length === 0;
  const showError = isError && error;

  // Build results count text
  const resultsText = (() => {
    if (total === 0) return null;
    const count = `${total} employee${total !== 1 ? 's' : ''}`;
    return debouncedSearch
      ? <>{count} matching "<strong>{debouncedSearch}</strong>"</>
      : count;
  })();

  return (
    <div className="app" ref={appRef}>
      <header className="header">
        <div className="header__inner">
          <h1 className="header__brand">
            <svg className="header__logo" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
            People Directory
          </h1>
        </div>
      </header>

      <main className="main">
        <div className="main__inner">
          <div className="page-intro">
            <h2 className="page-intro__title">Employees</h2>
            <p className="page-intro__subtitle">
              Search by name or department to find team members
            </p>
          </div>

          <SearchBar
            value={searchInput}
            onChange={setSearchInput}
            onClear={clearSearch}
            isFetching={isFetching && !isLoading}
          />

          {/* Results count */}
          {!isLoading && !isError && resultsText && (
            <div className="results-meta" aria-live="polite">
              <span className="results-meta__count">
                {resultsText}
              </span>
            </div>
          )}

          {/* Employee list / loading skeleton */}
          <EmployeeList
            employees={employees}
            isLoading={isLoading}
          />

          {/* Empty state */}
          {showEmpty && (
            <EmptyState
              searchTerm={debouncedSearch}
              onClear={clearSearch}
            />
          )}

          {/* Error state */}
          {showError && (
            <ErrorState error={error} onRetry={() => refetch()} />
          )}

          {/* Pagination */}
          {showResults && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={goToPage}
              hasNext={hasNextPage}
              hasPrev={hasPrevPage}
            />
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
