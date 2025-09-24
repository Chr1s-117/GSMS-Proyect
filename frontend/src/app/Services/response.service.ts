import { Injectable, OnDestroy } from '@angular/core';
import { WebSocketBaseService } from './websocket-base.service';
import { ResponseMessage } from '../Models/response.model';
import { RequestAction } from '../Models/request.model';
import { Observable } from 'rxjs';
import { filter } from 'rxjs/operators';

/**
 * Servicio para recibir respuestas desde el backend vía WebSocket.
 */
@Injectable({ providedIn: 'root' })
export class ResponseService extends WebSocketBaseService<ResponseMessage> implements OnDestroy {

  constructor() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.host;
    super(`${wsProtocol}//${wsHost}/response`);

    // Debug: imprimir todos los mensajes recibidos
    this.onMessage().subscribe({
      next: (resp: ResponseMessage | null) => {
        if (!resp) return;

        console.debug('[RESPONSE] Received message:', resp);

        if (resp.status === 'error') {
          console.error(`[RESPONSE-ERROR] action=${resp.action} request_id=${resp.request_id}`, resp.data);
        } else {
          console.log(`[RESPONSE-SUCCESS] action=${resp.action} request_id=${resp.request_id}`, resp.data);
        }
      },
      error: (err) => console.error('[WebSocket Response ERROR]', err),
    });
  }

  /** Observable general de todas las respuestas */
  public onResponse(): Observable<ResponseMessage | null> {
    return this.latestMessage$.asObservable();
  }

  /**
   * Observable filtrado por action.
   * Permite suscribirse solo a un tipo específico de respuesta.
   */
  public onResponseByAction(action: RequestAction): Observable<ResponseMessage> {
    return this.onResponse().pipe(
      filter((resp): resp is ResponseMessage => !!resp && resp.action === action)
    );
  }

  override ngOnDestroy(): void {
    super.ngOnDestroy();
  }
}
