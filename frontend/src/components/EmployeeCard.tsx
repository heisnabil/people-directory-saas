/**
 * EmployeeCard — A single employee row in the directory list.
 *
 * Displays name, designation, department, email, and join date.
 * Uses initials-based avatar with deterministic department-based color.
 * Purely presentational — receives all data through props.
 */

import React from 'react';
import type { Employee } from '../types/employee';

interface EmployeeCardProps {
  employee: Employee;
  /** Index for staggered animation (used by parent for GSAP) */
  index?: number;
}

/**
 * Format an ISO date string to a human-readable format.
 * e.g. "2021-03-15" → "Mar 15, 2021"
 */
function formatDate(dateStr: string): string {
  try {
    const date = new Date(dateStr + 'T00:00:00'); // Avoid timezone shift
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

/**
 * Generate initials from a full name.
 * "Rahul Sharma" → "RS"
 */
function getInitials(name: string): string {
  return name
    .split(' ')
    .filter(Boolean)
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

/**
 * Map departments to curated, muted HSL colors that work on warm surfaces.
 * Falls back to a deterministic hash for unknown departments.
 */
const DEPARTMENT_COLORS: Record<string, string> = {
  Engineering:       'hsl(220, 42%, 52%)',
  Product:           'hsl(262, 38%, 52%)',
  Design:            'hsl(340, 42%, 52%)',
  Marketing:         'hsl(25, 50%, 50%)',
  'Human Resources': 'hsl(170, 40%, 44%)',
  Finance:           'hsl(195, 45%, 48%)',
  Operations:        'hsl(145, 38%, 46%)',
  Sales:             'hsl(15, 50%, 50%)',
  Legal:             'hsl(210, 30%, 50%)',
};

function getDepartmentColor(department: string): string {
  if (DEPARTMENT_COLORS[department]) {
    return DEPARTMENT_COLORS[department];
  }
  // Deterministic fallback
  let hash = 0;
  for (let i = 0; i < department.length; i++) {
    hash = department.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 35%, 50%)`;
}

export const EmployeeCard: React.FC<EmployeeCardProps> = ({ employee }) => {
  const initials = getInitials(employee.name);
  const color = getDepartmentColor(employee.department);

  return (
    <article className="employee-row" data-testid="employee-card">
      <div
        className="employee-row__avatar"
        style={{ backgroundColor: color }}
        aria-hidden="true"
      >
        {initials}
      </div>

      <div className="employee-row__identity">
        <h3 className="employee-row__name">{employee.name}</h3>
        <p className="employee-row__designation">{employee.designation}</p>
      </div>

      <div className="employee-row__meta">
        <span
          className="employee-row__department"
          style={{
            backgroundColor: `${color}0f`,
            color: color,
            borderColor: `${color}25`,
          }}
        >
          {employee.department}
        </span>

        <span className="employee-row__detail" title={employee.email}>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <rect width="20" height="16" x="2" y="4" rx="2" />
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
          </svg>
          <span className="employee-row__email">{employee.email}</span>
        </span>

        <span className="employee-row__detail">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M8 2v4" /><path d="M16 2v4" />
            <rect width="18" height="18" x="3" y="4" rx="2" />
            <path d="M3 10h18" />
          </svg>
          <span className="employee-row__date">{formatDate(employee.date_of_joining)}</span>
        </span>
      </div>
    </article>
  );
};
