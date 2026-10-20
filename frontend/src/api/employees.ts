/**
 * Employee API client.
 *
 * Separated from components so network concerns don't leak into presentation.
 * Accepts an AbortSignal for request cancellation (used by TanStack Query).
 */

import { config } from '../config/env';
import type { Employee, PaginatedResponse } from '../types/employee';

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Fetch employees from the backend.
 *
 * @param search  - Search term (name or department)
 * @param limit   - Page size
 * @param offset  - Pagination offset
 * @param signal  - AbortSignal for request cancellation
 */
export async function fetchEmployees(
  search: string = '',
  limit: number = 20,
  offset: number = 0,
  signal?: AbortSignal,
): Promise<PaginatedResponse<Employee>> {
  const url = new URL(`${config.apiBaseUrl}/employees`);

  if (search.trim()) {
    url.searchParams.set('search', search.trim());
  }
  url.searchParams.set('limit', String(limit));
  url.searchParams.set('offset', String(offset));

  const response = await fetch(url.toString(), {
    signal,
    headers: { Accept: 'application/json' },
  });

  if (!response.ok) {
    let detail: string | undefined;
    try {
      const body = await response.json();
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      // Response body wasn't JSON – use status text
    }

    throw new ApiError(
      `Request failed with status ${response.status}`,
      response.status,
      detail,
    );
  }

  return response.json();
}
