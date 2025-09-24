// src/app/Models/log.model.ts

export type LogMessageType = 'log' | 'error';

export interface LogMessage {
  msg_type: LogMessageType;
  message: string;
}
