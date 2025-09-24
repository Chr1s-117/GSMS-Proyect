// src/app/app.spec.ts

import { TestBed } from '@angular/core/testing';
import { App } from './app';

/**
 * App Test Suite
 *
 * Responsibilities:
 * - Provides baseline automated tests for the root application component.
 * - Ensures that the app initializes correctly and renders the title.
 *
 * Notes:
 * - Default Angular tests are retained as smoke tests.
 * - Recommended to keep as a safety check during development.
 */
describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App], // Import the root App component for testing
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    // Verify that the root component instance is created successfully
    expect(app).toBeTruthy();
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;

    // Verify that the title renders correctly in the DOM
    // Adjust text expectation to match your actual app title
    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, GSMS_FrontEnd');
  });
});
