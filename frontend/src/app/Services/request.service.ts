// src/app/Services/request.service.ts
import { Injectable, OnDestroy } from '@angular/core';
import { WebSocketBaseService } from './websocket-base.service';
import { RequestMessage, RequestAction } from '../Models/request.model';

/**
 * RequestService
 *
 * Angular service for sending requests to the backend via WebSocket `/request`.
 * Simplified: no tracking of requestTable.
 */
@Injectable({ providedIn: 'root' })
export class RequestService extends WebSocketBaseService<RequestMessage> implements OnDestroy {

  constructor() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.host;
    super(`${wsProtocol}//${wsHost}/request`);
  }

  /**
   * Send a request to the backend.
   * @param action The action type
   * @param params Optional parameters for the request
   * @param request_id Optional request ID (auto-generated if not provided)
   * @returns The request ID used
   */
  public sendRequest(
    action: RequestAction,
    params?: Record<string, any>,
    request_id?: string
  ): string {
    const id = request_id ?? crypto.randomUUID();
    const payload: RequestMessage = { action, params, request_id: id };

    // Send message via WebSocket
    this.sendMessage(payload);

    console.log(`[RequestService] Request enviado action=${action}, request_id=${id}`);
    return id;
  }

  /** Convenience ping */
  public ping(): string {
    return this.sendRequest('ping');
  }

  override ngOnDestroy(): void {
    super.ngOnDestroy();
  }
}
