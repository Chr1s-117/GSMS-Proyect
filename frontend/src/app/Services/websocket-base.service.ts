// src/app/Services/websocket-base.service.ts
import { Directive, OnDestroy } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { BehaviorSubject, Observable, Subject, timer } from 'rxjs';
import { retry, share, tap, finalize } from 'rxjs/operators';

/**
 * Abstract base service for WebSocket communication.
 *
 * Generics:
 *  - Incoming: messages received from the server.
 *  - Outgoing: messages sent to the server (can differ from Incoming).
 */
@Directive()
export abstract class WebSocketBaseService<Incoming, Outgoing = Incoming> implements OnDestroy {
  /** Active WebSocket connection */
  protected socket$: WebSocketSubject<Incoming> | null = null;

  /** Stream of all incoming messages for immediate broadcast to multiple subscribers */
  protected messages$ = new Subject<Incoming>();

  /**
   * Maintains the latest value received from the WebSocket.
   * This ensures that late subscribers immediately receive the last known value.
   * Can be null initially if no data has been received yet.
   */
  protected latestMessage$ = new BehaviorSubject<Incoming | null>(null);

  /** Tracks the connection status: 'connecting' | 'connected' | 'disconnected' */
  protected connectionStatus$ = new BehaviorSubject<'connecting' | 'connected' | 'disconnected'>('connecting');

  /** Maximum backoff and retry configuration */
  private reconnectInterval = 5000;        // Base delay before reconnection (ms)
  private maxReconnectInterval = 60000;    // Maximum backoff delay (ms)
  private isClosed = false;                // Flag for intentional closure
  private maxRetries = 50;                 // Maximum reconnection attempts

  constructor(private url: string) {}

  /** Explicitly initialize the WebSocket connection. */
  public initialize(): void {
    console.log(`[WebSocketBaseService] Initializing connection to ${this.url}`);
    this.connect();
  }

  /** Internal method to establish or re-establish the WebSocket connection. */
  private connect(attempt = 0): void {
    this.isClosed = false;
    this.connectionStatus$.next('connecting');

    // Create the WebSocketSubject for Incoming messages
    this.socket$ = webSocket<Incoming>(this.url);

    this.socket$
      .pipe(
        retry({
          count: this.maxRetries,
          delay: (error, retryCount) => {
            const delay = Math.min(this.reconnectInterval * Math.pow(2, retryCount), this.maxReconnectInterval);
            console.warn(`[WebSocket] Error occurred. Retry #${retryCount} in ${delay}ms.`, error);
            return timer(delay);
          }
        }),
        tap(() => this.connectionStatus$.next('connected')),
        share(),
        finalize(() => {
          this.socket$ = null;

          if (!this.isClosed && attempt < this.maxRetries) {
            this.connectionStatus$.next('disconnected');
            console.warn('[WebSocket] Connection closed unexpectedly. Reconnecting...');
            this.connect(attempt + 1);
          } else if (this.isClosed) {
            console.log('[WebSocket] Connection closed intentionally.');
          } else {
            console.error('[WebSocket] Maximum reconnection attempts reached. Connection failed permanently.');
            this.connectionStatus$.next('disconnected');
          }
        })
      )
      .subscribe({
        next: (msg: Incoming) => {
          this.messages$.next(msg);
          this.latestMessage$.next(msg);
        },
        error: (err) => {
          this.connectionStatus$.next('disconnected');
          console.error('[WebSocket] Fatal error:', err);
        }
      });
  }

  /** Observable stream of all messages received from the server. */
  public onMessage(): Observable<Incoming | null> {
    return this.latestMessage$.asObservable();
  }

  /** Observable stream of connection status changes. */
  public onConnectionStatus(): Observable<'connecting' | 'connected' | 'disconnected'> {
    return this.connectionStatus$.asObservable();
  }

  /**
   * Safely send a message to the WebSocket server.
   * Accepts the Outgoing type (which can be different from Incoming).
   */
  public sendMessage(msg: Outgoing): boolean {
    if (this.socket$) {
      this.socket$.next(msg as any);
      return true;
    }
    console.warn('[WebSocket] Attempted to send message while socket is not connected.');
    return false;
  }

  /** Close the WebSocket connection intentionally. */
  public close(): void {
    this.isClosed = true;
    this.connectionStatus$.next('disconnected');
    this.socket$?.complete();
    this.socket$ = null;
  }

  /** Angular lifecycle hook invoked when the service is destroyed. */
  ngOnDestroy(): void {
    this.close();
  }
}
