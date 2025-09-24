// src/app/Models/gps.model.ts

/**
 * Represents a single GPS data point received from the backend WebSocket.
 *
 * This interface mirrors the structure of the payload sent by the backend
 * via the `/gps` WebSocket endpoint.
 *
 * Properties:
 * - Latitude: number representing the geographic latitude in decimal degrees.
 * - Longitude: number representing the geographic longitude in decimal degrees.
 * - Altitude: number representing the altitude in meters above sea level.
 * - Accuracy: number indicating the estimated accuracy of the GPS reading in meters.
 * - Timestamp: Date object representing the time the GPS data was recorded.
 */
export interface GpsData {
  Latitude: number;
  Longitude: number;
  Altitude: number;
  Accuracy: number;
  Timestamp: string | null;
}