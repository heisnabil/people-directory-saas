/**
 * Environment configuration.
 *
 * Centralises all env-var access so no component imports import.meta.env directly.
 * Validates at module load time – if VITE_API_BASE_URL is missing, the app
 * fails immediately with a clear message instead of silently breaking at runtime.
 */

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error(
    '[Config] VITE_API_BASE_URL is not set. ' +
    'Create a .env file with VITE_API_BASE_URL=http://localhost:8000/api/v1'
  );
}

export const config = {
  apiBaseUrl: apiBaseUrl as string,
} as const;
