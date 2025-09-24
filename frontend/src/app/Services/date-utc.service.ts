// src/app/Services/date-utc.service.ts
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class DateUtcService {

  /**
   * Construye un instante UTC (Date) a partir de una fecha "calendar" + horas/minutos.
   *
   * IMPORTANT: `date` debe representar el día que el usuario vio en el picker,
   * es decir, debe tener las componentes año/mes/día correctas según la vista del calendario.
   * Ejemplos válidos para `date`:
   * - un Date devuelto por el MatDatepicker (normalmente new Date(y,m,d) -> local-midnight), o
   * - el resultado de toUtcDateOnly(...) (ver abajo) que garantiza las componentes correctas.
   *
   * Usamos Date.UTC(...) para construir el instante UTC resultante.
   */
  buildUtcDate(date: Date, hours: number, minutes: number): Date {
    return new Date(Date.UTC(
      date.getFullYear(), date.getMonth(), date.getDate(),
      hours, minutes, 0
    ));
  }

  /** Formatea la hora (en UTC) como 'HH:mm' */
  formatUtcTime(date: Date): string {
    return `${date.getUTCHours().toString().padStart(2,'0')}:${date.getUTCMinutes().toString().padStart(2,'0')}`;
  }

  /**
   * Parsea una cadena ISO (esperando un timestamp UTC como '2025-09-20T12:34:56Z')
   * y devuelve un Date que representa ese instante UTC.
   *
   * Nota: si el backend pudiera enviar ISOs sin 'Z', conviene normalizar antes de llamar aquí.
   */
  parseIsoToUtc(iso: string): Date {
    const d = new Date(iso);
    return new Date(Date.UTC(
      d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(),
      d.getUTCHours(), d.getUTCMinutes(), d.getUTCSeconds()
    ));
  }

  /**
   * Devuelve un Date apto para pasar al datepicker y para que éste muestre el "día UTC correcto".
   *
   * Comportamiento: toma un `Date`-instante (por ejemplo, 2025-09-20T13:15:40Z) y
   * devuelve new Date(utcYear, utcMonth, utcDate) => **local-midnight**
   * cuyas componentes (year/month/date) coinciden con el día UTC original.
   *
   * Esto garantiza que el MatDatepicker (que usa getters locales getFullYear/getDate)
   * muestre el día correspondiente al UTC del instante.
   */
  toUtcDateOnly(date: Date): Date {
    return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
  }

  /**
   * Redondea un instante hacia arriba al minuto más cercano en UTC.
   * - Si tiene segundos > 0 o ms > 0, avanza un minuto y pone segundos=0,ms=0.
   * - Si ya está exacto en minuto, solo deja segundos=0,ms=0.
   * Devuelve un nuevo Date (no muta el original).
   */
  ceilToNextMinute(date: Date): Date {
    const rounded = new Date(date.getTime());
    if (rounded.getUTCSeconds() > 0 || rounded.getUTCMilliseconds() > 0) {
      rounded.setUTCSeconds(0, 0);
      rounded.setUTCMinutes(rounded.getUTCMinutes() + 1);
    } else {
      rounded.setUTCSeconds(0, 0);
    }
    return rounded;
  }
  
  /**
   * Redondea un instante hacia abajo al minuto más cercano en UTC.
   * - Descarta segundos y milisegundos, no avanza el minuto.
   * Devuelve un nuevo Date (no muta el original).
   */
  floorToPrevMinute(date: Date): Date {
    const rounded = new Date(date.getTime());
    rounded.setUTCSeconds(0, 0); // elimina segundos y ms
    return rounded;
  }
}
