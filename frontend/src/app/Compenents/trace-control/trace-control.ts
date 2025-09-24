// src/app/Components/trace-control/trace-control.ts
import { Component, EventEmitter, Output, ViewChild, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TraceToggleButtonComponent } from '../trace-toggle-button/trace-toggle-button';
import { TraceCalendarButtonComponent } from '../trace-calendar-button/trace-calendar-button';
import { TraceCalendarComponent } from '../trace-calendar/trace-calendar';
import { RequestService } from '../../Services/request.service';
import { ResponseService } from '../../Services/response.service';
import { GpsService } from '../../Services/gps.service';
import { GpsData } from '../../Models/gps.model';
import { Subscription, filter } from 'rxjs';
import { DateUtcService } from '../../Services/date-utc.service';
import { ResponseMessage } from '../../Models/response.model';

@Component({
  selector: 'app-trace-control',
  standalone: true,
  imports: [
    CommonModule,
    TraceToggleButtonComponent,
    TraceCalendarButtonComponent,
    TraceCalendarComponent
  ],
  templateUrl: './trace-control.html',
  styleUrls: ['./trace-control.css']
})
export class TraceControlComponent implements OnInit, OnDestroy {
  @Output() traceVisibilityChanged = new EventEmitter<boolean>();

  isTraceVisible = false;
  isCalendarVisible = false;

  @ViewChild(TraceCalendarButtonComponent) calendarButton?: TraceCalendarButtonComponent;

  selectedDateRangeISO: { startISO: string; endISO: string } | null = null;
  selectedStartDate: Date | null = null;
  selectedEndDate: Date | null = null;

  bounds: { startISO: string; endISO: string } | null = null;
  maxCalendarDate: Date | null = null;  // último GPS
  minCalendarDate: Date | null = null;  // primer GPS

  private gpsSub?: Subscription;
  private boundsSub?: Subscription;

  constructor(
    private requestService: RequestService,
    private responseService: ResponseService,
    private gpsService: GpsService,
    private dateUtcService: DateUtcService
  ) {
    console.log('[TraceControl] initialized');
  }

  ngOnInit(): void {
    // 1) Suscribirse al límite superior dinámico (último GPS)
    this.gpsSub = this.gpsService.onGPS().subscribe((data: GpsData | null) => {
      if (data && data.Timestamp) {
        const timestampISO = new Date(data.Timestamp).toISOString();
        this.bounds = { startISO: timestampISO, endISO: timestampISO };

        const utcDate = this.dateUtcService.parseIsoToUtc(timestampISO);
        this.maxCalendarDate = this.dateUtcService.ceilToNextMinute(utcDate);

        console.log(`[TraceControl] 📍 Nuevo timestamp GPS recibido: ${timestampISO}`);
        console.log(`[TraceControl] ⏰ Límite máximo permitido: ${this.maxCalendarDate.toISOString()}`);
      }
    });

    // 2) Pedir y suscribir al límite inferior (get_history_bounds subscribe: true)
    this.requestService.sendRequest('get_history_bounds', { subscribe: true });
    console.log('[TraceControl] 📤 Request get_history_bounds enviado (subscribe:true)');

    // 3) Suscribirse a las respuestas de get_history_bounds
    this.boundsSub = this.responseService.onResponse()
      .pipe(filter((msg): msg is ResponseMessage<any> => !!msg && msg.action === 'get_history_bounds'))
      .subscribe({
        next: (msg) => {
          if (!msg.data || typeof msg.data.Timestamp !== 'string') return;

          try {
            // 🔹 Extraemos Timestamp desde data y redondeamos hacia abajo
            const utcStart = this.dateUtcService.parseIsoToUtc(msg.data.Timestamp);
            this.minCalendarDate = this.dateUtcService.floorToPrevMinute(utcStart);

            console.log(`[TraceControl] ⏳ Límite mínimo permitido actualizado: ${this.minCalendarDate.toISOString()}`);
          } catch (err) {
            console.error('[TraceControl] Error parseando get_history_bounds', err);
          }
        },
        error: (err) => console.error('[TraceControl] ERROR get_history_bounds', err)
      });
  }

  ngOnDestroy(): void {
    this.gpsSub?.unsubscribe();
    this.boundsSub?.unsubscribe();

    // Avisar al backend para cancelar monitor
    this.requestService.sendRequest('get_history_bounds', { subscribe: false });
    console.log('[TraceControl] 📤 Request get_history_bounds enviado (subscribe:false)');
  }

  onTraceToggled(isVisible: boolean): void {
    this.isTraceVisible = isVisible;
    this.traceVisibilityChanged.emit(isVisible);
  }

  toggleCalendarVisibility(isVisible: boolean) {
    this.isCalendarVisible = isVisible;
  }

  onDateRangeSelected(range: { start: Date; end: Date }) {
    if (!range.start || !range.end) return;

    // Normalizamos lo que viene del calendario a UTC
    const utcStart = this.dateUtcService.parseIsoToUtc(range.start.toISOString());
    const utcEnd = this.dateUtcService.parseIsoToUtc(range.end.toISOString());

    // Aseguramos que start <= end
    if (utcStart > utcEnd) {
      alert('La fecha/hora de inicio debe ser menor o igual a la de fin');
      return;
    }

    // Validación contra límite superior real
    if (this.maxCalendarDate && utcEnd > this.maxCalendarDate) {
      alert(`No puedes seleccionar una fecha/hora posterior al último GPS: ${this.maxCalendarDate.toISOString()}`);
      return;
    }

    // Validación contra límite inferior real
    if (this.minCalendarDate && utcStart < this.minCalendarDate) {
      alert(`No puedes seleccionar una fecha/hora anterior al primer GPS disponible: ${this.minCalendarDate.toISOString()}`);
      return;
    }

    this.selectedStartDate = utcStart;
    this.selectedEndDate = utcEnd;

    this.selectedDateRangeISO = {
      startISO: utcStart.toISOString(),
      endISO: utcEnd.toISOString()
    };

    this.isCalendarVisible = false;
    if (this.calendarButton) this.calendarButton.isActive = false;

    // Enviar petición al backend (get_history)
    const requestId = this.requestService.sendRequest('get_history', {
      start: this.selectedDateRangeISO.startISO,
      end: this.selectedDateRangeISO.endISO,
      deviceId: 'default_user'
    });

    console.log(`[TraceControl] 📤 Request get_history enviado con request_id=${requestId}`);
  }
}
