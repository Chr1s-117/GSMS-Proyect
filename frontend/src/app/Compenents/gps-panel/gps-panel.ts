// src/app/Compenents/gps-panel/gps-panel.ts
import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GpsService } from '../../Services/gps.service';
import { GpsData } from '../../Models/gps.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-gps-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './gps-panel.html',
  styleUrls: ['./gps-panel.css']
})
export class GpsPanelComponent implements OnInit, OnDestroy {
  /**
   * Signal that holds the latest GPS data directly from backend.
   * Starts as `null` until the first valid GPS packet arrives.
   */
  gpsData = signal<GpsData | null>(null);

  /** Subscription reference for clean teardown */
  private gpsSubscription: Subscription | null = null;

  constructor(private gpsService: GpsService) {}

  ngOnInit(): void {
    // Subscribe to GPS data directly (backend fields in uppercase)
    this.gpsSubscription = this.gpsService.onGPS().subscribe({
      next: (data: GpsData | null) => {
        this.gpsData.set(data);
      },
      error: (err) => console.error('[GPS Panel ERROR]', err)
    });
  }

  ngOnDestroy(): void {
    // Cleanly unsubscribe on component destruction
    this.gpsSubscription?.unsubscribe();
    this.gpsSubscription = null;
  }
}
