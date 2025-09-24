// src/app/Compenents/gps-panel/gps-panel.ts
import { 
  Component, 
  OnInit, 
  OnDestroy, 
  signal, 
  effect, 
  runInInjectionContext, 
  Injector, 
  Input, 
  OnChanges, 
  SimpleChanges 
} from '@angular/core';
import { CommonModule } from '@angular/common';
import * as L from 'leaflet';
import { GpsService } from '../../Services/gps.service';
import { GpsData } from '../../Models/gps.model';
import { TraceService } from '../../Services/trace.service';
import { TracePoint } from '../../Models/tracepoint.model';

@Component({
  selector: 'app-gps-map',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './gps-map.html',
  styleUrls: ['./gps-map.css']
})
export class GpsMapComponent implements OnInit, OnDestroy, OnChanges {
  
  private map: L.Map | null = null;
  private marker: L.Marker | null = null;
  private traceLine: L.Polyline | null = null;
  private traceEffectRef: ReturnType<typeof effect> | null = null;

  gpsData = signal<GpsData | null>(null);

  @Input() showTrace = false;

  private defaultLocation: L.LatLngExpression = [10.971354, -74.764425];

  constructor(
    private gpsService: GpsService,
    private traceService: TraceService,
    private injector: Injector
  ) {}

  ngOnInit(): void {
    // Inicialización del mapa
    this.map = L.map('gps-map', {
      center: this.defaultLocation,
      zoom: 15,
      dragging: false,
      scrollWheelZoom: true,
      doubleClickZoom: true,
      touchZoom: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);

    const customIcon = L.icon({
      iconUrl: '/gps.ico',
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    });

    this.marker = L.marker(this.defaultLocation, {
      icon: customIcon,
      opacity: 0
    }).addTo(this.map);

    this.traceLine = L.polyline([], {
      color: 'red',
      weight: 3,
      opacity: this.showTrace ? 0.7 : 0
    }).addTo(this.map);

    // Suscripción GPS en tiempo real usando signal
    this.gpsService.onGPS().subscribe({
      next: (data: GpsData | null) => {
        this.gpsData.set(data);

        if (!data) {
          this.marker!.setOpacity(0);
          return;
        }

        const latLng: L.LatLngExpression = [data.Latitude, data.Longitude];
        this.marker!.setLatLng(latLng);
        this.marker!.setOpacity(1);

        this.map!.panTo(latLng, { animate: true });
      },
      error: (err) => console.error('[GPS Map ERROR]', err)
    });

    // Reactive trace subscription usando effect
    runInInjectionContext(this.injector, () => {
      this.traceEffectRef = effect(() => {
        const trace: TracePoint[] = this.traceService.getTrace()();
        if (!this.traceLine) return;

        this.traceLine.setLatLngs(trace.map(p => [p.Latitude, p.Longitude]));
        this.traceLine.setStyle({
          opacity: this.showTrace ? 0.7 : 0
        });
      });
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['showTrace'] && this.traceLine) {
      this.traceLine.setStyle({
        opacity: this.showTrace ? 0.7 : 0
      });
    }
  }

  ngOnDestroy(): void {
    this.traceEffectRef?.destroy();
    this.map?.remove();
    this.map = null;
  }
}
