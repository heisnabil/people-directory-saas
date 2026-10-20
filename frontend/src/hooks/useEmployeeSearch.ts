/**
 * Custom hook for employee search with TanStack Query.
 *
 * Handles:
 * - Debounced search input (300ms default)
 * - Request cancellation via AbortSignal
 * - Stable cache keys based on search + pagination
 * - Automatic retries on failure (configurable)
 * - keepPreviousData to avoid layout flicker during pagination
 */

import { useState, useEffect, useCallback } from 'react';
import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { fetchEmployees } from '../api/employees';

const DEBOUNCE_MS = 300;
const PAGE_SIZE = 20;

/**
 * Debounce hook – delays updating the output value until input
 * has been stable for `delay` ms.
 */
function useDebouncedValue<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

export function useEmployeeSearch() {
  const [searchInput, setSearchInput] = useState('');
  const [offset, setOffset] = useState(0);

  // Debounce the raw input to avoid a request per keystroke
  const debouncedSearch = useDebouncedValue(searchInput, DEBOUNCE_MS);

  // Reset pagination when search term changes
  useEffect(() => {
    setOffset(0);
  }, [debouncedSearch]);

  const query = useQuery({
    // Cache key includes debounced search + pagination for stable lookups
    queryKey: ['employees', debouncedSearch, PAGE_SIZE, offset],
    queryFn: ({ signal }) =>
      fetchEmployees(debouncedSearch, PAGE_SIZE, offset, signal),
    // Keep showing previous results while new data loads (avoids layout jump)
    placeholderData: keepPreviousData,
    // Retry network failures, but not validation errors
    retry: (failureCount, error) => {
      if (error instanceof Error && 'status' in error) {
        const status = (error as { status: number }).status;
        // Don't retry client errors (4xx)
        if (status >= 400 && status < 500) return false;
      }
      return failureCount < 2;
    },
    staleTime: 30_000, // Consider data fresh for 30s
  });

  const clearSearch = useCallback(() => {
    setSearchInput('');
    setOffset(0);
  }, []);

  const goToPage = useCallback((page: number) => {
    setOffset(page * PAGE_SIZE);
  }, []);

  const totalPages = query.data
    ? Math.ceil(query.data.total / PAGE_SIZE)
    : 0;

  const currentPage = Math.floor(offset / PAGE_SIZE);

  return {
    // Input state
    searchInput,
    setSearchInput,
    debouncedSearch,
    clearSearch,

    // Query state
    employees: query.data?.items ?? [],
    total: query.data?.total ?? 0,
    isLoading: query.isLoading,
    isFetching: query.isFetching,
    isError: query.isError,
    error: query.error,
    refetch: query.refetch,

    // Pagination
    currentPage,
    totalPages,
    goToPage,
    pageSize: PAGE_SIZE,
    hasNextPage: currentPage < totalPages - 1,
    hasPrevPage: currentPage > 0,
  };
}
