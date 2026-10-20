/**
 * SearchBar component.
 *
 * A controlled search input with clear button. Does NOT own debounce logic
 * or make API calls — those responsibilities belong to the parent/hook layer.
 */

import React, { useRef, useEffect } from 'react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onClear: () => void;
  placeholder?: string;
  isFetching?: boolean;
  /** Auto-focus on mount */
  autoFocus?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  onClear,
  placeholder = 'Search by name or department…',
  isFetching = false,
  autoFocus = true,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  const handleClear = () => {
    onClear();
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleClear();
    }
  };

  return (
    <div className="search-bar" role="search">
      <div className="search-bar__input-wrapper">
        <svg
          className="search-bar__icon"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
        </svg>

        <input
          ref={inputRef}
          id="employee-search"
          type="search"
          className="search-bar__input"
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          aria-label="Search employees"
          autoComplete="off"
          spellCheck={false}
        />

        {isFetching && (
          <div className="search-bar__spinner" aria-label="Loading" role="status">
            <div className="spinner" />
          </div>
        )}

        {value && !isFetching && (
          <button
            className="search-bar__clear"
            onClick={handleClear}
            aria-label="Clear search"
            type="button"
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M18 6 6 18" />
              <path d="m6 6 12 12" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};
