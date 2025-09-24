import { Component, EventEmitter, Input, Output, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatButtonModule } from '@angular/material/button';
import { MatNativeDateModule } from '@angular/material/core';
import { DateUtcService } from '../../Services/date-utc.service';

@Component({
  selector: 'app-trace-calendar',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule
  ],
  templateUrl: './trace-calendar.html',
  styleUrls: ['./trace-calendar.css']
})
export class TraceCalendarComponent implements OnChanges {
  @Input() startDate: Date | null = null;
  @Input() endDate: Date | null = null;

  @Input() minDate: Date | null = null;
  @Input() maxDate: Date | null = null;

  @Output() dateRangeSelected = new EventEmitter<{ start: Date; end: Date }>();

  // Variables temporales para UI
  tempStartDate: Date | null = null;
  tempStartTime: string = '00:00';
  tempEndDate: Date | null = null;
  tempEndTime: string = '23:59';

  // Para el datepicker (solo fecha)
  uiMinDate: Date | null = null;
  uiMaxDate: Date | null = null;

  constructor(private dateUtcService: DateUtcService) {}

  ngOnChanges(): void {
    console.log('[TRACE-CALENDAR][ngOnChanges] >>> startDate=', this.startDate,
      ' endDate=', this.endDate, ' minDate=', this.minDate, ' maxDate=', this.maxDate);

    // --- Inicializar tempStartDate y tempStartTime ---
    if (this.startDate) {
      this.tempStartDate = this.dateUtcService.toUtcDateOnly(this.startDate);
      this.tempStartTime = this.dateUtcService.formatUtcTime(this.startDate);
      console.log('[TRACE-CALENDAR] Usando startDate para tempStartDate:', this.tempStartDate, ' tempStartTime:', this.tempStartTime);
    } else if (this.minDate) {
      this.tempStartDate = this.dateUtcService.toUtcDateOnly(this.minDate);
      this.tempStartTime = this.dateUtcService.formatUtcTime(this.minDate);
      console.log('[TRACE-CALENDAR] startDate null, usando minDate para tempStartDate:', this.tempStartDate, ' tempStartTime:', this.tempStartTime);
    }

    // --- Inicializar tempEndDate y tempEndTime ---
    if (this.endDate) {
      this.tempEndDate = this.dateUtcService.toUtcDateOnly(this.endDate);
      this.tempEndTime = this.dateUtcService.formatUtcTime(this.endDate);
    }

    // --- Manejo simétrico de maxDate ---
    if (this.maxDate) {
      this.uiMaxDate = this.dateUtcService.toUtcDateOnly(this.maxDate);
      this.tempEndDate = this.uiMaxDate;
      this.tempEndTime = this.dateUtcService.formatUtcTime(this.maxDate);
      console.log('[TRACE-CALENDAR][ngOnChanges] maxDate (real)=', this.maxDate.toISOString(),
        ' -> uiMaxDate=', this.uiMaxDate,
        ' tempEndTime=', this.tempEndTime);
    }

    // --- Manejo simétrico de minDate ---
    if (this.minDate) {
      this.uiMinDate = this.dateUtcService.toUtcDateOnly(this.minDate);
      // Pre-cargar tempStartDate si no estaba definido
      if (!this.startDate) {
        this.tempStartDate = this.uiMinDate;
        this.tempStartTime = this.dateUtcService.formatUtcTime(this.minDate);
        console.log('[TRACE-CALENDAR][ngOnChanges] uiMinDate aplicada a tempStartDate:', this.tempStartDate,
          ' tempStartTime:', this.tempStartTime);
      }
    }

    console.log('[TRACE-CALENDAR][ngOnChanges] Estado final tempStartDate=', this.tempStartDate,
      ' tempEndDate=', this.tempEndDate,
      ' tempStartTime=', this.tempStartTime,
      ' tempEndTime=', this.tempEndTime,
      ' uiMinDate=', this.uiMinDate,
      ' uiMaxDate=', this.uiMaxDate);
  }

  confirmRange(): void {
    if (!this.tempStartDate || !this.tempEndDate) {
      alert('Selecciona fecha válida');
      return;
    }

    const [sh, sm] = this.tempStartTime.split(':').map(Number);
    const [eh, em] = this.tempEndTime.split(':').map(Number);

    let start = this.dateUtcService.buildUtcDate(this.tempStartDate, sh, sm);
    let end = this.dateUtcService.buildUtcDate(this.tempEndDate, eh, em);

    console.log('[TRACE-CALENDAR][confirmRange] Construido rango inicial:',
      ' start=', start.toISOString(), ' end=', end.toISOString());

    // --- Ajuste por límite superior ---
    if (this.maxDate) {
      const isSameDayAsMax = this.tempEndDate?.getTime() === this.uiMaxDate?.getTime();
      if (isSameDayAsMax && end > this.maxDate) {
        console.log('[TRACE-CALENDAR] Ajustando hora fin al máximo permitido');
        end = new Date(this.maxDate);
        this.tempEndTime = this.dateUtcService.formatUtcTime(this.maxDate);
      }
    }

    // --- Ajuste por límite inferior ---
    if (this.minDate) {
      const isSameDayAsMin = this.tempStartDate?.getTime() === this.uiMinDate?.getTime();
      if (isSameDayAsMin && start < this.minDate) {
        console.log('[TRACE-CALENDAR] Ajustando hora inicio al mínimo permitido');
        start = new Date(this.minDate);
        this.tempStartTime = this.dateUtcService.formatUtcTime(this.minDate);
      }
    }

    // --- Comprobación global de coherencia ---
    if (start > end) {
      console.log('[TRACE-CALENDAR] start > end, invirtiendo valores');
      [start, end] = [end, start];
    }

    console.log('[TRACE-CALENDAR][confirmRange] Rango final:',
      ' start=', start.toISOString(), ' end=', end.toISOString());

    this.dateRangeSelected.emit({ start, end });
  }
}
