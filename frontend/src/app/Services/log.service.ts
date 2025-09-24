import { Injectable, OnDestroy } from '@angular/core';
import { WebSocketBaseService } from './websocket-base.service';
import { LogMessage } from '../Models/log.model';
import { Observable } from 'rxjs';

/**
 * LogService
 *
 * Angular service for receiving log messages from the backend
 * via the dedicated WebSocket endpoint `/logs`.
 *
 * Responsibilities:
 * - Maintain a live WebSocket connection to `/logs`.
 * - Expose incoming log messages as an observable.
 * - Print logs/errors to the browser console for debugging.
 */
@Injectable({ providedIn: 'root' })
export class LogService extends WebSocketBaseService<LogMessage> implements OnDestroy {

  constructor() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.host;
    super(`${wsProtocol}//${wsHost}/logs`);

    // Console debugging of incoming log messages
    this.onMessage().subscribe({
      next: (log: LogMessage | null) => {
        if (!log) return;

        switch (log.msg_type) {
          case 'log':
            console.log(`[LOG] ${log.message}`);
            break;

          case 'error':
            console.error(`[ERROR] ${log.message}`);
            break;

          default:
            console.warn('[UNKNOWN LOG TYPE]', log);
        }
      },
      error: (err) => console.error('[WebSocket Log ERROR]', err),
    });
  }

  /**
   * Observable stream of log messages.
   */
  public onLog(): Observable<LogMessage | null> {
    return this.latestMessage$.asObservable();
  }

  override ngOnDestroy(): void {
    super.ngOnDestroy();
  }
}
