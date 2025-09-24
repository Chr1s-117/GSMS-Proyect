// src/app/app.ts
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GpsPanelComponent } from './Compenents/gps-panel/gps-panel';
import { GpsMapComponent } from './Compenents/gps-map/gps-map';
import { TraceControlComponent } from './Compenents/trace-control/trace-control';

/**
 * App
 *
 * Root standalone component for the Angular application.
 *
 * Responsibilities:
 * - Provides the global layout (title, GPS panels, map).
 * - Hosts the RouterOutlet for navigation between routes.
 * - Integrates GPS Panel (live data) and Trace Control components.
 * - Passes down "trace visibility" state to the map component.
 * - Manages application-level signals, such as title.
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    GpsPanelComponent,
    GpsMapComponent,
    TraceControlComponent
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  /**
   * Application title, stored as a reactive signal.
   * Displayed in the root template header.
   */
  title = signal('GSMS - GPS Monitoring System');

  /**
   * Current state of trace visibility.
   * Passed as Input to the GPS Map component.
   */
  showTrace = false;

  /**
   * Event handler for toggling trace visibility.
   * Receives state from TraceControlComponent and updates map state.
   *
   * @param state - New visibility state (true = show trace, false = hide trace)
   */
  onToggleTrace(state: boolean): void {
    console.log('[App] Trace toggled:', state);
    this.showTrace = state;
  }
}
