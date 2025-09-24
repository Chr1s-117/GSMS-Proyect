// src/app/Models/request.model.ts

/**
 * Defines the set of valid request actions 
 * that the frontend can send to the backend.
 */
export type RequestAction =
  | 'get_history'        // request GPS history
  | 'get_history_bounds' // request GPS history bounds
  | 'get_devices'        // request list of devices
  | 'get_device_status'  // request device status by ID
  | 'ping';              // simple connectivity test

/**
 * General structure for messages sent over the RequestService WebSocket.
 */
export interface RequestMessage {
  action: RequestAction;
  params?: Record<string, any>; // optional parameters (e.g., range, deviceId, filters)
  request_id?: string;
}
