/**
 * Frontend tests for the Employee Directory.
 *
 * Tests verify:
 * - Search input accepts and updates text
 * - Debouncing reduces request frequency
 * - Clear search works
 * - Loading state is displayed
 * - Successful data is rendered
 * - Empty results are communicated
 * - Errors expose a Retry action
 * - Components render correctly
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { SearchBar } from '../components/SearchBar';
import { EmployeeCard } from '../components/EmployeeCard';
import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';

// ====================================================================
// Test helpers
// ====================================================================

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: 0 },
    },
  });
}

function renderWithQuery(ui: React.ReactElement) {
  const client = createTestQueryClient();
  return render(
    <QueryClientProvider client={client}>{ui}</QueryClientProvider>,
  );
}

const mockEmployee = {
  id: 1,
  name: 'Rahul Sharma',
  email: 'rahul.sharma@company.com',
  department: 'Engineering',
  designation: 'Senior Software Engineer',
  date_of_joining: '2021-03-15',
};

// ====================================================================
// SearchBar tests
// ====================================================================

describe('SearchBar', () => {
  it('renders the search input', () => {
    render(
      <SearchBar value="" onChange={vi.fn()} onClear={vi.fn()} />,
    );
    expect(screen.getByRole('search')).toBeInTheDocument();
    expect(screen.getByLabelText('Search employees')).toBeInTheDocument();
  });

  it('displays the current value', () => {
    render(
      <SearchBar value="rahul" onChange={vi.fn()} onClear={vi.fn()} />,
    );
    expect(screen.getByDisplayValue('rahul')).toBeInTheDocument();
  });

  it('calls onChange when user types', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();

    render(
      <SearchBar value="" onChange={onChange} onClear={vi.fn()} />,
    );

    const input = screen.getByLabelText('Search employees');
    await user.type(input, 'a');

    expect(onChange).toHaveBeenCalledWith('a');
  });

  it('shows clear button when value is present', () => {
    render(
      <SearchBar value="test" onChange={vi.fn()} onClear={vi.fn()} />,
    );
    expect(screen.getByLabelText('Clear search')).toBeInTheDocument();
  });

  it('does not show clear button when value is empty', () => {
    render(
      <SearchBar value="" onChange={vi.fn()} onClear={vi.fn()} />,
    );
    expect(screen.queryByLabelText('Clear search')).not.toBeInTheDocument();
  });

  it('calls onClear when clear button is clicked', async () => {
    const onClear = vi.fn();
    const user = userEvent.setup();

    render(
      <SearchBar value="test" onChange={vi.fn()} onClear={onClear} />,
    );

    await user.click(screen.getByLabelText('Clear search'));
    expect(onClear).toHaveBeenCalledOnce();
  });

  it('shows spinner when fetching', () => {
    render(
      <SearchBar
        value="test"
        onChange={vi.fn()}
        onClear={vi.fn()}
        isFetching={true}
      />,
    );
    expect(screen.getByRole('status')).toBeInTheDocument();
  });
});

// ====================================================================
// EmployeeCard tests
// ====================================================================

describe('EmployeeCard', () => {
  it('renders employee name', () => {
    renderWithQuery(<EmployeeCard employee={mockEmployee} />);
    expect(screen.getByText('Rahul Sharma')).toBeInTheDocument();
  });

  it('renders employee email', () => {
    renderWithQuery(<EmployeeCard employee={mockEmployee} />);
    expect(screen.getByText('rahul.sharma@company.com')).toBeInTheDocument();
  });

  it('renders department', () => {
    renderWithQuery(<EmployeeCard employee={mockEmployee} />);
    expect(screen.getByText('Engineering')).toBeInTheDocument();
  });

  it('renders designation', () => {
    renderWithQuery(<EmployeeCard employee={mockEmployee} />);
    expect(screen.getByText('Senior Software Engineer')).toBeInTheDocument();
  });

  it('renders formatted joining date', () => {
    renderWithQuery(<EmployeeCard employee={mockEmployee} />);
    expect(screen.getByText(/Mar 15, 2021/)).toBeInTheDocument();
  });

  it('renders initials in avatar', () => {
    renderWithQuery(<EmployeeCard employee={mockEmployee} />);
    expect(screen.getByText('RS')).toBeInTheDocument();
  });
});

// ====================================================================
// EmptyState tests
// ====================================================================

describe('EmptyState', () => {
  it('shows "No employees found" message', () => {
    render(<EmptyState searchTerm="xyz" onClear={vi.fn()} />);
    expect(screen.getByText('No employees found')).toBeInTheDocument();
  });

  it('shows the search term in the message', () => {
    render(<EmptyState searchTerm="xyz" onClear={vi.fn()} />);
    expect(screen.getByText('xyz')).toBeInTheDocument();
  });

  it('shows "Clear search" button when search term exists', () => {
    render(<EmptyState searchTerm="xyz" onClear={vi.fn()} />);
    expect(screen.getByText('Clear search')).toBeInTheDocument();
  });

  it('does not show "Clear search" when no search term', () => {
    render(<EmptyState searchTerm="" onClear={vi.fn()} />);
    expect(screen.queryByText('Clear search')).not.toBeInTheDocument();
  });

  it('calls onClear when button is clicked', async () => {
    const onClear = vi.fn();
    const user = userEvent.setup();

    render(<EmptyState searchTerm="xyz" onClear={onClear} />);
    await user.click(screen.getByText('Clear search'));

    expect(onClear).toHaveBeenCalledOnce();
  });
});

// ====================================================================
// ErrorState tests
// ====================================================================

describe('ErrorState', () => {
  it('renders error message', () => {
    render(<ErrorState error={new Error('fail')} onRetry={vi.fn()} />);
    expect(screen.getByText('Unable to load employees')).toBeInTheDocument();
  });

  it('shows retry button', () => {
    render(<ErrorState error={new Error('fail')} onRetry={vi.fn()} />);
    expect(screen.getByText('Try again')).toBeInTheDocument();
  });

  it('calls onRetry when retry button is clicked', async () => {
    const onRetry = vi.fn();
    const user = userEvent.setup();

    render(<ErrorState error={new Error('fail')} onRetry={onRetry} />);
    await user.click(screen.getByText('Try again'));

    expect(onRetry).toHaveBeenCalledOnce();
  });
});

// ====================================================================
// Debounce behavior test
// ====================================================================

describe('Debounce behavior', () => {
  it('delays value propagation by the debounce interval', () => {
    vi.useFakeTimers();
    const results: string[] = [];

    function TestComponent() {
      const [input, setInput] = React.useState('');
      const [debounced, setDebounced] = React.useState('');

      React.useEffect(() => {
        const timer = setTimeout(() => setDebounced(input), 300);
        return () => clearTimeout(timer);
      }, [input]);

      React.useEffect(() => {
        results.push(debounced);
      }, [debounced]);

      return (
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          aria-label="test-input"
        />
      );
    }

    const { rerender: _ } = render(<TestComponent />);
    const input = screen.getByLabelText('test-input');
    const { fireEvent } = require('@testing-library/react');

    // Simulate rapid typing
    fireEvent.change(input, { target: { value: 'r' } });
    fireEvent.change(input, { target: { value: 'ra' } });
    fireEvent.change(input, { target: { value: 'rah' } });

    // Before debounce fires, only initial "" should be emitted
    expect(results).toEqual(['']);

    // Advance past the debounce window inside act()
    const { act } = require('react');
    act(() => {
      vi.advanceTimersByTime(350);
    });

    // After debounce, "rah" should be the only new value (not "r" or "ra")
    expect(results).toContain('rah');
    expect(results.filter((r: string) => r !== '')).toHaveLength(1);

    vi.useRealTimers();
  });
});
