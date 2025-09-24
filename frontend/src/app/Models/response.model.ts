// src/app/Models/response.model.ts

import { RequestAction } from './request.model';

export interface ResponseMessage<T = any> {
  action: RequestAction;          // acción que disparó la respuesta, e.g., "ping" o "get_history_bounds"
  request_id?: string;     // correlación con el request enviado
  status: 'success' | 'error';
  data?: T;                // payload con los datos o error
}
