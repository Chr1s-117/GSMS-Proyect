// src/app/Models/gps.tracepoint.ts

/**
 * TracePoint
 *
 * Represents a single point in a GPS trace (historical path).
 * Each trace point includes geographic coordinates and
 * an optional timestamp for chronological ordering.
 *
 * Typical usage:
 * - Stored in a buffer managed by {@link TraceService}.
 * - Rendered as part of a polyline on the map.
 */
export interface TracePoint {
  /**
   * Latitude coordinate of the trace point.
   * - Positive values: northern hemisphere
   * - Negative values: southern hemisphere
   */
  Latitude: number;

  /**
   * Longitude coordinate of the trace point.
   * - Positive values: eastern hemisphere
   * - Negative values: western hemisphere
   */
  Longitude: number;

  /**
   * Timestamp associated with this trace point.
   * - ISO 8601 string format is recommended (e.g., "2025-09-16T12:34:56Z").
   * - Can be `null` if the timestamp is not available.
   */
  Timestamp: string | null;
}
