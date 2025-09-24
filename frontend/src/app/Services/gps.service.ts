// src/app/Services/gps.service.ts
import { Injectable, OnDestroy } from '@angular/core';
import { WebSocketBaseService } from './websocket-base.service';
import { GpsData } from '../Models/gps.model';
import { Observable } from 'rxjs';

/**
 * GpsService
 *
 * Angular service for receiving real-time GPS updates
 * directly from the backend WebSocket endpoint `/gps`.
 *
 * Responsibilities:
 * - Establishes and maintains a WebSocket connection via WebSocketBaseService.
 * - Exposes the raw GPS payload as Observable<GpsData | null> for components to consume.
 * - Handles teardown of the WebSocket connection when destroyed.
 */
@Injectable({ providedIn: 'root' })
export class GpsService extends WebSocketBaseService<GpsData> implements OnDestroy {

  constructor() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.host;
    super(`${wsProtocol}//${wsHost}/gps`);
  }

  /**
   * Returns an observable stream of GPS data.
   * If no data has been received yet, it emits `null`.
   */
  public onGPS(): Observable<GpsData | null> {
    return this.latestMessage$.asObservable();
  }

  /**
   * Exposes WebSocket connection status as observable.
   */
  public getConnectionStatus() {
    return this.connectionStatus$.asObservable();
  }

  override ngOnDestroy(): void {
    super.ngOnDestroy();
  }
}

