/**
 * EmployeeList component.
 *
 * Renders a list of employee rows with GSAP stagger animation
 * when results change. Handles loading skeleton state.
 * Empty state is handled by the parent.
 *
 * Animation is scoped to the container ref and respects prefers-reduced-motion.
 */

import React, { useRef } from 'react';
import { gsap } from 'gsap';
import { useGSAP } from '@gsap/react';
import type { Employee } from '../types/employee';
import { EmployeeCard } from './EmployeeCard';

gsap.registerPlugin(useGSAP);

interface EmployeeListProps {
  employees: Employee[];
  isLoading: boolean;
  searchTerm?: string;
}

export const EmployeeList: React.FC<EmployeeListProps> = ({
  employees,
  isLoading,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Animate rows when the employee list changes
  useGSAP(
    () => {
      if (isLoading || employees.length === 0) return;

      const prefersReducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)',
      ).matches;

      if (prefersReducedMotion) {
        gsap.set('.employee-row', { opacity: 1, y: 0 });
        return;
      }

      gsap.fromTo(
        '.employee-row',
        { opacity: 0, y: 8 },
        {
          opacity: 1,
          y: 0,
          duration: 0.3,
          stagger: 0.03,
          ease: 'power2.out',
          clearProps: 'transform',
        },
      );
    },
    { scope: containerRef, dependencies: [employees, isLoading] },
  );

  if (isLoading) {
    return (
      <div className="skeleton-list" aria-busy="true" aria-label="Loading employees">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="skeleton-row" aria-hidden="true">
            <div className="skeleton skeleton--circle" />
            <div className="skeleton-row__lines">
              <div className="skeleton skeleton--name skeleton--w60" />
              <div className="skeleton skeleton--text skeleton--w40" />
            </div>
            <div className="skeleton-row__meta">
              <div className="skeleton skeleton--text skeleton--w100" />
              <div className="skeleton skeleton--text skeleton--w120" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (employees.length === 0) {
    return null; // Empty state is handled by parent
  }

  return (
    <div ref={containerRef} className="employee-list" role="list" aria-label="Employee results">
      {employees.map((employee, index) => (
        <div key={employee.id} role="listitem">
          <EmployeeCard employee={employee} index={index} />
        </div>
      ))}
    </div>
  );
};
