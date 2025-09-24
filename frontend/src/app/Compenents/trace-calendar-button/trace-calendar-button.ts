// src/app/Components/trace-calendar-button/trace-calendar-button.ts
import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * TraceCalendarButtonComponent
 *
 * A standalone button that toggles the visibility of the calendar
 * used to select historical GPS trace ranges.
 *
 * Features:
 * - Maintains internal active state (`isActive`).
 * - Emits an event when clicked to notify parent components.
 */
@Component({
  selector: 'app-trace-calendar-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './trace-calendar-button.html',
  styleUrls: ['./trace-calendar-button.css']
})
export class TraceCalendarButtonComponent {
  isActive = false;

  @Output() toggled = new EventEmitter<boolean>();

  onClick(): void {
    this.isActive = !this.isActive;
    console.log('[TraceCalendarButton] toggled:', this.isActive);
    this.toggled.emit(this.isActive);
  }
}
