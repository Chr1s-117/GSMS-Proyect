import { 
  ApplicationConfig, 
  provideBrowserGlobalErrorListeners, 
  provideZoneChangeDetection, 
  inject, 
  provideAppInitializer 
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { LogService } from './Services/log.service';
import { GpsService } from './Services/gps.service';
import { RequestService } from './Services/request.service';
import { ResponseService } from './Services/response.service';
import { TraceService } from './Services/trace.service';
import { routes } from './app.routes';

/**
 * appConfig
 *
 * Root-level configuration object for the Angular standalone application.
 *
 * Responsibilities:
 * - Registers application-wide providers, including:
 *   * Global error handling
 *   * Optimized change detection
 *   * Router setup
 *   * Core services (LogService, GpsService, TraceService)
 * - Uses `provideAppInitializer` to force early instantiation of critical services:
 *   * Ensures WebSocket connections (GPS + Logs) are established immediately on app bootstrap.
 *   * Guarantees that logging and GPS data streams are available before any component is mounted.
 * - Promotes a **centralized initialization pattern**, where each service exposes its own `initialize()` method.
 */
export const appConfig: ApplicationConfig = {
  providers: [
    /**
     * Enable global error listeners to capture both
     * synchronous and asynchronous application errors.
     */
    provideBrowserGlobalErrorListeners(),

    /**
     * Optimize Angular's change detection.
     * Event coalescing batches multiple events into a single cycle,
     * reducing performance overhead in large applications.
     */
    provideZoneChangeDetection({ eventCoalescing: true }),

    /**
     * Register Angular Router with application routes.
     */
    provideRouter(routes),

    /**
     * Core application services registered as singletons.
     */
    LogService,
    GpsService,
    RequestService,
    ResponseService,
    TraceService,

    /**
     * Force early initialization of GPS service.
     * Starts WebSocket connection and GPS data streaming immediately.
     */
    provideAppInitializer(() => {
      const gpsService = inject(GpsService);
      gpsService.initialize();
    }),

    /**
     * Force early initialization of Log service.
     * Ensures that all logs are captured from the moment
     * the application is bootstrapped.
     */
    provideAppInitializer(() => {
      const logService = inject(LogService);
      logService.initialize();
    }),

    provideAppInitializer(() => {
      const responseService = inject(ResponseService);
      responseService.initialize();
    }),

    provideAppInitializer(() => {
      const requestService = inject(RequestService);
      requestService.initialize();

      // Envia un ping y obtiene el request_id
      const requestId = requestService.ping();

    }),

    /**
     * Ensure TraceService is instantiated early.
     * This guarantees that the GPS trace buffer starts collecting
     * data immediately, even before any component consumes it.
     */
    provideAppInitializer(() => {
      inject(TraceService);
    })
  ]
};
