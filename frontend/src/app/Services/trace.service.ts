import { Injectable, OnDestroy, signal } from '@angular/core'; 
import { Subscription, filter } from 'rxjs';
import { GpsService } from './gps.service';
import { ResponseService } from './response.service';
import { TracePoint } from '../Models/tracepoint.model';
import { ResponseMessage } from '../Models/response.model';
import { DateUtcService } from '../Services/date-utc.service';

@Injectable({ providedIn: 'root' })
export class TraceService implements OnDestroy {
  private gpsSub: Subscription | null = null;
  private historySub: Subscription | null = null;

  // Buffers separados
  private dummyBuffer = signal<TracePoint[]>([]);
  private dummyHashSet = new Set<string>();

  private realtimeBuffer = signal<TracePoint[]>([]);
  private realtimeHashSet = new Set<string>();

  // Buffer final para el mapa
  private finalBuffer = signal<TracePoint[]>([]);

  private readonly COORD_DECIMALS = 6;

  constructor(
    private gpsService: GpsService,
    private responseService: ResponseService,
    private dateUtc: DateUtcService
  ) {
    // Suscripción GPS en tiempo real
    this.gpsSub = this.gpsService.onGPS().subscribe({
      next: (data) => {
        if (!data) return;
        if (typeof data.Latitude === 'number' && typeof data.Longitude === 'number') {
          this.addToRealtime({
            Latitude: data.Latitude,
            Longitude: data.Longitude,
            Timestamp: data.Timestamp ?? null
          });
        }
      },
      error: (err) => console.error('[TraceService ERROR GPS]', err)
    });

    // Suscripción al get_history (dummy)
    this.historySub = this.responseService.onResponse()
      .pipe(filter((msg): msg is ResponseMessage<any> => !!msg && msg.action === 'get_history'))
      .subscribe({
        next: (msg) => {
          if (!msg.data || !Array.isArray(msg.data)) return;

          // 🔹 Limpiar dummyBuffer antes de agregar nuevos puntos
          this.dummyBuffer.set([]);
          this.dummyHashSet.clear();
          console.log('[TraceService] dummyBuffer reset antes de agregar history');

          for (const p of msg.data) {
            if (!p || typeof p.Latitude !== 'number' || typeof p.Longitude !== 'number') continue;
            this.addToDummy({
              Latitude: p.Latitude,
              Longitude: p.Longitude,
              Timestamp: p.Timestamp ?? null
            });
          }
        },
        error: (err) => console.error('[TraceService ERROR get_history]', err)
      });
  }

  // -----------------------
  // Hash y normalización
  private normalizeCoord(value: number): number {
    const factor = Math.pow(10, this.COORD_DECIMALS);
    return Math.round(value * factor) / factor;
  }

  private hashPoint(point: TracePoint): string {
    return `${point.Latitude.toFixed(this.COORD_DECIMALS)}|${point.Longitude.toFixed(this.COORD_DECIMALS)}|${point.Timestamp ?? ''}`;
  }

  private parseTimestamp(ts: string | null): number {
    if (!ts) return 0;
    try {
      const d = this.dateUtc.parseIsoToUtc(ts);
      return d.getTime();
    } catch {
      return 0;
    }
  }

  // -----------------------
  // Inserción binaria en buffer
  private insertSorted(buffer: TracePoint[], point: TracePoint): number {
    let left = 0, right = buffer.length;
    const ts = this.parseTimestamp(point.Timestamp);

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (this.parseTimestamp(buffer[mid].Timestamp) < ts) left = mid + 1;
      else right = mid;
    }
    buffer.splice(left, 0, point);
    return left;
  }

  // -----------------------
  // Dummy (A) con prioridad
  private addToDummy(point: TracePoint) {
    point = {
      Latitude: this.normalizeCoord(point.Latitude),
      Longitude: this.normalizeCoord(point.Longitude),
      Timestamp: point.Timestamp ?? null
    };

    const hash = this.hashPoint(point);
    if (this.dummyHashSet.has(hash)) return;

    const buffer = [...this.dummyBuffer()];
    this.insertSorted(buffer, point);
    this.dummyBuffer.set(buffer);
    this.dummyHashSet.add(hash);

    console.log('[TraceService] addToDummy -> punto agregado:', point);

    // Reconstruir finalBuffer al actualizar dummy
    this.rebuildFinalBuffer();
  }

  // Realtime (B) dinámico
  private addToRealtime(point: TracePoint) {
    point = {
      Latitude: this.normalizeCoord(point.Latitude),
      Longitude: this.normalizeCoord(point.Longitude),
      Timestamp: point.Timestamp ?? null
    };

    const hash = this.hashPoint(point);
    if (this.realtimeHashSet.has(hash)) return;

    const buffer = [...this.realtimeBuffer()];
    this.insertSorted(buffer, point);
    this.realtimeBuffer.set(buffer);
    this.realtimeHashSet.add(hash);

    console.log('[TraceService] addToRealtime -> punto agregado:', point);

    // Reconstruir finalBuffer al actualizar realtime
    this.rebuildFinalBuffer();
  }

  // -----------------------
  // Construye C = A + B
  private rebuildFinalBuffer() {
    const A = this.dummyBuffer();
    const B_all = this.realtimeBuffer();

    let B: TracePoint[] = [];

    if (A.length === 0) {
      B = B_all;
    } else {
      const oldestDummyTs = this.parseTimestamp(A[A.length - 1].Timestamp);
      B = B_all.filter(p => this.parseTimestamp(p.Timestamp) > oldestDummyTs);
    }

    const combined: TracePoint[] = [];
    const seen = new Set<string>();

    for (const p of [...A, ...B]) {
      const hash = this.hashPoint(p);
      if (!seen.has(hash)) {
        combined.push(p);
        seen.add(hash);
      }
    }

    this.finalBuffer.set(combined);
    console.log('[TraceService] finalBuffer reconstruido -> total puntos:', combined.length);
  }

  // -----------------------
  // Acceso externo
  public getTrace() {
    return this.finalBuffer.asReadonly();
  }

  public clearTrace() {
    this.dummyBuffer.set([]);
    this.dummyHashSet.clear();
    this.realtimeBuffer.set([]);
    this.realtimeHashSet.clear();
    this.finalBuffer.set([]);
    console.log('[TraceService] Buffers cleared');
  }

  ngOnDestroy(): void {
    this.gpsSub?.unsubscribe();
    this.historySub?.unsubscribe();
  }
}
