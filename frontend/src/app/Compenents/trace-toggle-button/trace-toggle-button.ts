// src/app/Compenents/trace-toggle-button/trace-toggle-button.ts

import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * TraceToggleButtonComponent
 *
 * A reusable standalone button component that toggles the visibility
 * of the GPS trace on the map. 
 *
 * Features:
 * - Maintains internal active state (`isActive`).
 * - Emits an event whenever the button is clicked to notify the parent.
 * - Provides visual feedback with distinct styles for active/inactive states.
 *
 * Usage:
 * ```html
 * <app-trace-toggle-button (toggled)="onTraceToggle($event)"></app-trace-toggle-button>
 * ```
 */
@Component({
  selector: 'app-trace-toggle-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './trace-toggle-button.html',
  styleUrls: ['./trace-toggle-button.css']
})
export class TraceToggleButtonComponent {
  /**
   * Internal state flag representing whether the trace is currently visible.
   *
   * @default false
   */
  isActive = false;

  /**
   * EventEmitter that notifies parent components whenever
   * the button is toggled.
   *
   * @event boolean - `true` if active (trace visible), `false` if inactive.
   */
  @Output() toggled = new EventEmitter<boolean>();

  /**
   * Handles button clicks:
   * - Toggles the internal state.
   * - Logs the action for debugging purposes.
   * - Emits the updated visibility state to the parent.
   */
  onClick(): void {
    this.isActive = !this.isActive;

    console.log('[TraceToggleButton] toggled:', this.isActive);

    this.toggled.emit(this.isActive);
  }
}
