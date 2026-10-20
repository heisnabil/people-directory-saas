/**
 * Employee data types matching the backend API contract.
 */

export interface Employee {
  id: number;
  name: string;
  email: string;
  department: string;
  designation: string;
  date_of_joining: string; // ISO date string from API
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface EmployeeSearchParams {
  search: string;
  limit: number;
  offset: number;
}
