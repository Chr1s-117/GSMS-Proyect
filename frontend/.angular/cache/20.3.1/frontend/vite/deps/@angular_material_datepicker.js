import {
  MatButton,
  MatButtonModule,
  MatIconButton
} from "./chunk-UELXAEM4.js";
import {
  DateAdapter,
  MAT_DATE_FORMATS
} from "./chunk-SL4WJTP2.js";
import "./chunk-OHTGYQ3W.js";
import "./chunk-UQNEGBTI.js";
import {
  MAT_INPUT_VALUE_ACCESSOR
} from "./chunk-LUC2WYNS.js";
import {
  ErrorStateMatcher,
  _ErrorStateTracker
} from "./chunk-I3J5DV5L.js";
import {
  MAT_FORM_FIELD,
  MatFormFieldControl
} from "./chunk-XPIMXOAB.js";
import "./chunk-55OABCSW.js";
import {
  coerceBooleanProperty,
  coerceStringArray
} from "./chunk-CGUWAHN6.js";
import {
  _StructuralStylesLoader
} from "./chunk-KKUV3KVZ.js";
import {
  _animationsDisabled
} from "./chunk-BGN7QJKV.js";
import {
  A11yModule,
  AriaDescriber,
  CdkMonitorFocus,
  CdkTrapFocus,
  FocusMonitor,
  MatCommonModule,
  _VisuallyHiddenLoader,
  normalizePassiveListenerOptions
} from "./chunk-GXIY53OB.js";
import {
  FlexibleConnectedPositionStrategy,
  OverlayConfig,
  OverlayModule,
  createBlockScrollStrategy,
  createFlexibleConnectedPositionStrategy,
  createGlobalPositionStrategy,
  createOverlayRef,
  createRepositionScrollStrategy
} from "./chunk-SWIM4QTS.js";
import "./chunk-ZGDQ3GWN.js";
import "./chunk-6BKD3BMU.js";
import {
  BACKSPACE,
  DOWN_ARROW,
  END,
  ENTER,
  ESCAPE,
  HOME,
  LEFT_ARROW,
  PAGE_DOWN,
  PAGE_UP,
  RIGHT_ARROW,
  SPACE,
  UP_ARROW,
  _IdGenerator,
  _getFocusedElementPierceShadowDom,
  hasModifierKey
} from "./chunk-D6EGXCKV.js";
import {
  CdkPortalOutlet,
  ComponentPortal,
  PortalModule,
  TemplatePortal
} from "./chunk-TDYT2IWJ.js";
import {
  CdkScrollableModule,
  ScrollDispatcher
} from "./chunk-VBXWXNGP.js";
import "./chunk-HAI453QW.js";
import "./chunk-FTCHFBTZ.js";
import {
  Directionality
} from "./chunk-U5634LHI.js";
import {
  _CdkPrivateStyleLoader
} from "./chunk-3UAARJPV.js";
import {
  Platform,
  coerceNumberProperty
} from "./chunk-I6BOHX6S.js";
import {
  ControlContainer,
  FormGroupDirective,
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  NgControl,
  NgForm,
  Validators
} from "./chunk-V73NHR6L.js";
import {
  NgClass
} from "./chunk-GXOWEAQE.js";
import "./chunk-WMCYXEPE.js";
import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  ContentChild,
  DOCUMENT,
  Directive,
  ElementRef,
  EventEmitter,
  HostAttributeToken,
  Injectable,
  InjectionToken,
  Injector,
  Input,
  NgModule,
  NgZone,
  Optional,
  Output,
  Renderer2,
  SkipSelf,
  TemplateRef,
  ViewChild,
  ViewContainerRef,
  ViewEncapsulation,
  afterNextRender,
  booleanAttribute,
  forwardRef,
  inject,
  setClassMetadata,
  signal,
  ɵɵInheritDefinitionFeature,
  ɵɵNgOnChangesFeature,
  ɵɵProvidersFeature,
  ɵɵadvance,
  ɵɵattribute,
  ɵɵclassMap,
  ɵɵclassProp,
  ɵɵconditional,
  ɵɵconditionalCreate,
  ɵɵcontentQuery,
  ɵɵdefineComponent,
  ɵɵdefineDirective,
  ɵɵdefineInjectable,
  ɵɵdefineInjector,
  ɵɵdefineNgModule,
  ɵɵdomElementEnd,
  ɵɵdomElementStart,
  ɵɵdomProperty,
  ɵɵdomTemplate,
  ɵɵelement,
  ɵɵelementEnd,
  ɵɵelementStart,
  ɵɵgetCurrentView,
  ɵɵgetInheritedFactory,
  ɵɵinject,
  ɵɵinvalidFactory,
  ɵɵlistener,
  ɵɵloadQuery,
  ɵɵnamespaceHTML,
  ɵɵnamespaceSVG,
  ɵɵnextContext,
  ɵɵprojection,
  ɵɵprojectionDef,
  ɵɵproperty,
  ɵɵqueryRefresh,
  ɵɵrepeater,
  ɵɵrepeaterCreate,
  ɵɵresetView,
  ɵɵrestoreView,
  ɵɵstyleProp,
  ɵɵtemplate,
  ɵɵtext,
  ɵɵtextInterpolate,
  ɵɵtextInterpolate1,
  ɵɵtextInterpolate2,
  ɵɵtwoWayBindingSet,
  ɵɵtwoWayListener,
  ɵɵtwoWayProperty,
  ɵɵviewQuery
} from "./chunk-L6HAKNJU.js";
import "./chunk-AHFTOZG5.js";
import {
  merge
} from "./chunk-GR6CC6I7.js";
import {
  filter,
  of,
  startWith,
  take,
  takeUntil
} from "./chunk-YRHOY6S2.js";
import {
  Subject,
  Subscription
} from "./chunk-QQHXZCUH.js";
import {
  __name,
  __publicField,
  __spreadValues
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/material/fesm2022/tooltip2.mjs
var _c0 = ["tooltip"];
var SCROLL_THROTTLE_MS = 20;
function getMatTooltipInvalidPositionError(position) {
  return Error(`Tooltip position "${position}" is invalid.`);
}
__name(getMatTooltipInvalidPositionError, "getMatTooltipInvalidPositionError");
var MAT_TOOLTIP_SCROLL_STRATEGY = new InjectionToken("mat-tooltip-scroll-strategy", {
  providedIn: "root",
  factory: /* @__PURE__ */ __name(() => {
    const injector = inject(Injector);
    return () => createRepositionScrollStrategy(injector, {
      scrollThrottle: SCROLL_THROTTLE_MS
    });
  }, "factory")
});
function MAT_TOOLTIP_DEFAULT_OPTIONS_FACTORY() {
  return {
    showDelay: 0,
    hideDelay: 0,
    touchendHideDelay: 1500
  };
}
__name(MAT_TOOLTIP_DEFAULT_OPTIONS_FACTORY, "MAT_TOOLTIP_DEFAULT_OPTIONS_FACTORY");
var MAT_TOOLTIP_DEFAULT_OPTIONS = new InjectionToken("mat-tooltip-default-options", {
  providedIn: "root",
  factory: MAT_TOOLTIP_DEFAULT_OPTIONS_FACTORY
});
var PANEL_CLASS = "tooltip-panel";
var passiveListenerOptions = normalizePassiveListenerOptions({
  passive: true
});
var MIN_VIEWPORT_TOOLTIP_THRESHOLD = 8;
var UNBOUNDED_ANCHOR_GAP = 8;
var MIN_HEIGHT = 24;
var MAX_WIDTH = 200;
var _MatTooltip = class _MatTooltip {
  _elementRef = inject(ElementRef);
  _ngZone = inject(NgZone);
  _platform = inject(Platform);
  _ariaDescriber = inject(AriaDescriber);
  _focusMonitor = inject(FocusMonitor);
  _dir = inject(Directionality);
  _injector = inject(Injector);
  _viewContainerRef = inject(ViewContainerRef);
  _animationsDisabled = _animationsDisabled();
  _defaultOptions = inject(MAT_TOOLTIP_DEFAULT_OPTIONS, {
    optional: true
  });
  _overlayRef;
  _tooltipInstance;
  _overlayPanelClass;
  // Used for styling internally.
  _portal;
  _position = "below";
  _positionAtOrigin = false;
  _disabled = false;
  _tooltipClass;
  _viewInitialized = false;
  _pointerExitEventsInitialized = false;
  _tooltipComponent = TooltipComponent;
  _viewportMargin = 8;
  _currentPosition;
  _cssClassPrefix = "mat-mdc";
  _ariaDescriptionPending;
  _dirSubscribed = false;
  /** Allows the user to define the position of the tooltip relative to the parent element */
  get position() {
    return this._position;
  }
  set position(value) {
    if (value !== this._position) {
      this._position = value;
      if (this._overlayRef) {
        this._updatePosition(this._overlayRef);
        this._tooltipInstance?.show(0);
        this._overlayRef.updatePosition();
      }
    }
  }
  /**
   * Whether tooltip should be relative to the click or touch origin
   * instead of outside the element bounding box.
   */
  get positionAtOrigin() {
    return this._positionAtOrigin;
  }
  set positionAtOrigin(value) {
    this._positionAtOrigin = coerceBooleanProperty(value);
    this._detach();
    this._overlayRef = null;
  }
  /** Disables the display of the tooltip. */
  get disabled() {
    return this._disabled;
  }
  set disabled(value) {
    const isDisabled = coerceBooleanProperty(value);
    if (this._disabled !== isDisabled) {
      this._disabled = isDisabled;
      if (isDisabled) {
        this.hide(0);
      } else {
        this._setupPointerEnterEventsIfNeeded();
      }
      this._syncAriaDescription(this.message);
    }
  }
  /** The default delay in ms before showing the tooltip after show is called */
  get showDelay() {
    return this._showDelay;
  }
  set showDelay(value) {
    this._showDelay = coerceNumberProperty(value);
  }
  _showDelay;
  /** The default delay in ms before hiding the tooltip after hide is called */
  get hideDelay() {
    return this._hideDelay;
  }
  set hideDelay(value) {
    this._hideDelay = coerceNumberProperty(value);
    if (this._tooltipInstance) {
      this._tooltipInstance._mouseLeaveHideDelay = this._hideDelay;
    }
  }
  _hideDelay;
  /**
   * How touch gestures should be handled by the tooltip. On touch devices the tooltip directive
   * uses a long press gesture to show and hide, however it can conflict with the native browser
   * gestures. To work around the conflict, Angular Material disables native gestures on the
   * trigger, but that might not be desirable on particular elements (e.g. inputs and draggable
   * elements). The different values for this option configure the touch event handling as follows:
   * - `auto` - Enables touch gestures for all elements, but tries to avoid conflicts with native
   *   browser gestures on particular elements. In particular, it allows text selection on inputs
   *   and textareas, and preserves the native browser dragging on elements marked as `draggable`.
   * - `on` - Enables touch gestures for all elements and disables native
   *   browser gestures with no exceptions.
   * - `off` - Disables touch gestures. Note that this will prevent the tooltip from
   *   showing on touch devices.
   */
  touchGestures = "auto";
  /** The message to be displayed in the tooltip */
  get message() {
    return this._message;
  }
  set message(value) {
    const oldMessage = this._message;
    this._message = value != null ? String(value).trim() : "";
    if (!this._message && this._isTooltipVisible()) {
      this.hide(0);
    } else {
      this._setupPointerEnterEventsIfNeeded();
      this._updateTooltipMessage();
    }
    this._syncAriaDescription(oldMessage);
  }
  _message = "";
  /** Classes to be passed to the tooltip. Supports the same syntax as `ngClass`. */
  get tooltipClass() {
    return this._tooltipClass;
  }
  set tooltipClass(value) {
    this._tooltipClass = value;
    if (this._tooltipInstance) {
      this._setTooltipClass(this._tooltipClass);
    }
  }
  /** Manually-bound passive event listeners. */
  _passiveListeners = [];
  /** Timer started at the last `touchstart` event. */
  _touchstartTimeout = null;
  /** Emits when the component is destroyed. */
  _destroyed = new Subject();
  /** Whether ngOnDestroyed has been called. */
  _isDestroyed = false;
  constructor() {
    const defaultOptions = this._defaultOptions;
    if (defaultOptions) {
      this._showDelay = defaultOptions.showDelay;
      this._hideDelay = defaultOptions.hideDelay;
      if (defaultOptions.position) {
        this.position = defaultOptions.position;
      }
      if (defaultOptions.positionAtOrigin) {
        this.positionAtOrigin = defaultOptions.positionAtOrigin;
      }
      if (defaultOptions.touchGestures) {
        this.touchGestures = defaultOptions.touchGestures;
      }
      if (defaultOptions.tooltipClass) {
        this.tooltipClass = defaultOptions.tooltipClass;
      }
    }
    this._viewportMargin = MIN_VIEWPORT_TOOLTIP_THRESHOLD;
  }
  ngAfterViewInit() {
    this._viewInitialized = true;
    this._setupPointerEnterEventsIfNeeded();
    this._focusMonitor.monitor(this._elementRef).pipe(takeUntil(this._destroyed)).subscribe((origin) => {
      if (!origin) {
        this._ngZone.run(() => this.hide(0));
      } else if (origin === "keyboard") {
        this._ngZone.run(() => this.show());
      }
    });
  }
  /**
   * Dispose the tooltip when destroyed.
   */
  ngOnDestroy() {
    const nativeElement = this._elementRef.nativeElement;
    if (this._touchstartTimeout) {
      clearTimeout(this._touchstartTimeout);
    }
    if (this._overlayRef) {
      this._overlayRef.dispose();
      this._tooltipInstance = null;
    }
    this._passiveListeners.forEach(([event, listener]) => {
      nativeElement.removeEventListener(event, listener, passiveListenerOptions);
    });
    this._passiveListeners.length = 0;
    this._destroyed.next();
    this._destroyed.complete();
    this._isDestroyed = true;
    this._ariaDescriber.removeDescription(nativeElement, this.message, "tooltip");
    this._focusMonitor.stopMonitoring(nativeElement);
  }
  /** Shows the tooltip after the delay in ms, defaults to tooltip-delay-show or 0ms if no input */
  show(delay = this.showDelay, origin) {
    if (this.disabled || !this.message || this._isTooltipVisible()) {
      this._tooltipInstance?._cancelPendingAnimations();
      return;
    }
    const overlayRef = this._createOverlay(origin);
    this._detach();
    this._portal = this._portal || new ComponentPortal(this._tooltipComponent, this._viewContainerRef);
    const instance = this._tooltipInstance = overlayRef.attach(this._portal).instance;
    instance._triggerElement = this._elementRef.nativeElement;
    instance._mouseLeaveHideDelay = this._hideDelay;
    instance.afterHidden().pipe(takeUntil(this._destroyed)).subscribe(() => this._detach());
    this._setTooltipClass(this._tooltipClass);
    this._updateTooltipMessage();
    instance.show(delay);
  }
  /** Hides the tooltip after the delay in ms, defaults to tooltip-delay-hide or 0ms if no input */
  hide(delay = this.hideDelay) {
    const instance = this._tooltipInstance;
    if (instance) {
      if (instance.isVisible()) {
        instance.hide(delay);
      } else {
        instance._cancelPendingAnimations();
        this._detach();
      }
    }
  }
  /** Shows/hides the tooltip */
  toggle(origin) {
    this._isTooltipVisible() ? this.hide() : this.show(void 0, origin);
  }
  /** Returns true if the tooltip is currently visible to the user */
  _isTooltipVisible() {
    return !!this._tooltipInstance && this._tooltipInstance.isVisible();
  }
  /** Create the overlay config and position strategy */
  _createOverlay(origin) {
    if (this._overlayRef) {
      const existingStrategy = this._overlayRef.getConfig().positionStrategy;
      if ((!this.positionAtOrigin || !origin) && existingStrategy._origin instanceof ElementRef) {
        return this._overlayRef;
      }
      this._detach();
    }
    const scrollableAncestors = this._injector.get(ScrollDispatcher).getAncestorScrollContainers(this._elementRef);
    const panelClass = `${this._cssClassPrefix}-${PANEL_CLASS}`;
    const strategy = createFlexibleConnectedPositionStrategy(this._injector, this.positionAtOrigin ? origin || this._elementRef : this._elementRef).withTransformOriginOn(`.${this._cssClassPrefix}-tooltip`).withFlexibleDimensions(false).withViewportMargin(this._viewportMargin).withScrollableContainers(scrollableAncestors);
    strategy.positionChanges.pipe(takeUntil(this._destroyed)).subscribe((change) => {
      this._updateCurrentPositionClass(change.connectionPair);
      if (this._tooltipInstance) {
        if (change.scrollableViewProperties.isOverlayClipped && this._tooltipInstance.isVisible()) {
          this._ngZone.run(() => this.hide(0));
        }
      }
    });
    this._overlayRef = createOverlayRef(this._injector, {
      direction: this._dir,
      positionStrategy: strategy,
      panelClass: this._overlayPanelClass ? [...this._overlayPanelClass, panelClass] : panelClass,
      scrollStrategy: this._injector.get(MAT_TOOLTIP_SCROLL_STRATEGY)(),
      disableAnimations: this._animationsDisabled
    });
    this._updatePosition(this._overlayRef);
    this._overlayRef.detachments().pipe(takeUntil(this._destroyed)).subscribe(() => this._detach());
    this._overlayRef.outsidePointerEvents().pipe(takeUntil(this._destroyed)).subscribe(() => this._tooltipInstance?._handleBodyInteraction());
    this._overlayRef.keydownEvents().pipe(takeUntil(this._destroyed)).subscribe((event) => {
      if (this._isTooltipVisible() && event.keyCode === ESCAPE && !hasModifierKey(event)) {
        event.preventDefault();
        event.stopPropagation();
        this._ngZone.run(() => this.hide(0));
      }
    });
    if (this._defaultOptions?.disableTooltipInteractivity) {
      this._overlayRef.addPanelClass(`${this._cssClassPrefix}-tooltip-panel-non-interactive`);
    }
    if (!this._dirSubscribed) {
      this._dirSubscribed = true;
      this._dir.change.pipe(takeUntil(this._destroyed)).subscribe(() => {
        if (this._overlayRef) {
          this._updatePosition(this._overlayRef);
        }
      });
    }
    return this._overlayRef;
  }
  /** Detaches the currently-attached tooltip. */
  _detach() {
    if (this._overlayRef && this._overlayRef.hasAttached()) {
      this._overlayRef.detach();
    }
    this._tooltipInstance = null;
  }
  /** Updates the position of the current tooltip. */
  _updatePosition(overlayRef) {
    const position = overlayRef.getConfig().positionStrategy;
    const origin = this._getOrigin();
    const overlay = this._getOverlayPosition();
    position.withPositions([this._addOffset(__spreadValues(__spreadValues({}, origin.main), overlay.main)), this._addOffset(__spreadValues(__spreadValues({}, origin.fallback), overlay.fallback))]);
  }
  /** Adds the configured offset to a position. Used as a hook for child classes. */
  _addOffset(position) {
    const offset = UNBOUNDED_ANCHOR_GAP;
    const isLtr = !this._dir || this._dir.value == "ltr";
    if (position.originY === "top") {
      position.offsetY = -offset;
    } else if (position.originY === "bottom") {
      position.offsetY = offset;
    } else if (position.originX === "start") {
      position.offsetX = isLtr ? -offset : offset;
    } else if (position.originX === "end") {
      position.offsetX = isLtr ? offset : -offset;
    }
    return position;
  }
  /**
   * Returns the origin position and a fallback position based on the user's position preference.
   * The fallback position is the inverse of the origin (e.g. `'below' -> 'above'`).
   */
  _getOrigin() {
    const isLtr = !this._dir || this._dir.value == "ltr";
    const position = this.position;
    let originPosition;
    if (position == "above" || position == "below") {
      originPosition = {
        originX: "center",
        originY: position == "above" ? "top" : "bottom"
      };
    } else if (position == "before" || position == "left" && isLtr || position == "right" && !isLtr) {
      originPosition = {
        originX: "start",
        originY: "center"
      };
    } else if (position == "after" || position == "right" && isLtr || position == "left" && !isLtr) {
      originPosition = {
        originX: "end",
        originY: "center"
      };
    } else if (typeof ngDevMode === "undefined" || ngDevMode) {
      throw getMatTooltipInvalidPositionError(position);
    }
    const {
      x,
      y
    } = this._invertPosition(originPosition.originX, originPosition.originY);
    return {
      main: originPosition,
      fallback: {
        originX: x,
        originY: y
      }
    };
  }
  /** Returns the overlay position and a fallback position based on the user's preference */
  _getOverlayPosition() {
    const isLtr = !this._dir || this._dir.value == "ltr";
    const position = this.position;
    let overlayPosition;
    if (position == "above") {
      overlayPosition = {
        overlayX: "center",
        overlayY: "bottom"
      };
    } else if (position == "below") {
      overlayPosition = {
        overlayX: "center",
        overlayY: "top"
      };
    } else if (position == "before" || position == "left" && isLtr || position == "right" && !isLtr) {
      overlayPosition = {
        overlayX: "end",
        overlayY: "center"
      };
    } else if (position == "after" || position == "right" && isLtr || position == "left" && !isLtr) {
      overlayPosition = {
        overlayX: "start",
        overlayY: "center"
      };
    } else if (typeof ngDevMode === "undefined" || ngDevMode) {
      throw getMatTooltipInvalidPositionError(position);
    }
    const {
      x,
      y
    } = this._invertPosition(overlayPosition.overlayX, overlayPosition.overlayY);
    return {
      main: overlayPosition,
      fallback: {
        overlayX: x,
        overlayY: y
      }
    };
  }
  /** Updates the tooltip message and repositions the overlay according to the new message length */
  _updateTooltipMessage() {
    if (this._tooltipInstance) {
      this._tooltipInstance.message = this.message;
      this._tooltipInstance._markForCheck();
      afterNextRender(() => {
        if (this._tooltipInstance) {
          this._overlayRef.updatePosition();
        }
      }, {
        injector: this._injector
      });
    }
  }
  /** Updates the tooltip class */
  _setTooltipClass(tooltipClass) {
    if (this._tooltipInstance) {
      this._tooltipInstance.tooltipClass = tooltipClass;
      this._tooltipInstance._markForCheck();
    }
  }
  /** Inverts an overlay position. */
  _invertPosition(x, y) {
    if (this.position === "above" || this.position === "below") {
      if (y === "top") {
        y = "bottom";
      } else if (y === "bottom") {
        y = "top";
      }
    } else {
      if (x === "end") {
        x = "start";
      } else if (x === "start") {
        x = "end";
      }
    }
    return {
      x,
      y
    };
  }
  /** Updates the class on the overlay panel based on the current position of the tooltip. */
  _updateCurrentPositionClass(connectionPair) {
    const {
      overlayY,
      originX,
      originY
    } = connectionPair;
    let newPosition;
    if (overlayY === "center") {
      if (this._dir && this._dir.value === "rtl") {
        newPosition = originX === "end" ? "left" : "right";
      } else {
        newPosition = originX === "start" ? "left" : "right";
      }
    } else {
      newPosition = overlayY === "bottom" && originY === "top" ? "above" : "below";
    }
    if (newPosition !== this._currentPosition) {
      const overlayRef = this._overlayRef;
      if (overlayRef) {
        const classPrefix = `${this._cssClassPrefix}-${PANEL_CLASS}-`;
        overlayRef.removePanelClass(classPrefix + this._currentPosition);
        overlayRef.addPanelClass(classPrefix + newPosition);
      }
      this._currentPosition = newPosition;
    }
  }
  /** Binds the pointer events to the tooltip trigger. */
  _setupPointerEnterEventsIfNeeded() {
    if (this._disabled || !this.message || !this._viewInitialized || this._passiveListeners.length) {
      return;
    }
    if (this._platformSupportsMouseEvents()) {
      this._passiveListeners.push(["mouseenter", (event) => {
        this._setupPointerExitEventsIfNeeded();
        let point = void 0;
        if (event.x !== void 0 && event.y !== void 0) {
          point = event;
        }
        this.show(void 0, point);
      }]);
    } else if (this.touchGestures !== "off") {
      this._disableNativeGesturesIfNecessary();
      this._passiveListeners.push(["touchstart", (event) => {
        const touch = event.targetTouches?.[0];
        const origin = touch ? {
          x: touch.clientX,
          y: touch.clientY
        } : void 0;
        this._setupPointerExitEventsIfNeeded();
        if (this._touchstartTimeout) {
          clearTimeout(this._touchstartTimeout);
        }
        const DEFAULT_LONGPRESS_DELAY = 500;
        this._touchstartTimeout = setTimeout(() => {
          this._touchstartTimeout = null;
          this.show(void 0, origin);
        }, this._defaultOptions?.touchLongPressShowDelay ?? DEFAULT_LONGPRESS_DELAY);
      }]);
    }
    this._addListeners(this._passiveListeners);
  }
  _setupPointerExitEventsIfNeeded() {
    if (this._pointerExitEventsInitialized) {
      return;
    }
    this._pointerExitEventsInitialized = true;
    const exitListeners = [];
    if (this._platformSupportsMouseEvents()) {
      exitListeners.push(["mouseleave", (event) => {
        const newTarget = event.relatedTarget;
        if (!newTarget || !this._overlayRef?.overlayElement.contains(newTarget)) {
          this.hide();
        }
      }], ["wheel", (event) => this._wheelListener(event)]);
    } else if (this.touchGestures !== "off") {
      this._disableNativeGesturesIfNecessary();
      const touchendListener = /* @__PURE__ */ __name(() => {
        if (this._touchstartTimeout) {
          clearTimeout(this._touchstartTimeout);
        }
        this.hide(this._defaultOptions?.touchendHideDelay);
      }, "touchendListener");
      exitListeners.push(["touchend", touchendListener], ["touchcancel", touchendListener]);
    }
    this._addListeners(exitListeners);
    this._passiveListeners.push(...exitListeners);
  }
  _addListeners(listeners) {
    listeners.forEach(([event, listener]) => {
      this._elementRef.nativeElement.addEventListener(event, listener, passiveListenerOptions);
    });
  }
  _platformSupportsMouseEvents() {
    return !this._platform.IOS && !this._platform.ANDROID;
  }
  /** Listener for the `wheel` event on the element. */
  _wheelListener(event) {
    if (this._isTooltipVisible()) {
      const elementUnderPointer = this._injector.get(DOCUMENT).elementFromPoint(event.clientX, event.clientY);
      const element = this._elementRef.nativeElement;
      if (elementUnderPointer !== element && !element.contains(elementUnderPointer)) {
        this.hide();
      }
    }
  }
  /** Disables the native browser gestures, based on how the tooltip has been configured. */
  _disableNativeGesturesIfNecessary() {
    const gestures = this.touchGestures;
    if (gestures !== "off") {
      const element = this._elementRef.nativeElement;
      const style = element.style;
      if (gestures === "on" || element.nodeName !== "INPUT" && element.nodeName !== "TEXTAREA") {
        style.userSelect = style.msUserSelect = style.webkitUserSelect = style.MozUserSelect = "none";
      }
      if (gestures === "on" || !element.draggable) {
        style.webkitUserDrag = "none";
      }
      style.touchAction = "none";
      style.webkitTapHighlightColor = "transparent";
    }
  }
  /** Updates the tooltip's ARIA description based on it current state. */
  _syncAriaDescription(oldMessage) {
    if (this._ariaDescriptionPending) {
      return;
    }
    this._ariaDescriptionPending = true;
    this._ariaDescriber.removeDescription(this._elementRef.nativeElement, oldMessage, "tooltip");
    if (!this._isDestroyed) {
      afterNextRender({
        write: /* @__PURE__ */ __name(() => {
          this._ariaDescriptionPending = false;
          if (this.message && !this.disabled) {
            this._ariaDescriber.describe(this._elementRef.nativeElement, this.message, "tooltip");
          }
        }, "write")
      }, {
        injector: this._injector
      });
    }
  }
};
__name(_MatTooltip, "MatTooltip");
__publicField(_MatTooltip, "ɵfac", /* @__PURE__ */ __name(function MatTooltip_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatTooltip)();
}, "MatTooltip_Factory"));
__publicField(_MatTooltip, "ɵdir", ɵɵdefineDirective({
  type: _MatTooltip,
  selectors: [["", "matTooltip", ""]],
  hostAttrs: [1, "mat-mdc-tooltip-trigger"],
  hostVars: 2,
  hostBindings: /* @__PURE__ */ __name(function MatTooltip_HostBindings(rf, ctx) {
    if (rf & 2) {
      ɵɵclassProp("mat-mdc-tooltip-disabled", ctx.disabled);
    }
  }, "MatTooltip_HostBindings"),
  inputs: {
    position: [0, "matTooltipPosition", "position"],
    positionAtOrigin: [0, "matTooltipPositionAtOrigin", "positionAtOrigin"],
    disabled: [0, "matTooltipDisabled", "disabled"],
    showDelay: [0, "matTooltipShowDelay", "showDelay"],
    hideDelay: [0, "matTooltipHideDelay", "hideDelay"],
    touchGestures: [0, "matTooltipTouchGestures", "touchGestures"],
    message: [0, "matTooltip", "message"],
    tooltipClass: [0, "matTooltipClass", "tooltipClass"]
  },
  exportAs: ["matTooltip"]
}));
var MatTooltip = _MatTooltip;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatTooltip, [{
    type: Directive,
    args: [{
      selector: "[matTooltip]",
      exportAs: "matTooltip",
      host: {
        "class": "mat-mdc-tooltip-trigger",
        "[class.mat-mdc-tooltip-disabled]": "disabled"
      }
    }]
  }], () => [], {
    position: [{
      type: Input,
      args: ["matTooltipPosition"]
    }],
    positionAtOrigin: [{
      type: Input,
      args: ["matTooltipPositionAtOrigin"]
    }],
    disabled: [{
      type: Input,
      args: ["matTooltipDisabled"]
    }],
    showDelay: [{
      type: Input,
      args: ["matTooltipShowDelay"]
    }],
    hideDelay: [{
      type: Input,
      args: ["matTooltipHideDelay"]
    }],
    touchGestures: [{
      type: Input,
      args: ["matTooltipTouchGestures"]
    }],
    message: [{
      type: Input,
      args: ["matTooltip"]
    }],
    tooltipClass: [{
      type: Input,
      args: ["matTooltipClass"]
    }]
  });
})();
var _TooltipComponent = class _TooltipComponent {
  _changeDetectorRef = inject(ChangeDetectorRef);
  _elementRef = inject(ElementRef);
  /* Whether the tooltip text overflows to multiple lines */
  _isMultiline = false;
  /** Message to display in the tooltip */
  message;
  /** Classes to be added to the tooltip. Supports the same syntax as `ngClass`. */
  tooltipClass;
  /** The timeout ID of any current timer set to show the tooltip */
  _showTimeoutId;
  /** The timeout ID of any current timer set to hide the tooltip */
  _hideTimeoutId;
  /** Element that caused the tooltip to open. */
  _triggerElement;
  /** Amount of milliseconds to delay the closing sequence. */
  _mouseLeaveHideDelay;
  /** Whether animations are currently disabled. */
  _animationsDisabled = _animationsDisabled();
  /** Reference to the internal tooltip element. */
  _tooltip;
  /** Whether interactions on the page should close the tooltip */
  _closeOnInteraction = false;
  /** Whether the tooltip is currently visible. */
  _isVisible = false;
  /** Subject for notifying that the tooltip has been hidden from the view */
  _onHide = new Subject();
  /** Name of the show animation and the class that toggles it. */
  _showAnimation = "mat-mdc-tooltip-show";
  /** Name of the hide animation and the class that toggles it. */
  _hideAnimation = "mat-mdc-tooltip-hide";
  constructor() {
  }
  /**
   * Shows the tooltip with an animation originating from the provided origin
   * @param delay Amount of milliseconds to the delay showing the tooltip.
   */
  show(delay) {
    if (this._hideTimeoutId != null) {
      clearTimeout(this._hideTimeoutId);
    }
    this._showTimeoutId = setTimeout(() => {
      this._toggleVisibility(true);
      this._showTimeoutId = void 0;
    }, delay);
  }
  /**
   * Begins the animation to hide the tooltip after the provided delay in ms.
   * @param delay Amount of milliseconds to delay showing the tooltip.
   */
  hide(delay) {
    if (this._showTimeoutId != null) {
      clearTimeout(this._showTimeoutId);
    }
    this._hideTimeoutId = setTimeout(() => {
      this._toggleVisibility(false);
      this._hideTimeoutId = void 0;
    }, delay);
  }
  /** Returns an observable that notifies when the tooltip has been hidden from view. */
  afterHidden() {
    return this._onHide;
  }
  /** Whether the tooltip is being displayed. */
  isVisible() {
    return this._isVisible;
  }
  ngOnDestroy() {
    this._cancelPendingAnimations();
    this._onHide.complete();
    this._triggerElement = null;
  }
  /**
   * Interactions on the HTML body should close the tooltip immediately as defined in the
   * material design spec.
   * https://material.io/design/components/tooltips.html#behavior
   */
  _handleBodyInteraction() {
    if (this._closeOnInteraction) {
      this.hide(0);
    }
  }
  /**
   * Marks that the tooltip needs to be checked in the next change detection run.
   * Mainly used for rendering the initial text before positioning a tooltip, which
   * can be problematic in components with OnPush change detection.
   */
  _markForCheck() {
    this._changeDetectorRef.markForCheck();
  }
  _handleMouseLeave({
    relatedTarget
  }) {
    if (!relatedTarget || !this._triggerElement.contains(relatedTarget)) {
      if (this.isVisible()) {
        this.hide(this._mouseLeaveHideDelay);
      } else {
        this._finalizeAnimation(false);
      }
    }
  }
  /**
   * Callback for when the timeout in this.show() gets completed.
   * This method is only needed by the mdc-tooltip, and so it is only implemented
   * in the mdc-tooltip, not here.
   */
  _onShow() {
    this._isMultiline = this._isTooltipMultiline();
    this._markForCheck();
  }
  /** Whether the tooltip text has overflown to the next line */
  _isTooltipMultiline() {
    const rect = this._elementRef.nativeElement.getBoundingClientRect();
    return rect.height > MIN_HEIGHT && rect.width >= MAX_WIDTH;
  }
  /** Event listener dispatched when an animation on the tooltip finishes. */
  _handleAnimationEnd({
    animationName
  }) {
    if (animationName === this._showAnimation || animationName === this._hideAnimation) {
      this._finalizeAnimation(animationName === this._showAnimation);
    }
  }
  /** Cancels any pending animation sequences. */
  _cancelPendingAnimations() {
    if (this._showTimeoutId != null) {
      clearTimeout(this._showTimeoutId);
    }
    if (this._hideTimeoutId != null) {
      clearTimeout(this._hideTimeoutId);
    }
    this._showTimeoutId = this._hideTimeoutId = void 0;
  }
  /** Handles the cleanup after an animation has finished. */
  _finalizeAnimation(toVisible) {
    if (toVisible) {
      this._closeOnInteraction = true;
    } else if (!this.isVisible()) {
      this._onHide.next();
    }
  }
  /** Toggles the visibility of the tooltip element. */
  _toggleVisibility(isVisible) {
    const tooltip = this._tooltip.nativeElement;
    const showClass = this._showAnimation;
    const hideClass = this._hideAnimation;
    tooltip.classList.remove(isVisible ? hideClass : showClass);
    tooltip.classList.add(isVisible ? showClass : hideClass);
    if (this._isVisible !== isVisible) {
      this._isVisible = isVisible;
      this._changeDetectorRef.markForCheck();
    }
    if (isVisible && !this._animationsDisabled && typeof getComputedStyle === "function") {
      const styles = getComputedStyle(tooltip);
      if (styles.getPropertyValue("animation-duration") === "0s" || styles.getPropertyValue("animation-name") === "none") {
        this._animationsDisabled = true;
      }
    }
    if (isVisible) {
      this._onShow();
    }
    if (this._animationsDisabled) {
      tooltip.classList.add("_mat-animation-noopable");
      this._finalizeAnimation(isVisible);
    }
  }
};
__name(_TooltipComponent, "TooltipComponent");
__publicField(_TooltipComponent, "ɵfac", /* @__PURE__ */ __name(function TooltipComponent_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _TooltipComponent)();
}, "TooltipComponent_Factory"));
__publicField(_TooltipComponent, "ɵcmp", ɵɵdefineComponent({
  type: _TooltipComponent,
  selectors: [["mat-tooltip-component"]],
  viewQuery: /* @__PURE__ */ __name(function TooltipComponent_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(_c0, 7);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._tooltip = _t.first);
    }
  }, "TooltipComponent_Query"),
  hostAttrs: ["aria-hidden", "true"],
  hostBindings: /* @__PURE__ */ __name(function TooltipComponent_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("mouseleave", /* @__PURE__ */ __name(function TooltipComponent_mouseleave_HostBindingHandler($event) {
        return ctx._handleMouseLeave($event);
      }, "TooltipComponent_mouseleave_HostBindingHandler"));
    }
  }, "TooltipComponent_HostBindings"),
  decls: 4,
  vars: 4,
  consts: [["tooltip", ""], [1, "mdc-tooltip", "mat-mdc-tooltip", 3, "animationend", "ngClass"], [1, "mat-mdc-tooltip-surface", "mdc-tooltip__surface"]],
  template: /* @__PURE__ */ __name(function TooltipComponent_Template(rf, ctx) {
    if (rf & 1) {
      const _r1 = ɵɵgetCurrentView();
      ɵɵelementStart(0, "div", 1, 0);
      ɵɵlistener("animationend", /* @__PURE__ */ __name(function TooltipComponent_Template_div_animationend_0_listener($event) {
        ɵɵrestoreView(_r1);
        return ɵɵresetView(ctx._handleAnimationEnd($event));
      }, "TooltipComponent_Template_div_animationend_0_listener"));
      ɵɵelementStart(2, "div", 2);
      ɵɵtext(3);
      ɵɵelementEnd()();
    }
    if (rf & 2) {
      ɵɵclassProp("mdc-tooltip--multiline", ctx._isMultiline);
      ɵɵproperty("ngClass", ctx.tooltipClass);
      ɵɵadvance(3);
      ɵɵtextInterpolate(ctx.message);
    }
  }, "TooltipComponent_Template"),
  dependencies: [NgClass],
  styles: ['.mat-mdc-tooltip{position:relative;transform:scale(0);display:inline-flex}.mat-mdc-tooltip::before{content:"";top:0;right:0;bottom:0;left:0;z-index:-1;position:absolute}.mat-mdc-tooltip-panel-below .mat-mdc-tooltip::before{top:-8px}.mat-mdc-tooltip-panel-above .mat-mdc-tooltip::before{bottom:-8px}.mat-mdc-tooltip-panel-right .mat-mdc-tooltip::before{left:-8px}.mat-mdc-tooltip-panel-left .mat-mdc-tooltip::before{right:-8px}.mat-mdc-tooltip._mat-animation-noopable{animation:none;transform:scale(1)}.mat-mdc-tooltip-surface{word-break:normal;overflow-wrap:anywhere;padding:4px 8px;min-width:40px;max-width:200px;min-height:24px;max-height:40vh;box-sizing:border-box;overflow:hidden;text-align:center;will-change:transform,opacity;background-color:var(--mat-tooltip-container-color, var(--mat-sys-inverse-surface));color:var(--mat-tooltip-supporting-text-color, var(--mat-sys-inverse-on-surface));border-radius:var(--mat-tooltip-container-shape, var(--mat-sys-corner-extra-small));font-family:var(--mat-tooltip-supporting-text-font, var(--mat-sys-body-small-font));font-size:var(--mat-tooltip-supporting-text-size, var(--mat-sys-body-small-size));font-weight:var(--mat-tooltip-supporting-text-weight, var(--mat-sys-body-small-weight));line-height:var(--mat-tooltip-supporting-text-line-height, var(--mat-sys-body-small-line-height));letter-spacing:var(--mat-tooltip-supporting-text-tracking, var(--mat-sys-body-small-tracking))}.mat-mdc-tooltip-surface::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid rgba(0,0,0,0);border-radius:inherit;content:"";pointer-events:none}.mdc-tooltip--multiline .mat-mdc-tooltip-surface{text-align:left}[dir=rtl] .mdc-tooltip--multiline .mat-mdc-tooltip-surface{text-align:right}.mat-mdc-tooltip-panel{line-height:normal}.mat-mdc-tooltip-panel.mat-mdc-tooltip-panel-non-interactive{pointer-events:none}@keyframes mat-mdc-tooltip-show{0%{opacity:0;transform:scale(0.8)}100%{opacity:1;transform:scale(1)}}@keyframes mat-mdc-tooltip-hide{0%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(0.8)}}.mat-mdc-tooltip-show{animation:mat-mdc-tooltip-show 150ms cubic-bezier(0, 0, 0.2, 1) forwards}.mat-mdc-tooltip-hide{animation:mat-mdc-tooltip-hide 75ms cubic-bezier(0.4, 0, 1, 1) forwards}\n'],
  encapsulation: 2,
  changeDetection: 0
}));
var TooltipComponent = _TooltipComponent;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(TooltipComponent, [{
    type: Component,
    args: [{
      selector: "mat-tooltip-component",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      host: {
        "(mouseleave)": "_handleMouseLeave($event)",
        "aria-hidden": "true"
      },
      imports: [NgClass],
      template: '<div\n  #tooltip\n  class="mdc-tooltip mat-mdc-tooltip"\n  [ngClass]="tooltipClass"\n  (animationend)="_handleAnimationEnd($event)"\n  [class.mdc-tooltip--multiline]="_isMultiline">\n  <div class="mat-mdc-tooltip-surface mdc-tooltip__surface">{{message}}</div>\n</div>\n',
      styles: ['.mat-mdc-tooltip{position:relative;transform:scale(0);display:inline-flex}.mat-mdc-tooltip::before{content:"";top:0;right:0;bottom:0;left:0;z-index:-1;position:absolute}.mat-mdc-tooltip-panel-below .mat-mdc-tooltip::before{top:-8px}.mat-mdc-tooltip-panel-above .mat-mdc-tooltip::before{bottom:-8px}.mat-mdc-tooltip-panel-right .mat-mdc-tooltip::before{left:-8px}.mat-mdc-tooltip-panel-left .mat-mdc-tooltip::before{right:-8px}.mat-mdc-tooltip._mat-animation-noopable{animation:none;transform:scale(1)}.mat-mdc-tooltip-surface{word-break:normal;overflow-wrap:anywhere;padding:4px 8px;min-width:40px;max-width:200px;min-height:24px;max-height:40vh;box-sizing:border-box;overflow:hidden;text-align:center;will-change:transform,opacity;background-color:var(--mat-tooltip-container-color, var(--mat-sys-inverse-surface));color:var(--mat-tooltip-supporting-text-color, var(--mat-sys-inverse-on-surface));border-radius:var(--mat-tooltip-container-shape, var(--mat-sys-corner-extra-small));font-family:var(--mat-tooltip-supporting-text-font, var(--mat-sys-body-small-font));font-size:var(--mat-tooltip-supporting-text-size, var(--mat-sys-body-small-size));font-weight:var(--mat-tooltip-supporting-text-weight, var(--mat-sys-body-small-weight));line-height:var(--mat-tooltip-supporting-text-line-height, var(--mat-sys-body-small-line-height));letter-spacing:var(--mat-tooltip-supporting-text-tracking, var(--mat-sys-body-small-tracking))}.mat-mdc-tooltip-surface::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid rgba(0,0,0,0);border-radius:inherit;content:"";pointer-events:none}.mdc-tooltip--multiline .mat-mdc-tooltip-surface{text-align:left}[dir=rtl] .mdc-tooltip--multiline .mat-mdc-tooltip-surface{text-align:right}.mat-mdc-tooltip-panel{line-height:normal}.mat-mdc-tooltip-panel.mat-mdc-tooltip-panel-non-interactive{pointer-events:none}@keyframes mat-mdc-tooltip-show{0%{opacity:0;transform:scale(0.8)}100%{opacity:1;transform:scale(1)}}@keyframes mat-mdc-tooltip-hide{0%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(0.8)}}.mat-mdc-tooltip-show{animation:mat-mdc-tooltip-show 150ms cubic-bezier(0, 0, 0.2, 1) forwards}.mat-mdc-tooltip-hide{animation:mat-mdc-tooltip-hide 75ms cubic-bezier(0.4, 0, 1, 1) forwards}\n']
    }]
  }], () => [], {
    _tooltip: [{
      type: ViewChild,
      args: ["tooltip", {
        // Use a static query here since we interact directly with
        // the DOM which can happen before `ngAfterViewInit`.
        static: true
      }]
    }]
  });
})();

// node_modules/@angular/material/fesm2022/datepicker.mjs
var _c02 = ["mat-calendar-body", ""];
function _forTrack0($index, $item) {
  return this._trackRow($item);
}
__name(_forTrack0, "_forTrack0");
var _forTrack1 = /* @__PURE__ */ __name(($index, $item) => $item.id, "_forTrack1");
function MatCalendarBody_Conditional_0_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵelementStart(0, "tr", 0)(1, "td", 3);
    ɵɵtext(2);
    ɵɵelementEnd()();
  }
  if (rf & 2) {
    const ctx_r0 = ɵɵnextContext();
    ɵɵadvance();
    ɵɵstyleProp("padding-top", ctx_r0._cellPadding)("padding-bottom", ctx_r0._cellPadding);
    ɵɵattribute("colspan", ctx_r0.numCols);
    ɵɵadvance();
    ɵɵtextInterpolate1(" ", ctx_r0.label, " ");
  }
}
__name(MatCalendarBody_Conditional_0_Template, "MatCalendarBody_Conditional_0_Template");
function MatCalendarBody_For_2_Conditional_1_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵelementStart(0, "td", 3);
    ɵɵtext(1);
    ɵɵelementEnd();
  }
  if (rf & 2) {
    const ctx_r0 = ɵɵnextContext(2);
    ɵɵstyleProp("padding-top", ctx_r0._cellPadding)("padding-bottom", ctx_r0._cellPadding);
    ɵɵattribute("colspan", ctx_r0._firstRowOffset);
    ɵɵadvance();
    ɵɵtextInterpolate1(" ", ctx_r0._firstRowOffset >= ctx_r0.labelMinRequiredCells ? ctx_r0.label : "", " ");
  }
}
__name(MatCalendarBody_For_2_Conditional_1_Template, "MatCalendarBody_For_2_Conditional_1_Template");
function MatCalendarBody_For_2_For_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r2 = ɵɵgetCurrentView();
    ɵɵelementStart(0, "td", 6)(1, "button", 7);
    ɵɵlistener("click", /* @__PURE__ */ __name(function MatCalendarBody_For_2_For_3_Template_button_click_1_listener($event) {
      const item_r3 = ɵɵrestoreView(_r2).$implicit;
      const ctx_r0 = ɵɵnextContext(2);
      return ɵɵresetView(ctx_r0._cellClicked(item_r3, $event));
    }, "MatCalendarBody_For_2_For_3_Template_button_click_1_listener"))("focus", /* @__PURE__ */ __name(function MatCalendarBody_For_2_For_3_Template_button_focus_1_listener($event) {
      const item_r3 = ɵɵrestoreView(_r2).$implicit;
      const ctx_r0 = ɵɵnextContext(2);
      return ɵɵresetView(ctx_r0._emitActiveDateChange(item_r3, $event));
    }, "MatCalendarBody_For_2_For_3_Template_button_focus_1_listener"));
    ɵɵelementStart(2, "span", 8);
    ɵɵtext(3);
    ɵɵelementEnd();
    ɵɵelement(4, "span", 9);
    ɵɵelementEnd()();
  }
  if (rf & 2) {
    const item_r3 = ctx.$implicit;
    const ɵ$index_14_r4 = ctx.$index;
    const ɵ$index_7_r5 = ɵɵnextContext().$index;
    const ctx_r0 = ɵɵnextContext();
    ɵɵstyleProp("width", ctx_r0._cellWidth)("padding-top", ctx_r0._cellPadding)("padding-bottom", ctx_r0._cellPadding);
    ɵɵattribute("data-mat-row", ɵ$index_7_r5)("data-mat-col", ɵ$index_14_r4);
    ɵɵadvance();
    ɵɵclassProp("mat-calendar-body-disabled", !item_r3.enabled)("mat-calendar-body-active", ctx_r0._isActiveCell(ɵ$index_7_r5, ɵ$index_14_r4))("mat-calendar-body-range-start", ctx_r0._isRangeStart(item_r3.compareValue))("mat-calendar-body-range-end", ctx_r0._isRangeEnd(item_r3.compareValue))("mat-calendar-body-in-range", ctx_r0._isInRange(item_r3.compareValue))("mat-calendar-body-comparison-bridge-start", ctx_r0._isComparisonBridgeStart(item_r3.compareValue, ɵ$index_7_r5, ɵ$index_14_r4))("mat-calendar-body-comparison-bridge-end", ctx_r0._isComparisonBridgeEnd(item_r3.compareValue, ɵ$index_7_r5, ɵ$index_14_r4))("mat-calendar-body-comparison-start", ctx_r0._isComparisonStart(item_r3.compareValue))("mat-calendar-body-comparison-end", ctx_r0._isComparisonEnd(item_r3.compareValue))("mat-calendar-body-in-comparison-range", ctx_r0._isInComparisonRange(item_r3.compareValue))("mat-calendar-body-preview-start", ctx_r0._isPreviewStart(item_r3.compareValue))("mat-calendar-body-preview-end", ctx_r0._isPreviewEnd(item_r3.compareValue))("mat-calendar-body-in-preview", ctx_r0._isInPreview(item_r3.compareValue));
    ɵɵproperty("ngClass", item_r3.cssClasses)("tabindex", ctx_r0._isActiveCell(ɵ$index_7_r5, ɵ$index_14_r4) ? 0 : -1);
    ɵɵattribute("aria-label", item_r3.ariaLabel)("aria-disabled", !item_r3.enabled || null)("aria-pressed", ctx_r0._isSelected(item_r3.compareValue))("aria-current", ctx_r0.todayValue === item_r3.compareValue ? "date" : null)("aria-describedby", ctx_r0._getDescribedby(item_r3.compareValue));
    ɵɵadvance();
    ɵɵclassProp("mat-calendar-body-selected", ctx_r0._isSelected(item_r3.compareValue))("mat-calendar-body-comparison-identical", ctx_r0._isComparisonIdentical(item_r3.compareValue))("mat-calendar-body-today", ctx_r0.todayValue === item_r3.compareValue);
    ɵɵadvance();
    ɵɵtextInterpolate1(" ", item_r3.displayValue, " ");
  }
}
__name(MatCalendarBody_For_2_For_3_Template, "MatCalendarBody_For_2_For_3_Template");
function MatCalendarBody_For_2_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵelementStart(0, "tr", 1);
    ɵɵconditionalCreate(1, MatCalendarBody_For_2_Conditional_1_Template, 2, 6, "td", 4);
    ɵɵrepeaterCreate(2, MatCalendarBody_For_2_For_3_Template, 5, 48, "td", 5, _forTrack1);
    ɵɵelementEnd();
  }
  if (rf & 2) {
    const row_r6 = ctx.$implicit;
    const ɵ$index_7_r5 = ctx.$index;
    const ctx_r0 = ɵɵnextContext();
    ɵɵadvance();
    ɵɵconditional(ɵ$index_7_r5 === 0 && ctx_r0._firstRowOffset ? 1 : -1);
    ɵɵadvance();
    ɵɵrepeater(row_r6);
  }
}
__name(MatCalendarBody_For_2_Template, "MatCalendarBody_For_2_Template");
function MatMonthView_For_4_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵelementStart(0, "th", 2)(1, "span", 6);
    ɵɵtext(2);
    ɵɵelementEnd();
    ɵɵelementStart(3, "span", 3);
    ɵɵtext(4);
    ɵɵelementEnd()();
  }
  if (rf & 2) {
    const day_r1 = ctx.$implicit;
    ɵɵadvance(2);
    ɵɵtextInterpolate(day_r1.long);
    ɵɵadvance(2);
    ɵɵtextInterpolate(day_r1.narrow);
  }
}
__name(MatMonthView_For_4_Template, "MatMonthView_For_4_Template");
var _c1 = ["*"];
function MatCalendar_ng_template_0_Template(rf, ctx) {
}
__name(MatCalendar_ng_template_0_Template, "MatCalendar_ng_template_0_Template");
function MatCalendar_Case_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r1 = ɵɵgetCurrentView();
    ɵɵelementStart(0, "mat-month-view", 4);
    ɵɵtwoWayListener("activeDateChange", /* @__PURE__ */ __name(function MatCalendar_Case_2_Template_mat_month_view_activeDateChange_0_listener($event) {
      ɵɵrestoreView(_r1);
      const ctx_r1 = ɵɵnextContext();
      ɵɵtwoWayBindingSet(ctx_r1.activeDate, $event) || (ctx_r1.activeDate = $event);
      return ɵɵresetView($event);
    }, "MatCalendar_Case_2_Template_mat_month_view_activeDateChange_0_listener"));
    ɵɵlistener("_userSelection", /* @__PURE__ */ __name(function MatCalendar_Case_2_Template_mat_month_view__userSelection_0_listener($event) {
      ɵɵrestoreView(_r1);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._dateSelected($event));
    }, "MatCalendar_Case_2_Template_mat_month_view__userSelection_0_listener"))("dragStarted", /* @__PURE__ */ __name(function MatCalendar_Case_2_Template_mat_month_view_dragStarted_0_listener($event) {
      ɵɵrestoreView(_r1);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._dragStarted($event));
    }, "MatCalendar_Case_2_Template_mat_month_view_dragStarted_0_listener"))("dragEnded", /* @__PURE__ */ __name(function MatCalendar_Case_2_Template_mat_month_view_dragEnded_0_listener($event) {
      ɵɵrestoreView(_r1);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._dragEnded($event));
    }, "MatCalendar_Case_2_Template_mat_month_view_dragEnded_0_listener"));
    ɵɵelementEnd();
  }
  if (rf & 2) {
    const ctx_r1 = ɵɵnextContext();
    ɵɵtwoWayProperty("activeDate", ctx_r1.activeDate);
    ɵɵproperty("selected", ctx_r1.selected)("dateFilter", ctx_r1.dateFilter)("maxDate", ctx_r1.maxDate)("minDate", ctx_r1.minDate)("dateClass", ctx_r1.dateClass)("comparisonStart", ctx_r1.comparisonStart)("comparisonEnd", ctx_r1.comparisonEnd)("startDateAccessibleName", ctx_r1.startDateAccessibleName)("endDateAccessibleName", ctx_r1.endDateAccessibleName)("activeDrag", ctx_r1._activeDrag);
  }
}
__name(MatCalendar_Case_2_Template, "MatCalendar_Case_2_Template");
function MatCalendar_Case_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r3 = ɵɵgetCurrentView();
    ɵɵelementStart(0, "mat-year-view", 5);
    ɵɵtwoWayListener("activeDateChange", /* @__PURE__ */ __name(function MatCalendar_Case_3_Template_mat_year_view_activeDateChange_0_listener($event) {
      ɵɵrestoreView(_r3);
      const ctx_r1 = ɵɵnextContext();
      ɵɵtwoWayBindingSet(ctx_r1.activeDate, $event) || (ctx_r1.activeDate = $event);
      return ɵɵresetView($event);
    }, "MatCalendar_Case_3_Template_mat_year_view_activeDateChange_0_listener"));
    ɵɵlistener("monthSelected", /* @__PURE__ */ __name(function MatCalendar_Case_3_Template_mat_year_view_monthSelected_0_listener($event) {
      ɵɵrestoreView(_r3);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._monthSelectedInYearView($event));
    }, "MatCalendar_Case_3_Template_mat_year_view_monthSelected_0_listener"))("selectedChange", /* @__PURE__ */ __name(function MatCalendar_Case_3_Template_mat_year_view_selectedChange_0_listener($event) {
      ɵɵrestoreView(_r3);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._goToDateInView($event, "month"));
    }, "MatCalendar_Case_3_Template_mat_year_view_selectedChange_0_listener"));
    ɵɵelementEnd();
  }
  if (rf & 2) {
    const ctx_r1 = ɵɵnextContext();
    ɵɵtwoWayProperty("activeDate", ctx_r1.activeDate);
    ɵɵproperty("selected", ctx_r1.selected)("dateFilter", ctx_r1.dateFilter)("maxDate", ctx_r1.maxDate)("minDate", ctx_r1.minDate)("dateClass", ctx_r1.dateClass);
  }
}
__name(MatCalendar_Case_3_Template, "MatCalendar_Case_3_Template");
function MatCalendar_Case_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r4 = ɵɵgetCurrentView();
    ɵɵelementStart(0, "mat-multi-year-view", 6);
    ɵɵtwoWayListener("activeDateChange", /* @__PURE__ */ __name(function MatCalendar_Case_4_Template_mat_multi_year_view_activeDateChange_0_listener($event) {
      ɵɵrestoreView(_r4);
      const ctx_r1 = ɵɵnextContext();
      ɵɵtwoWayBindingSet(ctx_r1.activeDate, $event) || (ctx_r1.activeDate = $event);
      return ɵɵresetView($event);
    }, "MatCalendar_Case_4_Template_mat_multi_year_view_activeDateChange_0_listener"));
    ɵɵlistener("yearSelected", /* @__PURE__ */ __name(function MatCalendar_Case_4_Template_mat_multi_year_view_yearSelected_0_listener($event) {
      ɵɵrestoreView(_r4);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._yearSelectedInMultiYearView($event));
    }, "MatCalendar_Case_4_Template_mat_multi_year_view_yearSelected_0_listener"))("selectedChange", /* @__PURE__ */ __name(function MatCalendar_Case_4_Template_mat_multi_year_view_selectedChange_0_listener($event) {
      ɵɵrestoreView(_r4);
      const ctx_r1 = ɵɵnextContext();
      return ɵɵresetView(ctx_r1._goToDateInView($event, "year"));
    }, "MatCalendar_Case_4_Template_mat_multi_year_view_selectedChange_0_listener"));
    ɵɵelementEnd();
  }
  if (rf & 2) {
    const ctx_r1 = ɵɵnextContext();
    ɵɵtwoWayProperty("activeDate", ctx_r1.activeDate);
    ɵɵproperty("selected", ctx_r1.selected)("dateFilter", ctx_r1.dateFilter)("maxDate", ctx_r1.maxDate)("minDate", ctx_r1.minDate)("dateClass", ctx_r1.dateClass);
  }
}
__name(MatCalendar_Case_4_Template, "MatCalendar_Case_4_Template");
function MatDatepickerContent_ng_template_2_Template(rf, ctx) {
}
__name(MatDatepickerContent_ng_template_2_Template, "MatDatepickerContent_ng_template_2_Template");
var _c2 = ["button"];
var _c3 = [[["", "matDatepickerToggleIcon", ""]]];
var _c4 = ["[matDatepickerToggleIcon]"];
function MatDatepickerToggle_Conditional_2_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵnamespaceSVG();
    ɵɵelementStart(0, "svg", 2);
    ɵɵelement(1, "path", 3);
    ɵɵelementEnd();
  }
}
__name(MatDatepickerToggle_Conditional_2_Template, "MatDatepickerToggle_Conditional_2_Template");
var _c5 = [[["input", "matStartDate", ""]], [["input", "matEndDate", ""]]];
var _c6 = ["input[matStartDate]", "input[matEndDate]"];
function MatDatepickerActions_ng_template_0_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵdomElementStart(0, "div", 0);
    ɵɵprojection(1);
    ɵɵdomElementEnd();
  }
}
__name(MatDatepickerActions_ng_template_0_Template, "MatDatepickerActions_ng_template_0_Template");
function createMissingDateImplError(provider) {
  return Error(`MatDatepicker: No provider found for ${provider}. You must add one of the following to your app config: provideNativeDateAdapter, provideDateFnsAdapter, provideLuxonDateAdapter, provideMomentDateAdapter, or provide a custom implementation.`);
}
__name(createMissingDateImplError, "createMissingDateImplError");
var _MatDatepickerIntl = class _MatDatepickerIntl {
  /**
   * Stream that emits whenever the labels here are changed. Use this to notify
   * components if the labels have changed after initialization.
   */
  changes = new Subject();
  /** A label for the calendar popup (used by screen readers). */
  calendarLabel = "Calendar";
  /** A label for the button used to open the calendar popup (used by screen readers). */
  openCalendarLabel = "Open calendar";
  /** Label for the button used to close the calendar popup. */
  closeCalendarLabel = "Close calendar";
  /** A label for the previous month button (used by screen readers). */
  prevMonthLabel = "Previous month";
  /** A label for the next month button (used by screen readers). */
  nextMonthLabel = "Next month";
  /** A label for the previous year button (used by screen readers). */
  prevYearLabel = "Previous year";
  /** A label for the next year button (used by screen readers). */
  nextYearLabel = "Next year";
  /** A label for the previous multi-year button (used by screen readers). */
  prevMultiYearLabel = "Previous 24 years";
  /** A label for the next multi-year button (used by screen readers). */
  nextMultiYearLabel = "Next 24 years";
  /** A label for the 'switch to month view' button (used by screen readers). */
  switchToMonthViewLabel = "Choose date";
  /** A label for the 'switch to year view' button (used by screen readers). */
  switchToMultiYearViewLabel = "Choose month and year";
  /**
   * A label for the first date of a range of dates (used by screen readers).
   * @deprecated Provide your own internationalization string.
   * @breaking-change 17.0.0
   */
  startDateLabel = "Start date";
  /**
   * A label for the last date of a range of dates (used by screen readers).
   * @deprecated Provide your own internationalization string.
   * @breaking-change 17.0.0
   */
  endDateLabel = "End date";
  /**
   * A label for the Comparison date of a range of dates (used by screen readers).
   */
  comparisonDateLabel = "Comparison range";
  /** Formats a range of years (used for visuals). */
  formatYearRange(start, end) {
    return `${start} – ${end}`;
  }
  /** Formats a label for a range of years (used by screen readers). */
  formatYearRangeLabel(start, end) {
    return `${start} to ${end}`;
  }
};
__name(_MatDatepickerIntl, "MatDatepickerIntl");
__publicField(_MatDatepickerIntl, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerIntl_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerIntl)();
}, "MatDatepickerIntl_Factory"));
__publicField(_MatDatepickerIntl, "ɵprov", ɵɵdefineInjectable({
  token: _MatDatepickerIntl,
  factory: _MatDatepickerIntl.ɵfac,
  providedIn: "root"
}));
var MatDatepickerIntl = _MatDatepickerIntl;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerIntl, [{
    type: Injectable,
    args: [{
      providedIn: "root"
    }]
  }], null, null);
})();
var uniqueIdCounter$1 = 0;
var _MatCalendarCell = class _MatCalendarCell {
  value;
  displayValue;
  ariaLabel;
  enabled;
  cssClasses;
  compareValue;
  rawValue;
  id = uniqueIdCounter$1++;
  constructor(value, displayValue, ariaLabel, enabled, cssClasses = {}, compareValue = value, rawValue) {
    this.value = value;
    this.displayValue = displayValue;
    this.ariaLabel = ariaLabel;
    this.enabled = enabled;
    this.cssClasses = cssClasses;
    this.compareValue = compareValue;
    this.rawValue = rawValue;
  }
};
__name(_MatCalendarCell, "MatCalendarCell");
var MatCalendarCell = _MatCalendarCell;
var activeCapturingEventOptions = {
  passive: false,
  capture: true
};
var passiveCapturingEventOptions = {
  passive: true,
  capture: true
};
var passiveEventOptions = {
  passive: true
};
var _MatCalendarBody = class _MatCalendarBody {
  _elementRef = inject(ElementRef);
  _ngZone = inject(NgZone);
  _platform = inject(Platform);
  _intl = inject(MatDatepickerIntl);
  _eventCleanups;
  /**
   * Used to skip the next focus event when rendering the preview range.
   * We need a flag like this, because some browsers fire focus events asynchronously.
   */
  _skipNextFocus;
  /**
   * Used to focus the active cell after change detection has run.
   */
  _focusActiveCellAfterViewChecked = false;
  /** The label for the table. (e.g. "Jan 2017"). */
  label;
  /** The cells to display in the table. */
  rows;
  /** The value in the table that corresponds to today. */
  todayValue;
  /** Start value of the selected date range. */
  startValue;
  /** End value of the selected date range. */
  endValue;
  /** The minimum number of free cells needed to fit the label in the first row. */
  labelMinRequiredCells;
  /** The number of columns in the table. */
  numCols = 7;
  /** The cell number of the active cell in the table. */
  activeCell = 0;
  ngAfterViewChecked() {
    if (this._focusActiveCellAfterViewChecked) {
      this._focusActiveCell();
      this._focusActiveCellAfterViewChecked = false;
    }
  }
  /** Whether a range is being selected. */
  isRange = false;
  /**
   * The aspect ratio (width / height) to use for the cells in the table. This aspect ratio will be
   * maintained even as the table resizes.
   */
  cellAspectRatio = 1;
  /** Start of the comparison range. */
  comparisonStart;
  /** End of the comparison range. */
  comparisonEnd;
  /** Start of the preview range. */
  previewStart = null;
  /** End of the preview range. */
  previewEnd = null;
  /** ARIA Accessible name of the `<input matStartDate/>` */
  startDateAccessibleName;
  /** ARIA Accessible name of the `<input matEndDate/>` */
  endDateAccessibleName;
  /** Emits when a new value is selected. */
  selectedValueChange = new EventEmitter();
  /** Emits when the preview has changed as a result of a user action. */
  previewChange = new EventEmitter();
  activeDateChange = new EventEmitter();
  /** Emits the date at the possible start of a drag event. */
  dragStarted = new EventEmitter();
  /** Emits the date at the conclusion of a drag, or null if mouse was not released on a date. */
  dragEnded = new EventEmitter();
  /** The number of blank cells to put at the beginning for the first row. */
  _firstRowOffset;
  /** Padding for the individual date cells. */
  _cellPadding;
  /** Width of an individual cell. */
  _cellWidth;
  /** ID for the start date label. */
  _startDateLabelId;
  /** ID for the end date label. */
  _endDateLabelId;
  /** ID for the comparison start date label. */
  _comparisonStartDateLabelId;
  /** ID for the comparison end date label. */
  _comparisonEndDateLabelId;
  _didDragSinceMouseDown = false;
  _injector = inject(Injector);
  comparisonDateAccessibleName = this._intl.comparisonDateLabel;
  /**
   * Tracking function for rows based on their identity. Ideally we would use some sort of
   * key on the row, but that would require a breaking change for the `rows` input. We don't
   * use the built-in identity tracking, because it logs warnings.
   */
  _trackRow = /* @__PURE__ */ __name((row) => row, "_trackRow");
  constructor() {
    const renderer = inject(Renderer2);
    const idGenerator = inject(_IdGenerator);
    this._startDateLabelId = idGenerator.getId("mat-calendar-body-start-");
    this._endDateLabelId = idGenerator.getId("mat-calendar-body-end-");
    this._comparisonStartDateLabelId = idGenerator.getId("mat-calendar-body-comparison-start-");
    this._comparisonEndDateLabelId = idGenerator.getId("mat-calendar-body-comparison-end-");
    inject(_CdkPrivateStyleLoader).load(_StructuralStylesLoader);
    this._ngZone.runOutsideAngular(() => {
      const element = this._elementRef.nativeElement;
      const cleanups = [
        // `touchmove` is active since we need to call `preventDefault`.
        renderer.listen(element, "touchmove", this._touchmoveHandler, activeCapturingEventOptions),
        renderer.listen(element, "mouseenter", this._enterHandler, passiveCapturingEventOptions),
        renderer.listen(element, "focus", this._enterHandler, passiveCapturingEventOptions),
        renderer.listen(element, "mouseleave", this._leaveHandler, passiveCapturingEventOptions),
        renderer.listen(element, "blur", this._leaveHandler, passiveCapturingEventOptions),
        renderer.listen(element, "mousedown", this._mousedownHandler, passiveEventOptions),
        renderer.listen(element, "touchstart", this._mousedownHandler, passiveEventOptions)
      ];
      if (this._platform.isBrowser) {
        cleanups.push(renderer.listen("window", "mouseup", this._mouseupHandler), renderer.listen("window", "touchend", this._touchendHandler));
      }
      this._eventCleanups = cleanups;
    });
  }
  /** Called when a cell is clicked. */
  _cellClicked(cell, event) {
    if (this._didDragSinceMouseDown) {
      return;
    }
    if (cell.enabled) {
      this.selectedValueChange.emit({
        value: cell.value,
        event
      });
    }
  }
  _emitActiveDateChange(cell, event) {
    if (cell.enabled) {
      this.activeDateChange.emit({
        value: cell.value,
        event
      });
    }
  }
  /** Returns whether a cell should be marked as selected. */
  _isSelected(value) {
    return this.startValue === value || this.endValue === value;
  }
  ngOnChanges(changes) {
    const columnChanges = changes["numCols"];
    const {
      rows,
      numCols
    } = this;
    if (changes["rows"] || columnChanges) {
      this._firstRowOffset = rows && rows.length && rows[0].length ? numCols - rows[0].length : 0;
    }
    if (changes["cellAspectRatio"] || columnChanges || !this._cellPadding) {
      this._cellPadding = `${50 * this.cellAspectRatio / numCols}%`;
    }
    if (columnChanges || !this._cellWidth) {
      this._cellWidth = `${100 / numCols}%`;
    }
  }
  ngOnDestroy() {
    this._eventCleanups.forEach((cleanup) => cleanup());
  }
  /** Returns whether a cell is active. */
  _isActiveCell(rowIndex, colIndex) {
    let cellNumber = rowIndex * this.numCols + colIndex;
    if (rowIndex) {
      cellNumber -= this._firstRowOffset;
    }
    return cellNumber == this.activeCell;
  }
  /**
   * Focuses the active cell after the microtask queue is empty.
   *
   * Adding a 0ms setTimeout seems to fix Voiceover losing focus when pressing PageUp/PageDown
   * (issue #24330).
   *
   * Determined a 0ms by gradually increasing duration from 0 and testing two use cases with screen
   * reader enabled:
   *
   * 1. Pressing PageUp/PageDown repeatedly with pausing between each key press.
   * 2. Pressing and holding the PageDown key with repeated keys enabled.
   *
   * Test 1 worked roughly 95-99% of the time with 0ms and got a little bit better as the duration
   * increased. Test 2 got slightly better until the duration was long enough to interfere with
   * repeated keys. If the repeated key speed was faster than the timeout duration, then pressing
   * and holding pagedown caused the entire page to scroll.
   *
   * Since repeated key speed can verify across machines, determined that any duration could
   * potentially interfere with repeated keys. 0ms would be best because it almost entirely
   * eliminates the focus being lost in Voiceover (#24330) without causing unintended side effects.
   * Adding delay also complicates writing tests.
   */
  _focusActiveCell(movePreview = true) {
    afterNextRender(() => {
      setTimeout(() => {
        const activeCell = this._elementRef.nativeElement.querySelector(".mat-calendar-body-active");
        if (activeCell) {
          if (!movePreview) {
            this._skipNextFocus = true;
          }
          activeCell.focus();
        }
      });
    }, {
      injector: this._injector
    });
  }
  /** Focuses the active cell after change detection has run and the microtask queue is empty. */
  _scheduleFocusActiveCellAfterViewChecked() {
    this._focusActiveCellAfterViewChecked = true;
  }
  /** Gets whether a value is the start of the main range. */
  _isRangeStart(value) {
    return isStart(value, this.startValue, this.endValue);
  }
  /** Gets whether a value is the end of the main range. */
  _isRangeEnd(value) {
    return isEnd(value, this.startValue, this.endValue);
  }
  /** Gets whether a value is within the currently-selected range. */
  _isInRange(value) {
    return isInRange(value, this.startValue, this.endValue, this.isRange);
  }
  /** Gets whether a value is the start of the comparison range. */
  _isComparisonStart(value) {
    return isStart(value, this.comparisonStart, this.comparisonEnd);
  }
  /** Whether the cell is a start bridge cell between the main and comparison ranges. */
  _isComparisonBridgeStart(value, rowIndex, colIndex) {
    if (!this._isComparisonStart(value) || this._isRangeStart(value) || !this._isInRange(value)) {
      return false;
    }
    let previousCell = this.rows[rowIndex][colIndex - 1];
    if (!previousCell) {
      const previousRow = this.rows[rowIndex - 1];
      previousCell = previousRow && previousRow[previousRow.length - 1];
    }
    return previousCell && !this._isRangeEnd(previousCell.compareValue);
  }
  /** Whether the cell is an end bridge cell between the main and comparison ranges. */
  _isComparisonBridgeEnd(value, rowIndex, colIndex) {
    if (!this._isComparisonEnd(value) || this._isRangeEnd(value) || !this._isInRange(value)) {
      return false;
    }
    let nextCell = this.rows[rowIndex][colIndex + 1];
    if (!nextCell) {
      const nextRow = this.rows[rowIndex + 1];
      nextCell = nextRow && nextRow[0];
    }
    return nextCell && !this._isRangeStart(nextCell.compareValue);
  }
  /** Gets whether a value is the end of the comparison range. */
  _isComparisonEnd(value) {
    return isEnd(value, this.comparisonStart, this.comparisonEnd);
  }
  /** Gets whether a value is within the current comparison range. */
  _isInComparisonRange(value) {
    return isInRange(value, this.comparisonStart, this.comparisonEnd, this.isRange);
  }
  /**
   * Gets whether a value is the same as the start and end of the comparison range.
   * For context, the functions that we use to determine whether something is the start/end of
   * a range don't allow for the start and end to be on the same day, because we'd have to use
   * much more specific CSS selectors to style them correctly in all scenarios. This is fine for
   * the regular range, because when it happens, the selected styles take over and still show where
   * the range would've been, however we don't have these selected styles for a comparison range.
   * This function is used to apply a class that serves the same purpose as the one for selected
   * dates, but it only applies in the context of a comparison range.
   */
  _isComparisonIdentical(value) {
    return this.comparisonStart === this.comparisonEnd && value === this.comparisonStart;
  }
  /** Gets whether a value is the start of the preview range. */
  _isPreviewStart(value) {
    return isStart(value, this.previewStart, this.previewEnd);
  }
  /** Gets whether a value is the end of the preview range. */
  _isPreviewEnd(value) {
    return isEnd(value, this.previewStart, this.previewEnd);
  }
  /** Gets whether a value is inside the preview range. */
  _isInPreview(value) {
    return isInRange(value, this.previewStart, this.previewEnd, this.isRange);
  }
  /** Gets ids of aria descriptions for the start and end of a date range. */
  _getDescribedby(value) {
    if (!this.isRange) {
      return null;
    }
    if (this.startValue === value && this.endValue === value) {
      return `${this._startDateLabelId} ${this._endDateLabelId}`;
    } else if (this.startValue === value) {
      return this._startDateLabelId;
    } else if (this.endValue === value) {
      return this._endDateLabelId;
    }
    if (this.comparisonStart !== null && this.comparisonEnd !== null) {
      if (value === this.comparisonStart && value === this.comparisonEnd) {
        return `${this._comparisonStartDateLabelId} ${this._comparisonEndDateLabelId}`;
      } else if (value === this.comparisonStart) {
        return this._comparisonStartDateLabelId;
      } else if (value === this.comparisonEnd) {
        return this._comparisonEndDateLabelId;
      }
    }
    return null;
  }
  /**
   * Event handler for when the user enters an element
   * inside the calendar body (e.g. by hovering in or focus).
   */
  _enterHandler = /* @__PURE__ */ __name((event) => {
    if (this._skipNextFocus && event.type === "focus") {
      this._skipNextFocus = false;
      return;
    }
    if (event.target && this.isRange) {
      const cell = this._getCellFromElement(event.target);
      if (cell) {
        this._ngZone.run(() => this.previewChange.emit({
          value: cell.enabled ? cell : null,
          event
        }));
      }
    }
  }, "_enterHandler");
  _touchmoveHandler = /* @__PURE__ */ __name((event) => {
    if (!this.isRange) return;
    const target = getActualTouchTarget(event);
    const cell = target ? this._getCellFromElement(target) : null;
    if (target !== event.target) {
      this._didDragSinceMouseDown = true;
    }
    if (getCellElement(event.target)) {
      event.preventDefault();
    }
    this._ngZone.run(() => this.previewChange.emit({
      value: cell?.enabled ? cell : null,
      event
    }));
  }, "_touchmoveHandler");
  /**
   * Event handler for when the user's pointer leaves an element
   * inside the calendar body (e.g. by hovering out or blurring).
   */
  _leaveHandler = /* @__PURE__ */ __name((event) => {
    if (this.previewEnd !== null && this.isRange) {
      if (event.type !== "blur") {
        this._didDragSinceMouseDown = true;
      }
      if (event.target && this._getCellFromElement(event.target) && !(event.relatedTarget && this._getCellFromElement(event.relatedTarget))) {
        this._ngZone.run(() => this.previewChange.emit({
          value: null,
          event
        }));
      }
    }
  }, "_leaveHandler");
  /**
   * Triggered on mousedown or touchstart on a date cell.
   * Respsonsible for starting a drag sequence.
   */
  _mousedownHandler = /* @__PURE__ */ __name((event) => {
    if (!this.isRange) return;
    this._didDragSinceMouseDown = false;
    const cell = event.target && this._getCellFromElement(event.target);
    if (!cell || !this._isInRange(cell.compareValue)) {
      return;
    }
    this._ngZone.run(() => {
      this.dragStarted.emit({
        value: cell.rawValue,
        event
      });
    });
  }, "_mousedownHandler");
  /** Triggered on mouseup anywhere. Respsonsible for ending a drag sequence. */
  _mouseupHandler = /* @__PURE__ */ __name((event) => {
    if (!this.isRange) return;
    const cellElement = getCellElement(event.target);
    if (!cellElement) {
      this._ngZone.run(() => {
        this.dragEnded.emit({
          value: null,
          event
        });
      });
      return;
    }
    if (cellElement.closest(".mat-calendar-body") !== this._elementRef.nativeElement) {
      return;
    }
    this._ngZone.run(() => {
      const cell = this._getCellFromElement(cellElement);
      this.dragEnded.emit({
        value: cell?.rawValue ?? null,
        event
      });
    });
  }, "_mouseupHandler");
  /** Triggered on touchend anywhere. Respsonsible for ending a drag sequence. */
  _touchendHandler = /* @__PURE__ */ __name((event) => {
    const target = getActualTouchTarget(event);
    if (target) {
      this._mouseupHandler({
        target
      });
    }
  }, "_touchendHandler");
  /** Finds the MatCalendarCell that corresponds to a DOM node. */
  _getCellFromElement(element) {
    const cell = getCellElement(element);
    if (cell) {
      const row = cell.getAttribute("data-mat-row");
      const col = cell.getAttribute("data-mat-col");
      if (row && col) {
        return this.rows[parseInt(row)][parseInt(col)];
      }
    }
    return null;
  }
};
__name(_MatCalendarBody, "MatCalendarBody");
__publicField(_MatCalendarBody, "ɵfac", /* @__PURE__ */ __name(function MatCalendarBody_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatCalendarBody)();
}, "MatCalendarBody_Factory"));
__publicField(_MatCalendarBody, "ɵcmp", ɵɵdefineComponent({
  type: _MatCalendarBody,
  selectors: [["", "mat-calendar-body", ""]],
  hostAttrs: [1, "mat-calendar-body"],
  inputs: {
    label: "label",
    rows: "rows",
    todayValue: "todayValue",
    startValue: "startValue",
    endValue: "endValue",
    labelMinRequiredCells: "labelMinRequiredCells",
    numCols: "numCols",
    activeCell: "activeCell",
    isRange: "isRange",
    cellAspectRatio: "cellAspectRatio",
    comparisonStart: "comparisonStart",
    comparisonEnd: "comparisonEnd",
    previewStart: "previewStart",
    previewEnd: "previewEnd",
    startDateAccessibleName: "startDateAccessibleName",
    endDateAccessibleName: "endDateAccessibleName"
  },
  outputs: {
    selectedValueChange: "selectedValueChange",
    previewChange: "previewChange",
    activeDateChange: "activeDateChange",
    dragStarted: "dragStarted",
    dragEnded: "dragEnded"
  },
  exportAs: ["matCalendarBody"],
  features: [ɵɵNgOnChangesFeature],
  attrs: _c02,
  decls: 11,
  vars: 11,
  consts: [["aria-hidden", "true"], ["role", "row"], [1, "mat-calendar-body-hidden-label", 3, "id"], [1, "mat-calendar-body-label"], [1, "mat-calendar-body-label", 3, "paddingTop", "paddingBottom"], ["role", "gridcell", 1, "mat-calendar-body-cell-container", 3, "width", "paddingTop", "paddingBottom"], ["role", "gridcell", 1, "mat-calendar-body-cell-container"], ["type", "button", 1, "mat-calendar-body-cell", 3, "click", "focus", "ngClass", "tabindex"], [1, "mat-calendar-body-cell-content", "mat-focus-indicator"], ["aria-hidden", "true", 1, "mat-calendar-body-cell-preview"]],
  template: /* @__PURE__ */ __name(function MatCalendarBody_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵconditionalCreate(0, MatCalendarBody_Conditional_0_Template, 3, 6, "tr", 0);
      ɵɵrepeaterCreate(1, MatCalendarBody_For_2_Template, 4, 1, "tr", 1, _forTrack0, true);
      ɵɵelementStart(3, "span", 2);
      ɵɵtext(4);
      ɵɵelementEnd();
      ɵɵelementStart(5, "span", 2);
      ɵɵtext(6);
      ɵɵelementEnd();
      ɵɵelementStart(7, "span", 2);
      ɵɵtext(8);
      ɵɵelementEnd();
      ɵɵelementStart(9, "span", 2);
      ɵɵtext(10);
      ɵɵelementEnd();
    }
    if (rf & 2) {
      ɵɵconditional(ctx._firstRowOffset < ctx.labelMinRequiredCells ? 0 : -1);
      ɵɵadvance();
      ɵɵrepeater(ctx.rows);
      ɵɵadvance(2);
      ɵɵproperty("id", ctx._startDateLabelId);
      ɵɵadvance();
      ɵɵtextInterpolate1(" ", ctx.startDateAccessibleName, "\n");
      ɵɵadvance();
      ɵɵproperty("id", ctx._endDateLabelId);
      ɵɵadvance();
      ɵɵtextInterpolate1(" ", ctx.endDateAccessibleName, "\n");
      ɵɵadvance();
      ɵɵproperty("id", ctx._comparisonStartDateLabelId);
      ɵɵadvance();
      ɵɵtextInterpolate2(" ", ctx.comparisonDateAccessibleName, " ", ctx.startDateAccessibleName, "\n");
      ɵɵadvance();
      ɵɵproperty("id", ctx._comparisonEndDateLabelId);
      ɵɵadvance();
      ɵɵtextInterpolate2(" ", ctx.comparisonDateAccessibleName, " ", ctx.endDateAccessibleName, "\n");
    }
  }, "MatCalendarBody_Template"),
  dependencies: [NgClass],
  styles: ['.mat-calendar-body{min-width:224px}.mat-calendar-body-today:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){border-color:var(--mat-datepicker-calendar-date-today-outline-color, var(--mat-sys-primary))}.mat-calendar-body-label{height:0;line-height:0;text-align:start;padding-left:4.7142857143%;padding-right:4.7142857143%;font-size:var(--mat-datepicker-calendar-body-label-text-size, var(--mat-sys-title-small-size));font-weight:var(--mat-datepicker-calendar-body-label-text-weight, var(--mat-sys-title-small-weight));color:var(--mat-datepicker-calendar-body-label-text-color, var(--mat-sys-on-surface))}.mat-calendar-body-hidden-label{display:none}.mat-calendar-body-cell-container{position:relative;height:0;line-height:0}.mat-calendar-body-cell{position:absolute;top:0;left:0;width:100%;height:100%;background:none;text-align:center;outline:none;margin:0;font-family:var(--mat-datepicker-calendar-text-font, var(--mat-sys-body-medium-font));font-size:var(--mat-datepicker-calendar-text-size, var(--mat-sys-body-medium-size));-webkit-user-select:none;user-select:none;cursor:pointer;outline:none;border:none;-webkit-tap-highlight-color:rgba(0,0,0,0)}.mat-calendar-body-cell::-moz-focus-inner{border:0}.mat-calendar-body-cell::before,.mat-calendar-body-cell::after,.mat-calendar-body-cell-preview{content:"";position:absolute;top:5%;left:0;z-index:0;box-sizing:border-box;display:block;height:90%;width:100%}.mat-calendar-body-range-start:not(.mat-calendar-body-in-comparison-range)::before,.mat-calendar-body-range-start::after,.mat-calendar-body-comparison-start:not(.mat-calendar-body-comparison-bridge-start)::before,.mat-calendar-body-comparison-start::after,.mat-calendar-body-preview-start .mat-calendar-body-cell-preview{left:5%;width:95%;border-top-left-radius:999px;border-bottom-left-radius:999px}[dir=rtl] .mat-calendar-body-range-start:not(.mat-calendar-body-in-comparison-range)::before,[dir=rtl] .mat-calendar-body-range-start::after,[dir=rtl] .mat-calendar-body-comparison-start:not(.mat-calendar-body-comparison-bridge-start)::before,[dir=rtl] .mat-calendar-body-comparison-start::after,[dir=rtl] .mat-calendar-body-preview-start .mat-calendar-body-cell-preview{left:0;border-radius:0;border-top-right-radius:999px;border-bottom-right-radius:999px}.mat-calendar-body-range-end:not(.mat-calendar-body-in-comparison-range)::before,.mat-calendar-body-range-end::after,.mat-calendar-body-comparison-end:not(.mat-calendar-body-comparison-bridge-end)::before,.mat-calendar-body-comparison-end::after,.mat-calendar-body-preview-end .mat-calendar-body-cell-preview{width:95%;border-top-right-radius:999px;border-bottom-right-radius:999px}[dir=rtl] .mat-calendar-body-range-end:not(.mat-calendar-body-in-comparison-range)::before,[dir=rtl] .mat-calendar-body-range-end::after,[dir=rtl] .mat-calendar-body-comparison-end:not(.mat-calendar-body-comparison-bridge-end)::before,[dir=rtl] .mat-calendar-body-comparison-end::after,[dir=rtl] .mat-calendar-body-preview-end .mat-calendar-body-cell-preview{left:5%;border-radius:0;border-top-left-radius:999px;border-bottom-left-radius:999px}[dir=rtl] .mat-calendar-body-comparison-bridge-start.mat-calendar-body-range-end::after,[dir=rtl] .mat-calendar-body-comparison-bridge-end.mat-calendar-body-range-start::after{width:95%;border-top-right-radius:999px;border-bottom-right-radius:999px}.mat-calendar-body-comparison-start.mat-calendar-body-range-end::after,[dir=rtl] .mat-calendar-body-comparison-start.mat-calendar-body-range-end::after,.mat-calendar-body-comparison-end.mat-calendar-body-range-start::after,[dir=rtl] .mat-calendar-body-comparison-end.mat-calendar-body-range-start::after{width:90%}.mat-calendar-body-in-preview{color:var(--mat-datepicker-calendar-date-preview-state-outline-color, var(--mat-sys-primary))}.mat-calendar-body-in-preview .mat-calendar-body-cell-preview{border-top:dashed 1px;border-bottom:dashed 1px}.mat-calendar-body-preview-start .mat-calendar-body-cell-preview{border-left:dashed 1px}[dir=rtl] .mat-calendar-body-preview-start .mat-calendar-body-cell-preview{border-left:0;border-right:dashed 1px}.mat-calendar-body-preview-end .mat-calendar-body-cell-preview{border-right:dashed 1px}[dir=rtl] .mat-calendar-body-preview-end .mat-calendar-body-cell-preview{border-right:0;border-left:dashed 1px}.mat-calendar-body-disabled{cursor:default}.mat-calendar-body-disabled>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){color:var(--mat-datepicker-calendar-date-disabled-state-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-calendar-body-disabled>.mat-calendar-body-today:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){border-color:var(--mat-datepicker-calendar-date-today-disabled-state-outline-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}@media(forced-colors: active){.mat-calendar-body-disabled{opacity:.5}}.mat-calendar-body-cell-content{top:5%;left:5%;z-index:1;display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:90%;height:90%;line-height:1;border-width:1px;border-style:solid;border-radius:999px;color:var(--mat-datepicker-calendar-date-text-color, var(--mat-sys-on-surface));border-color:var(--mat-datepicker-calendar-date-outline-color, transparent)}.mat-calendar-body-cell-content.mat-focus-indicator{position:absolute}@media(forced-colors: active){.mat-calendar-body-cell-content{border:none}}.cdk-keyboard-focused .mat-calendar-body-active>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical),.cdk-program-focused .mat-calendar-body-active>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){background-color:var(--mat-datepicker-calendar-date-focus-state-background-color, color-mix(in srgb, var(--mat-sys-on-surface) calc(var(--mat-sys-focus-state-layer-opacity) * 100%), transparent))}@media(hover: hover){.mat-calendar-body-cell:not(.mat-calendar-body-disabled):hover>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){background-color:var(--mat-datepicker-calendar-date-hover-state-background-color, color-mix(in srgb, var(--mat-sys-on-surface) calc(var(--mat-sys-hover-state-layer-opacity) * 100%), transparent))}}.mat-calendar-body-selected{background-color:var(--mat-datepicker-calendar-date-selected-state-background-color, var(--mat-sys-primary));color:var(--mat-datepicker-calendar-date-selected-state-text-color, var(--mat-sys-on-primary))}.mat-calendar-body-disabled>.mat-calendar-body-selected{background-color:var(--mat-datepicker-calendar-date-selected-disabled-state-background-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-calendar-body-selected.mat-calendar-body-today{box-shadow:inset 0 0 0 1px var(--mat-datepicker-calendar-date-today-selected-state-outline-color, var(--mat-sys-primary))}.mat-calendar-body-in-range::before{background:var(--mat-datepicker-calendar-date-in-range-state-background-color, var(--mat-sys-primary-container))}.mat-calendar-body-comparison-identical,.mat-calendar-body-in-comparison-range::before{background:var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container))}.mat-calendar-body-comparison-identical,.mat-calendar-body-in-comparison-range::before{background:var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container))}.mat-calendar-body-comparison-bridge-start::before,[dir=rtl] .mat-calendar-body-comparison-bridge-end::before{background:linear-gradient(to right, var(--mat-datepicker-calendar-date-in-range-state-background-color, var(--mat-sys-primary-container)) 50%, var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container)) 50%)}.mat-calendar-body-comparison-bridge-end::before,[dir=rtl] .mat-calendar-body-comparison-bridge-start::before{background:linear-gradient(to left, var(--mat-datepicker-calendar-date-in-range-state-background-color, var(--mat-sys-primary-container)) 50%, var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container)) 50%)}.mat-calendar-body-in-range>.mat-calendar-body-comparison-identical,.mat-calendar-body-in-comparison-range.mat-calendar-body-in-range::after{background:var(--mat-datepicker-calendar-date-in-overlap-range-state-background-color, var(--mat-sys-secondary-container))}.mat-calendar-body-comparison-identical.mat-calendar-body-selected,.mat-calendar-body-in-comparison-range>.mat-calendar-body-selected{background:var(--mat-datepicker-calendar-date-in-overlap-range-selected-state-background-color, var(--mat-sys-secondary))}@media(forced-colors: active){.mat-datepicker-popup:not(:empty),.mat-calendar-body-cell:not(.mat-calendar-body-in-range) .mat-calendar-body-selected{outline:solid 1px}.mat-calendar-body-today{outline:dotted 1px}.mat-calendar-body-cell::before,.mat-calendar-body-cell::after,.mat-calendar-body-selected{background:none}.mat-calendar-body-in-range::before,.mat-calendar-body-comparison-bridge-start::before,.mat-calendar-body-comparison-bridge-end::before{border-top:solid 1px;border-bottom:solid 1px}.mat-calendar-body-range-start::before{border-left:solid 1px}[dir=rtl] .mat-calendar-body-range-start::before{border-left:0;border-right:solid 1px}.mat-calendar-body-range-end::before{border-right:solid 1px}[dir=rtl] .mat-calendar-body-range-end::before{border-right:0;border-left:solid 1px}.mat-calendar-body-in-comparison-range::before{border-top:dashed 1px;border-bottom:dashed 1px}.mat-calendar-body-comparison-start::before{border-left:dashed 1px}[dir=rtl] .mat-calendar-body-comparison-start::before{border-left:0;border-right:dashed 1px}.mat-calendar-body-comparison-end::before{border-right:dashed 1px}[dir=rtl] .mat-calendar-body-comparison-end::before{border-right:0;border-left:dashed 1px}}\n'],
  encapsulation: 2,
  changeDetection: 0
}));
var MatCalendarBody = _MatCalendarBody;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatCalendarBody, [{
    type: Component,
    args: [{
      selector: "[mat-calendar-body]",
      host: {
        "class": "mat-calendar-body"
      },
      exportAs: "matCalendarBody",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [NgClass],
      template: `<!--
  If there's not enough space in the first row, create a separate label row. We mark this row as
  aria-hidden because we don't want it to be read out as one of the weeks in the month.
-->
@if (_firstRowOffset < labelMinRequiredCells) {
  <tr aria-hidden="true">
    <td class="mat-calendar-body-label"
        [attr.colspan]="numCols"
        [style.paddingTop]="_cellPadding"
        [style.paddingBottom]="_cellPadding">
      {{label}}
    </td>
  </tr>
}

<!-- Create the first row separately so we can include a special spacer cell. -->
@for (row of rows; track _trackRow(row); let rowIndex = $index) {
  <tr role="row">
    <!--
      This cell is purely decorative, but we can't put \`aria-hidden\` or \`role="presentation"\` on it,
      because it throws off the week days for the rest of the row on NVDA. The aspect ratio of the
      table cells is maintained by setting the top and bottom padding as a percentage of the width
      (a variant of the trick described here: https://www.w3schools.com/howto/howto_css_aspect_ratio.asp).
    -->
    @if (rowIndex === 0 && _firstRowOffset) {
      <td
        class="mat-calendar-body-label"
        [attr.colspan]="_firstRowOffset"
        [style.paddingTop]="_cellPadding"
        [style.paddingBottom]="_cellPadding">
        {{_firstRowOffset >= labelMinRequiredCells ? label : ''}}
      </td>
    }
    <!--
      Each gridcell in the calendar contains a button, which signals to assistive technology that the
      cell is interactable, as well as the selection state via \`aria-pressed\`. See #23476 for
      background.
    -->
    @for (item of row; track item.id; let colIndex = $index) {
      <td
        role="gridcell"
        class="mat-calendar-body-cell-container"
        [style.width]="_cellWidth"
        [style.paddingTop]="_cellPadding"
        [style.paddingBottom]="_cellPadding"
        [attr.data-mat-row]="rowIndex"
        [attr.data-mat-col]="colIndex"
      >
        <button
            type="button"
            class="mat-calendar-body-cell"
            [ngClass]="item.cssClasses"
            [tabindex]="_isActiveCell(rowIndex, colIndex) ? 0 : -1"
            [class.mat-calendar-body-disabled]="!item.enabled"
            [class.mat-calendar-body-active]="_isActiveCell(rowIndex, colIndex)"
            [class.mat-calendar-body-range-start]="_isRangeStart(item.compareValue)"
            [class.mat-calendar-body-range-end]="_isRangeEnd(item.compareValue)"
            [class.mat-calendar-body-in-range]="_isInRange(item.compareValue)"
            [class.mat-calendar-body-comparison-bridge-start]="_isComparisonBridgeStart(item.compareValue, rowIndex, colIndex)"
            [class.mat-calendar-body-comparison-bridge-end]="_isComparisonBridgeEnd(item.compareValue, rowIndex, colIndex)"
            [class.mat-calendar-body-comparison-start]="_isComparisonStart(item.compareValue)"
            [class.mat-calendar-body-comparison-end]="_isComparisonEnd(item.compareValue)"
            [class.mat-calendar-body-in-comparison-range]="_isInComparisonRange(item.compareValue)"
            [class.mat-calendar-body-preview-start]="_isPreviewStart(item.compareValue)"
            [class.mat-calendar-body-preview-end]="_isPreviewEnd(item.compareValue)"
            [class.mat-calendar-body-in-preview]="_isInPreview(item.compareValue)"
            [attr.aria-label]="item.ariaLabel"
            [attr.aria-disabled]="!item.enabled || null"
            [attr.aria-pressed]="_isSelected(item.compareValue)"
            [attr.aria-current]="todayValue === item.compareValue ? 'date' : null"
            [attr.aria-describedby]="_getDescribedby(item.compareValue)"
            (click)="_cellClicked(item, $event)"
            (focus)="_emitActiveDateChange(item, $event)">
            <span class="mat-calendar-body-cell-content mat-focus-indicator"
              [class.mat-calendar-body-selected]="_isSelected(item.compareValue)"
              [class.mat-calendar-body-comparison-identical]="_isComparisonIdentical(item.compareValue)"
              [class.mat-calendar-body-today]="todayValue === item.compareValue">
              {{item.displayValue}}
            </span>
            <span class="mat-calendar-body-cell-preview" aria-hidden="true"></span>
        </button>
      </td>
    }
  </tr>
}

<span [id]="_startDateLabelId" class="mat-calendar-body-hidden-label">
  {{startDateAccessibleName}}
</span>
<span [id]="_endDateLabelId" class="mat-calendar-body-hidden-label">
  {{endDateAccessibleName}}
</span>
<span [id]="_comparisonStartDateLabelId" class="mat-calendar-body-hidden-label">
  {{comparisonDateAccessibleName}} {{startDateAccessibleName}}
</span>
<span [id]="_comparisonEndDateLabelId" class="mat-calendar-body-hidden-label">
  {{comparisonDateAccessibleName}} {{endDateAccessibleName}}
</span>
`,
      styles: ['.mat-calendar-body{min-width:224px}.mat-calendar-body-today:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){border-color:var(--mat-datepicker-calendar-date-today-outline-color, var(--mat-sys-primary))}.mat-calendar-body-label{height:0;line-height:0;text-align:start;padding-left:4.7142857143%;padding-right:4.7142857143%;font-size:var(--mat-datepicker-calendar-body-label-text-size, var(--mat-sys-title-small-size));font-weight:var(--mat-datepicker-calendar-body-label-text-weight, var(--mat-sys-title-small-weight));color:var(--mat-datepicker-calendar-body-label-text-color, var(--mat-sys-on-surface))}.mat-calendar-body-hidden-label{display:none}.mat-calendar-body-cell-container{position:relative;height:0;line-height:0}.mat-calendar-body-cell{position:absolute;top:0;left:0;width:100%;height:100%;background:none;text-align:center;outline:none;margin:0;font-family:var(--mat-datepicker-calendar-text-font, var(--mat-sys-body-medium-font));font-size:var(--mat-datepicker-calendar-text-size, var(--mat-sys-body-medium-size));-webkit-user-select:none;user-select:none;cursor:pointer;outline:none;border:none;-webkit-tap-highlight-color:rgba(0,0,0,0)}.mat-calendar-body-cell::-moz-focus-inner{border:0}.mat-calendar-body-cell::before,.mat-calendar-body-cell::after,.mat-calendar-body-cell-preview{content:"";position:absolute;top:5%;left:0;z-index:0;box-sizing:border-box;display:block;height:90%;width:100%}.mat-calendar-body-range-start:not(.mat-calendar-body-in-comparison-range)::before,.mat-calendar-body-range-start::after,.mat-calendar-body-comparison-start:not(.mat-calendar-body-comparison-bridge-start)::before,.mat-calendar-body-comparison-start::after,.mat-calendar-body-preview-start .mat-calendar-body-cell-preview{left:5%;width:95%;border-top-left-radius:999px;border-bottom-left-radius:999px}[dir=rtl] .mat-calendar-body-range-start:not(.mat-calendar-body-in-comparison-range)::before,[dir=rtl] .mat-calendar-body-range-start::after,[dir=rtl] .mat-calendar-body-comparison-start:not(.mat-calendar-body-comparison-bridge-start)::before,[dir=rtl] .mat-calendar-body-comparison-start::after,[dir=rtl] .mat-calendar-body-preview-start .mat-calendar-body-cell-preview{left:0;border-radius:0;border-top-right-radius:999px;border-bottom-right-radius:999px}.mat-calendar-body-range-end:not(.mat-calendar-body-in-comparison-range)::before,.mat-calendar-body-range-end::after,.mat-calendar-body-comparison-end:not(.mat-calendar-body-comparison-bridge-end)::before,.mat-calendar-body-comparison-end::after,.mat-calendar-body-preview-end .mat-calendar-body-cell-preview{width:95%;border-top-right-radius:999px;border-bottom-right-radius:999px}[dir=rtl] .mat-calendar-body-range-end:not(.mat-calendar-body-in-comparison-range)::before,[dir=rtl] .mat-calendar-body-range-end::after,[dir=rtl] .mat-calendar-body-comparison-end:not(.mat-calendar-body-comparison-bridge-end)::before,[dir=rtl] .mat-calendar-body-comparison-end::after,[dir=rtl] .mat-calendar-body-preview-end .mat-calendar-body-cell-preview{left:5%;border-radius:0;border-top-left-radius:999px;border-bottom-left-radius:999px}[dir=rtl] .mat-calendar-body-comparison-bridge-start.mat-calendar-body-range-end::after,[dir=rtl] .mat-calendar-body-comparison-bridge-end.mat-calendar-body-range-start::after{width:95%;border-top-right-radius:999px;border-bottom-right-radius:999px}.mat-calendar-body-comparison-start.mat-calendar-body-range-end::after,[dir=rtl] .mat-calendar-body-comparison-start.mat-calendar-body-range-end::after,.mat-calendar-body-comparison-end.mat-calendar-body-range-start::after,[dir=rtl] .mat-calendar-body-comparison-end.mat-calendar-body-range-start::after{width:90%}.mat-calendar-body-in-preview{color:var(--mat-datepicker-calendar-date-preview-state-outline-color, var(--mat-sys-primary))}.mat-calendar-body-in-preview .mat-calendar-body-cell-preview{border-top:dashed 1px;border-bottom:dashed 1px}.mat-calendar-body-preview-start .mat-calendar-body-cell-preview{border-left:dashed 1px}[dir=rtl] .mat-calendar-body-preview-start .mat-calendar-body-cell-preview{border-left:0;border-right:dashed 1px}.mat-calendar-body-preview-end .mat-calendar-body-cell-preview{border-right:dashed 1px}[dir=rtl] .mat-calendar-body-preview-end .mat-calendar-body-cell-preview{border-right:0;border-left:dashed 1px}.mat-calendar-body-disabled{cursor:default}.mat-calendar-body-disabled>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){color:var(--mat-datepicker-calendar-date-disabled-state-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-calendar-body-disabled>.mat-calendar-body-today:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){border-color:var(--mat-datepicker-calendar-date-today-disabled-state-outline-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}@media(forced-colors: active){.mat-calendar-body-disabled{opacity:.5}}.mat-calendar-body-cell-content{top:5%;left:5%;z-index:1;display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:90%;height:90%;line-height:1;border-width:1px;border-style:solid;border-radius:999px;color:var(--mat-datepicker-calendar-date-text-color, var(--mat-sys-on-surface));border-color:var(--mat-datepicker-calendar-date-outline-color, transparent)}.mat-calendar-body-cell-content.mat-focus-indicator{position:absolute}@media(forced-colors: active){.mat-calendar-body-cell-content{border:none}}.cdk-keyboard-focused .mat-calendar-body-active>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical),.cdk-program-focused .mat-calendar-body-active>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){background-color:var(--mat-datepicker-calendar-date-focus-state-background-color, color-mix(in srgb, var(--mat-sys-on-surface) calc(var(--mat-sys-focus-state-layer-opacity) * 100%), transparent))}@media(hover: hover){.mat-calendar-body-cell:not(.mat-calendar-body-disabled):hover>.mat-calendar-body-cell-content:not(.mat-calendar-body-selected):not(.mat-calendar-body-comparison-identical){background-color:var(--mat-datepicker-calendar-date-hover-state-background-color, color-mix(in srgb, var(--mat-sys-on-surface) calc(var(--mat-sys-hover-state-layer-opacity) * 100%), transparent))}}.mat-calendar-body-selected{background-color:var(--mat-datepicker-calendar-date-selected-state-background-color, var(--mat-sys-primary));color:var(--mat-datepicker-calendar-date-selected-state-text-color, var(--mat-sys-on-primary))}.mat-calendar-body-disabled>.mat-calendar-body-selected{background-color:var(--mat-datepicker-calendar-date-selected-disabled-state-background-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-calendar-body-selected.mat-calendar-body-today{box-shadow:inset 0 0 0 1px var(--mat-datepicker-calendar-date-today-selected-state-outline-color, var(--mat-sys-primary))}.mat-calendar-body-in-range::before{background:var(--mat-datepicker-calendar-date-in-range-state-background-color, var(--mat-sys-primary-container))}.mat-calendar-body-comparison-identical,.mat-calendar-body-in-comparison-range::before{background:var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container))}.mat-calendar-body-comparison-identical,.mat-calendar-body-in-comparison-range::before{background:var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container))}.mat-calendar-body-comparison-bridge-start::before,[dir=rtl] .mat-calendar-body-comparison-bridge-end::before{background:linear-gradient(to right, var(--mat-datepicker-calendar-date-in-range-state-background-color, var(--mat-sys-primary-container)) 50%, var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container)) 50%)}.mat-calendar-body-comparison-bridge-end::before,[dir=rtl] .mat-calendar-body-comparison-bridge-start::before{background:linear-gradient(to left, var(--mat-datepicker-calendar-date-in-range-state-background-color, var(--mat-sys-primary-container)) 50%, var(--mat-datepicker-calendar-date-in-comparison-range-state-background-color, var(--mat-sys-tertiary-container)) 50%)}.mat-calendar-body-in-range>.mat-calendar-body-comparison-identical,.mat-calendar-body-in-comparison-range.mat-calendar-body-in-range::after{background:var(--mat-datepicker-calendar-date-in-overlap-range-state-background-color, var(--mat-sys-secondary-container))}.mat-calendar-body-comparison-identical.mat-calendar-body-selected,.mat-calendar-body-in-comparison-range>.mat-calendar-body-selected{background:var(--mat-datepicker-calendar-date-in-overlap-range-selected-state-background-color, var(--mat-sys-secondary))}@media(forced-colors: active){.mat-datepicker-popup:not(:empty),.mat-calendar-body-cell:not(.mat-calendar-body-in-range) .mat-calendar-body-selected{outline:solid 1px}.mat-calendar-body-today{outline:dotted 1px}.mat-calendar-body-cell::before,.mat-calendar-body-cell::after,.mat-calendar-body-selected{background:none}.mat-calendar-body-in-range::before,.mat-calendar-body-comparison-bridge-start::before,.mat-calendar-body-comparison-bridge-end::before{border-top:solid 1px;border-bottom:solid 1px}.mat-calendar-body-range-start::before{border-left:solid 1px}[dir=rtl] .mat-calendar-body-range-start::before{border-left:0;border-right:solid 1px}.mat-calendar-body-range-end::before{border-right:solid 1px}[dir=rtl] .mat-calendar-body-range-end::before{border-right:0;border-left:solid 1px}.mat-calendar-body-in-comparison-range::before{border-top:dashed 1px;border-bottom:dashed 1px}.mat-calendar-body-comparison-start::before{border-left:dashed 1px}[dir=rtl] .mat-calendar-body-comparison-start::before{border-left:0;border-right:dashed 1px}.mat-calendar-body-comparison-end::before{border-right:dashed 1px}[dir=rtl] .mat-calendar-body-comparison-end::before{border-right:0;border-left:dashed 1px}}\n']
    }]
  }], () => [], {
    label: [{
      type: Input
    }],
    rows: [{
      type: Input
    }],
    todayValue: [{
      type: Input
    }],
    startValue: [{
      type: Input
    }],
    endValue: [{
      type: Input
    }],
    labelMinRequiredCells: [{
      type: Input
    }],
    numCols: [{
      type: Input
    }],
    activeCell: [{
      type: Input
    }],
    isRange: [{
      type: Input
    }],
    cellAspectRatio: [{
      type: Input
    }],
    comparisonStart: [{
      type: Input
    }],
    comparisonEnd: [{
      type: Input
    }],
    previewStart: [{
      type: Input
    }],
    previewEnd: [{
      type: Input
    }],
    startDateAccessibleName: [{
      type: Input
    }],
    endDateAccessibleName: [{
      type: Input
    }],
    selectedValueChange: [{
      type: Output
    }],
    previewChange: [{
      type: Output
    }],
    activeDateChange: [{
      type: Output
    }],
    dragStarted: [{
      type: Output
    }],
    dragEnded: [{
      type: Output
    }]
  });
})();
function isTableCell(node) {
  return node?.nodeName === "TD";
}
__name(isTableCell, "isTableCell");
function getCellElement(element) {
  let cell;
  if (isTableCell(element)) {
    cell = element;
  } else if (isTableCell(element.parentNode)) {
    cell = element.parentNode;
  } else if (isTableCell(element.parentNode?.parentNode)) {
    cell = element.parentNode.parentNode;
  }
  return cell?.getAttribute("data-mat-row") != null ? cell : null;
}
__name(getCellElement, "getCellElement");
function isStart(value, start, end) {
  return end !== null && start !== end && value < end && value === start;
}
__name(isStart, "isStart");
function isEnd(value, start, end) {
  return start !== null && start !== end && value >= start && value === end;
}
__name(isEnd, "isEnd");
function isInRange(value, start, end, rangeEnabled) {
  return rangeEnabled && start !== null && end !== null && start !== end && value >= start && value <= end;
}
__name(isInRange, "isInRange");
function getActualTouchTarget(event) {
  const touchLocation = event.changedTouches[0];
  return document.elementFromPoint(touchLocation.clientX, touchLocation.clientY);
}
__name(getActualTouchTarget, "getActualTouchTarget");
var _DateRange = class _DateRange {
  start;
  end;
  /**
   * Ensures that objects with a `start` and `end` property can't be assigned to a variable that
   * expects a `DateRange`
   */
  // tslint:disable-next-line:no-unused-variable
  _disableStructuralEquivalency;
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
};
__name(_DateRange, "DateRange");
var DateRange = _DateRange;
var _MatDateSelectionModel = class _MatDateSelectionModel {
  selection;
  _adapter;
  _selectionChanged = new Subject();
  /** Emits when the selection has changed. */
  selectionChanged = this._selectionChanged;
  constructor(selection, _adapter) {
    this.selection = selection;
    this._adapter = _adapter;
    this.selection = selection;
  }
  /**
   * Updates the current selection in the model.
   * @param value New selection that should be assigned.
   * @param source Object that triggered the selection change.
   */
  updateSelection(value, source) {
    const oldValue = this.selection;
    this.selection = value;
    this._selectionChanged.next({
      selection: value,
      source,
      oldValue
    });
  }
  ngOnDestroy() {
    this._selectionChanged.complete();
  }
  _isValidDateInstance(date) {
    return this._adapter.isDateInstance(date) && this._adapter.isValid(date);
  }
};
__name(_MatDateSelectionModel, "MatDateSelectionModel");
__publicField(_MatDateSelectionModel, "ɵfac", /* @__PURE__ */ __name(function MatDateSelectionModel_Factory(__ngFactoryType__) {
  ɵɵinvalidFactory();
}, "MatDateSelectionModel_Factory"));
__publicField(_MatDateSelectionModel, "ɵprov", ɵɵdefineInjectable({
  token: _MatDateSelectionModel,
  factory: _MatDateSelectionModel.ɵfac
}));
var MatDateSelectionModel = _MatDateSelectionModel;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDateSelectionModel, [{
    type: Injectable
  }], () => [{
    type: void 0
  }, {
    type: DateAdapter
  }], null);
})();
var _MatSingleDateSelectionModel = class _MatSingleDateSelectionModel extends MatDateSelectionModel {
  constructor(adapter) {
    super(null, adapter);
  }
  /**
   * Adds a date to the current selection. In the case of a single date selection, the added date
   * simply overwrites the previous selection
   */
  add(date) {
    super.updateSelection(date, this);
  }
  /** Checks whether the current selection is valid. */
  isValid() {
    return this.selection != null && this._isValidDateInstance(this.selection);
  }
  /**
   * Checks whether the current selection is complete. In the case of a single date selection, this
   * is true if the current selection is not null.
   */
  isComplete() {
    return this.selection != null;
  }
  /** Clones the selection model. */
  clone() {
    const clone = new _MatSingleDateSelectionModel(this._adapter);
    clone.updateSelection(this.selection, this);
    return clone;
  }
};
__name(_MatSingleDateSelectionModel, "MatSingleDateSelectionModel");
__publicField(_MatSingleDateSelectionModel, "ɵfac", /* @__PURE__ */ __name(function MatSingleDateSelectionModel_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatSingleDateSelectionModel)(ɵɵinject(DateAdapter));
}, "MatSingleDateSelectionModel_Factory"));
__publicField(_MatSingleDateSelectionModel, "ɵprov", ɵɵdefineInjectable({
  token: _MatSingleDateSelectionModel,
  factory: _MatSingleDateSelectionModel.ɵfac
}));
var MatSingleDateSelectionModel = _MatSingleDateSelectionModel;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatSingleDateSelectionModel, [{
    type: Injectable
  }], () => [{
    type: DateAdapter
  }], null);
})();
var _MatRangeDateSelectionModel = class _MatRangeDateSelectionModel extends MatDateSelectionModel {
  constructor(adapter) {
    super(new DateRange(null, null), adapter);
  }
  /**
   * Adds a date to the current selection. In the case of a date range selection, the added date
   * fills in the next `null` value in the range. If both the start and the end already have a date,
   * the selection is reset so that the given date is the new `start` and the `end` is null.
   */
  add(date) {
    let {
      start,
      end
    } = this.selection;
    if (start == null) {
      start = date;
    } else if (end == null) {
      end = date;
    } else {
      start = date;
      end = null;
    }
    super.updateSelection(new DateRange(start, end), this);
  }
  /** Checks whether the current selection is valid. */
  isValid() {
    const {
      start,
      end
    } = this.selection;
    if (start == null && end == null) {
      return true;
    }
    if (start != null && end != null) {
      return this._isValidDateInstance(start) && this._isValidDateInstance(end) && this._adapter.compareDate(start, end) <= 0;
    }
    return (start == null || this._isValidDateInstance(start)) && (end == null || this._isValidDateInstance(end));
  }
  /**
   * Checks whether the current selection is complete. In the case of a date range selection, this
   * is true if the current selection has a non-null `start` and `end`.
   */
  isComplete() {
    return this.selection.start != null && this.selection.end != null;
  }
  /** Clones the selection model. */
  clone() {
    const clone = new _MatRangeDateSelectionModel(this._adapter);
    clone.updateSelection(this.selection, this);
    return clone;
  }
};
__name(_MatRangeDateSelectionModel, "MatRangeDateSelectionModel");
__publicField(_MatRangeDateSelectionModel, "ɵfac", /* @__PURE__ */ __name(function MatRangeDateSelectionModel_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatRangeDateSelectionModel)(ɵɵinject(DateAdapter));
}, "MatRangeDateSelectionModel_Factory"));
__publicField(_MatRangeDateSelectionModel, "ɵprov", ɵɵdefineInjectable({
  token: _MatRangeDateSelectionModel,
  factory: _MatRangeDateSelectionModel.ɵfac
}));
var MatRangeDateSelectionModel = _MatRangeDateSelectionModel;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatRangeDateSelectionModel, [{
    type: Injectable
  }], () => [{
    type: DateAdapter
  }], null);
})();
function MAT_SINGLE_DATE_SELECTION_MODEL_FACTORY(parent, adapter) {
  return parent || new MatSingleDateSelectionModel(adapter);
}
__name(MAT_SINGLE_DATE_SELECTION_MODEL_FACTORY, "MAT_SINGLE_DATE_SELECTION_MODEL_FACTORY");
var MAT_SINGLE_DATE_SELECTION_MODEL_PROVIDER = {
  provide: MatDateSelectionModel,
  deps: [[new Optional(), new SkipSelf(), MatDateSelectionModel], DateAdapter],
  useFactory: MAT_SINGLE_DATE_SELECTION_MODEL_FACTORY
};
function MAT_RANGE_DATE_SELECTION_MODEL_FACTORY(parent, adapter) {
  return parent || new MatRangeDateSelectionModel(adapter);
}
__name(MAT_RANGE_DATE_SELECTION_MODEL_FACTORY, "MAT_RANGE_DATE_SELECTION_MODEL_FACTORY");
var MAT_RANGE_DATE_SELECTION_MODEL_PROVIDER = {
  provide: MatDateSelectionModel,
  deps: [[new Optional(), new SkipSelf(), MatDateSelectionModel], DateAdapter],
  useFactory: MAT_RANGE_DATE_SELECTION_MODEL_FACTORY
};
var MAT_DATE_RANGE_SELECTION_STRATEGY = new InjectionToken("MAT_DATE_RANGE_SELECTION_STRATEGY");
var _DefaultMatCalendarRangeStrategy = class _DefaultMatCalendarRangeStrategy {
  _dateAdapter;
  constructor(_dateAdapter) {
    this._dateAdapter = _dateAdapter;
  }
  selectionFinished(date, currentRange) {
    let {
      start,
      end
    } = currentRange;
    if (start == null) {
      start = date;
    } else if (end == null && date && this._dateAdapter.compareDate(date, start) >= 0) {
      end = date;
    } else {
      start = date;
      end = null;
    }
    return new DateRange(start, end);
  }
  createPreview(activeDate, currentRange) {
    let start = null;
    let end = null;
    if (currentRange.start && !currentRange.end && activeDate) {
      start = currentRange.start;
      end = activeDate;
    }
    return new DateRange(start, end);
  }
  createDrag(dragOrigin, originalRange, newDate) {
    let start = originalRange.start;
    let end = originalRange.end;
    if (!start || !end) {
      return null;
    }
    const adapter = this._dateAdapter;
    const isRange = adapter.compareDate(start, end) !== 0;
    const diffYears = adapter.getYear(newDate) - adapter.getYear(dragOrigin);
    const diffMonths = adapter.getMonth(newDate) - adapter.getMonth(dragOrigin);
    const diffDays = adapter.getDate(newDate) - adapter.getDate(dragOrigin);
    if (isRange && adapter.sameDate(dragOrigin, originalRange.start)) {
      start = newDate;
      if (adapter.compareDate(newDate, end) > 0) {
        end = adapter.addCalendarYears(end, diffYears);
        end = adapter.addCalendarMonths(end, diffMonths);
        end = adapter.addCalendarDays(end, diffDays);
      }
    } else if (isRange && adapter.sameDate(dragOrigin, originalRange.end)) {
      end = newDate;
      if (adapter.compareDate(newDate, start) < 0) {
        start = adapter.addCalendarYears(start, diffYears);
        start = adapter.addCalendarMonths(start, diffMonths);
        start = adapter.addCalendarDays(start, diffDays);
      }
    } else {
      start = adapter.addCalendarYears(start, diffYears);
      start = adapter.addCalendarMonths(start, diffMonths);
      start = adapter.addCalendarDays(start, diffDays);
      end = adapter.addCalendarYears(end, diffYears);
      end = adapter.addCalendarMonths(end, diffMonths);
      end = adapter.addCalendarDays(end, diffDays);
    }
    return new DateRange(start, end);
  }
};
__name(_DefaultMatCalendarRangeStrategy, "DefaultMatCalendarRangeStrategy");
__publicField(_DefaultMatCalendarRangeStrategy, "ɵfac", /* @__PURE__ */ __name(function DefaultMatCalendarRangeStrategy_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _DefaultMatCalendarRangeStrategy)(ɵɵinject(DateAdapter));
}, "DefaultMatCalendarRangeStrategy_Factory"));
__publicField(_DefaultMatCalendarRangeStrategy, "ɵprov", ɵɵdefineInjectable({
  token: _DefaultMatCalendarRangeStrategy,
  factory: _DefaultMatCalendarRangeStrategy.ɵfac
}));
var DefaultMatCalendarRangeStrategy = _DefaultMatCalendarRangeStrategy;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(DefaultMatCalendarRangeStrategy, [{
    type: Injectable
  }], () => [{
    type: DateAdapter
  }], null);
})();
function MAT_CALENDAR_RANGE_STRATEGY_PROVIDER_FACTORY(parent, adapter) {
  return parent || new DefaultMatCalendarRangeStrategy(adapter);
}
__name(MAT_CALENDAR_RANGE_STRATEGY_PROVIDER_FACTORY, "MAT_CALENDAR_RANGE_STRATEGY_PROVIDER_FACTORY");
var MAT_CALENDAR_RANGE_STRATEGY_PROVIDER = {
  provide: MAT_DATE_RANGE_SELECTION_STRATEGY,
  deps: [[new Optional(), new SkipSelf(), MAT_DATE_RANGE_SELECTION_STRATEGY], DateAdapter],
  useFactory: MAT_CALENDAR_RANGE_STRATEGY_PROVIDER_FACTORY
};
var DAYS_PER_WEEK = 7;
var uniqueIdCounter = 0;
var _MatMonthView = class _MatMonthView {
  _changeDetectorRef = inject(ChangeDetectorRef);
  _dateFormats = inject(MAT_DATE_FORMATS, {
    optional: true
  });
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dir = inject(Directionality, {
    optional: true
  });
  _rangeStrategy = inject(MAT_DATE_RANGE_SELECTION_STRATEGY, {
    optional: true
  });
  _rerenderSubscription = Subscription.EMPTY;
  /** Flag used to filter out space/enter keyup events that originated outside of the view. */
  _selectionKeyPressed;
  /**
   * The date to display in this month view (everything other than the month and year is ignored).
   */
  get activeDate() {
    return this._activeDate;
  }
  set activeDate(value) {
    const oldActiveDate = this._activeDate;
    const validDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value)) || this._dateAdapter.today();
    this._activeDate = this._dateAdapter.clampDate(validDate, this.minDate, this.maxDate);
    if (!this._hasSameMonthAndYear(oldActiveDate, this._activeDate)) {
      this._init();
    }
  }
  _activeDate;
  /** The currently selected date. */
  get selected() {
    return this._selected;
  }
  set selected(value) {
    if (value instanceof DateRange) {
      this._selected = value;
    } else {
      this._selected = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    }
    this._setRanges(this._selected);
  }
  _selected;
  /** The minimum selectable date. */
  get minDate() {
    return this._minDate;
  }
  set minDate(value) {
    this._minDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _minDate;
  /** The maximum selectable date. */
  get maxDate() {
    return this._maxDate;
  }
  set maxDate(value) {
    this._maxDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _maxDate;
  /** Function used to filter which dates are selectable. */
  dateFilter;
  /** Function that can be used to add custom CSS classes to dates. */
  dateClass;
  /** Start of the comparison range. */
  comparisonStart;
  /** End of the comparison range. */
  comparisonEnd;
  /** ARIA Accessible name of the `<input matStartDate/>` */
  startDateAccessibleName;
  /** ARIA Accessible name of the `<input matEndDate/>` */
  endDateAccessibleName;
  /** Origin of active drag, or null when dragging is not active. */
  activeDrag = null;
  /** Emits when a new date is selected. */
  selectedChange = new EventEmitter();
  /** Emits when any date is selected. */
  _userSelection = new EventEmitter();
  /** Emits when the user initiates a date range drag via mouse or touch. */
  dragStarted = new EventEmitter();
  /**
   * Emits when the user completes or cancels a date range drag.
   * Emits null when the drag was canceled or the newly selected date range if completed.
   */
  dragEnded = new EventEmitter();
  /** Emits when any date is activated. */
  activeDateChange = new EventEmitter();
  /** The body of calendar table */
  _matCalendarBody;
  /** The label for this month (e.g. "January 2017"). */
  _monthLabel;
  /** Grid of calendar cells representing the dates of the month. */
  _weeks;
  /** The number of blank cells in the first row before the 1st of the month. */
  _firstWeekOffset;
  /** Start value of the currently-shown date range. */
  _rangeStart;
  /** End value of the currently-shown date range. */
  _rangeEnd;
  /** Start value of the currently-shown comparison date range. */
  _comparisonRangeStart;
  /** End value of the currently-shown comparison date range. */
  _comparisonRangeEnd;
  /** Start of the preview range. */
  _previewStart;
  /** End of the preview range. */
  _previewEnd;
  /** Whether the user is currently selecting a range of dates. */
  _isRange;
  /** The date of the month that today falls on. Null if today is in another month. */
  _todayDate;
  /** The names of the weekdays. */
  _weekdays;
  constructor() {
    inject(_CdkPrivateStyleLoader).load(_VisuallyHiddenLoader);
    if (typeof ngDevMode === "undefined" || ngDevMode) {
      if (!this._dateAdapter) {
        throw createMissingDateImplError("DateAdapter");
      }
      if (!this._dateFormats) {
        throw createMissingDateImplError("MAT_DATE_FORMATS");
      }
    }
    this._activeDate = this._dateAdapter.today();
  }
  ngAfterContentInit() {
    this._rerenderSubscription = this._dateAdapter.localeChanges.pipe(startWith(null)).subscribe(() => this._init());
  }
  ngOnChanges(changes) {
    const comparisonChange = changes["comparisonStart"] || changes["comparisonEnd"];
    if (comparisonChange && !comparisonChange.firstChange) {
      this._setRanges(this.selected);
    }
    if (changes["activeDrag"] && !this.activeDrag) {
      this._clearPreview();
    }
  }
  ngOnDestroy() {
    this._rerenderSubscription.unsubscribe();
  }
  /** Handles when a new date is selected. */
  _dateSelected(event) {
    const date = event.value;
    const selectedDate = this._getDateFromDayOfMonth(date);
    let rangeStartDate;
    let rangeEndDate;
    if (this._selected instanceof DateRange) {
      rangeStartDate = this._getDateInCurrentMonth(this._selected.start);
      rangeEndDate = this._getDateInCurrentMonth(this._selected.end);
    } else {
      rangeStartDate = rangeEndDate = this._getDateInCurrentMonth(this._selected);
    }
    if (rangeStartDate !== date || rangeEndDate !== date) {
      this.selectedChange.emit(selectedDate);
    }
    this._userSelection.emit({
      value: selectedDate,
      event: event.event
    });
    this._clearPreview();
    this._changeDetectorRef.markForCheck();
  }
  /**
   * Takes the index of a calendar body cell wrapped in an event as argument. For the date that
   * corresponds to the given cell, set `activeDate` to that date and fire `activeDateChange` with
   * that date.
   *
   * This function is used to match each component's model of the active date with the calendar
   * body cell that was focused. It updates its value of `activeDate` synchronously and updates the
   * parent's value asynchronously via the `activeDateChange` event. The child component receives an
   * updated value asynchronously via the `activeCell` Input.
   */
  _updateActiveDate(event) {
    const month = event.value;
    const oldActiveDate = this._activeDate;
    this.activeDate = this._getDateFromDayOfMonth(month);
    if (this._dateAdapter.compareDate(oldActiveDate, this.activeDate)) {
      this.activeDateChange.emit(this._activeDate);
    }
  }
  /** Handles keydown events on the calendar body when calendar is in month view. */
  _handleCalendarBodyKeydown(event) {
    const oldActiveDate = this._activeDate;
    const isRtl = this._isRtl();
    switch (event.keyCode) {
      case LEFT_ARROW:
        this.activeDate = this._dateAdapter.addCalendarDays(this._activeDate, isRtl ? 1 : -1);
        break;
      case RIGHT_ARROW:
        this.activeDate = this._dateAdapter.addCalendarDays(this._activeDate, isRtl ? -1 : 1);
        break;
      case UP_ARROW:
        this.activeDate = this._dateAdapter.addCalendarDays(this._activeDate, -7);
        break;
      case DOWN_ARROW:
        this.activeDate = this._dateAdapter.addCalendarDays(this._activeDate, 7);
        break;
      case HOME:
        this.activeDate = this._dateAdapter.addCalendarDays(this._activeDate, 1 - this._dateAdapter.getDate(this._activeDate));
        break;
      case END:
        this.activeDate = this._dateAdapter.addCalendarDays(this._activeDate, this._dateAdapter.getNumDaysInMonth(this._activeDate) - this._dateAdapter.getDate(this._activeDate));
        break;
      case PAGE_UP:
        this.activeDate = event.altKey ? this._dateAdapter.addCalendarYears(this._activeDate, -1) : this._dateAdapter.addCalendarMonths(this._activeDate, -1);
        break;
      case PAGE_DOWN:
        this.activeDate = event.altKey ? this._dateAdapter.addCalendarYears(this._activeDate, 1) : this._dateAdapter.addCalendarMonths(this._activeDate, 1);
        break;
      case ENTER:
      case SPACE:
        this._selectionKeyPressed = true;
        if (this._canSelect(this._activeDate)) {
          event.preventDefault();
        }
        return;
      case ESCAPE:
        if (this._previewEnd != null && !hasModifierKey(event)) {
          this._clearPreview();
          if (this.activeDrag) {
            this.dragEnded.emit({
              value: null,
              event
            });
          } else {
            this.selectedChange.emit(null);
            this._userSelection.emit({
              value: null,
              event
            });
          }
          event.preventDefault();
          event.stopPropagation();
        }
        return;
      default:
        return;
    }
    if (this._dateAdapter.compareDate(oldActiveDate, this.activeDate)) {
      this.activeDateChange.emit(this.activeDate);
      this._focusActiveCellAfterViewChecked();
    }
    event.preventDefault();
  }
  /** Handles keyup events on the calendar body when calendar is in month view. */
  _handleCalendarBodyKeyup(event) {
    if (event.keyCode === SPACE || event.keyCode === ENTER) {
      if (this._selectionKeyPressed && this._canSelect(this._activeDate)) {
        this._dateSelected({
          value: this._dateAdapter.getDate(this._activeDate),
          event
        });
      }
      this._selectionKeyPressed = false;
    }
  }
  /** Initializes this month view. */
  _init() {
    this._setRanges(this.selected);
    this._todayDate = this._getCellCompareValue(this._dateAdapter.today());
    this._monthLabel = this._dateFormats.display.monthLabel ? this._dateAdapter.format(this.activeDate, this._dateFormats.display.monthLabel) : this._dateAdapter.getMonthNames("short")[this._dateAdapter.getMonth(this.activeDate)].toLocaleUpperCase();
    let firstOfMonth = this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), this._dateAdapter.getMonth(this.activeDate), 1);
    this._firstWeekOffset = (DAYS_PER_WEEK + this._dateAdapter.getDayOfWeek(firstOfMonth) - this._dateAdapter.getFirstDayOfWeek()) % DAYS_PER_WEEK;
    this._initWeekdays();
    this._createWeekCells();
    this._changeDetectorRef.markForCheck();
  }
  /** Focuses the active cell after the microtask queue is empty. */
  _focusActiveCell(movePreview) {
    this._matCalendarBody._focusActiveCell(movePreview);
  }
  /** Focuses the active cell after change detection has run and the microtask queue is empty. */
  _focusActiveCellAfterViewChecked() {
    this._matCalendarBody._scheduleFocusActiveCellAfterViewChecked();
  }
  /** Called when the user has activated a new cell and the preview needs to be updated. */
  _previewChanged({
    event,
    value: cell
  }) {
    if (this._rangeStrategy) {
      const value = cell ? cell.rawValue : null;
      const previewRange = this._rangeStrategy.createPreview(value, this.selected, event);
      this._previewStart = this._getCellCompareValue(previewRange.start);
      this._previewEnd = this._getCellCompareValue(previewRange.end);
      if (this.activeDrag && value) {
        const dragRange = this._rangeStrategy.createDrag?.(this.activeDrag.value, this.selected, value, event);
        if (dragRange) {
          this._previewStart = this._getCellCompareValue(dragRange.start);
          this._previewEnd = this._getCellCompareValue(dragRange.end);
        }
      }
      this._changeDetectorRef.detectChanges();
    }
  }
  /**
   * Called when the user has ended a drag. If the drag/drop was successful,
   * computes and emits the new range selection.
   */
  _dragEnded(event) {
    if (!this.activeDrag) return;
    if (event.value) {
      const dragDropResult = this._rangeStrategy?.createDrag?.(this.activeDrag.value, this.selected, event.value, event.event);
      this.dragEnded.emit({
        value: dragDropResult ?? null,
        event: event.event
      });
    } else {
      this.dragEnded.emit({
        value: null,
        event: event.event
      });
    }
  }
  /**
   * Takes a day of the month and returns a new date in the same month and year as the currently
   *  active date. The returned date will have the same day of the month as the argument date.
   */
  _getDateFromDayOfMonth(dayOfMonth) {
    return this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), this._dateAdapter.getMonth(this.activeDate), dayOfMonth);
  }
  /** Initializes the weekdays. */
  _initWeekdays() {
    const firstDayOfWeek = this._dateAdapter.getFirstDayOfWeek();
    const narrowWeekdays = this._dateAdapter.getDayOfWeekNames("narrow");
    const longWeekdays = this._dateAdapter.getDayOfWeekNames("long");
    let weekdays = longWeekdays.map((long, i) => {
      return {
        long,
        narrow: narrowWeekdays[i],
        id: uniqueIdCounter++
      };
    });
    this._weekdays = weekdays.slice(firstDayOfWeek).concat(weekdays.slice(0, firstDayOfWeek));
  }
  /** Creates MatCalendarCells for the dates in this month. */
  _createWeekCells() {
    const daysInMonth = this._dateAdapter.getNumDaysInMonth(this.activeDate);
    const dateNames = this._dateAdapter.getDateNames();
    this._weeks = [[]];
    for (let i = 0, cell = this._firstWeekOffset; i < daysInMonth; i++, cell++) {
      if (cell == DAYS_PER_WEEK) {
        this._weeks.push([]);
        cell = 0;
      }
      const date = this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), this._dateAdapter.getMonth(this.activeDate), i + 1);
      const enabled = this._shouldEnableDate(date);
      const ariaLabel = this._dateAdapter.format(date, this._dateFormats.display.dateA11yLabel);
      const cellClasses = this.dateClass ? this.dateClass(date, "month") : void 0;
      this._weeks[this._weeks.length - 1].push(new MatCalendarCell(i + 1, dateNames[i], ariaLabel, enabled, cellClasses, this._getCellCompareValue(date), date));
    }
  }
  /** Date filter for the month */
  _shouldEnableDate(date) {
    return !!date && (!this.minDate || this._dateAdapter.compareDate(date, this.minDate) >= 0) && (!this.maxDate || this._dateAdapter.compareDate(date, this.maxDate) <= 0) && (!this.dateFilter || this.dateFilter(date));
  }
  /**
   * Gets the date in this month that the given Date falls on.
   * Returns null if the given Date is in another month.
   */
  _getDateInCurrentMonth(date) {
    return date && this._hasSameMonthAndYear(date, this.activeDate) ? this._dateAdapter.getDate(date) : null;
  }
  /** Checks whether the 2 dates are non-null and fall within the same month of the same year. */
  _hasSameMonthAndYear(d1, d2) {
    return !!(d1 && d2 && this._dateAdapter.getMonth(d1) == this._dateAdapter.getMonth(d2) && this._dateAdapter.getYear(d1) == this._dateAdapter.getYear(d2));
  }
  /** Gets the value that will be used to one cell to another. */
  _getCellCompareValue(date) {
    if (date) {
      const year = this._dateAdapter.getYear(date);
      const month = this._dateAdapter.getMonth(date);
      const day = this._dateAdapter.getDate(date);
      return new Date(year, month, day).getTime();
    }
    return null;
  }
  /** Determines whether the user has the RTL layout direction. */
  _isRtl() {
    return this._dir && this._dir.value === "rtl";
  }
  /** Sets the current range based on a model value. */
  _setRanges(selectedValue) {
    if (selectedValue instanceof DateRange) {
      this._rangeStart = this._getCellCompareValue(selectedValue.start);
      this._rangeEnd = this._getCellCompareValue(selectedValue.end);
      this._isRange = true;
    } else {
      this._rangeStart = this._rangeEnd = this._getCellCompareValue(selectedValue);
      this._isRange = false;
    }
    this._comparisonRangeStart = this._getCellCompareValue(this.comparisonStart);
    this._comparisonRangeEnd = this._getCellCompareValue(this.comparisonEnd);
  }
  /** Gets whether a date can be selected in the month view. */
  _canSelect(date) {
    return !this.dateFilter || this.dateFilter(date);
  }
  /** Clears out preview state. */
  _clearPreview() {
    this._previewStart = this._previewEnd = null;
  }
};
__name(_MatMonthView, "MatMonthView");
__publicField(_MatMonthView, "ɵfac", /* @__PURE__ */ __name(function MatMonthView_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatMonthView)();
}, "MatMonthView_Factory"));
__publicField(_MatMonthView, "ɵcmp", ɵɵdefineComponent({
  type: _MatMonthView,
  selectors: [["mat-month-view"]],
  viewQuery: /* @__PURE__ */ __name(function MatMonthView_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(MatCalendarBody, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._matCalendarBody = _t.first);
    }
  }, "MatMonthView_Query"),
  inputs: {
    activeDate: "activeDate",
    selected: "selected",
    minDate: "minDate",
    maxDate: "maxDate",
    dateFilter: "dateFilter",
    dateClass: "dateClass",
    comparisonStart: "comparisonStart",
    comparisonEnd: "comparisonEnd",
    startDateAccessibleName: "startDateAccessibleName",
    endDateAccessibleName: "endDateAccessibleName",
    activeDrag: "activeDrag"
  },
  outputs: {
    selectedChange: "selectedChange",
    _userSelection: "_userSelection",
    dragStarted: "dragStarted",
    dragEnded: "dragEnded",
    activeDateChange: "activeDateChange"
  },
  exportAs: ["matMonthView"],
  features: [ɵɵNgOnChangesFeature],
  decls: 8,
  vars: 14,
  consts: [["role", "grid", 1, "mat-calendar-table"], [1, "mat-calendar-table-header"], ["scope", "col"], ["aria-hidden", "true"], ["colspan", "7", 1, "mat-calendar-table-header-divider"], ["mat-calendar-body", "", 3, "selectedValueChange", "activeDateChange", "previewChange", "dragStarted", "dragEnded", "keyup", "keydown", "label", "rows", "todayValue", "startValue", "endValue", "comparisonStart", "comparisonEnd", "previewStart", "previewEnd", "isRange", "labelMinRequiredCells", "activeCell", "startDateAccessibleName", "endDateAccessibleName"], [1, "cdk-visually-hidden"]],
  template: /* @__PURE__ */ __name(function MatMonthView_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵelementStart(0, "table", 0)(1, "thead", 1)(2, "tr");
      ɵɵrepeaterCreate(3, MatMonthView_For_4_Template, 5, 2, "th", 2, _forTrack1);
      ɵɵelementEnd();
      ɵɵelementStart(5, "tr", 3);
      ɵɵelement(6, "th", 4);
      ɵɵelementEnd()();
      ɵɵelementStart(7, "tbody", 5);
      ɵɵlistener("selectedValueChange", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_selectedValueChange_7_listener($event) {
        return ctx._dateSelected($event);
      }, "MatMonthView_Template_tbody_selectedValueChange_7_listener"))("activeDateChange", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_activeDateChange_7_listener($event) {
        return ctx._updateActiveDate($event);
      }, "MatMonthView_Template_tbody_activeDateChange_7_listener"))("previewChange", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_previewChange_7_listener($event) {
        return ctx._previewChanged($event);
      }, "MatMonthView_Template_tbody_previewChange_7_listener"))("dragStarted", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_dragStarted_7_listener($event) {
        return ctx.dragStarted.emit($event);
      }, "MatMonthView_Template_tbody_dragStarted_7_listener"))("dragEnded", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_dragEnded_7_listener($event) {
        return ctx._dragEnded($event);
      }, "MatMonthView_Template_tbody_dragEnded_7_listener"))("keyup", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_keyup_7_listener($event) {
        return ctx._handleCalendarBodyKeyup($event);
      }, "MatMonthView_Template_tbody_keyup_7_listener"))("keydown", /* @__PURE__ */ __name(function MatMonthView_Template_tbody_keydown_7_listener($event) {
        return ctx._handleCalendarBodyKeydown($event);
      }, "MatMonthView_Template_tbody_keydown_7_listener"));
      ɵɵelementEnd()();
    }
    if (rf & 2) {
      ɵɵadvance(3);
      ɵɵrepeater(ctx._weekdays);
      ɵɵadvance(4);
      ɵɵproperty("label", ctx._monthLabel)("rows", ctx._weeks)("todayValue", ctx._todayDate)("startValue", ctx._rangeStart)("endValue", ctx._rangeEnd)("comparisonStart", ctx._comparisonRangeStart)("comparisonEnd", ctx._comparisonRangeEnd)("previewStart", ctx._previewStart)("previewEnd", ctx._previewEnd)("isRange", ctx._isRange)("labelMinRequiredCells", 3)("activeCell", ctx._dateAdapter.getDate(ctx.activeDate) - 1)("startDateAccessibleName", ctx.startDateAccessibleName)("endDateAccessibleName", ctx.endDateAccessibleName);
    }
  }, "MatMonthView_Template"),
  dependencies: [MatCalendarBody],
  encapsulation: 2,
  changeDetection: 0
}));
var MatMonthView = _MatMonthView;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatMonthView, [{
    type: Component,
    args: [{
      selector: "mat-month-view",
      exportAs: "matMonthView",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [MatCalendarBody],
      template: '<table class="mat-calendar-table" role="grid">\n  <thead class="mat-calendar-table-header">\n    <tr>\n      @for (day of _weekdays; track day.id) {\n        <th scope="col">\n          <span class="cdk-visually-hidden">{{day.long}}</span>\n          <span aria-hidden="true">{{day.narrow}}</span>\n        </th>\n      }\n    </tr>\n    <tr aria-hidden="true"><th class="mat-calendar-table-header-divider" colspan="7"></th></tr>\n  </thead>\n  <tbody mat-calendar-body\n         [label]="_monthLabel"\n         [rows]="_weeks"\n         [todayValue]="_todayDate!"\n         [startValue]="_rangeStart!"\n         [endValue]="_rangeEnd!"\n         [comparisonStart]="_comparisonRangeStart"\n         [comparisonEnd]="_comparisonRangeEnd"\n         [previewStart]="_previewStart"\n         [previewEnd]="_previewEnd"\n         [isRange]="_isRange"\n         [labelMinRequiredCells]="3"\n         [activeCell]="_dateAdapter.getDate(activeDate) - 1"\n         [startDateAccessibleName]="startDateAccessibleName"\n         [endDateAccessibleName]="endDateAccessibleName"\n         (selectedValueChange)="_dateSelected($event)"\n         (activeDateChange)="_updateActiveDate($event)"\n         (previewChange)="_previewChanged($event)"\n         (dragStarted)="dragStarted.emit($event)"\n         (dragEnded)="_dragEnded($event)"\n         (keyup)="_handleCalendarBodyKeyup($event)"\n         (keydown)="_handleCalendarBodyKeydown($event)">\n  </tbody>\n</table>\n'
    }]
  }], () => [], {
    activeDate: [{
      type: Input
    }],
    selected: [{
      type: Input
    }],
    minDate: [{
      type: Input
    }],
    maxDate: [{
      type: Input
    }],
    dateFilter: [{
      type: Input
    }],
    dateClass: [{
      type: Input
    }],
    comparisonStart: [{
      type: Input
    }],
    comparisonEnd: [{
      type: Input
    }],
    startDateAccessibleName: [{
      type: Input
    }],
    endDateAccessibleName: [{
      type: Input
    }],
    activeDrag: [{
      type: Input
    }],
    selectedChange: [{
      type: Output
    }],
    _userSelection: [{
      type: Output
    }],
    dragStarted: [{
      type: Output
    }],
    dragEnded: [{
      type: Output
    }],
    activeDateChange: [{
      type: Output
    }],
    _matCalendarBody: [{
      type: ViewChild,
      args: [MatCalendarBody]
    }]
  });
})();
var yearsPerPage = 24;
var yearsPerRow = 4;
var _MatMultiYearView = class _MatMultiYearView {
  _changeDetectorRef = inject(ChangeDetectorRef);
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dir = inject(Directionality, {
    optional: true
  });
  _rerenderSubscription = Subscription.EMPTY;
  /** Flag used to filter out space/enter keyup events that originated outside of the view. */
  _selectionKeyPressed;
  /** The date to display in this multi-year view (everything other than the year is ignored). */
  get activeDate() {
    return this._activeDate;
  }
  set activeDate(value) {
    let oldActiveDate = this._activeDate;
    const validDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value)) || this._dateAdapter.today();
    this._activeDate = this._dateAdapter.clampDate(validDate, this.minDate, this.maxDate);
    if (!isSameMultiYearView(this._dateAdapter, oldActiveDate, this._activeDate, this.minDate, this.maxDate)) {
      this._init();
    }
  }
  _activeDate;
  /** The currently selected date. */
  get selected() {
    return this._selected;
  }
  set selected(value) {
    if (value instanceof DateRange) {
      this._selected = value;
    } else {
      this._selected = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    }
    this._setSelectedYear(value);
  }
  _selected;
  /** The minimum selectable date. */
  get minDate() {
    return this._minDate;
  }
  set minDate(value) {
    this._minDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _minDate;
  /** The maximum selectable date. */
  get maxDate() {
    return this._maxDate;
  }
  set maxDate(value) {
    this._maxDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _maxDate;
  /** A function used to filter which dates are selectable. */
  dateFilter;
  /** Function that can be used to add custom CSS classes to date cells. */
  dateClass;
  /** Emits when a new year is selected. */
  selectedChange = new EventEmitter();
  /** Emits the selected year. This doesn't imply a change on the selected date */
  yearSelected = new EventEmitter();
  /** Emits when any date is activated. */
  activeDateChange = new EventEmitter();
  /** The body of calendar table */
  _matCalendarBody;
  /** Grid of calendar cells representing the currently displayed years. */
  _years;
  /** The year that today falls on. */
  _todayYear;
  /** The year of the selected date. Null if the selected date is null. */
  _selectedYear;
  constructor() {
    if (!this._dateAdapter && (typeof ngDevMode === "undefined" || ngDevMode)) {
      throw createMissingDateImplError("DateAdapter");
    }
    this._activeDate = this._dateAdapter.today();
  }
  ngAfterContentInit() {
    this._rerenderSubscription = this._dateAdapter.localeChanges.pipe(startWith(null)).subscribe(() => this._init());
  }
  ngOnDestroy() {
    this._rerenderSubscription.unsubscribe();
  }
  /** Initializes this multi-year view. */
  _init() {
    this._todayYear = this._dateAdapter.getYear(this._dateAdapter.today());
    const activeYear = this._dateAdapter.getYear(this._activeDate);
    const minYearOfPage = activeYear - getActiveOffset(this._dateAdapter, this.activeDate, this.minDate, this.maxDate);
    this._years = [];
    for (let i = 0, row = []; i < yearsPerPage; i++) {
      row.push(minYearOfPage + i);
      if (row.length == yearsPerRow) {
        this._years.push(row.map((year) => this._createCellForYear(year)));
        row = [];
      }
    }
    this._changeDetectorRef.markForCheck();
  }
  /** Handles when a new year is selected. */
  _yearSelected(event) {
    const year = event.value;
    const selectedYear = this._dateAdapter.createDate(year, 0, 1);
    const selectedDate = this._getDateFromYear(year);
    this.yearSelected.emit(selectedYear);
    this.selectedChange.emit(selectedDate);
  }
  /**
   * Takes the index of a calendar body cell wrapped in an event as argument. For the date that
   * corresponds to the given cell, set `activeDate` to that date and fire `activeDateChange` with
   * that date.
   *
   * This function is used to match each component's model of the active date with the calendar
   * body cell that was focused. It updates its value of `activeDate` synchronously and updates the
   * parent's value asynchronously via the `activeDateChange` event. The child component receives an
   * updated value asynchronously via the `activeCell` Input.
   */
  _updateActiveDate(event) {
    const year = event.value;
    const oldActiveDate = this._activeDate;
    this.activeDate = this._getDateFromYear(year);
    if (this._dateAdapter.compareDate(oldActiveDate, this.activeDate)) {
      this.activeDateChange.emit(this.activeDate);
    }
  }
  /** Handles keydown events on the calendar body when calendar is in multi-year view. */
  _handleCalendarBodyKeydown(event) {
    const oldActiveDate = this._activeDate;
    const isRtl = this._isRtl();
    switch (event.keyCode) {
      case LEFT_ARROW:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, isRtl ? 1 : -1);
        break;
      case RIGHT_ARROW:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, isRtl ? -1 : 1);
        break;
      case UP_ARROW:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, -yearsPerRow);
        break;
      case DOWN_ARROW:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, yearsPerRow);
        break;
      case HOME:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, -getActiveOffset(this._dateAdapter, this.activeDate, this.minDate, this.maxDate));
        break;
      case END:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, yearsPerPage - getActiveOffset(this._dateAdapter, this.activeDate, this.minDate, this.maxDate) - 1);
        break;
      case PAGE_UP:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, event.altKey ? -yearsPerPage * 10 : -yearsPerPage);
        break;
      case PAGE_DOWN:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, event.altKey ? yearsPerPage * 10 : yearsPerPage);
        break;
      case ENTER:
      case SPACE:
        this._selectionKeyPressed = true;
        break;
      default:
        return;
    }
    if (this._dateAdapter.compareDate(oldActiveDate, this.activeDate)) {
      this.activeDateChange.emit(this.activeDate);
    }
    this._focusActiveCellAfterViewChecked();
    event.preventDefault();
  }
  /** Handles keyup events on the calendar body when calendar is in multi-year view. */
  _handleCalendarBodyKeyup(event) {
    if (event.keyCode === SPACE || event.keyCode === ENTER) {
      if (this._selectionKeyPressed) {
        this._yearSelected({
          value: this._dateAdapter.getYear(this._activeDate),
          event
        });
      }
      this._selectionKeyPressed = false;
    }
  }
  _getActiveCell() {
    return getActiveOffset(this._dateAdapter, this.activeDate, this.minDate, this.maxDate);
  }
  /** Focuses the active cell after the microtask queue is empty. */
  _focusActiveCell() {
    this._matCalendarBody._focusActiveCell();
  }
  /** Focuses the active cell after change detection has run and the microtask queue is empty. */
  _focusActiveCellAfterViewChecked() {
    this._matCalendarBody._scheduleFocusActiveCellAfterViewChecked();
  }
  /**
   * Takes a year and returns a new date on the same day and month as the currently active date
   *  The returned date will have the same year as the argument date.
   */
  _getDateFromYear(year) {
    const activeMonth = this._dateAdapter.getMonth(this.activeDate);
    const daysInMonth = this._dateAdapter.getNumDaysInMonth(this._dateAdapter.createDate(year, activeMonth, 1));
    const normalizedDate = this._dateAdapter.createDate(year, activeMonth, Math.min(this._dateAdapter.getDate(this.activeDate), daysInMonth));
    return normalizedDate;
  }
  /** Creates an MatCalendarCell for the given year. */
  _createCellForYear(year) {
    const date = this._dateAdapter.createDate(year, 0, 1);
    const yearName = this._dateAdapter.getYearName(date);
    const cellClasses = this.dateClass ? this.dateClass(date, "multi-year") : void 0;
    return new MatCalendarCell(year, yearName, yearName, this._shouldEnableYear(year), cellClasses);
  }
  /** Whether the given year is enabled. */
  _shouldEnableYear(year) {
    if (year === void 0 || year === null || this.maxDate && year > this._dateAdapter.getYear(this.maxDate) || this.minDate && year < this._dateAdapter.getYear(this.minDate)) {
      return false;
    }
    if (!this.dateFilter) {
      return true;
    }
    const firstOfYear = this._dateAdapter.createDate(year, 0, 1);
    for (let date = firstOfYear; this._dateAdapter.getYear(date) == year; date = this._dateAdapter.addCalendarDays(date, 1)) {
      if (this.dateFilter(date)) {
        return true;
      }
    }
    return false;
  }
  /** Determines whether the user has the RTL layout direction. */
  _isRtl() {
    return this._dir && this._dir.value === "rtl";
  }
  /** Sets the currently-highlighted year based on a model value. */
  _setSelectedYear(value) {
    this._selectedYear = null;
    if (value instanceof DateRange) {
      const displayValue = value.start || value.end;
      if (displayValue) {
        this._selectedYear = this._dateAdapter.getYear(displayValue);
      }
    } else if (value) {
      this._selectedYear = this._dateAdapter.getYear(value);
    }
  }
};
__name(_MatMultiYearView, "MatMultiYearView");
__publicField(_MatMultiYearView, "ɵfac", /* @__PURE__ */ __name(function MatMultiYearView_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatMultiYearView)();
}, "MatMultiYearView_Factory"));
__publicField(_MatMultiYearView, "ɵcmp", ɵɵdefineComponent({
  type: _MatMultiYearView,
  selectors: [["mat-multi-year-view"]],
  viewQuery: /* @__PURE__ */ __name(function MatMultiYearView_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(MatCalendarBody, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._matCalendarBody = _t.first);
    }
  }, "MatMultiYearView_Query"),
  inputs: {
    activeDate: "activeDate",
    selected: "selected",
    minDate: "minDate",
    maxDate: "maxDate",
    dateFilter: "dateFilter",
    dateClass: "dateClass"
  },
  outputs: {
    selectedChange: "selectedChange",
    yearSelected: "yearSelected",
    activeDateChange: "activeDateChange"
  },
  exportAs: ["matMultiYearView"],
  decls: 5,
  vars: 7,
  consts: [["role", "grid", 1, "mat-calendar-table"], ["aria-hidden", "true", 1, "mat-calendar-table-header"], ["colspan", "4", 1, "mat-calendar-table-header-divider"], ["mat-calendar-body", "", 3, "selectedValueChange", "activeDateChange", "keyup", "keydown", "rows", "todayValue", "startValue", "endValue", "numCols", "cellAspectRatio", "activeCell"]],
  template: /* @__PURE__ */ __name(function MatMultiYearView_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵelementStart(0, "table", 0)(1, "thead", 1)(2, "tr");
      ɵɵelement(3, "th", 2);
      ɵɵelementEnd()();
      ɵɵelementStart(4, "tbody", 3);
      ɵɵlistener("selectedValueChange", /* @__PURE__ */ __name(function MatMultiYearView_Template_tbody_selectedValueChange_4_listener($event) {
        return ctx._yearSelected($event);
      }, "MatMultiYearView_Template_tbody_selectedValueChange_4_listener"))("activeDateChange", /* @__PURE__ */ __name(function MatMultiYearView_Template_tbody_activeDateChange_4_listener($event) {
        return ctx._updateActiveDate($event);
      }, "MatMultiYearView_Template_tbody_activeDateChange_4_listener"))("keyup", /* @__PURE__ */ __name(function MatMultiYearView_Template_tbody_keyup_4_listener($event) {
        return ctx._handleCalendarBodyKeyup($event);
      }, "MatMultiYearView_Template_tbody_keyup_4_listener"))("keydown", /* @__PURE__ */ __name(function MatMultiYearView_Template_tbody_keydown_4_listener($event) {
        return ctx._handleCalendarBodyKeydown($event);
      }, "MatMultiYearView_Template_tbody_keydown_4_listener"));
      ɵɵelementEnd()();
    }
    if (rf & 2) {
      ɵɵadvance(4);
      ɵɵproperty("rows", ctx._years)("todayValue", ctx._todayYear)("startValue", ctx._selectedYear)("endValue", ctx._selectedYear)("numCols", 4)("cellAspectRatio", 4 / 7)("activeCell", ctx._getActiveCell());
    }
  }, "MatMultiYearView_Template"),
  dependencies: [MatCalendarBody],
  encapsulation: 2,
  changeDetection: 0
}));
var MatMultiYearView = _MatMultiYearView;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatMultiYearView, [{
    type: Component,
    args: [{
      selector: "mat-multi-year-view",
      exportAs: "matMultiYearView",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [MatCalendarBody],
      template: '<table class="mat-calendar-table" role="grid">\n  <thead aria-hidden="true" class="mat-calendar-table-header">\n    <tr><th class="mat-calendar-table-header-divider" colspan="4"></th></tr>\n  </thead>\n  <tbody mat-calendar-body\n         [rows]="_years"\n         [todayValue]="_todayYear"\n         [startValue]="_selectedYear!"\n         [endValue]="_selectedYear!"\n         [numCols]="4"\n         [cellAspectRatio]="4 / 7"\n         [activeCell]="_getActiveCell()"\n         (selectedValueChange)="_yearSelected($event)"\n         (activeDateChange)="_updateActiveDate($event)"\n         (keyup)="_handleCalendarBodyKeyup($event)"\n         (keydown)="_handleCalendarBodyKeydown($event)">\n  </tbody>\n</table>\n'
    }]
  }], () => [], {
    activeDate: [{
      type: Input
    }],
    selected: [{
      type: Input
    }],
    minDate: [{
      type: Input
    }],
    maxDate: [{
      type: Input
    }],
    dateFilter: [{
      type: Input
    }],
    dateClass: [{
      type: Input
    }],
    selectedChange: [{
      type: Output
    }],
    yearSelected: [{
      type: Output
    }],
    activeDateChange: [{
      type: Output
    }],
    _matCalendarBody: [{
      type: ViewChild,
      args: [MatCalendarBody]
    }]
  });
})();
function isSameMultiYearView(dateAdapter, date1, date2, minDate, maxDate) {
  const year1 = dateAdapter.getYear(date1);
  const year2 = dateAdapter.getYear(date2);
  const startingYear = getStartingYear(dateAdapter, minDate, maxDate);
  return Math.floor((year1 - startingYear) / yearsPerPage) === Math.floor((year2 - startingYear) / yearsPerPage);
}
__name(isSameMultiYearView, "isSameMultiYearView");
function getActiveOffset(dateAdapter, activeDate, minDate, maxDate) {
  const activeYear = dateAdapter.getYear(activeDate);
  return euclideanModulo(activeYear - getStartingYear(dateAdapter, minDate, maxDate), yearsPerPage);
}
__name(getActiveOffset, "getActiveOffset");
function getStartingYear(dateAdapter, minDate, maxDate) {
  let startingYear = 0;
  if (maxDate) {
    const maxYear = dateAdapter.getYear(maxDate);
    startingYear = maxYear - yearsPerPage + 1;
  } else if (minDate) {
    startingYear = dateAdapter.getYear(minDate);
  }
  return startingYear;
}
__name(getStartingYear, "getStartingYear");
function euclideanModulo(a, b) {
  return (a % b + b) % b;
}
__name(euclideanModulo, "euclideanModulo");
var _MatYearView = class _MatYearView {
  _changeDetectorRef = inject(ChangeDetectorRef);
  _dateFormats = inject(MAT_DATE_FORMATS, {
    optional: true
  });
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dir = inject(Directionality, {
    optional: true
  });
  _rerenderSubscription = Subscription.EMPTY;
  /** Flag used to filter out space/enter keyup events that originated outside of the view. */
  _selectionKeyPressed;
  /** The date to display in this year view (everything other than the year is ignored). */
  get activeDate() {
    return this._activeDate;
  }
  set activeDate(value) {
    let oldActiveDate = this._activeDate;
    const validDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value)) || this._dateAdapter.today();
    this._activeDate = this._dateAdapter.clampDate(validDate, this.minDate, this.maxDate);
    if (this._dateAdapter.getYear(oldActiveDate) !== this._dateAdapter.getYear(this._activeDate)) {
      this._init();
    }
  }
  _activeDate;
  /** The currently selected date. */
  get selected() {
    return this._selected;
  }
  set selected(value) {
    if (value instanceof DateRange) {
      this._selected = value;
    } else {
      this._selected = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    }
    this._setSelectedMonth(value);
  }
  _selected;
  /** The minimum selectable date. */
  get minDate() {
    return this._minDate;
  }
  set minDate(value) {
    this._minDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _minDate;
  /** The maximum selectable date. */
  get maxDate() {
    return this._maxDate;
  }
  set maxDate(value) {
    this._maxDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _maxDate;
  /** A function used to filter which dates are selectable. */
  dateFilter;
  /** Function that can be used to add custom CSS classes to date cells. */
  dateClass;
  /** Emits when a new month is selected. */
  selectedChange = new EventEmitter();
  /** Emits the selected month. This doesn't imply a change on the selected date */
  monthSelected = new EventEmitter();
  /** Emits when any date is activated. */
  activeDateChange = new EventEmitter();
  /** The body of calendar table */
  _matCalendarBody;
  /** Grid of calendar cells representing the months of the year. */
  _months;
  /** The label for this year (e.g. "2017"). */
  _yearLabel;
  /** The month in this year that today falls on. Null if today is in a different year. */
  _todayMonth;
  /**
   * The month in this year that the selected Date falls on.
   * Null if the selected Date is in a different year.
   */
  _selectedMonth;
  constructor() {
    if (typeof ngDevMode === "undefined" || ngDevMode) {
      if (!this._dateAdapter) {
        throw createMissingDateImplError("DateAdapter");
      }
      if (!this._dateFormats) {
        throw createMissingDateImplError("MAT_DATE_FORMATS");
      }
    }
    this._activeDate = this._dateAdapter.today();
  }
  ngAfterContentInit() {
    this._rerenderSubscription = this._dateAdapter.localeChanges.pipe(startWith(null)).subscribe(() => this._init());
  }
  ngOnDestroy() {
    this._rerenderSubscription.unsubscribe();
  }
  /** Handles when a new month is selected. */
  _monthSelected(event) {
    const month = event.value;
    const selectedMonth = this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), month, 1);
    this.monthSelected.emit(selectedMonth);
    const selectedDate = this._getDateFromMonth(month);
    this.selectedChange.emit(selectedDate);
  }
  /**
   * Takes the index of a calendar body cell wrapped in an event as argument. For the date that
   * corresponds to the given cell, set `activeDate` to that date and fire `activeDateChange` with
   * that date.
   *
   * This function is used to match each component's model of the active date with the calendar
   * body cell that was focused. It updates its value of `activeDate` synchronously and updates the
   * parent's value asynchronously via the `activeDateChange` event. The child component receives an
   * updated value asynchronously via the `activeCell` Input.
   */
  _updateActiveDate(event) {
    const month = event.value;
    const oldActiveDate = this._activeDate;
    this.activeDate = this._getDateFromMonth(month);
    if (this._dateAdapter.compareDate(oldActiveDate, this.activeDate)) {
      this.activeDateChange.emit(this.activeDate);
    }
  }
  /** Handles keydown events on the calendar body when calendar is in year view. */
  _handleCalendarBodyKeydown(event) {
    const oldActiveDate = this._activeDate;
    const isRtl = this._isRtl();
    switch (event.keyCode) {
      case LEFT_ARROW:
        this.activeDate = this._dateAdapter.addCalendarMonths(this._activeDate, isRtl ? 1 : -1);
        break;
      case RIGHT_ARROW:
        this.activeDate = this._dateAdapter.addCalendarMonths(this._activeDate, isRtl ? -1 : 1);
        break;
      case UP_ARROW:
        this.activeDate = this._dateAdapter.addCalendarMonths(this._activeDate, -4);
        break;
      case DOWN_ARROW:
        this.activeDate = this._dateAdapter.addCalendarMonths(this._activeDate, 4);
        break;
      case HOME:
        this.activeDate = this._dateAdapter.addCalendarMonths(this._activeDate, -this._dateAdapter.getMonth(this._activeDate));
        break;
      case END:
        this.activeDate = this._dateAdapter.addCalendarMonths(this._activeDate, 11 - this._dateAdapter.getMonth(this._activeDate));
        break;
      case PAGE_UP:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, event.altKey ? -10 : -1);
        break;
      case PAGE_DOWN:
        this.activeDate = this._dateAdapter.addCalendarYears(this._activeDate, event.altKey ? 10 : 1);
        break;
      case ENTER:
      case SPACE:
        this._selectionKeyPressed = true;
        break;
      default:
        return;
    }
    if (this._dateAdapter.compareDate(oldActiveDate, this.activeDate)) {
      this.activeDateChange.emit(this.activeDate);
      this._focusActiveCellAfterViewChecked();
    }
    event.preventDefault();
  }
  /** Handles keyup events on the calendar body when calendar is in year view. */
  _handleCalendarBodyKeyup(event) {
    if (event.keyCode === SPACE || event.keyCode === ENTER) {
      if (this._selectionKeyPressed) {
        this._monthSelected({
          value: this._dateAdapter.getMonth(this._activeDate),
          event
        });
      }
      this._selectionKeyPressed = false;
    }
  }
  /** Initializes this year view. */
  _init() {
    this._setSelectedMonth(this.selected);
    this._todayMonth = this._getMonthInCurrentYear(this._dateAdapter.today());
    this._yearLabel = this._dateAdapter.getYearName(this.activeDate);
    let monthNames = this._dateAdapter.getMonthNames("short");
    this._months = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]].map((row) => row.map((month) => this._createCellForMonth(month, monthNames[month])));
    this._changeDetectorRef.markForCheck();
  }
  /** Focuses the active cell after the microtask queue is empty. */
  _focusActiveCell() {
    this._matCalendarBody._focusActiveCell();
  }
  /** Schedules the matCalendarBody to focus the active cell after change detection has run */
  _focusActiveCellAfterViewChecked() {
    this._matCalendarBody._scheduleFocusActiveCellAfterViewChecked();
  }
  /**
   * Gets the month in this year that the given Date falls on.
   * Returns null if the given Date is in another year.
   */
  _getMonthInCurrentYear(date) {
    return date && this._dateAdapter.getYear(date) == this._dateAdapter.getYear(this.activeDate) ? this._dateAdapter.getMonth(date) : null;
  }
  /**
   * Takes a month and returns a new date in the same day and year as the currently active date.
   *  The returned date will have the same month as the argument date.
   */
  _getDateFromMonth(month) {
    const normalizedDate = this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), month, 1);
    const daysInMonth = this._dateAdapter.getNumDaysInMonth(normalizedDate);
    return this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), month, Math.min(this._dateAdapter.getDate(this.activeDate), daysInMonth));
  }
  /** Creates an MatCalendarCell for the given month. */
  _createCellForMonth(month, monthName) {
    const date = this._dateAdapter.createDate(this._dateAdapter.getYear(this.activeDate), month, 1);
    const ariaLabel = this._dateAdapter.format(date, this._dateFormats.display.monthYearA11yLabel);
    const cellClasses = this.dateClass ? this.dateClass(date, "year") : void 0;
    return new MatCalendarCell(month, monthName.toLocaleUpperCase(), ariaLabel, this._shouldEnableMonth(month), cellClasses);
  }
  /** Whether the given month is enabled. */
  _shouldEnableMonth(month) {
    const activeYear = this._dateAdapter.getYear(this.activeDate);
    if (month === void 0 || month === null || this._isYearAndMonthAfterMaxDate(activeYear, month) || this._isYearAndMonthBeforeMinDate(activeYear, month)) {
      return false;
    }
    if (!this.dateFilter) {
      return true;
    }
    const firstOfMonth = this._dateAdapter.createDate(activeYear, month, 1);
    for (let date = firstOfMonth; this._dateAdapter.getMonth(date) == month; date = this._dateAdapter.addCalendarDays(date, 1)) {
      if (this.dateFilter(date)) {
        return true;
      }
    }
    return false;
  }
  /**
   * Tests whether the combination month/year is after this.maxDate, considering
   * just the month and year of this.maxDate
   */
  _isYearAndMonthAfterMaxDate(year, month) {
    if (this.maxDate) {
      const maxYear = this._dateAdapter.getYear(this.maxDate);
      const maxMonth = this._dateAdapter.getMonth(this.maxDate);
      return year > maxYear || year === maxYear && month > maxMonth;
    }
    return false;
  }
  /**
   * Tests whether the combination month/year is before this.minDate, considering
   * just the month and year of this.minDate
   */
  _isYearAndMonthBeforeMinDate(year, month) {
    if (this.minDate) {
      const minYear = this._dateAdapter.getYear(this.minDate);
      const minMonth = this._dateAdapter.getMonth(this.minDate);
      return year < minYear || year === minYear && month < minMonth;
    }
    return false;
  }
  /** Determines whether the user has the RTL layout direction. */
  _isRtl() {
    return this._dir && this._dir.value === "rtl";
  }
  /** Sets the currently-selected month based on a model value. */
  _setSelectedMonth(value) {
    if (value instanceof DateRange) {
      this._selectedMonth = this._getMonthInCurrentYear(value.start) || this._getMonthInCurrentYear(value.end);
    } else {
      this._selectedMonth = this._getMonthInCurrentYear(value);
    }
  }
};
__name(_MatYearView, "MatYearView");
__publicField(_MatYearView, "ɵfac", /* @__PURE__ */ __name(function MatYearView_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatYearView)();
}, "MatYearView_Factory"));
__publicField(_MatYearView, "ɵcmp", ɵɵdefineComponent({
  type: _MatYearView,
  selectors: [["mat-year-view"]],
  viewQuery: /* @__PURE__ */ __name(function MatYearView_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(MatCalendarBody, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._matCalendarBody = _t.first);
    }
  }, "MatYearView_Query"),
  inputs: {
    activeDate: "activeDate",
    selected: "selected",
    minDate: "minDate",
    maxDate: "maxDate",
    dateFilter: "dateFilter",
    dateClass: "dateClass"
  },
  outputs: {
    selectedChange: "selectedChange",
    monthSelected: "monthSelected",
    activeDateChange: "activeDateChange"
  },
  exportAs: ["matYearView"],
  decls: 5,
  vars: 9,
  consts: [["role", "grid", 1, "mat-calendar-table"], ["aria-hidden", "true", 1, "mat-calendar-table-header"], ["colspan", "4", 1, "mat-calendar-table-header-divider"], ["mat-calendar-body", "", 3, "selectedValueChange", "activeDateChange", "keyup", "keydown", "label", "rows", "todayValue", "startValue", "endValue", "labelMinRequiredCells", "numCols", "cellAspectRatio", "activeCell"]],
  template: /* @__PURE__ */ __name(function MatYearView_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵelementStart(0, "table", 0)(1, "thead", 1)(2, "tr");
      ɵɵelement(3, "th", 2);
      ɵɵelementEnd()();
      ɵɵelementStart(4, "tbody", 3);
      ɵɵlistener("selectedValueChange", /* @__PURE__ */ __name(function MatYearView_Template_tbody_selectedValueChange_4_listener($event) {
        return ctx._monthSelected($event);
      }, "MatYearView_Template_tbody_selectedValueChange_4_listener"))("activeDateChange", /* @__PURE__ */ __name(function MatYearView_Template_tbody_activeDateChange_4_listener($event) {
        return ctx._updateActiveDate($event);
      }, "MatYearView_Template_tbody_activeDateChange_4_listener"))("keyup", /* @__PURE__ */ __name(function MatYearView_Template_tbody_keyup_4_listener($event) {
        return ctx._handleCalendarBodyKeyup($event);
      }, "MatYearView_Template_tbody_keyup_4_listener"))("keydown", /* @__PURE__ */ __name(function MatYearView_Template_tbody_keydown_4_listener($event) {
        return ctx._handleCalendarBodyKeydown($event);
      }, "MatYearView_Template_tbody_keydown_4_listener"));
      ɵɵelementEnd()();
    }
    if (rf & 2) {
      ɵɵadvance(4);
      ɵɵproperty("label", ctx._yearLabel)("rows", ctx._months)("todayValue", ctx._todayMonth)("startValue", ctx._selectedMonth)("endValue", ctx._selectedMonth)("labelMinRequiredCells", 2)("numCols", 4)("cellAspectRatio", 4 / 7)("activeCell", ctx._dateAdapter.getMonth(ctx.activeDate));
    }
  }, "MatYearView_Template"),
  dependencies: [MatCalendarBody],
  encapsulation: 2,
  changeDetection: 0
}));
var MatYearView = _MatYearView;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatYearView, [{
    type: Component,
    args: [{
      selector: "mat-year-view",
      exportAs: "matYearView",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [MatCalendarBody],
      template: '<table class="mat-calendar-table" role="grid">\n  <thead aria-hidden="true" class="mat-calendar-table-header">\n    <tr><th class="mat-calendar-table-header-divider" colspan="4"></th></tr>\n  </thead>\n  <tbody mat-calendar-body\n         [label]="_yearLabel"\n         [rows]="_months"\n         [todayValue]="_todayMonth!"\n         [startValue]="_selectedMonth!"\n         [endValue]="_selectedMonth!"\n         [labelMinRequiredCells]="2"\n         [numCols]="4"\n         [cellAspectRatio]="4 / 7"\n         [activeCell]="_dateAdapter.getMonth(activeDate)"\n         (selectedValueChange)="_monthSelected($event)"\n         (activeDateChange)="_updateActiveDate($event)"\n         (keyup)="_handleCalendarBodyKeyup($event)"\n         (keydown)="_handleCalendarBodyKeydown($event)">\n  </tbody>\n</table>\n'
    }]
  }], () => [], {
    activeDate: [{
      type: Input
    }],
    selected: [{
      type: Input
    }],
    minDate: [{
      type: Input
    }],
    maxDate: [{
      type: Input
    }],
    dateFilter: [{
      type: Input
    }],
    dateClass: [{
      type: Input
    }],
    selectedChange: [{
      type: Output
    }],
    monthSelected: [{
      type: Output
    }],
    activeDateChange: [{
      type: Output
    }],
    _matCalendarBody: [{
      type: ViewChild,
      args: [MatCalendarBody]
    }]
  });
})();
var _MatCalendarHeader = class _MatCalendarHeader {
  _intl = inject(MatDatepickerIntl);
  calendar = inject(MatCalendar);
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dateFormats = inject(MAT_DATE_FORMATS, {
    optional: true
  });
  _periodButtonText;
  _periodButtonDescription;
  _periodButtonLabel;
  _prevButtonLabel;
  _nextButtonLabel;
  constructor() {
    inject(_CdkPrivateStyleLoader).load(_VisuallyHiddenLoader);
    const changeDetectorRef = inject(ChangeDetectorRef);
    this._updateLabels();
    this.calendar.stateChanges.subscribe(() => {
      this._updateLabels();
      changeDetectorRef.markForCheck();
    });
  }
  /** The display text for the current calendar view. */
  get periodButtonText() {
    return this._periodButtonText;
  }
  /** The aria description for the current calendar view. */
  get periodButtonDescription() {
    return this._periodButtonDescription;
  }
  /** The `aria-label` for changing the calendar view. */
  get periodButtonLabel() {
    return this._periodButtonLabel;
  }
  /** The label for the previous button. */
  get prevButtonLabel() {
    return this._prevButtonLabel;
  }
  /** The label for the next button. */
  get nextButtonLabel() {
    return this._nextButtonLabel;
  }
  /** Handles user clicks on the period label. */
  currentPeriodClicked() {
    this.calendar.currentView = this.calendar.currentView == "month" ? "multi-year" : "month";
  }
  /** Handles user clicks on the previous button. */
  previousClicked() {
    if (this.previousEnabled()) {
      this.calendar.activeDate = this.calendar.currentView == "month" ? this._dateAdapter.addCalendarMonths(this.calendar.activeDate, -1) : this._dateAdapter.addCalendarYears(this.calendar.activeDate, this.calendar.currentView == "year" ? -1 : -yearsPerPage);
    }
  }
  /** Handles user clicks on the next button. */
  nextClicked() {
    if (this.nextEnabled()) {
      this.calendar.activeDate = this.calendar.currentView == "month" ? this._dateAdapter.addCalendarMonths(this.calendar.activeDate, 1) : this._dateAdapter.addCalendarYears(this.calendar.activeDate, this.calendar.currentView == "year" ? 1 : yearsPerPage);
    }
  }
  /** Whether the previous period button is enabled. */
  previousEnabled() {
    if (!this.calendar.minDate) {
      return true;
    }
    return !this.calendar.minDate || !this._isSameView(this.calendar.activeDate, this.calendar.minDate);
  }
  /** Whether the next period button is enabled. */
  nextEnabled() {
    return !this.calendar.maxDate || !this._isSameView(this.calendar.activeDate, this.calendar.maxDate);
  }
  /** Updates the labels for the various sections of the header. */
  _updateLabels() {
    const calendar = this.calendar;
    const intl = this._intl;
    const adapter = this._dateAdapter;
    if (calendar.currentView === "month") {
      this._periodButtonText = adapter.format(calendar.activeDate, this._dateFormats.display.monthYearLabel).toLocaleUpperCase();
      this._periodButtonDescription = adapter.format(calendar.activeDate, this._dateFormats.display.monthYearLabel).toLocaleUpperCase();
      this._periodButtonLabel = intl.switchToMultiYearViewLabel;
      this._prevButtonLabel = intl.prevMonthLabel;
      this._nextButtonLabel = intl.nextMonthLabel;
    } else if (calendar.currentView === "year") {
      this._periodButtonText = adapter.getYearName(calendar.activeDate);
      this._periodButtonDescription = adapter.getYearName(calendar.activeDate);
      this._periodButtonLabel = intl.switchToMonthViewLabel;
      this._prevButtonLabel = intl.prevYearLabel;
      this._nextButtonLabel = intl.nextYearLabel;
    } else {
      this._periodButtonText = intl.formatYearRange(...this._formatMinAndMaxYearLabels());
      this._periodButtonDescription = intl.formatYearRangeLabel(...this._formatMinAndMaxYearLabels());
      this._periodButtonLabel = intl.switchToMonthViewLabel;
      this._prevButtonLabel = intl.prevMultiYearLabel;
      this._nextButtonLabel = intl.nextMultiYearLabel;
    }
  }
  /** Whether the two dates represent the same view in the current view mode (month or year). */
  _isSameView(date1, date2) {
    if (this.calendar.currentView == "month") {
      return this._dateAdapter.getYear(date1) == this._dateAdapter.getYear(date2) && this._dateAdapter.getMonth(date1) == this._dateAdapter.getMonth(date2);
    }
    if (this.calendar.currentView == "year") {
      return this._dateAdapter.getYear(date1) == this._dateAdapter.getYear(date2);
    }
    return isSameMultiYearView(this._dateAdapter, date1, date2, this.calendar.minDate, this.calendar.maxDate);
  }
  /**
   * Format two individual labels for the minimum year and maximum year available in the multi-year
   * calendar view. Returns an array of two strings where the first string is the formatted label
   * for the minimum year, and the second string is the formatted label for the maximum year.
   */
  _formatMinAndMaxYearLabels() {
    const activeYear = this._dateAdapter.getYear(this.calendar.activeDate);
    const minYearOfPage = activeYear - getActiveOffset(this._dateAdapter, this.calendar.activeDate, this.calendar.minDate, this.calendar.maxDate);
    const maxYearOfPage = minYearOfPage + yearsPerPage - 1;
    const minYearLabel = this._dateAdapter.getYearName(this._dateAdapter.createDate(minYearOfPage, 0, 1));
    const maxYearLabel = this._dateAdapter.getYearName(this._dateAdapter.createDate(maxYearOfPage, 0, 1));
    return [minYearLabel, maxYearLabel];
  }
  _periodButtonLabelId = inject(_IdGenerator).getId("mat-calendar-period-label-");
};
__name(_MatCalendarHeader, "MatCalendarHeader");
__publicField(_MatCalendarHeader, "ɵfac", /* @__PURE__ */ __name(function MatCalendarHeader_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatCalendarHeader)();
}, "MatCalendarHeader_Factory"));
__publicField(_MatCalendarHeader, "ɵcmp", ɵɵdefineComponent({
  type: _MatCalendarHeader,
  selectors: [["mat-calendar-header"]],
  exportAs: ["matCalendarHeader"],
  ngContentSelectors: _c1,
  decls: 17,
  vars: 13,
  consts: [[1, "mat-calendar-header"], [1, "mat-calendar-controls"], ["aria-live", "polite", 1, "cdk-visually-hidden", 3, "id"], ["matButton", "", "type", "button", 1, "mat-calendar-period-button", 3, "click"], ["aria-hidden", "true"], ["viewBox", "0 0 10 5", "focusable", "false", "aria-hidden", "true", 1, "mat-calendar-arrow"], ["points", "0,0 5,5 10,0"], [1, "mat-calendar-spacer"], ["matIconButton", "", "type", "button", "disabledInteractive", "", 1, "mat-calendar-previous-button", 3, "click", "disabled", "matTooltip"], ["viewBox", "0 0 24 24", "focusable", "false", "aria-hidden", "true"], ["d", "M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"], ["matIconButton", "", "type", "button", "disabledInteractive", "", 1, "mat-calendar-next-button", 3, "click", "disabled", "matTooltip"], ["d", "M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"]],
  template: /* @__PURE__ */ __name(function MatCalendarHeader_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵprojectionDef();
      ɵɵelementStart(0, "div", 0)(1, "div", 1)(2, "span", 2);
      ɵɵtext(3);
      ɵɵelementEnd();
      ɵɵelementStart(4, "button", 3);
      ɵɵlistener("click", /* @__PURE__ */ __name(function MatCalendarHeader_Template_button_click_4_listener() {
        return ctx.currentPeriodClicked();
      }, "MatCalendarHeader_Template_button_click_4_listener"));
      ɵɵelementStart(5, "span", 4);
      ɵɵtext(6);
      ɵɵelementEnd();
      ɵɵnamespaceSVG();
      ɵɵelementStart(7, "svg", 5);
      ɵɵelement(8, "polygon", 6);
      ɵɵelementEnd()();
      ɵɵnamespaceHTML();
      ɵɵelement(9, "div", 7);
      ɵɵprojection(10);
      ɵɵelementStart(11, "button", 8);
      ɵɵlistener("click", /* @__PURE__ */ __name(function MatCalendarHeader_Template_button_click_11_listener() {
        return ctx.previousClicked();
      }, "MatCalendarHeader_Template_button_click_11_listener"));
      ɵɵnamespaceSVG();
      ɵɵelementStart(12, "svg", 9);
      ɵɵelement(13, "path", 10);
      ɵɵelementEnd()();
      ɵɵnamespaceHTML();
      ɵɵelementStart(14, "button", 11);
      ɵɵlistener("click", /* @__PURE__ */ __name(function MatCalendarHeader_Template_button_click_14_listener() {
        return ctx.nextClicked();
      }, "MatCalendarHeader_Template_button_click_14_listener"));
      ɵɵnamespaceSVG();
      ɵɵelementStart(15, "svg", 9);
      ɵɵelement(16, "path", 12);
      ɵɵelementEnd()()()();
    }
    if (rf & 2) {
      ɵɵadvance(2);
      ɵɵproperty("id", ctx._periodButtonLabelId);
      ɵɵadvance();
      ɵɵtextInterpolate(ctx.periodButtonDescription);
      ɵɵadvance();
      ɵɵattribute("aria-label", ctx.periodButtonLabel)("aria-describedby", ctx._periodButtonLabelId);
      ɵɵadvance(2);
      ɵɵtextInterpolate(ctx.periodButtonText);
      ɵɵadvance();
      ɵɵclassProp("mat-calendar-invert", ctx.calendar.currentView !== "month");
      ɵɵadvance(4);
      ɵɵproperty("disabled", !ctx.previousEnabled())("matTooltip", ctx.prevButtonLabel);
      ɵɵattribute("aria-label", ctx.prevButtonLabel);
      ɵɵadvance(3);
      ɵɵproperty("disabled", !ctx.nextEnabled())("matTooltip", ctx.nextButtonLabel);
      ɵɵattribute("aria-label", ctx.nextButtonLabel);
    }
  }, "MatCalendarHeader_Template"),
  dependencies: [MatButton, MatIconButton, MatTooltip],
  encapsulation: 2,
  changeDetection: 0
}));
var MatCalendarHeader = _MatCalendarHeader;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatCalendarHeader, [{
    type: Component,
    args: [{
      selector: "mat-calendar-header",
      exportAs: "matCalendarHeader",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [MatButton, MatIconButton, MatTooltip],
      template: `<div class="mat-calendar-header">
  <div class="mat-calendar-controls">
    <!-- [Firefox Issue: https://bugzilla.mozilla.org/show_bug.cgi?id=1880533]
      Relocated label next to related button and made visually hidden via cdk-visually-hidden
      to enable label to appear in a11y tree for SR when using Firefox -->
    <span [id]="_periodButtonLabelId" class="cdk-visually-hidden" aria-live="polite">{{periodButtonDescription}}</span>
    <button matButton type="button" class="mat-calendar-period-button"
            (click)="currentPeriodClicked()" [attr.aria-label]="periodButtonLabel"
            [attr.aria-describedby]="_periodButtonLabelId">
      <span aria-hidden="true">{{periodButtonText}}</span>
      <svg class="mat-calendar-arrow" [class.mat-calendar-invert]="calendar.currentView !== 'month'"
           viewBox="0 0 10 5" focusable="false" aria-hidden="true">
           <polygon points="0,0 5,5 10,0"/>
      </svg>
    </button>

    <div class="mat-calendar-spacer"></div>

    <ng-content></ng-content>

    <button matIconButton type="button" class="mat-calendar-previous-button"
            [disabled]="!previousEnabled()" (click)="previousClicked()"
            [matTooltip]="prevButtonLabel" [attr.aria-label]="prevButtonLabel" disabledInteractive>
      <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
       </svg>
    </button>

    <button matIconButton type="button" class="mat-calendar-next-button"
            [disabled]="!nextEnabled()" (click)="nextClicked()"
            [matTooltip]="nextButtonLabel" [attr.aria-label]="nextButtonLabel" disabledInteractive>
      <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
        <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
      </svg>
    </button>
  </div>
</div>
`
    }]
  }], () => [], null);
})();
var _MatCalendar = class _MatCalendar {
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dateFormats = inject(MAT_DATE_FORMATS, {
    optional: true
  });
  _changeDetectorRef = inject(ChangeDetectorRef);
  _elementRef = inject(ElementRef);
  /** An input indicating the type of the header component, if set. */
  headerComponent;
  /** A portal containing the header component type for this calendar. */
  _calendarHeaderPortal;
  _intlChanges;
  /**
   * Used for scheduling that focus should be moved to the active cell on the next tick.
   * We need to schedule it, rather than do it immediately, because we have to wait
   * for Angular to re-evaluate the view children.
   */
  _moveFocusOnNextTick = false;
  /** A date representing the period (month or year) to start the calendar in. */
  get startAt() {
    return this._startAt;
  }
  set startAt(value) {
    this._startAt = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _startAt;
  /** Whether the calendar should be started in month or year view. */
  startView = "month";
  /** The currently selected date. */
  get selected() {
    return this._selected;
  }
  set selected(value) {
    if (value instanceof DateRange) {
      this._selected = value;
    } else {
      this._selected = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    }
  }
  _selected;
  /** The minimum selectable date. */
  get minDate() {
    return this._minDate;
  }
  set minDate(value) {
    this._minDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _minDate;
  /** The maximum selectable date. */
  get maxDate() {
    return this._maxDate;
  }
  set maxDate(value) {
    this._maxDate = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _maxDate;
  /** Function used to filter which dates are selectable. */
  dateFilter;
  /** Function that can be used to add custom CSS classes to dates. */
  dateClass;
  /** Start of the comparison range. */
  comparisonStart;
  /** End of the comparison range. */
  comparisonEnd;
  /** ARIA Accessible name of the `<input matStartDate/>` */
  startDateAccessibleName;
  /** ARIA Accessible name of the `<input matEndDate/>` */
  endDateAccessibleName;
  /** Emits when the currently selected date changes. */
  selectedChange = new EventEmitter();
  /**
   * Emits the year chosen in multiyear view.
   * This doesn't imply a change on the selected date.
   */
  yearSelected = new EventEmitter();
  /**
   * Emits the month chosen in year view.
   * This doesn't imply a change on the selected date.
   */
  monthSelected = new EventEmitter();
  /**
   * Emits when the current view changes.
   */
  viewChanged = new EventEmitter(true);
  /** Emits when any date is selected. */
  _userSelection = new EventEmitter();
  /** Emits a new date range value when the user completes a drag drop operation. */
  _userDragDrop = new EventEmitter();
  /** Reference to the current month view component. */
  monthView;
  /** Reference to the current year view component. */
  yearView;
  /** Reference to the current multi-year view component. */
  multiYearView;
  /**
   * The current active date. This determines which time period is shown and which date is
   * highlighted when using keyboard navigation.
   */
  get activeDate() {
    return this._clampedActiveDate;
  }
  set activeDate(value) {
    this._clampedActiveDate = this._dateAdapter.clampDate(value, this.minDate, this.maxDate);
    this.stateChanges.next();
    this._changeDetectorRef.markForCheck();
  }
  _clampedActiveDate;
  /** Whether the calendar is in month view. */
  get currentView() {
    return this._currentView;
  }
  set currentView(value) {
    const viewChangedResult = this._currentView !== value ? value : null;
    this._currentView = value;
    this._moveFocusOnNextTick = true;
    this._changeDetectorRef.markForCheck();
    if (viewChangedResult) {
      this.stateChanges.next();
      this.viewChanged.emit(viewChangedResult);
    }
  }
  _currentView;
  /** Origin of active drag, or null when dragging is not active. */
  _activeDrag = null;
  /**
   * Emits whenever there is a state change that the header may need to respond to.
   */
  stateChanges = new Subject();
  constructor() {
    if (typeof ngDevMode === "undefined" || ngDevMode) {
      if (!this._dateAdapter) {
        throw createMissingDateImplError("DateAdapter");
      }
      if (!this._dateFormats) {
        throw createMissingDateImplError("MAT_DATE_FORMATS");
      }
    }
    this._intlChanges = inject(MatDatepickerIntl).changes.subscribe(() => {
      this._changeDetectorRef.markForCheck();
      this.stateChanges.next();
    });
  }
  ngAfterContentInit() {
    this._calendarHeaderPortal = new ComponentPortal(this.headerComponent || MatCalendarHeader);
    this.activeDate = this.startAt || this._dateAdapter.today();
    this._currentView = this.startView;
  }
  ngAfterViewChecked() {
    if (this._moveFocusOnNextTick) {
      this._moveFocusOnNextTick = false;
      this.focusActiveCell();
    }
  }
  ngOnDestroy() {
    this._intlChanges.unsubscribe();
    this.stateChanges.complete();
  }
  ngOnChanges(changes) {
    const minDateChange = changes["minDate"] && !this._dateAdapter.sameDate(changes["minDate"].previousValue, changes["minDate"].currentValue) ? changes["minDate"] : void 0;
    const maxDateChange = changes["maxDate"] && !this._dateAdapter.sameDate(changes["maxDate"].previousValue, changes["maxDate"].currentValue) ? changes["maxDate"] : void 0;
    const changeRequiringRerender = minDateChange || maxDateChange || changes["dateFilter"];
    if (changeRequiringRerender && !changeRequiringRerender.firstChange) {
      const view = this._getCurrentViewComponent();
      if (view) {
        if (this._elementRef.nativeElement.contains(_getFocusedElementPierceShadowDom())) {
          this._moveFocusOnNextTick = true;
        }
        this._changeDetectorRef.detectChanges();
        view._init();
      }
    }
    this.stateChanges.next();
  }
  /** Focuses the active date. */
  focusActiveCell() {
    this._getCurrentViewComponent()._focusActiveCell(false);
  }
  /** Updates today's date after an update of the active date */
  updateTodaysDate() {
    this._getCurrentViewComponent()._init();
  }
  /** Handles date selection in the month view. */
  _dateSelected(event) {
    const date = event.value;
    if (this.selected instanceof DateRange || date && !this._dateAdapter.sameDate(date, this.selected)) {
      this.selectedChange.emit(date);
    }
    this._userSelection.emit(event);
  }
  /** Handles year selection in the multiyear view. */
  _yearSelectedInMultiYearView(normalizedYear) {
    this.yearSelected.emit(normalizedYear);
  }
  /** Handles month selection in the year view. */
  _monthSelectedInYearView(normalizedMonth) {
    this.monthSelected.emit(normalizedMonth);
  }
  /** Handles year/month selection in the multi-year/year views. */
  _goToDateInView(date, view) {
    this.activeDate = date;
    this.currentView = view;
  }
  /** Called when the user starts dragging to change a date range. */
  _dragStarted(event) {
    this._activeDrag = event;
  }
  /**
   * Called when a drag completes. It may end in cancelation or in the selection
   * of a new range.
   */
  _dragEnded(event) {
    if (!this._activeDrag) return;
    if (event.value) {
      this._userDragDrop.emit(event);
    }
    this._activeDrag = null;
  }
  /** Returns the component instance that corresponds to the current calendar view. */
  _getCurrentViewComponent() {
    return this.monthView || this.yearView || this.multiYearView;
  }
};
__name(_MatCalendar, "MatCalendar");
__publicField(_MatCalendar, "ɵfac", /* @__PURE__ */ __name(function MatCalendar_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatCalendar)();
}, "MatCalendar_Factory"));
__publicField(_MatCalendar, "ɵcmp", ɵɵdefineComponent({
  type: _MatCalendar,
  selectors: [["mat-calendar"]],
  viewQuery: /* @__PURE__ */ __name(function MatCalendar_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(MatMonthView, 5);
      ɵɵviewQuery(MatYearView, 5);
      ɵɵviewQuery(MatMultiYearView, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx.monthView = _t.first);
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx.yearView = _t.first);
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx.multiYearView = _t.first);
    }
  }, "MatCalendar_Query"),
  hostAttrs: [1, "mat-calendar"],
  inputs: {
    headerComponent: "headerComponent",
    startAt: "startAt",
    startView: "startView",
    selected: "selected",
    minDate: "minDate",
    maxDate: "maxDate",
    dateFilter: "dateFilter",
    dateClass: "dateClass",
    comparisonStart: "comparisonStart",
    comparisonEnd: "comparisonEnd",
    startDateAccessibleName: "startDateAccessibleName",
    endDateAccessibleName: "endDateAccessibleName"
  },
  outputs: {
    selectedChange: "selectedChange",
    yearSelected: "yearSelected",
    monthSelected: "monthSelected",
    viewChanged: "viewChanged",
    _userSelection: "_userSelection",
    _userDragDrop: "_userDragDrop"
  },
  exportAs: ["matCalendar"],
  features: [ɵɵProvidersFeature([MAT_SINGLE_DATE_SELECTION_MODEL_PROVIDER]), ɵɵNgOnChangesFeature],
  decls: 5,
  vars: 2,
  consts: [[3, "cdkPortalOutlet"], ["cdkMonitorSubtreeFocus", "", "tabindex", "-1", 1, "mat-calendar-content"], [3, "activeDate", "selected", "dateFilter", "maxDate", "minDate", "dateClass", "comparisonStart", "comparisonEnd", "startDateAccessibleName", "endDateAccessibleName", "activeDrag"], [3, "activeDate", "selected", "dateFilter", "maxDate", "minDate", "dateClass"], [3, "activeDateChange", "_userSelection", "dragStarted", "dragEnded", "activeDate", "selected", "dateFilter", "maxDate", "minDate", "dateClass", "comparisonStart", "comparisonEnd", "startDateAccessibleName", "endDateAccessibleName", "activeDrag"], [3, "activeDateChange", "monthSelected", "selectedChange", "activeDate", "selected", "dateFilter", "maxDate", "minDate", "dateClass"], [3, "activeDateChange", "yearSelected", "selectedChange", "activeDate", "selected", "dateFilter", "maxDate", "minDate", "dateClass"]],
  template: /* @__PURE__ */ __name(function MatCalendar_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵtemplate(0, MatCalendar_ng_template_0_Template, 0, 0, "ng-template", 0);
      ɵɵelementStart(1, "div", 1);
      ɵɵconditionalCreate(2, MatCalendar_Case_2_Template, 1, 11, "mat-month-view", 2)(3, MatCalendar_Case_3_Template, 1, 6, "mat-year-view", 3)(4, MatCalendar_Case_4_Template, 1, 6, "mat-multi-year-view", 3);
      ɵɵelementEnd();
    }
    if (rf & 2) {
      let tmp_1_0;
      ɵɵproperty("cdkPortalOutlet", ctx._calendarHeaderPortal);
      ɵɵadvance(2);
      ɵɵconditional((tmp_1_0 = ctx.currentView) === "month" ? 2 : tmp_1_0 === "year" ? 3 : tmp_1_0 === "multi-year" ? 4 : -1);
    }
  }, "MatCalendar_Template"),
  dependencies: [CdkPortalOutlet, CdkMonitorFocus, MatMonthView, MatYearView, MatMultiYearView],
  styles: ['.mat-calendar{display:block;line-height:normal;font-family:var(--mat-datepicker-calendar-text-font, var(--mat-sys-body-medium-font));font-size:var(--mat-datepicker-calendar-text-size, var(--mat-sys-body-medium-size))}.mat-calendar-header{padding:8px 8px 0 8px}.mat-calendar-content{padding:0 8px 8px 8px;outline:none}.mat-calendar-controls{display:flex;align-items:center;margin:5% calc(4.7142857143% - 16px)}.mat-calendar-spacer{flex:1 1 auto}.mat-calendar-period-button{min-width:0;margin:0 8px;font-size:var(--mat-datepicker-calendar-period-button-text-size, var(--mat-sys-title-small-size));font-weight:var(--mat-datepicker-calendar-period-button-text-weight, var(--mat-sys-title-small-weight));--mat-button-text-label-text-color: var(--mat-datepicker-calendar-period-button-text-color, var(--mat-sys-on-surface-variant))}.mat-calendar-arrow{display:inline-block;width:10px;height:5px;margin:0 0 0 5px;vertical-align:middle;fill:var(--mat-datepicker-calendar-period-button-icon-color, var(--mat-sys-on-surface-variant))}.mat-calendar-arrow.mat-calendar-invert{transform:rotate(180deg)}[dir=rtl] .mat-calendar-arrow{margin:0 5px 0 0}@media(forced-colors: active){.mat-calendar-arrow{fill:CanvasText}}.mat-datepicker-content .mat-calendar-previous-button:not(.mat-mdc-button-disabled),.mat-datepicker-content .mat-calendar-next-button:not(.mat-mdc-button-disabled){color:var(--mat-datepicker-calendar-navigation-button-icon-color, var(--mat-sys-on-surface-variant))}[dir=rtl] .mat-calendar-previous-button,[dir=rtl] .mat-calendar-next-button{transform:rotate(180deg)}.mat-calendar-table{border-spacing:0;border-collapse:collapse;width:100%}.mat-calendar-table-header th{text-align:center;padding:0 0 8px 0;color:var(--mat-datepicker-calendar-header-text-color, var(--mat-sys-on-surface-variant));font-size:var(--mat-datepicker-calendar-header-text-size, var(--mat-sys-title-small-size));font-weight:var(--mat-datepicker-calendar-header-text-weight, var(--mat-sys-title-small-weight))}.mat-calendar-table-header-divider{position:relative;height:1px}.mat-calendar-table-header-divider::after{content:"";position:absolute;top:0;left:-8px;right:-8px;height:1px;background:var(--mat-datepicker-calendar-header-divider-color, transparent)}.mat-calendar-body-cell-content::before{margin:calc(calc(var(--mat-focus-indicator-border-width, 3px) + 3px)*-1)}.mat-calendar-body-cell:focus .mat-focus-indicator::before{content:""}\n'],
  encapsulation: 2,
  changeDetection: 0
}));
var MatCalendar = _MatCalendar;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatCalendar, [{
    type: Component,
    args: [{
      selector: "mat-calendar",
      host: {
        "class": "mat-calendar"
      },
      exportAs: "matCalendar",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      providers: [MAT_SINGLE_DATE_SELECTION_MODEL_PROVIDER],
      imports: [CdkPortalOutlet, CdkMonitorFocus, MatMonthView, MatYearView, MatMultiYearView],
      template: `<ng-template [cdkPortalOutlet]="_calendarHeaderPortal"></ng-template>

<div class="mat-calendar-content" cdkMonitorSubtreeFocus tabindex="-1">
  @switch (currentView) {
    @case ('month') {
        <mat-month-view
            [(activeDate)]="activeDate"
            [selected]="selected"
            [dateFilter]="dateFilter"
            [maxDate]="maxDate"
            [minDate]="minDate"
            [dateClass]="dateClass"
            [comparisonStart]="comparisonStart"
            [comparisonEnd]="comparisonEnd"
            [startDateAccessibleName]="startDateAccessibleName"
            [endDateAccessibleName]="endDateAccessibleName"
            (_userSelection)="_dateSelected($event)"
            (dragStarted)="_dragStarted($event)"
            (dragEnded)="_dragEnded($event)"
            [activeDrag]="_activeDrag"></mat-month-view>
    }

    @case ('year') {
        <mat-year-view
            [(activeDate)]="activeDate"
            [selected]="selected"
            [dateFilter]="dateFilter"
            [maxDate]="maxDate"
            [minDate]="minDate"
            [dateClass]="dateClass"
            (monthSelected)="_monthSelectedInYearView($event)"
            (selectedChange)="_goToDateInView($event, 'month')"></mat-year-view>
    }

    @case ('multi-year') {
        <mat-multi-year-view
            [(activeDate)]="activeDate"
            [selected]="selected"
            [dateFilter]="dateFilter"
            [maxDate]="maxDate"
            [minDate]="minDate"
            [dateClass]="dateClass"
            (yearSelected)="_yearSelectedInMultiYearView($event)"
            (selectedChange)="_goToDateInView($event, 'year')"></mat-multi-year-view>
    }
  }
</div>
`,
      styles: ['.mat-calendar{display:block;line-height:normal;font-family:var(--mat-datepicker-calendar-text-font, var(--mat-sys-body-medium-font));font-size:var(--mat-datepicker-calendar-text-size, var(--mat-sys-body-medium-size))}.mat-calendar-header{padding:8px 8px 0 8px}.mat-calendar-content{padding:0 8px 8px 8px;outline:none}.mat-calendar-controls{display:flex;align-items:center;margin:5% calc(4.7142857143% - 16px)}.mat-calendar-spacer{flex:1 1 auto}.mat-calendar-period-button{min-width:0;margin:0 8px;font-size:var(--mat-datepicker-calendar-period-button-text-size, var(--mat-sys-title-small-size));font-weight:var(--mat-datepicker-calendar-period-button-text-weight, var(--mat-sys-title-small-weight));--mat-button-text-label-text-color: var(--mat-datepicker-calendar-period-button-text-color, var(--mat-sys-on-surface-variant))}.mat-calendar-arrow{display:inline-block;width:10px;height:5px;margin:0 0 0 5px;vertical-align:middle;fill:var(--mat-datepicker-calendar-period-button-icon-color, var(--mat-sys-on-surface-variant))}.mat-calendar-arrow.mat-calendar-invert{transform:rotate(180deg)}[dir=rtl] .mat-calendar-arrow{margin:0 5px 0 0}@media(forced-colors: active){.mat-calendar-arrow{fill:CanvasText}}.mat-datepicker-content .mat-calendar-previous-button:not(.mat-mdc-button-disabled),.mat-datepicker-content .mat-calendar-next-button:not(.mat-mdc-button-disabled){color:var(--mat-datepicker-calendar-navigation-button-icon-color, var(--mat-sys-on-surface-variant))}[dir=rtl] .mat-calendar-previous-button,[dir=rtl] .mat-calendar-next-button{transform:rotate(180deg)}.mat-calendar-table{border-spacing:0;border-collapse:collapse;width:100%}.mat-calendar-table-header th{text-align:center;padding:0 0 8px 0;color:var(--mat-datepicker-calendar-header-text-color, var(--mat-sys-on-surface-variant));font-size:var(--mat-datepicker-calendar-header-text-size, var(--mat-sys-title-small-size));font-weight:var(--mat-datepicker-calendar-header-text-weight, var(--mat-sys-title-small-weight))}.mat-calendar-table-header-divider{position:relative;height:1px}.mat-calendar-table-header-divider::after{content:"";position:absolute;top:0;left:-8px;right:-8px;height:1px;background:var(--mat-datepicker-calendar-header-divider-color, transparent)}.mat-calendar-body-cell-content::before{margin:calc(calc(var(--mat-focus-indicator-border-width, 3px) + 3px)*-1)}.mat-calendar-body-cell:focus .mat-focus-indicator::before{content:""}\n']
    }]
  }], () => [], {
    headerComponent: [{
      type: Input
    }],
    startAt: [{
      type: Input
    }],
    startView: [{
      type: Input
    }],
    selected: [{
      type: Input
    }],
    minDate: [{
      type: Input
    }],
    maxDate: [{
      type: Input
    }],
    dateFilter: [{
      type: Input
    }],
    dateClass: [{
      type: Input
    }],
    comparisonStart: [{
      type: Input
    }],
    comparisonEnd: [{
      type: Input
    }],
    startDateAccessibleName: [{
      type: Input
    }],
    endDateAccessibleName: [{
      type: Input
    }],
    selectedChange: [{
      type: Output
    }],
    yearSelected: [{
      type: Output
    }],
    monthSelected: [{
      type: Output
    }],
    viewChanged: [{
      type: Output
    }],
    _userSelection: [{
      type: Output
    }],
    _userDragDrop: [{
      type: Output
    }],
    monthView: [{
      type: ViewChild,
      args: [MatMonthView]
    }],
    yearView: [{
      type: ViewChild,
      args: [MatYearView]
    }],
    multiYearView: [{
      type: ViewChild,
      args: [MatMultiYearView]
    }]
  });
})();
var MAT_DATEPICKER_SCROLL_STRATEGY = new InjectionToken("mat-datepicker-scroll-strategy", {
  providedIn: "root",
  factory: /* @__PURE__ */ __name(() => {
    const injector = inject(Injector);
    return () => createRepositionScrollStrategy(injector);
  }, "factory")
});
function MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY(_overlay) {
  const injector = inject(Injector);
  return () => createRepositionScrollStrategy(injector);
}
__name(MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY, "MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY");
var MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY_PROVIDER = {
  provide: MAT_DATEPICKER_SCROLL_STRATEGY,
  deps: [],
  useFactory: MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY
};
var _MatDatepickerContent = class _MatDatepickerContent {
  _elementRef = inject(ElementRef);
  _animationsDisabled = _animationsDisabled();
  _changeDetectorRef = inject(ChangeDetectorRef);
  _globalModel = inject(MatDateSelectionModel);
  _dateAdapter = inject(DateAdapter);
  _ngZone = inject(NgZone);
  _rangeSelectionStrategy = inject(MAT_DATE_RANGE_SELECTION_STRATEGY, {
    optional: true
  });
  _stateChanges;
  _model;
  _eventCleanups;
  _animationFallback;
  /** Reference to the internal calendar component. */
  _calendar;
  /**
   * Theme color of the internal calendar. This API is supported in M2 themes
   * only, it has no effect in M3 themes. For color customization in M3, see https://material.angular.dev/components/datepicker/styling.
   *
   * For information on applying color variants in M3, see
   * https://material.angular.dev/guide/material-2-theming#optional-add-backwards-compatibility-styles-for-color-variants
   */
  color;
  /** Reference to the datepicker that created the overlay. */
  datepicker;
  /** Start of the comparison range. */
  comparisonStart;
  /** End of the comparison range. */
  comparisonEnd;
  /** ARIA Accessible name of the `<input matStartDate/>` */
  startDateAccessibleName;
  /** ARIA Accessible name of the `<input matEndDate/>` */
  endDateAccessibleName;
  /** Whether the datepicker is above or below the input. */
  _isAbove;
  /** Emits when an animation has finished. */
  _animationDone = new Subject();
  /** Whether there is an in-progress animation. */
  _isAnimating = false;
  /** Text for the close button. */
  _closeButtonText;
  /** Whether the close button currently has focus. */
  _closeButtonFocused;
  /** Portal with projected action buttons. */
  _actionsPortal = null;
  /** Id of the label for the `role="dialog"` element. */
  _dialogLabelId;
  constructor() {
    inject(_CdkPrivateStyleLoader).load(_VisuallyHiddenLoader);
    this._closeButtonText = inject(MatDatepickerIntl).closeCalendarLabel;
    if (!this._animationsDisabled) {
      const element = this._elementRef.nativeElement;
      const renderer = inject(Renderer2);
      this._eventCleanups = this._ngZone.runOutsideAngular(() => [renderer.listen(element, "animationstart", this._handleAnimationEvent), renderer.listen(element, "animationend", this._handleAnimationEvent), renderer.listen(element, "animationcancel", this._handleAnimationEvent)]);
    }
  }
  ngAfterViewInit() {
    this._stateChanges = this.datepicker.stateChanges.subscribe(() => {
      this._changeDetectorRef.markForCheck();
    });
    this._calendar.focusActiveCell();
  }
  ngOnDestroy() {
    clearTimeout(this._animationFallback);
    this._eventCleanups?.forEach((cleanup) => cleanup());
    this._stateChanges?.unsubscribe();
    this._animationDone.complete();
  }
  _handleUserSelection(event) {
    const selection = this._model.selection;
    const value = event.value;
    const isRange = selection instanceof DateRange;
    if (isRange && this._rangeSelectionStrategy) {
      const newSelection = this._rangeSelectionStrategy.selectionFinished(value, selection, event.event);
      this._model.updateSelection(newSelection, this);
    } else if (value && (isRange || !this._dateAdapter.sameDate(value, selection))) {
      this._model.add(value);
    }
    if ((!this._model || this._model.isComplete()) && !this._actionsPortal) {
      this.datepicker.close();
    }
  }
  _handleUserDragDrop(event) {
    this._model.updateSelection(event.value, this);
  }
  _startExitAnimation() {
    this._elementRef.nativeElement.classList.add("mat-datepicker-content-exit");
    if (this._animationsDisabled) {
      this._animationDone.next();
    } else {
      clearTimeout(this._animationFallback);
      this._animationFallback = setTimeout(() => {
        if (!this._isAnimating) {
          this._animationDone.next();
        }
      }, 200);
    }
  }
  _handleAnimationEvent = /* @__PURE__ */ __name((event) => {
    const element = this._elementRef.nativeElement;
    if (event.target !== element || !event.animationName.startsWith("_mat-datepicker-content")) {
      return;
    }
    clearTimeout(this._animationFallback);
    this._isAnimating = event.type === "animationstart";
    element.classList.toggle("mat-datepicker-content-animating", this._isAnimating);
    if (!this._isAnimating) {
      this._animationDone.next();
    }
  }, "_handleAnimationEvent");
  _getSelected() {
    return this._model.selection;
  }
  /** Applies the current pending selection to the global model. */
  _applyPendingSelection() {
    if (this._model !== this._globalModel) {
      this._globalModel.updateSelection(this._model.selection, this);
    }
  }
  /**
   * Assigns a new portal containing the datepicker actions.
   * @param portal Portal with the actions to be assigned.
   * @param forceRerender Whether a re-render of the portal should be triggered. This isn't
   * necessary if the portal is assigned during initialization, but it may be required if it's
   * added at a later point.
   */
  _assignActions(portal, forceRerender) {
    this._model = portal ? this._globalModel.clone() : this._globalModel;
    this._actionsPortal = portal;
    if (forceRerender) {
      this._changeDetectorRef.detectChanges();
    }
  }
};
__name(_MatDatepickerContent, "MatDatepickerContent");
__publicField(_MatDatepickerContent, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerContent_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerContent)();
}, "MatDatepickerContent_Factory"));
__publicField(_MatDatepickerContent, "ɵcmp", ɵɵdefineComponent({
  type: _MatDatepickerContent,
  selectors: [["mat-datepicker-content"]],
  viewQuery: /* @__PURE__ */ __name(function MatDatepickerContent_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(MatCalendar, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._calendar = _t.first);
    }
  }, "MatDatepickerContent_Query"),
  hostAttrs: [1, "mat-datepicker-content"],
  hostVars: 6,
  hostBindings: /* @__PURE__ */ __name(function MatDatepickerContent_HostBindings(rf, ctx) {
    if (rf & 2) {
      ɵɵclassMap(ctx.color ? "mat-" + ctx.color : "");
      ɵɵclassProp("mat-datepicker-content-touch", ctx.datepicker.touchUi)("mat-datepicker-content-animations-enabled", !ctx._animationsDisabled);
    }
  }, "MatDatepickerContent_HostBindings"),
  inputs: {
    color: "color"
  },
  exportAs: ["matDatepickerContent"],
  decls: 5,
  vars: 26,
  consts: [["cdkTrapFocus", "", "role", "dialog", 1, "mat-datepicker-content-container"], [3, "yearSelected", "monthSelected", "viewChanged", "_userSelection", "_userDragDrop", "id", "startAt", "startView", "minDate", "maxDate", "dateFilter", "headerComponent", "selected", "dateClass", "comparisonStart", "comparisonEnd", "startDateAccessibleName", "endDateAccessibleName"], [3, "cdkPortalOutlet"], ["type", "button", "matButton", "elevated", 1, "mat-datepicker-close-button", 3, "focus", "blur", "click", "color"]],
  template: /* @__PURE__ */ __name(function MatDatepickerContent_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵelementStart(0, "div", 0)(1, "mat-calendar", 1);
      ɵɵlistener("yearSelected", /* @__PURE__ */ __name(function MatDatepickerContent_Template_mat_calendar_yearSelected_1_listener($event) {
        return ctx.datepicker._selectYear($event);
      }, "MatDatepickerContent_Template_mat_calendar_yearSelected_1_listener"))("monthSelected", /* @__PURE__ */ __name(function MatDatepickerContent_Template_mat_calendar_monthSelected_1_listener($event) {
        return ctx.datepicker._selectMonth($event);
      }, "MatDatepickerContent_Template_mat_calendar_monthSelected_1_listener"))("viewChanged", /* @__PURE__ */ __name(function MatDatepickerContent_Template_mat_calendar_viewChanged_1_listener($event) {
        return ctx.datepicker._viewChanged($event);
      }, "MatDatepickerContent_Template_mat_calendar_viewChanged_1_listener"))("_userSelection", /* @__PURE__ */ __name(function MatDatepickerContent_Template_mat_calendar__userSelection_1_listener($event) {
        return ctx._handleUserSelection($event);
      }, "MatDatepickerContent_Template_mat_calendar__userSelection_1_listener"))("_userDragDrop", /* @__PURE__ */ __name(function MatDatepickerContent_Template_mat_calendar__userDragDrop_1_listener($event) {
        return ctx._handleUserDragDrop($event);
      }, "MatDatepickerContent_Template_mat_calendar__userDragDrop_1_listener"));
      ɵɵelementEnd();
      ɵɵtemplate(2, MatDatepickerContent_ng_template_2_Template, 0, 0, "ng-template", 2);
      ɵɵelementStart(3, "button", 3);
      ɵɵlistener("focus", /* @__PURE__ */ __name(function MatDatepickerContent_Template_button_focus_3_listener() {
        return ctx._closeButtonFocused = true;
      }, "MatDatepickerContent_Template_button_focus_3_listener"))("blur", /* @__PURE__ */ __name(function MatDatepickerContent_Template_button_blur_3_listener() {
        return ctx._closeButtonFocused = false;
      }, "MatDatepickerContent_Template_button_blur_3_listener"))("click", /* @__PURE__ */ __name(function MatDatepickerContent_Template_button_click_3_listener() {
        return ctx.datepicker.close();
      }, "MatDatepickerContent_Template_button_click_3_listener"));
      ɵɵtext(4);
      ɵɵelementEnd()();
    }
    if (rf & 2) {
      ɵɵclassProp("mat-datepicker-content-container-with-custom-header", ctx.datepicker.calendarHeaderComponent)("mat-datepicker-content-container-with-actions", ctx._actionsPortal);
      ɵɵattribute("aria-modal", true)("aria-labelledby", ctx._dialogLabelId ?? void 0);
      ɵɵadvance();
      ɵɵclassMap(ctx.datepicker.panelClass);
      ɵɵproperty("id", ctx.datepicker.id)("startAt", ctx.datepicker.startAt)("startView", ctx.datepicker.startView)("minDate", ctx.datepicker._getMinDate())("maxDate", ctx.datepicker._getMaxDate())("dateFilter", ctx.datepicker._getDateFilter())("headerComponent", ctx.datepicker.calendarHeaderComponent)("selected", ctx._getSelected())("dateClass", ctx.datepicker.dateClass)("comparisonStart", ctx.comparisonStart)("comparisonEnd", ctx.comparisonEnd)("startDateAccessibleName", ctx.startDateAccessibleName)("endDateAccessibleName", ctx.endDateAccessibleName);
      ɵɵadvance();
      ɵɵproperty("cdkPortalOutlet", ctx._actionsPortal);
      ɵɵadvance();
      ɵɵclassProp("cdk-visually-hidden", !ctx._closeButtonFocused);
      ɵɵproperty("color", ctx.color || "primary");
      ɵɵadvance();
      ɵɵtextInterpolate(ctx._closeButtonText);
    }
  }, "MatDatepickerContent_Template"),
  dependencies: [CdkTrapFocus, MatCalendar, CdkPortalOutlet, MatButton],
  styles: ["@keyframes _mat-datepicker-content-dropdown-enter{from{opacity:0;transform:scaleY(0.8)}to{opacity:1;transform:none}}@keyframes _mat-datepicker-content-dialog-enter{from{opacity:0;transform:scale(0.8)}to{opacity:1;transform:none}}@keyframes _mat-datepicker-content-exit{from{opacity:1}to{opacity:0}}.mat-datepicker-content{display:block;background-color:var(--mat-datepicker-calendar-container-background-color, var(--mat-sys-surface-container-high));color:var(--mat-datepicker-calendar-container-text-color, var(--mat-sys-on-surface));box-shadow:var(--mat-datepicker-calendar-container-elevation-shadow, 0px 0px 0px 0px rgba(0, 0, 0, 0.2), 0px 0px 0px 0px rgba(0, 0, 0, 0.14), 0px 0px 0px 0px rgba(0, 0, 0, 0.12));border-radius:var(--mat-datepicker-calendar-container-shape, var(--mat-sys-corner-large))}.mat-datepicker-content.mat-datepicker-content-animations-enabled{animation:_mat-datepicker-content-dropdown-enter 120ms cubic-bezier(0, 0, 0.2, 1)}.mat-datepicker-content .mat-calendar{width:296px;height:354px}.mat-datepicker-content .mat-datepicker-content-container-with-custom-header .mat-calendar{height:auto}.mat-datepicker-content .mat-datepicker-close-button{position:absolute;top:100%;left:0;margin-top:8px}.mat-datepicker-content-animating .mat-datepicker-content .mat-datepicker-close-button{display:none}.mat-datepicker-content-container{display:flex;flex-direction:column;justify-content:space-between}.mat-datepicker-content-touch{display:block;max-height:80vh;box-shadow:var(--mat-datepicker-calendar-container-touch-elevation-shadow, 0px 0px 0px 0px rgba(0, 0, 0, 0.2), 0px 0px 0px 0px rgba(0, 0, 0, 0.14), 0px 0px 0px 0px rgba(0, 0, 0, 0.12));border-radius:var(--mat-datepicker-calendar-container-touch-shape, var(--mat-sys-corner-extra-large));position:relative;overflow:visible}.mat-datepicker-content-touch.mat-datepicker-content-animations-enabled{animation:_mat-datepicker-content-dialog-enter 150ms cubic-bezier(0, 0, 0.2, 1)}.mat-datepicker-content-touch .mat-datepicker-content-container{min-height:312px;max-height:788px;min-width:250px;max-width:750px}.mat-datepicker-content-touch .mat-calendar{width:100%;height:auto}.mat-datepicker-content-exit.mat-datepicker-content-animations-enabled{animation:_mat-datepicker-content-exit 100ms linear}@media all and (orientation: landscape){.mat-datepicker-content-touch .mat-datepicker-content-container{width:64vh;height:80vh}}@media all and (orientation: portrait){.mat-datepicker-content-touch .mat-datepicker-content-container{width:80vw;height:100vw}.mat-datepicker-content-touch .mat-datepicker-content-container-with-actions{height:115vw}}\n"],
  encapsulation: 2,
  changeDetection: 0
}));
var MatDatepickerContent = _MatDatepickerContent;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerContent, [{
    type: Component,
    args: [{
      selector: "mat-datepicker-content",
      host: {
        "class": "mat-datepicker-content",
        "[class]": 'color ? "mat-" + color : ""',
        "[class.mat-datepicker-content-touch]": "datepicker.touchUi",
        "[class.mat-datepicker-content-animations-enabled]": "!_animationsDisabled"
      },
      exportAs: "matDatepickerContent",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [CdkTrapFocus, MatCalendar, CdkPortalOutlet, MatButton],
      template: `<div
  cdkTrapFocus
  role="dialog"
  [attr.aria-modal]="true"
  [attr.aria-labelledby]="_dialogLabelId ?? undefined"
  class="mat-datepicker-content-container"
  [class.mat-datepicker-content-container-with-custom-header]="datepicker.calendarHeaderComponent"
  [class.mat-datepicker-content-container-with-actions]="_actionsPortal">
  <mat-calendar
    [id]="datepicker.id"
    [class]="datepicker.panelClass"
    [startAt]="datepicker.startAt"
    [startView]="datepicker.startView"
    [minDate]="datepicker._getMinDate()"
    [maxDate]="datepicker._getMaxDate()"
    [dateFilter]="datepicker._getDateFilter()"
    [headerComponent]="datepicker.calendarHeaderComponent"
    [selected]="_getSelected()"
    [dateClass]="datepicker.dateClass"
    [comparisonStart]="comparisonStart"
    [comparisonEnd]="comparisonEnd"
    [startDateAccessibleName]="startDateAccessibleName"
    [endDateAccessibleName]="endDateAccessibleName"
    (yearSelected)="datepicker._selectYear($event)"
    (monthSelected)="datepicker._selectMonth($event)"
    (viewChanged)="datepicker._viewChanged($event)"
    (_userSelection)="_handleUserSelection($event)"
    (_userDragDrop)="_handleUserDragDrop($event)"></mat-calendar>

  <ng-template [cdkPortalOutlet]="_actionsPortal"></ng-template>

  <!-- Invisible close button for screen reader users. -->
  <button
    type="button"
    matButton="elevated"
    [color]="color || 'primary'"
    class="mat-datepicker-close-button"
    [class.cdk-visually-hidden]="!_closeButtonFocused"
    (focus)="_closeButtonFocused = true"
    (blur)="_closeButtonFocused = false"
    (click)="datepicker.close()">{{ _closeButtonText }}</button>
</div>
`,
      styles: ["@keyframes _mat-datepicker-content-dropdown-enter{from{opacity:0;transform:scaleY(0.8)}to{opacity:1;transform:none}}@keyframes _mat-datepicker-content-dialog-enter{from{opacity:0;transform:scale(0.8)}to{opacity:1;transform:none}}@keyframes _mat-datepicker-content-exit{from{opacity:1}to{opacity:0}}.mat-datepicker-content{display:block;background-color:var(--mat-datepicker-calendar-container-background-color, var(--mat-sys-surface-container-high));color:var(--mat-datepicker-calendar-container-text-color, var(--mat-sys-on-surface));box-shadow:var(--mat-datepicker-calendar-container-elevation-shadow, 0px 0px 0px 0px rgba(0, 0, 0, 0.2), 0px 0px 0px 0px rgba(0, 0, 0, 0.14), 0px 0px 0px 0px rgba(0, 0, 0, 0.12));border-radius:var(--mat-datepicker-calendar-container-shape, var(--mat-sys-corner-large))}.mat-datepicker-content.mat-datepicker-content-animations-enabled{animation:_mat-datepicker-content-dropdown-enter 120ms cubic-bezier(0, 0, 0.2, 1)}.mat-datepicker-content .mat-calendar{width:296px;height:354px}.mat-datepicker-content .mat-datepicker-content-container-with-custom-header .mat-calendar{height:auto}.mat-datepicker-content .mat-datepicker-close-button{position:absolute;top:100%;left:0;margin-top:8px}.mat-datepicker-content-animating .mat-datepicker-content .mat-datepicker-close-button{display:none}.mat-datepicker-content-container{display:flex;flex-direction:column;justify-content:space-between}.mat-datepicker-content-touch{display:block;max-height:80vh;box-shadow:var(--mat-datepicker-calendar-container-touch-elevation-shadow, 0px 0px 0px 0px rgba(0, 0, 0, 0.2), 0px 0px 0px 0px rgba(0, 0, 0, 0.14), 0px 0px 0px 0px rgba(0, 0, 0, 0.12));border-radius:var(--mat-datepicker-calendar-container-touch-shape, var(--mat-sys-corner-extra-large));position:relative;overflow:visible}.mat-datepicker-content-touch.mat-datepicker-content-animations-enabled{animation:_mat-datepicker-content-dialog-enter 150ms cubic-bezier(0, 0, 0.2, 1)}.mat-datepicker-content-touch .mat-datepicker-content-container{min-height:312px;max-height:788px;min-width:250px;max-width:750px}.mat-datepicker-content-touch .mat-calendar{width:100%;height:auto}.mat-datepicker-content-exit.mat-datepicker-content-animations-enabled{animation:_mat-datepicker-content-exit 100ms linear}@media all and (orientation: landscape){.mat-datepicker-content-touch .mat-datepicker-content-container{width:64vh;height:80vh}}@media all and (orientation: portrait){.mat-datepicker-content-touch .mat-datepicker-content-container{width:80vw;height:100vw}.mat-datepicker-content-touch .mat-datepicker-content-container-with-actions{height:115vw}}\n"]
    }]
  }], () => [], {
    _calendar: [{
      type: ViewChild,
      args: [MatCalendar]
    }],
    color: [{
      type: Input
    }]
  });
})();
var _MatDatepickerBase = class _MatDatepickerBase {
  _injector = inject(Injector);
  _viewContainerRef = inject(ViewContainerRef);
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dir = inject(Directionality, {
    optional: true
  });
  _model = inject(MatDateSelectionModel);
  _animationsDisabled = _animationsDisabled();
  _scrollStrategy = inject(MAT_DATEPICKER_SCROLL_STRATEGY);
  _inputStateChanges = Subscription.EMPTY;
  _document = inject(DOCUMENT);
  /** An input indicating the type of the custom header component for the calendar, if set. */
  calendarHeaderComponent;
  /** The date to open the calendar to initially. */
  get startAt() {
    return this._startAt || (this.datepickerInput ? this.datepickerInput.getStartValue() : null);
  }
  set startAt(value) {
    this._startAt = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
  }
  _startAt;
  /** The view that the calendar should start in. */
  startView = "month";
  /**
   * Theme color of the datepicker's calendar. This API is supported in M2 themes only, it
   * has no effect in M3 themes. For color customization in M3, see https://material.angular.dev/components/datepicker/styling.
   *
   * For information on applying color variants in M3, see
   * https://material.angular.dev/guide/material-2-theming#optional-add-backwards-compatibility-styles-for-color-variants
   */
  get color() {
    return this._color || (this.datepickerInput ? this.datepickerInput.getThemePalette() : void 0);
  }
  set color(value) {
    this._color = value;
  }
  _color;
  /**
   * Whether the calendar UI is in touch mode. In touch mode the calendar opens in a dialog rather
   * than a dropdown and elements have more padding to allow for bigger touch targets.
   */
  touchUi = false;
  /** Whether the datepicker pop-up should be disabled. */
  get disabled() {
    return this._disabled === void 0 && this.datepickerInput ? this.datepickerInput.disabled : !!this._disabled;
  }
  set disabled(value) {
    if (value !== this._disabled) {
      this._disabled = value;
      this.stateChanges.next(void 0);
    }
  }
  _disabled;
  /** Preferred position of the datepicker in the X axis. */
  xPosition = "start";
  /** Preferred position of the datepicker in the Y axis. */
  yPosition = "below";
  /**
   * Whether to restore focus to the previously-focused element when the calendar is closed.
   * Note that automatic focus restoration is an accessibility feature and it is recommended that
   * you provide your own equivalent, if you decide to turn it off.
   */
  restoreFocus = true;
  /**
   * Emits selected year in multiyear view.
   * This doesn't imply a change on the selected date.
   */
  yearSelected = new EventEmitter();
  /**
   * Emits selected month in year view.
   * This doesn't imply a change on the selected date.
   */
  monthSelected = new EventEmitter();
  /**
   * Emits when the current view changes.
   */
  viewChanged = new EventEmitter(true);
  /** Function that can be used to add custom CSS classes to dates. */
  dateClass;
  /** Emits when the datepicker has been opened. */
  openedStream = new EventEmitter();
  /** Emits when the datepicker has been closed. */
  closedStream = new EventEmitter();
  /** Classes to be passed to the date picker panel. */
  get panelClass() {
    return this._panelClass;
  }
  set panelClass(value) {
    this._panelClass = coerceStringArray(value);
  }
  _panelClass;
  /** Whether the calendar is open. */
  get opened() {
    return this._opened;
  }
  set opened(value) {
    if (value) {
      this.open();
    } else {
      this.close();
    }
  }
  _opened = false;
  /** The id for the datepicker calendar. */
  id = inject(_IdGenerator).getId("mat-datepicker-");
  /** The minimum selectable date. */
  _getMinDate() {
    return this.datepickerInput && this.datepickerInput.min;
  }
  /** The maximum selectable date. */
  _getMaxDate() {
    return this.datepickerInput && this.datepickerInput.max;
  }
  _getDateFilter() {
    return this.datepickerInput && this.datepickerInput.dateFilter;
  }
  /** A reference to the overlay into which we've rendered the calendar. */
  _overlayRef;
  /** Reference to the component instance rendered in the overlay. */
  _componentRef;
  /** The element that was focused before the datepicker was opened. */
  _focusedElementBeforeOpen = null;
  /** Unique class that will be added to the backdrop so that the test harnesses can look it up. */
  _backdropHarnessClass = `${this.id}-backdrop`;
  /** Currently-registered actions portal. */
  _actionsPortal;
  /** The input element this datepicker is associated with. */
  datepickerInput;
  /** Emits when the datepicker's state changes. */
  stateChanges = new Subject();
  _changeDetectorRef = inject(ChangeDetectorRef);
  constructor() {
    if (!this._dateAdapter && (typeof ngDevMode === "undefined" || ngDevMode)) {
      throw createMissingDateImplError("DateAdapter");
    }
    this._model.selectionChanged.subscribe(() => {
      this._changeDetectorRef.markForCheck();
    });
  }
  ngOnChanges(changes) {
    const positionChange = changes["xPosition"] || changes["yPosition"];
    if (positionChange && !positionChange.firstChange && this._overlayRef) {
      const positionStrategy = this._overlayRef.getConfig().positionStrategy;
      if (positionStrategy instanceof FlexibleConnectedPositionStrategy) {
        this._setConnectedPositions(positionStrategy);
        if (this.opened) {
          this._overlayRef.updatePosition();
        }
      }
    }
    this.stateChanges.next(void 0);
  }
  ngOnDestroy() {
    this._destroyOverlay();
    this.close();
    this._inputStateChanges.unsubscribe();
    this.stateChanges.complete();
  }
  /** Selects the given date */
  select(date) {
    this._model.add(date);
  }
  /** Emits the selected year in multiyear view */
  _selectYear(normalizedYear) {
    this.yearSelected.emit(normalizedYear);
  }
  /** Emits selected month in year view */
  _selectMonth(normalizedMonth) {
    this.monthSelected.emit(normalizedMonth);
  }
  /** Emits changed view */
  _viewChanged(view) {
    this.viewChanged.emit(view);
  }
  /**
   * Register an input with this datepicker.
   * @param input The datepicker input to register with this datepicker.
   * @returns Selection model that the input should hook itself up to.
   */
  registerInput(input) {
    if (this.datepickerInput && (typeof ngDevMode === "undefined" || ngDevMode)) {
      throw Error("A MatDatepicker can only be associated with a single input.");
    }
    this._inputStateChanges.unsubscribe();
    this.datepickerInput = input;
    this._inputStateChanges = input.stateChanges.subscribe(() => this.stateChanges.next(void 0));
    return this._model;
  }
  /**
   * Registers a portal containing action buttons with the datepicker.
   * @param portal Portal to be registered.
   */
  registerActions(portal) {
    if (this._actionsPortal && (typeof ngDevMode === "undefined" || ngDevMode)) {
      throw Error("A MatDatepicker can only be associated with a single actions row.");
    }
    this._actionsPortal = portal;
    this._componentRef?.instance._assignActions(portal, true);
  }
  /**
   * Removes a portal containing action buttons from the datepicker.
   * @param portal Portal to be removed.
   */
  removeActions(portal) {
    if (portal === this._actionsPortal) {
      this._actionsPortal = null;
      this._componentRef?.instance._assignActions(null, true);
    }
  }
  /** Open the calendar. */
  open() {
    if (this._opened || this.disabled || this._componentRef?.instance._isAnimating) {
      return;
    }
    if (!this.datepickerInput && (typeof ngDevMode === "undefined" || ngDevMode)) {
      throw Error("Attempted to open an MatDatepicker with no associated input.");
    }
    this._focusedElementBeforeOpen = _getFocusedElementPierceShadowDom();
    this._openOverlay();
    this._opened = true;
    this.openedStream.emit();
  }
  /** Close the calendar. */
  close() {
    if (!this._opened || this._componentRef?.instance._isAnimating) {
      return;
    }
    const canRestoreFocus = this.restoreFocus && this._focusedElementBeforeOpen && typeof this._focusedElementBeforeOpen.focus === "function";
    const completeClose = /* @__PURE__ */ __name(() => {
      if (this._opened) {
        this._opened = false;
        this.closedStream.emit();
      }
    }, "completeClose");
    if (this._componentRef) {
      const {
        instance,
        location
      } = this._componentRef;
      instance._animationDone.pipe(take(1)).subscribe(() => {
        const activeElement = this._document.activeElement;
        if (canRestoreFocus && (!activeElement || activeElement === this._document.activeElement || location.nativeElement.contains(activeElement))) {
          this._focusedElementBeforeOpen.focus();
        }
        this._focusedElementBeforeOpen = null;
        this._destroyOverlay();
      });
      instance._startExitAnimation();
    }
    if (canRestoreFocus) {
      setTimeout(completeClose);
    } else {
      completeClose();
    }
  }
  /** Applies the current pending selection on the overlay to the model. */
  _applyPendingSelection() {
    this._componentRef?.instance?._applyPendingSelection();
  }
  /** Forwards relevant values from the datepicker to the datepicker content inside the overlay. */
  _forwardContentValues(instance) {
    instance.datepicker = this;
    instance.color = this.color;
    instance._dialogLabelId = this.datepickerInput.getOverlayLabelId();
    instance._assignActions(this._actionsPortal, false);
  }
  /** Opens the overlay with the calendar. */
  _openOverlay() {
    this._destroyOverlay();
    const isDialog = this.touchUi;
    const portal = new ComponentPortal(MatDatepickerContent, this._viewContainerRef);
    const overlayRef = this._overlayRef = createOverlayRef(this._injector, new OverlayConfig({
      positionStrategy: isDialog ? this._getDialogStrategy() : this._getDropdownStrategy(),
      hasBackdrop: true,
      backdropClass: [isDialog ? "cdk-overlay-dark-backdrop" : "mat-overlay-transparent-backdrop", this._backdropHarnessClass],
      direction: this._dir || "ltr",
      scrollStrategy: isDialog ? createBlockScrollStrategy(this._injector) : this._scrollStrategy(),
      panelClass: `mat-datepicker-${isDialog ? "dialog" : "popup"}`,
      disableAnimations: this._animationsDisabled
    }));
    this._getCloseStream(overlayRef).subscribe((event) => {
      if (event) {
        event.preventDefault();
      }
      this.close();
    });
    overlayRef.keydownEvents().subscribe((event) => {
      const keyCode = event.keyCode;
      if (keyCode === UP_ARROW || keyCode === DOWN_ARROW || keyCode === LEFT_ARROW || keyCode === RIGHT_ARROW || keyCode === PAGE_UP || keyCode === PAGE_DOWN) {
        event.preventDefault();
      }
    });
    this._componentRef = overlayRef.attach(portal);
    this._forwardContentValues(this._componentRef.instance);
    if (!isDialog) {
      afterNextRender(() => {
        overlayRef.updatePosition();
      }, {
        injector: this._injector
      });
    }
  }
  /** Destroys the current overlay. */
  _destroyOverlay() {
    if (this._overlayRef) {
      this._overlayRef.dispose();
      this._overlayRef = this._componentRef = null;
    }
  }
  /** Gets a position strategy that will open the calendar as a dropdown. */
  _getDialogStrategy() {
    return createGlobalPositionStrategy(this._injector).centerHorizontally().centerVertically();
  }
  /** Gets a position strategy that will open the calendar as a dropdown. */
  _getDropdownStrategy() {
    const strategy = createFlexibleConnectedPositionStrategy(this._injector, this.datepickerInput.getConnectedOverlayOrigin()).withTransformOriginOn(".mat-datepicker-content").withFlexibleDimensions(false).withViewportMargin(8).withLockedPosition();
    return this._setConnectedPositions(strategy);
  }
  /** Sets the positions of the datepicker in dropdown mode based on the current configuration. */
  _setConnectedPositions(strategy) {
    const primaryX = this.xPosition === "end" ? "end" : "start";
    const secondaryX = primaryX === "start" ? "end" : "start";
    const primaryY = this.yPosition === "above" ? "bottom" : "top";
    const secondaryY = primaryY === "top" ? "bottom" : "top";
    return strategy.withPositions([{
      originX: primaryX,
      originY: secondaryY,
      overlayX: primaryX,
      overlayY: primaryY
    }, {
      originX: primaryX,
      originY: primaryY,
      overlayX: primaryX,
      overlayY: secondaryY
    }, {
      originX: secondaryX,
      originY: secondaryY,
      overlayX: secondaryX,
      overlayY: primaryY
    }, {
      originX: secondaryX,
      originY: primaryY,
      overlayX: secondaryX,
      overlayY: secondaryY
    }]);
  }
  /** Gets an observable that will emit when the overlay is supposed to be closed. */
  _getCloseStream(overlayRef) {
    const ctrlShiftMetaModifiers = ["ctrlKey", "shiftKey", "metaKey"];
    return merge(overlayRef.backdropClick(), overlayRef.detachments(), overlayRef.keydownEvents().pipe(filter((event) => {
      return event.keyCode === ESCAPE && !hasModifierKey(event) || this.datepickerInput && hasModifierKey(event, "altKey") && event.keyCode === UP_ARROW && ctrlShiftMetaModifiers.every((modifier) => !hasModifierKey(event, modifier));
    })));
  }
};
__name(_MatDatepickerBase, "MatDatepickerBase");
__publicField(_MatDatepickerBase, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerBase_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerBase)();
}, "MatDatepickerBase_Factory"));
__publicField(_MatDatepickerBase, "ɵdir", ɵɵdefineDirective({
  type: _MatDatepickerBase,
  inputs: {
    calendarHeaderComponent: "calendarHeaderComponent",
    startAt: "startAt",
    startView: "startView",
    color: "color",
    touchUi: [2, "touchUi", "touchUi", booleanAttribute],
    disabled: [2, "disabled", "disabled", booleanAttribute],
    xPosition: "xPosition",
    yPosition: "yPosition",
    restoreFocus: [2, "restoreFocus", "restoreFocus", booleanAttribute],
    dateClass: "dateClass",
    panelClass: "panelClass",
    opened: [2, "opened", "opened", booleanAttribute]
  },
  outputs: {
    yearSelected: "yearSelected",
    monthSelected: "monthSelected",
    viewChanged: "viewChanged",
    openedStream: "opened",
    closedStream: "closed"
  },
  features: [ɵɵNgOnChangesFeature]
}));
var MatDatepickerBase = _MatDatepickerBase;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerBase, [{
    type: Directive
  }], () => [], {
    calendarHeaderComponent: [{
      type: Input
    }],
    startAt: [{
      type: Input
    }],
    startView: [{
      type: Input
    }],
    color: [{
      type: Input
    }],
    touchUi: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    disabled: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    xPosition: [{
      type: Input
    }],
    yPosition: [{
      type: Input
    }],
    restoreFocus: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    yearSelected: [{
      type: Output
    }],
    monthSelected: [{
      type: Output
    }],
    viewChanged: [{
      type: Output
    }],
    dateClass: [{
      type: Input
    }],
    openedStream: [{
      type: Output,
      args: ["opened"]
    }],
    closedStream: [{
      type: Output,
      args: ["closed"]
    }],
    panelClass: [{
      type: Input
    }],
    opened: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }]
  });
})();
var _MatDatepicker = class _MatDatepicker extends MatDatepickerBase {
};
__name(_MatDatepicker, "MatDatepicker");
__publicField(_MatDatepicker, "ɵfac", /* @__PURE__ */ (() => {
  let ɵMatDatepicker_BaseFactory;
  return /* @__PURE__ */ __name(function MatDatepicker_Factory(__ngFactoryType__) {
    return (ɵMatDatepicker_BaseFactory || (ɵMatDatepicker_BaseFactory = ɵɵgetInheritedFactory(_MatDatepicker)))(__ngFactoryType__ || _MatDatepicker);
  }, "MatDatepicker_Factory");
})());
__publicField(_MatDatepicker, "ɵcmp", ɵɵdefineComponent({
  type: _MatDatepicker,
  selectors: [["mat-datepicker"]],
  exportAs: ["matDatepicker"],
  features: [ɵɵProvidersFeature([MAT_SINGLE_DATE_SELECTION_MODEL_PROVIDER, {
    provide: MatDatepickerBase,
    useExisting: _MatDatepicker
  }]), ɵɵInheritDefinitionFeature],
  decls: 0,
  vars: 0,
  template: /* @__PURE__ */ __name(function MatDatepicker_Template(rf, ctx) {
  }, "MatDatepicker_Template"),
  encapsulation: 2,
  changeDetection: 0
}));
var MatDatepicker = _MatDatepicker;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepicker, [{
    type: Component,
    args: [{
      selector: "mat-datepicker",
      template: "",
      exportAs: "matDatepicker",
      changeDetection: ChangeDetectionStrategy.OnPush,
      encapsulation: ViewEncapsulation.None,
      providers: [MAT_SINGLE_DATE_SELECTION_MODEL_PROVIDER, {
        provide: MatDatepickerBase,
        useExisting: MatDatepicker
      }]
    }]
  }], null, null);
})();
var _MatDatepickerInputEvent = class _MatDatepickerInputEvent {
  target;
  targetElement;
  /** The new value for the target datepicker input. */
  value;
  constructor(target, targetElement) {
    this.target = target;
    this.targetElement = targetElement;
    this.value = this.target.value;
  }
};
__name(_MatDatepickerInputEvent, "MatDatepickerInputEvent");
var MatDatepickerInputEvent = _MatDatepickerInputEvent;
var _MatDatepickerInputBase = class _MatDatepickerInputBase {
  _elementRef = inject(ElementRef);
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _dateFormats = inject(MAT_DATE_FORMATS, {
    optional: true
  });
  /** Whether the component has been initialized. */
  _isInitialized;
  /** The value of the input. */
  get value() {
    return this._model ? this._getValueFromModel(this._model.selection) : this._pendingValue;
  }
  set value(value) {
    this._assignValueProgrammatically(value);
  }
  _model;
  /** Whether the datepicker-input is disabled. */
  get disabled() {
    return !!this._disabled || this._parentDisabled();
  }
  set disabled(value) {
    const newValue = value;
    const element = this._elementRef.nativeElement;
    if (this._disabled !== newValue) {
      this._disabled = newValue;
      this.stateChanges.next(void 0);
    }
    if (newValue && this._isInitialized && element.blur) {
      element.blur();
    }
  }
  _disabled;
  /** Emits when a `change` event is fired on this `<input>`. */
  dateChange = new EventEmitter();
  /** Emits when an `input` event is fired on this `<input>`. */
  dateInput = new EventEmitter();
  /** Emits when the internal state has changed */
  stateChanges = new Subject();
  _onTouched = /* @__PURE__ */ __name(() => {
  }, "_onTouched");
  _validatorOnChange = /* @__PURE__ */ __name(() => {
  }, "_validatorOnChange");
  _cvaOnChange = /* @__PURE__ */ __name(() => {
  }, "_cvaOnChange");
  _valueChangesSubscription = Subscription.EMPTY;
  _localeSubscription = Subscription.EMPTY;
  /**
   * Since the value is kept on the model which is assigned in an Input,
   * we might get a value before we have a model. This property keeps track
   * of the value until we have somewhere to assign it.
   */
  _pendingValue;
  /** The form control validator for whether the input parses. */
  _parseValidator = /* @__PURE__ */ __name(() => {
    return this._lastValueValid ? null : {
      "matDatepickerParse": {
        "text": this._elementRef.nativeElement.value
      }
    };
  }, "_parseValidator");
  /** The form control validator for the date filter. */
  _filterValidator = /* @__PURE__ */ __name((control) => {
    const controlValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(control.value));
    return !controlValue || this._matchesFilter(controlValue) ? null : {
      "matDatepickerFilter": true
    };
  }, "_filterValidator");
  /** The form control validator for the min date. */
  _minValidator = /* @__PURE__ */ __name((control) => {
    const controlValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(control.value));
    const min = this._getMinDate();
    return !min || !controlValue || this._dateAdapter.compareDate(min, controlValue) <= 0 ? null : {
      "matDatepickerMin": {
        "min": min,
        "actual": controlValue
      }
    };
  }, "_minValidator");
  /** The form control validator for the max date. */
  _maxValidator = /* @__PURE__ */ __name((control) => {
    const controlValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(control.value));
    const max = this._getMaxDate();
    return !max || !controlValue || this._dateAdapter.compareDate(max, controlValue) >= 0 ? null : {
      "matDatepickerMax": {
        "max": max,
        "actual": controlValue
      }
    };
  }, "_maxValidator");
  /** Gets the base validator functions. */
  _getValidators() {
    return [this._parseValidator, this._minValidator, this._maxValidator, this._filterValidator];
  }
  /** Registers a date selection model with the input. */
  _registerModel(model) {
    this._model = model;
    this._valueChangesSubscription.unsubscribe();
    if (this._pendingValue) {
      this._assignValue(this._pendingValue);
    }
    this._valueChangesSubscription = this._model.selectionChanged.subscribe((event) => {
      if (this._shouldHandleChangeEvent(event)) {
        const value = this._getValueFromModel(event.selection);
        this._lastValueValid = this._isValidValue(value);
        this._cvaOnChange(value);
        this._onTouched();
        this._formatValue(value);
        this.dateInput.emit(new MatDatepickerInputEvent(this, this._elementRef.nativeElement));
        this.dateChange.emit(new MatDatepickerInputEvent(this, this._elementRef.nativeElement));
      }
    });
  }
  /** Whether the last value set on the input was valid. */
  _lastValueValid = false;
  constructor() {
    if (typeof ngDevMode === "undefined" || ngDevMode) {
      if (!this._dateAdapter) {
        throw createMissingDateImplError("DateAdapter");
      }
      if (!this._dateFormats) {
        throw createMissingDateImplError("MAT_DATE_FORMATS");
      }
    }
    this._localeSubscription = this._dateAdapter.localeChanges.subscribe(() => {
      this._assignValueProgrammatically(this.value);
    });
  }
  ngAfterViewInit() {
    this._isInitialized = true;
  }
  ngOnChanges(changes) {
    if (dateInputsHaveChanged(changes, this._dateAdapter)) {
      this.stateChanges.next(void 0);
    }
  }
  ngOnDestroy() {
    this._valueChangesSubscription.unsubscribe();
    this._localeSubscription.unsubscribe();
    this.stateChanges.complete();
  }
  /** @docs-private */
  registerOnValidatorChange(fn) {
    this._validatorOnChange = fn;
  }
  /** @docs-private */
  validate(c) {
    return this._validator ? this._validator(c) : null;
  }
  // Implemented as part of ControlValueAccessor.
  writeValue(value) {
    this._assignValueProgrammatically(value);
  }
  // Implemented as part of ControlValueAccessor.
  registerOnChange(fn) {
    this._cvaOnChange = fn;
  }
  // Implemented as part of ControlValueAccessor.
  registerOnTouched(fn) {
    this._onTouched = fn;
  }
  // Implemented as part of ControlValueAccessor.
  setDisabledState(isDisabled) {
    this.disabled = isDisabled;
  }
  _onKeydown(event) {
    const ctrlShiftMetaModifiers = ["ctrlKey", "shiftKey", "metaKey"];
    const isAltDownArrow = hasModifierKey(event, "altKey") && event.keyCode === DOWN_ARROW && ctrlShiftMetaModifiers.every((modifier) => !hasModifierKey(event, modifier));
    if (isAltDownArrow && !this._elementRef.nativeElement.readOnly) {
      this._openPopup();
      event.preventDefault();
    }
  }
  _onInput(event) {
    const value = event.target.value;
    const lastValueWasValid = this._lastValueValid;
    let date = this._dateAdapter.parse(value, this._dateFormats.parse.dateInput);
    this._lastValueValid = this._isValidValue(date);
    date = this._dateAdapter.getValidDateOrNull(date);
    const hasChanged = !this._dateAdapter.sameDate(date, this.value);
    if (!date || hasChanged) {
      this._cvaOnChange(date);
    } else {
      if (value && !this.value) {
        this._cvaOnChange(date);
      }
      if (lastValueWasValid !== this._lastValueValid) {
        this._validatorOnChange();
      }
    }
    if (hasChanged) {
      this._assignValue(date);
      this.dateInput.emit(new MatDatepickerInputEvent(this, this._elementRef.nativeElement));
    }
  }
  _onChange() {
    this.dateChange.emit(new MatDatepickerInputEvent(this, this._elementRef.nativeElement));
  }
  /** Handles blur events on the input. */
  _onBlur() {
    if (this.value) {
      this._formatValue(this.value);
    }
    this._onTouched();
  }
  /** Formats a value and sets it on the input element. */
  _formatValue(value) {
    this._elementRef.nativeElement.value = value != null ? this._dateAdapter.format(value, this._dateFormats.display.dateInput) : "";
  }
  /** Assigns a value to the model. */
  _assignValue(value) {
    if (this._model) {
      this._assignValueToModel(value);
      this._pendingValue = null;
    } else {
      this._pendingValue = value;
    }
  }
  /** Whether a value is considered valid. */
  _isValidValue(value) {
    return !value || this._dateAdapter.isValid(value);
  }
  /**
   * Checks whether a parent control is disabled. This is in place so that it can be overridden
   * by inputs extending this one which can be placed inside of a group that can be disabled.
   */
  _parentDisabled() {
    return false;
  }
  /** Programmatically assigns a value to the input. */
  _assignValueProgrammatically(value) {
    value = this._dateAdapter.deserialize(value);
    this._lastValueValid = this._isValidValue(value);
    value = this._dateAdapter.getValidDateOrNull(value);
    this._assignValue(value);
    this._formatValue(value);
  }
  /** Gets whether a value matches the current date filter. */
  _matchesFilter(value) {
    const filter2 = this._getDateFilter();
    return !filter2 || filter2(value);
  }
};
__name(_MatDatepickerInputBase, "MatDatepickerInputBase");
__publicField(_MatDatepickerInputBase, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerInputBase_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerInputBase)();
}, "MatDatepickerInputBase_Factory"));
__publicField(_MatDatepickerInputBase, "ɵdir", ɵɵdefineDirective({
  type: _MatDatepickerInputBase,
  inputs: {
    value: "value",
    disabled: [2, "disabled", "disabled", booleanAttribute]
  },
  outputs: {
    dateChange: "dateChange",
    dateInput: "dateInput"
  },
  features: [ɵɵNgOnChangesFeature]
}));
var MatDatepickerInputBase = _MatDatepickerInputBase;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerInputBase, [{
    type: Directive
  }], () => [], {
    value: [{
      type: Input
    }],
    disabled: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    dateChange: [{
      type: Output
    }],
    dateInput: [{
      type: Output
    }]
  });
})();
function dateInputsHaveChanged(changes, adapter) {
  const keys = Object.keys(changes);
  for (let key of keys) {
    const {
      previousValue,
      currentValue
    } = changes[key];
    if (adapter.isDateInstance(previousValue) && adapter.isDateInstance(currentValue)) {
      if (!adapter.sameDate(previousValue, currentValue)) {
        return true;
      }
    } else {
      return true;
    }
  }
  return false;
}
__name(dateInputsHaveChanged, "dateInputsHaveChanged");
var MAT_DATEPICKER_VALUE_ACCESSOR = {
  provide: NG_VALUE_ACCESSOR,
  useExisting: forwardRef(() => MatDatepickerInput),
  multi: true
};
var MAT_DATEPICKER_VALIDATORS = {
  provide: NG_VALIDATORS,
  useExisting: forwardRef(() => MatDatepickerInput),
  multi: true
};
var _MatDatepickerInput = class _MatDatepickerInput extends MatDatepickerInputBase {
  _formField = inject(MAT_FORM_FIELD, {
    optional: true
  });
  _closedSubscription = Subscription.EMPTY;
  _openedSubscription = Subscription.EMPTY;
  /** The datepicker that this input is associated with. */
  set matDatepicker(datepicker) {
    if (datepicker) {
      this._datepicker = datepicker;
      this._ariaOwns.set(datepicker.opened ? datepicker.id : null);
      this._closedSubscription = datepicker.closedStream.subscribe(() => {
        this._onTouched();
        this._ariaOwns.set(null);
      });
      this._openedSubscription = datepicker.openedStream.subscribe(() => {
        this._ariaOwns.set(datepicker.id);
      });
      this._registerModel(datepicker.registerInput(this));
    }
  }
  _datepicker;
  /** The id of the panel owned by this input. */
  _ariaOwns = signal(null, ...ngDevMode ? [{
    debugName: "_ariaOwns"
  }] : []);
  /** The minimum valid date. */
  get min() {
    return this._min;
  }
  set min(value) {
    const validValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    if (!this._dateAdapter.sameDate(validValue, this._min)) {
      this._min = validValue;
      this._validatorOnChange();
    }
  }
  _min;
  /** The maximum valid date. */
  get max() {
    return this._max;
  }
  set max(value) {
    const validValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    if (!this._dateAdapter.sameDate(validValue, this._max)) {
      this._max = validValue;
      this._validatorOnChange();
    }
  }
  _max;
  /** Function that can be used to filter out dates within the datepicker. */
  get dateFilter() {
    return this._dateFilter;
  }
  set dateFilter(value) {
    const wasMatchingValue = this._matchesFilter(this.value);
    this._dateFilter = value;
    if (this._matchesFilter(this.value) !== wasMatchingValue) {
      this._validatorOnChange();
    }
  }
  _dateFilter;
  /** The combined form control validator for this input. */
  _validator;
  constructor() {
    super();
    this._validator = Validators.compose(super._getValidators());
  }
  /**
   * Gets the element that the datepicker popup should be connected to.
   * @return The element to connect the popup to.
   */
  getConnectedOverlayOrigin() {
    return this._formField ? this._formField.getConnectedOverlayOrigin() : this._elementRef;
  }
  /** Gets the ID of an element that should be used a description for the calendar overlay. */
  getOverlayLabelId() {
    if (this._formField) {
      return this._formField.getLabelId();
    }
    return this._elementRef.nativeElement.getAttribute("aria-labelledby");
  }
  /** Returns the palette used by the input's form field, if any. */
  getThemePalette() {
    return this._formField ? this._formField.color : void 0;
  }
  /** Gets the value at which the calendar should start. */
  getStartValue() {
    return this.value;
  }
  ngOnDestroy() {
    super.ngOnDestroy();
    this._closedSubscription.unsubscribe();
    this._openedSubscription.unsubscribe();
  }
  /** Opens the associated datepicker. */
  _openPopup() {
    if (this._datepicker) {
      this._datepicker.open();
    }
  }
  _getValueFromModel(modelValue) {
    return modelValue;
  }
  _assignValueToModel(value) {
    if (this._model) {
      this._model.updateSelection(value, this);
    }
  }
  /** Gets the input's minimum date. */
  _getMinDate() {
    return this._min;
  }
  /** Gets the input's maximum date. */
  _getMaxDate() {
    return this._max;
  }
  /** Gets the input's date filtering function. */
  _getDateFilter() {
    return this._dateFilter;
  }
  _shouldHandleChangeEvent(event) {
    return event.source !== this;
  }
};
__name(_MatDatepickerInput, "MatDatepickerInput");
__publicField(_MatDatepickerInput, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerInput_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerInput)();
}, "MatDatepickerInput_Factory"));
__publicField(_MatDatepickerInput, "ɵdir", ɵɵdefineDirective({
  type: _MatDatepickerInput,
  selectors: [["input", "matDatepicker", ""]],
  hostAttrs: [1, "mat-datepicker-input"],
  hostVars: 6,
  hostBindings: /* @__PURE__ */ __name(function MatDatepickerInput_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("input", /* @__PURE__ */ __name(function MatDatepickerInput_input_HostBindingHandler($event) {
        return ctx._onInput($event);
      }, "MatDatepickerInput_input_HostBindingHandler"))("change", /* @__PURE__ */ __name(function MatDatepickerInput_change_HostBindingHandler() {
        return ctx._onChange();
      }, "MatDatepickerInput_change_HostBindingHandler"))("blur", /* @__PURE__ */ __name(function MatDatepickerInput_blur_HostBindingHandler() {
        return ctx._onBlur();
      }, "MatDatepickerInput_blur_HostBindingHandler"))("keydown", /* @__PURE__ */ __name(function MatDatepickerInput_keydown_HostBindingHandler($event) {
        return ctx._onKeydown($event);
      }, "MatDatepickerInput_keydown_HostBindingHandler"));
    }
    if (rf & 2) {
      ɵɵdomProperty("disabled", ctx.disabled);
      ɵɵattribute("aria-haspopup", ctx._datepicker ? "dialog" : null)("aria-owns", ctx._ariaOwns())("min", ctx.min ? ctx._dateAdapter.toIso8601(ctx.min) : null)("max", ctx.max ? ctx._dateAdapter.toIso8601(ctx.max) : null)("data-mat-calendar", ctx._datepicker ? ctx._datepicker.id : null);
    }
  }, "MatDatepickerInput_HostBindings"),
  inputs: {
    matDatepicker: "matDatepicker",
    min: "min",
    max: "max",
    dateFilter: [0, "matDatepickerFilter", "dateFilter"]
  },
  exportAs: ["matDatepickerInput"],
  features: [ɵɵProvidersFeature([MAT_DATEPICKER_VALUE_ACCESSOR, MAT_DATEPICKER_VALIDATORS, {
    provide: MAT_INPUT_VALUE_ACCESSOR,
    useExisting: _MatDatepickerInput
  }]), ɵɵInheritDefinitionFeature]
}));
var MatDatepickerInput = _MatDatepickerInput;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerInput, [{
    type: Directive,
    args: [{
      selector: "input[matDatepicker]",
      providers: [MAT_DATEPICKER_VALUE_ACCESSOR, MAT_DATEPICKER_VALIDATORS, {
        provide: MAT_INPUT_VALUE_ACCESSOR,
        useExisting: MatDatepickerInput
      }],
      host: {
        "class": "mat-datepicker-input",
        "[attr.aria-haspopup]": '_datepicker ? "dialog" : null',
        "[attr.aria-owns]": "_ariaOwns()",
        "[attr.min]": "min ? _dateAdapter.toIso8601(min) : null",
        "[attr.max]": "max ? _dateAdapter.toIso8601(max) : null",
        // Used by the test harness to tie this input to its calendar. We can't depend on
        // `aria-owns` for this, because it's only defined while the calendar is open.
        "[attr.data-mat-calendar]": "_datepicker ? _datepicker.id : null",
        "[disabled]": "disabled",
        "(input)": "_onInput($event)",
        "(change)": "_onChange()",
        "(blur)": "_onBlur()",
        "(keydown)": "_onKeydown($event)"
      },
      exportAs: "matDatepickerInput"
    }]
  }], () => [], {
    matDatepicker: [{
      type: Input
    }],
    min: [{
      type: Input
    }],
    max: [{
      type: Input
    }],
    dateFilter: [{
      type: Input,
      args: ["matDatepickerFilter"]
    }]
  });
})();
var _MatDatepickerToggleIcon = class _MatDatepickerToggleIcon {
};
__name(_MatDatepickerToggleIcon, "MatDatepickerToggleIcon");
__publicField(_MatDatepickerToggleIcon, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerToggleIcon_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerToggleIcon)();
}, "MatDatepickerToggleIcon_Factory"));
__publicField(_MatDatepickerToggleIcon, "ɵdir", ɵɵdefineDirective({
  type: _MatDatepickerToggleIcon,
  selectors: [["", "matDatepickerToggleIcon", ""]]
}));
var MatDatepickerToggleIcon = _MatDatepickerToggleIcon;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerToggleIcon, [{
    type: Directive,
    args: [{
      selector: "[matDatepickerToggleIcon]"
    }]
  }], null, null);
})();
var _MatDatepickerToggle = class _MatDatepickerToggle {
  _intl = inject(MatDatepickerIntl);
  _changeDetectorRef = inject(ChangeDetectorRef);
  _stateChanges = Subscription.EMPTY;
  /** Datepicker instance that the button will toggle. */
  datepicker;
  /** Tabindex for the toggle. */
  tabIndex;
  /** Screen-reader label for the button. */
  ariaLabel;
  /** Whether the toggle button is disabled. */
  get disabled() {
    if (this._disabled === void 0 && this.datepicker) {
      return this.datepicker.disabled;
    }
    return !!this._disabled;
  }
  set disabled(value) {
    this._disabled = value;
  }
  _disabled;
  /** Whether ripples on the toggle should be disabled. */
  disableRipple;
  /** Custom icon set by the consumer. */
  _customIcon;
  /** Underlying button element. */
  _button;
  constructor() {
    const defaultTabIndex = inject(new HostAttributeToken("tabindex"), {
      optional: true
    });
    const parsedTabIndex = Number(defaultTabIndex);
    this.tabIndex = parsedTabIndex || parsedTabIndex === 0 ? parsedTabIndex : null;
  }
  ngOnChanges(changes) {
    if (changes["datepicker"]) {
      this._watchStateChanges();
    }
  }
  ngOnDestroy() {
    this._stateChanges.unsubscribe();
  }
  ngAfterContentInit() {
    this._watchStateChanges();
  }
  _open(event) {
    if (this.datepicker && !this.disabled) {
      this.datepicker.open();
      event.stopPropagation();
    }
  }
  _watchStateChanges() {
    const datepickerStateChanged = this.datepicker ? this.datepicker.stateChanges : of();
    const inputStateChanged = this.datepicker && this.datepicker.datepickerInput ? this.datepicker.datepickerInput.stateChanges : of();
    const datepickerToggled = this.datepicker ? merge(this.datepicker.openedStream, this.datepicker.closedStream) : of();
    this._stateChanges.unsubscribe();
    this._stateChanges = merge(this._intl.changes, datepickerStateChanged, inputStateChanged, datepickerToggled).subscribe(() => this._changeDetectorRef.markForCheck());
  }
};
__name(_MatDatepickerToggle, "MatDatepickerToggle");
__publicField(_MatDatepickerToggle, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerToggle_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerToggle)();
}, "MatDatepickerToggle_Factory"));
__publicField(_MatDatepickerToggle, "ɵcmp", ɵɵdefineComponent({
  type: _MatDatepickerToggle,
  selectors: [["mat-datepicker-toggle"]],
  contentQueries: /* @__PURE__ */ __name(function MatDatepickerToggle_ContentQueries(rf, ctx, dirIndex) {
    if (rf & 1) {
      ɵɵcontentQuery(dirIndex, MatDatepickerToggleIcon, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._customIcon = _t.first);
    }
  }, "MatDatepickerToggle_ContentQueries"),
  viewQuery: /* @__PURE__ */ __name(function MatDatepickerToggle_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(_c2, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._button = _t.first);
    }
  }, "MatDatepickerToggle_Query"),
  hostAttrs: [1, "mat-datepicker-toggle"],
  hostVars: 8,
  hostBindings: /* @__PURE__ */ __name(function MatDatepickerToggle_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("click", /* @__PURE__ */ __name(function MatDatepickerToggle_click_HostBindingHandler($event) {
        return ctx._open($event);
      }, "MatDatepickerToggle_click_HostBindingHandler"));
    }
    if (rf & 2) {
      ɵɵattribute("tabindex", null)("data-mat-calendar", ctx.datepicker ? ctx.datepicker.id : null);
      ɵɵclassProp("mat-datepicker-toggle-active", ctx.datepicker && ctx.datepicker.opened)("mat-accent", ctx.datepicker && ctx.datepicker.color === "accent")("mat-warn", ctx.datepicker && ctx.datepicker.color === "warn");
    }
  }, "MatDatepickerToggle_HostBindings"),
  inputs: {
    datepicker: [0, "for", "datepicker"],
    tabIndex: "tabIndex",
    ariaLabel: [0, "aria-label", "ariaLabel"],
    disabled: [2, "disabled", "disabled", booleanAttribute],
    disableRipple: "disableRipple"
  },
  exportAs: ["matDatepickerToggle"],
  features: [ɵɵNgOnChangesFeature],
  ngContentSelectors: _c4,
  decls: 4,
  vars: 7,
  consts: [["button", ""], ["matIconButton", "", "type", "button", 3, "tabIndex", "disabled", "disableRipple"], ["viewBox", "0 0 24 24", "width", "24px", "height", "24px", "fill", "currentColor", "focusable", "false", "aria-hidden", "true", 1, "mat-datepicker-toggle-default-icon"], ["d", "M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"]],
  template: /* @__PURE__ */ __name(function MatDatepickerToggle_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵprojectionDef(_c3);
      ɵɵelementStart(0, "button", 1, 0);
      ɵɵconditionalCreate(2, MatDatepickerToggle_Conditional_2_Template, 2, 0, ":svg:svg", 2);
      ɵɵprojection(3);
      ɵɵelementEnd();
    }
    if (rf & 2) {
      ɵɵproperty("tabIndex", ctx.disabled ? -1 : ctx.tabIndex)("disabled", ctx.disabled)("disableRipple", ctx.disableRipple);
      ɵɵattribute("aria-haspopup", ctx.datepicker ? "dialog" : null)("aria-label", ctx.ariaLabel || ctx._intl.openCalendarLabel)("aria-expanded", ctx.datepicker ? ctx.datepicker.opened : null);
      ɵɵadvance(2);
      ɵɵconditional(!ctx._customIcon ? 2 : -1);
    }
  }, "MatDatepickerToggle_Template"),
  dependencies: [MatIconButton],
  styles: [".mat-datepicker-toggle{pointer-events:auto;color:var(--mat-datepicker-toggle-icon-color, var(--mat-sys-on-surface-variant))}.mat-datepicker-toggle button{color:inherit}.mat-datepicker-toggle-active{color:var(--mat-datepicker-toggle-active-state-icon-color, var(--mat-sys-primary))}@media(forced-colors: active){.mat-datepicker-toggle-default-icon{color:CanvasText}}\n"],
  encapsulation: 2,
  changeDetection: 0
}));
var MatDatepickerToggle = _MatDatepickerToggle;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerToggle, [{
    type: Component,
    args: [{
      selector: "mat-datepicker-toggle",
      host: {
        "class": "mat-datepicker-toggle",
        "[attr.tabindex]": "null",
        "[class.mat-datepicker-toggle-active]": "datepicker && datepicker.opened",
        "[class.mat-accent]": 'datepicker && datepicker.color === "accent"',
        "[class.mat-warn]": 'datepicker && datepicker.color === "warn"',
        // Used by the test harness to tie this toggle to its datepicker.
        "[attr.data-mat-calendar]": "datepicker ? datepicker.id : null",
        // Bind the `click` on the host, rather than the inner `button`, so that we can call
        // `stopPropagation` on it without affecting the user's `click` handlers. We need to stop
        // it so that the input doesn't get focused automatically by the form field (See #21836).
        "(click)": "_open($event)"
      },
      exportAs: "matDatepickerToggle",
      encapsulation: ViewEncapsulation.None,
      changeDetection: ChangeDetectionStrategy.OnPush,
      imports: [MatIconButton],
      template: `<button
  #button
  matIconButton
  type="button"
  [attr.aria-haspopup]="datepicker ? 'dialog' : null"
  [attr.aria-label]="ariaLabel || _intl.openCalendarLabel"
  [tabIndex]="disabled ? -1 : tabIndex"
  [attr.aria-expanded]="datepicker ? datepicker.opened : null"
  [disabled]="disabled"
  [disableRipple]="disableRipple">

  @if (!_customIcon) {
    <svg
      class="mat-datepicker-toggle-default-icon"
      viewBox="0 0 24 24"
      width="24px"
      height="24px"
      fill="currentColor"
      focusable="false"
      aria-hidden="true">
      <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
    </svg>
  }

  <ng-content select="[matDatepickerToggleIcon]"></ng-content>
</button>
`,
      styles: [".mat-datepicker-toggle{pointer-events:auto;color:var(--mat-datepicker-toggle-icon-color, var(--mat-sys-on-surface-variant))}.mat-datepicker-toggle button{color:inherit}.mat-datepicker-toggle-active{color:var(--mat-datepicker-toggle-active-state-icon-color, var(--mat-sys-primary))}@media(forced-colors: active){.mat-datepicker-toggle-default-icon{color:CanvasText}}\n"]
    }]
  }], () => [], {
    datepicker: [{
      type: Input,
      args: ["for"]
    }],
    tabIndex: [{
      type: Input
    }],
    ariaLabel: [{
      type: Input,
      args: ["aria-label"]
    }],
    disabled: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    disableRipple: [{
      type: Input
    }],
    _customIcon: [{
      type: ContentChild,
      args: [MatDatepickerToggleIcon]
    }],
    _button: [{
      type: ViewChild,
      args: ["button"]
    }]
  });
})();
var _MatDateRangeInput = class _MatDateRangeInput {
  _changeDetectorRef = inject(ChangeDetectorRef);
  _elementRef = inject(ElementRef);
  _dateAdapter = inject(DateAdapter, {
    optional: true
  });
  _formField = inject(MAT_FORM_FIELD, {
    optional: true
  });
  _closedSubscription = Subscription.EMPTY;
  _openedSubscription = Subscription.EMPTY;
  _startInput;
  _endInput;
  /** Current value of the range input. */
  get value() {
    return this._model ? this._model.selection : null;
  }
  /** Unique ID for the group. */
  id = inject(_IdGenerator).getId("mat-date-range-input-");
  /** Whether the control is focused. */
  focused = false;
  /** Whether the control's label should float. */
  get shouldLabelFloat() {
    return this.focused || !this.empty;
  }
  /** Name of the form control. */
  controlType = "mat-date-range-input";
  /**
   * Implemented as a part of `MatFormFieldControl`.
   * Set the placeholder attribute on `matStartDate` and `matEndDate`.
   * @docs-private
   */
  get placeholder() {
    const start = this._startInput?._getPlaceholder() || "";
    const end = this._endInput?._getPlaceholder() || "";
    return start || end ? `${start} ${this.separator} ${end}` : "";
  }
  /** The range picker that this input is associated with. */
  get rangePicker() {
    return this._rangePicker;
  }
  set rangePicker(rangePicker) {
    if (rangePicker) {
      this._model = rangePicker.registerInput(this);
      this._rangePicker = rangePicker;
      this._closedSubscription.unsubscribe();
      this._openedSubscription.unsubscribe();
      this._ariaOwns.set(this.rangePicker.opened ? rangePicker.id : null);
      this._closedSubscription = rangePicker.closedStream.subscribe(() => {
        this._startInput?._onTouched();
        this._endInput?._onTouched();
        this._ariaOwns.set(null);
      });
      this._openedSubscription = rangePicker.openedStream.subscribe(() => {
        this._ariaOwns.set(rangePicker.id);
      });
      this._registerModel(this._model);
    }
  }
  _rangePicker;
  /** The id of the panel owned by this input. */
  _ariaOwns = signal(null, ...ngDevMode ? [{
    debugName: "_ariaOwns"
  }] : []);
  /** Whether the input is required. */
  get required() {
    return this._required ?? (this._isTargetRequired(this) || this._isTargetRequired(this._startInput) || this._isTargetRequired(this._endInput)) ?? false;
  }
  set required(value) {
    this._required = value;
  }
  _required;
  /** Function that can be used to filter out dates within the date range picker. */
  get dateFilter() {
    return this._dateFilter;
  }
  set dateFilter(value) {
    const start = this._startInput;
    const end = this._endInput;
    const wasMatchingStart = start && start._matchesFilter(start.value);
    const wasMatchingEnd = end && end._matchesFilter(start.value);
    this._dateFilter = value;
    if (start && start._matchesFilter(start.value) !== wasMatchingStart) {
      start._validatorOnChange();
    }
    if (end && end._matchesFilter(end.value) !== wasMatchingEnd) {
      end._validatorOnChange();
    }
  }
  _dateFilter;
  /** The minimum valid date. */
  get min() {
    return this._min;
  }
  set min(value) {
    const validValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    if (!this._dateAdapter.sameDate(validValue, this._min)) {
      this._min = validValue;
      this._revalidate();
    }
  }
  _min;
  /** The maximum valid date. */
  get max() {
    return this._max;
  }
  set max(value) {
    const validValue = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(value));
    if (!this._dateAdapter.sameDate(validValue, this._max)) {
      this._max = validValue;
      this._revalidate();
    }
  }
  _max;
  /** Whether the input is disabled. */
  get disabled() {
    return this._startInput && this._endInput ? this._startInput.disabled && this._endInput.disabled : this._groupDisabled;
  }
  set disabled(value) {
    if (value !== this._groupDisabled) {
      this._groupDisabled = value;
      this.stateChanges.next(void 0);
    }
  }
  _groupDisabled = false;
  /** Whether the input is in an error state. */
  get errorState() {
    if (this._startInput && this._endInput) {
      return this._startInput.errorState || this._endInput.errorState;
    }
    return false;
  }
  /** Whether the datepicker input is empty. */
  get empty() {
    const startEmpty = this._startInput ? this._startInput.isEmpty() : false;
    const endEmpty = this._endInput ? this._endInput.isEmpty() : false;
    return startEmpty && endEmpty;
  }
  /** Value for the `aria-describedby` attribute of the inputs. */
  _ariaDescribedBy = null;
  /** Date selection model currently registered with the input. */
  _model;
  /** Separator text to be shown between the inputs. */
  separator = "–";
  /** Start of the comparison range that should be shown in the calendar. */
  comparisonStart = null;
  /** End of the comparison range that should be shown in the calendar. */
  comparisonEnd = null;
  /**
   * Implemented as a part of `MatFormFieldControl`.
   * TODO(crisbeto): change type to `AbstractControlDirective` after #18206 lands.
   * @docs-private
   */
  ngControl;
  /** Emits when the input's state has changed. */
  stateChanges = new Subject();
  /**
   * Disable the automatic labeling to avoid issues like #27241.
   * @docs-private
   */
  disableAutomaticLabeling = true;
  constructor() {
    if (!this._dateAdapter && (typeof ngDevMode === "undefined" || ngDevMode)) {
      throw createMissingDateImplError("DateAdapter");
    }
    if (this._formField?._elementRef.nativeElement.classList.contains("mat-mdc-form-field")) {
      this._elementRef.nativeElement.classList.add("mat-mdc-input-element", "mat-mdc-form-field-input-control", "mdc-text-field__input");
    }
    this.ngControl = inject(ControlContainer, {
      optional: true,
      self: true
    });
  }
  /**
   * Implemented as part of MatFormFieldControl.
   * @docs-private
   */
  get describedByIds() {
    const element = this._elementRef.nativeElement;
    const existingDescribedBy = element.getAttribute("aria-describedby");
    return existingDescribedBy?.split(" ") || [];
  }
  /**
   * Implemented as a part of `MatFormFieldControl`.
   * @docs-private
   */
  setDescribedByIds(ids) {
    this._ariaDescribedBy = ids.length ? ids.join(" ") : null;
  }
  /**
   * Implemented as a part of `MatFormFieldControl`.
   * @docs-private
   */
  onContainerClick() {
    if (!this.focused && !this.disabled) {
      if (!this._model || !this._model.selection.start) {
        this._startInput.focus();
      } else {
        this._endInput.focus();
      }
    }
  }
  ngAfterContentInit() {
    if (typeof ngDevMode === "undefined" || ngDevMode) {
      if (!this._startInput) {
        throw Error("mat-date-range-input must contain a matStartDate input");
      }
      if (!this._endInput) {
        throw Error("mat-date-range-input must contain a matEndDate input");
      }
    }
    if (this._model) {
      this._registerModel(this._model);
    }
    merge(this._startInput.stateChanges, this._endInput.stateChanges).subscribe(() => {
      this.stateChanges.next(void 0);
    });
  }
  ngOnChanges(changes) {
    if (dateInputsHaveChanged(changes, this._dateAdapter)) {
      this.stateChanges.next(void 0);
    }
  }
  ngOnDestroy() {
    this._closedSubscription.unsubscribe();
    this._openedSubscription.unsubscribe();
    this.stateChanges.complete();
  }
  /** Gets the date at which the calendar should start. */
  getStartValue() {
    return this.value ? this.value.start : null;
  }
  /** Gets the input's theme palette. */
  getThemePalette() {
    return this._formField ? this._formField.color : void 0;
  }
  /** Gets the element to which the calendar overlay should be attached. */
  getConnectedOverlayOrigin() {
    return this._formField ? this._formField.getConnectedOverlayOrigin() : this._elementRef;
  }
  /** Gets the ID of an element that should be used a description for the calendar overlay. */
  getOverlayLabelId() {
    return this._formField ? this._formField.getLabelId() : null;
  }
  /** Gets the value that is used to mirror the state input. */
  _getInputMirrorValue(part) {
    const input = part === "start" ? this._startInput : this._endInput;
    return input ? input.getMirrorValue() : "";
  }
  /** Whether the input placeholders should be hidden. */
  _shouldHidePlaceholders() {
    return this._startInput ? !this._startInput.isEmpty() : false;
  }
  /** Handles the value in one of the child inputs changing. */
  _handleChildValueChange() {
    this.stateChanges.next(void 0);
    this._changeDetectorRef.markForCheck();
  }
  /** Opens the date range picker associated with the input. */
  _openDatepicker() {
    if (this._rangePicker) {
      this._rangePicker.open();
    }
  }
  /** Whether the separate text should be hidden. */
  _shouldHideSeparator() {
    return (!this._formField || this._formField.getLabelId() && !this._formField._shouldLabelFloat()) && this.empty;
  }
  /** Gets the value for the `aria-labelledby` attribute of the inputs. */
  _getAriaLabelledby() {
    const formField = this._formField;
    return formField && formField._hasFloatingLabel() ? formField._labelId : null;
  }
  _getStartDateAccessibleName() {
    return this._startInput._getAccessibleName();
  }
  _getEndDateAccessibleName() {
    return this._endInput._getAccessibleName();
  }
  /** Updates the focused state of the range input. */
  _updateFocus(origin) {
    this.focused = origin !== null;
    this.stateChanges.next();
  }
  /** Re-runs the validators on the start/end inputs. */
  _revalidate() {
    if (this._startInput) {
      this._startInput._validatorOnChange();
    }
    if (this._endInput) {
      this._endInput._validatorOnChange();
    }
  }
  /** Registers the current date selection model with the start/end inputs. */
  _registerModel(model) {
    if (this._startInput) {
      this._startInput._registerModel(model);
    }
    if (this._endInput) {
      this._endInput._registerModel(model);
    }
  }
  /** Checks whether a specific range input directive is required. */
  _isTargetRequired(target) {
    return target?.ngControl?.control?.hasValidator(Validators.required);
  }
};
__name(_MatDateRangeInput, "MatDateRangeInput");
__publicField(_MatDateRangeInput, "ɵfac", /* @__PURE__ */ __name(function MatDateRangeInput_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDateRangeInput)();
}, "MatDateRangeInput_Factory"));
__publicField(_MatDateRangeInput, "ɵcmp", ɵɵdefineComponent({
  type: _MatDateRangeInput,
  selectors: [["mat-date-range-input"]],
  hostAttrs: ["role", "group", 1, "mat-date-range-input"],
  hostVars: 8,
  hostBindings: /* @__PURE__ */ __name(function MatDateRangeInput_HostBindings(rf, ctx) {
    if (rf & 2) {
      ɵɵattribute("id", ctx.id)("aria-labelledby", ctx._getAriaLabelledby())("aria-describedby", ctx._ariaDescribedBy)("data-mat-calendar", ctx.rangePicker ? ctx.rangePicker.id : null);
      ɵɵclassProp("mat-date-range-input-hide-placeholders", ctx._shouldHidePlaceholders())("mat-date-range-input-required", ctx.required);
    }
  }, "MatDateRangeInput_HostBindings"),
  inputs: {
    rangePicker: "rangePicker",
    required: [2, "required", "required", booleanAttribute],
    dateFilter: "dateFilter",
    min: "min",
    max: "max",
    disabled: [2, "disabled", "disabled", booleanAttribute],
    separator: "separator",
    comparisonStart: "comparisonStart",
    comparisonEnd: "comparisonEnd"
  },
  exportAs: ["matDateRangeInput"],
  features: [ɵɵProvidersFeature([{
    provide: MatFormFieldControl,
    useExisting: _MatDateRangeInput
  }]), ɵɵNgOnChangesFeature],
  ngContentSelectors: _c6,
  decls: 11,
  vars: 5,
  consts: [["cdkMonitorSubtreeFocus", "", 1, "mat-date-range-input-container", 3, "cdkFocusChange"], [1, "mat-date-range-input-wrapper"], ["aria-hidden", "true", 1, "mat-date-range-input-mirror"], [1, "mat-date-range-input-separator"], [1, "mat-date-range-input-wrapper", "mat-date-range-input-end-wrapper"]],
  template: /* @__PURE__ */ __name(function MatDateRangeInput_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵprojectionDef(_c5);
      ɵɵelementStart(0, "div", 0);
      ɵɵlistener("cdkFocusChange", /* @__PURE__ */ __name(function MatDateRangeInput_Template_div_cdkFocusChange_0_listener($event) {
        return ctx._updateFocus($event);
      }, "MatDateRangeInput_Template_div_cdkFocusChange_0_listener"));
      ɵɵelementStart(1, "div", 1);
      ɵɵprojection(2);
      ɵɵelementStart(3, "span", 2);
      ɵɵtext(4);
      ɵɵelementEnd()();
      ɵɵelementStart(5, "span", 3);
      ɵɵtext(6);
      ɵɵelementEnd();
      ɵɵelementStart(7, "div", 4);
      ɵɵprojection(8, 1);
      ɵɵelementStart(9, "span", 2);
      ɵɵtext(10);
      ɵɵelementEnd()()();
    }
    if (rf & 2) {
      ɵɵadvance(4);
      ɵɵtextInterpolate(ctx._getInputMirrorValue("start"));
      ɵɵadvance();
      ɵɵclassProp("mat-date-range-input-separator-hidden", ctx._shouldHideSeparator());
      ɵɵadvance();
      ɵɵtextInterpolate(ctx.separator);
      ɵɵadvance(4);
      ɵɵtextInterpolate(ctx._getInputMirrorValue("end"));
    }
  }, "MatDateRangeInput_Template"),
  dependencies: [CdkMonitorFocus],
  styles: [".mat-date-range-input{display:block;width:100%}.mat-date-range-input-container{display:flex;align-items:center}.mat-date-range-input-separator{transition:opacity 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1);margin:0 4px;color:var(--mat-datepicker-range-input-separator-color, var(--mat-sys-on-surface))}.mat-form-field-disabled .mat-date-range-input-separator{color:var(--mat-datepicker-range-input-disabled-state-separator-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}._mat-animation-noopable .mat-date-range-input-separator{transition:none}.mat-date-range-input-separator-hidden{-webkit-user-select:none;user-select:none;opacity:0;transition:none}.mat-date-range-input-wrapper{position:relative;overflow:hidden;max-width:calc(50% - 4px)}.mat-date-range-input-end-wrapper{flex-grow:1}.mat-date-range-input-inner{position:absolute;top:0;left:0;font:inherit;background:rgba(0,0,0,0);color:currentColor;border:none;outline:none;padding:0;margin:0;vertical-align:bottom;text-align:inherit;-webkit-appearance:none;width:100%;height:100%}.mat-date-range-input-inner:-moz-ui-invalid{box-shadow:none}.mat-date-range-input-inner::placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner::-moz-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner::-webkit-input-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner:-ms-input-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner[disabled]{color:var(--mat-datepicker-range-input-disabled-state-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-form-field-hide-placeholder .mat-date-range-input-inner::placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner::placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::placeholder{opacity:0}}.mat-form-field-hide-placeholder .mat-date-range-input-inner::-moz-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-moz-placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner::-moz-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-moz-placeholder{opacity:0}}.mat-form-field-hide-placeholder .mat-date-range-input-inner::-webkit-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-webkit-input-placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner::-webkit-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-webkit-input-placeholder{opacity:0}}.mat-form-field-hide-placeholder .mat-date-range-input-inner:-ms-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner:-ms-input-placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner:-ms-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner:-ms-input-placeholder{opacity:0}}._mat-animation-noopable .mat-date-range-input-inner::placeholder{transition:none}._mat-animation-noopable .mat-date-range-input-inner::-moz-placeholder{transition:none}._mat-animation-noopable .mat-date-range-input-inner::-webkit-input-placeholder{transition:none}._mat-animation-noopable .mat-date-range-input-inner:-ms-input-placeholder{transition:none}.mat-date-range-input-mirror{-webkit-user-select:none;user-select:none;visibility:hidden;white-space:nowrap;display:inline-block;min-width:2px}.mat-mdc-form-field-type-mat-date-range-input .mat-mdc-form-field-infix{width:200px}\n"],
  encapsulation: 2,
  changeDetection: 0
}));
var MatDateRangeInput = _MatDateRangeInput;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDateRangeInput, [{
    type: Component,
    args: [{
      selector: "mat-date-range-input",
      exportAs: "matDateRangeInput",
      host: {
        "class": "mat-date-range-input",
        "[class.mat-date-range-input-hide-placeholders]": "_shouldHidePlaceholders()",
        "[class.mat-date-range-input-required]": "required",
        "[attr.id]": "id",
        "role": "group",
        "[attr.aria-labelledby]": "_getAriaLabelledby()",
        "[attr.aria-describedby]": "_ariaDescribedBy",
        // Used by the test harness to tie this input to its calendar. We can't depend on
        // `aria-owns` for this, because it's only defined while the calendar is open.
        "[attr.data-mat-calendar]": "rangePicker ? rangePicker.id : null"
      },
      changeDetection: ChangeDetectionStrategy.OnPush,
      encapsulation: ViewEncapsulation.None,
      providers: [{
        provide: MatFormFieldControl,
        useExisting: MatDateRangeInput
      }],
      imports: [CdkMonitorFocus],
      template: `<div
  class="mat-date-range-input-container"
  cdkMonitorSubtreeFocus
  (cdkFocusChange)="_updateFocus($event)">
  <div class="mat-date-range-input-wrapper">
    <ng-content select="input[matStartDate]"></ng-content>
    <span
      class="mat-date-range-input-mirror"
      aria-hidden="true">{{_getInputMirrorValue('start')}}</span>
  </div>

  <span
    class="mat-date-range-input-separator"
    [class.mat-date-range-input-separator-hidden]="_shouldHideSeparator()">{{separator}}</span>

  <div class="mat-date-range-input-wrapper mat-date-range-input-end-wrapper">
    <ng-content select="input[matEndDate]"></ng-content>
    <span
      class="mat-date-range-input-mirror"
      aria-hidden="true">{{_getInputMirrorValue('end')}}</span>
  </div>
</div>

`,
      styles: [".mat-date-range-input{display:block;width:100%}.mat-date-range-input-container{display:flex;align-items:center}.mat-date-range-input-separator{transition:opacity 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1);margin:0 4px;color:var(--mat-datepicker-range-input-separator-color, var(--mat-sys-on-surface))}.mat-form-field-disabled .mat-date-range-input-separator{color:var(--mat-datepicker-range-input-disabled-state-separator-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}._mat-animation-noopable .mat-date-range-input-separator{transition:none}.mat-date-range-input-separator-hidden{-webkit-user-select:none;user-select:none;opacity:0;transition:none}.mat-date-range-input-wrapper{position:relative;overflow:hidden;max-width:calc(50% - 4px)}.mat-date-range-input-end-wrapper{flex-grow:1}.mat-date-range-input-inner{position:absolute;top:0;left:0;font:inherit;background:rgba(0,0,0,0);color:currentColor;border:none;outline:none;padding:0;margin:0;vertical-align:bottom;text-align:inherit;-webkit-appearance:none;width:100%;height:100%}.mat-date-range-input-inner:-moz-ui-invalid{box-shadow:none}.mat-date-range-input-inner::placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner::-moz-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner::-webkit-input-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner:-ms-input-placeholder{transition:color 400ms 133.3333333333ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-date-range-input-inner[disabled]{color:var(--mat-datepicker-range-input-disabled-state-text-color, color-mix(in srgb, var(--mat-sys-on-surface) 38%, transparent))}.mat-form-field-hide-placeholder .mat-date-range-input-inner::placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner::placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::placeholder{opacity:0}}.mat-form-field-hide-placeholder .mat-date-range-input-inner::-moz-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-moz-placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner::-moz-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-moz-placeholder{opacity:0}}.mat-form-field-hide-placeholder .mat-date-range-input-inner::-webkit-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-webkit-input-placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner::-webkit-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner::-webkit-input-placeholder{opacity:0}}.mat-form-field-hide-placeholder .mat-date-range-input-inner:-ms-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner:-ms-input-placeholder{-webkit-user-select:none;user-select:none;color:rgba(0,0,0,0) !important;-webkit-text-fill-color:rgba(0,0,0,0);transition:none}@media(forced-colors: active){.mat-form-field-hide-placeholder .mat-date-range-input-inner:-ms-input-placeholder,.mat-date-range-input-hide-placeholders .mat-date-range-input-inner:-ms-input-placeholder{opacity:0}}._mat-animation-noopable .mat-date-range-input-inner::placeholder{transition:none}._mat-animation-noopable .mat-date-range-input-inner::-moz-placeholder{transition:none}._mat-animation-noopable .mat-date-range-input-inner::-webkit-input-placeholder{transition:none}._mat-animation-noopable .mat-date-range-input-inner:-ms-input-placeholder{transition:none}.mat-date-range-input-mirror{-webkit-user-select:none;user-select:none;visibility:hidden;white-space:nowrap;display:inline-block;min-width:2px}.mat-mdc-form-field-type-mat-date-range-input .mat-mdc-form-field-infix{width:200px}\n"]
    }]
  }], () => [], {
    rangePicker: [{
      type: Input
    }],
    required: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    dateFilter: [{
      type: Input
    }],
    min: [{
      type: Input
    }],
    max: [{
      type: Input
    }],
    disabled: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    separator: [{
      type: Input
    }],
    comparisonStart: [{
      type: Input
    }],
    comparisonEnd: [{
      type: Input
    }]
  });
})();
function _computeAriaAccessibleName(element) {
  return _computeAriaAccessibleNameInternal(element, true);
}
__name(_computeAriaAccessibleName, "_computeAriaAccessibleName");
function ssrSafeIsElement(node) {
  return node.nodeType === Node.ELEMENT_NODE;
}
__name(ssrSafeIsElement, "ssrSafeIsElement");
function ssrSafeIsHTMLInputElement(node) {
  return node.nodeName === "INPUT";
}
__name(ssrSafeIsHTMLInputElement, "ssrSafeIsHTMLInputElement");
function ssrSafeIsHTMLTextAreaElement(node) {
  return node.nodeName === "TEXTAREA";
}
__name(ssrSafeIsHTMLTextAreaElement, "ssrSafeIsHTMLTextAreaElement");
function _computeAriaAccessibleNameInternal(currentNode, isDirectlyReferenced) {
  if (ssrSafeIsElement(currentNode) && isDirectlyReferenced) {
    const labelledbyIds = currentNode.getAttribute?.("aria-labelledby")?.split(/\s+/g) || [];
    const validIdRefs = labelledbyIds.reduce((validIds, id) => {
      const elem = document.getElementById(id);
      if (elem) {
        validIds.push(elem);
      }
      return validIds;
    }, []);
    if (validIdRefs.length) {
      return validIdRefs.map((idRef) => {
        return _computeAriaAccessibleNameInternal(idRef, false);
      }).join(" ");
    }
  }
  if (ssrSafeIsElement(currentNode)) {
    const ariaLabel = currentNode.getAttribute("aria-label")?.trim();
    if (ariaLabel) {
      return ariaLabel;
    }
  }
  if (ssrSafeIsHTMLInputElement(currentNode) || ssrSafeIsHTMLTextAreaElement(currentNode)) {
    if (currentNode.labels?.length) {
      return Array.from(currentNode.labels).map((x) => _computeAriaAccessibleNameInternal(x, false)).join(" ");
    }
    const placeholder = currentNode.getAttribute("placeholder")?.trim();
    if (placeholder) {
      return placeholder;
    }
    const title = currentNode.getAttribute("title")?.trim();
    if (title) {
      return title;
    }
  }
  return (currentNode.textContent || "").replace(/\s+/g, " ").trim();
}
__name(_computeAriaAccessibleNameInternal, "_computeAriaAccessibleNameInternal");
var _MatDateRangeInputPartBase = class _MatDateRangeInputPartBase extends MatDatepickerInputBase {
  _rangeInput = inject(MatDateRangeInput);
  _elementRef = inject(ElementRef);
  _defaultErrorStateMatcher = inject(ErrorStateMatcher);
  _injector = inject(Injector);
  _rawValue = signal("", ...ngDevMode ? [{
    debugName: "_rawValue"
  }] : []);
  _parentForm = inject(NgForm, {
    optional: true
  });
  _parentFormGroup = inject(FormGroupDirective, {
    optional: true
  });
  /**
   * Form control bound to this input part.
   * @docs-private
   */
  ngControl;
  _dir = inject(Directionality, {
    optional: true
  });
  _errorStateTracker;
  /** Object used to control when error messages are shown. */
  get errorStateMatcher() {
    return this._errorStateTracker.matcher;
  }
  set errorStateMatcher(value) {
    this._errorStateTracker.matcher = value;
  }
  /** Whether the input is in an error state. */
  get errorState() {
    return this._errorStateTracker.errorState;
  }
  set errorState(value) {
    this._errorStateTracker.errorState = value;
  }
  constructor() {
    super();
    this._errorStateTracker = new _ErrorStateTracker(this._defaultErrorStateMatcher, null, this._parentFormGroup, this._parentForm, this.stateChanges);
  }
  ngOnInit() {
    const ngControl = this._injector.get(NgControl, null, {
      optional: true,
      self: true
    });
    if (ngControl) {
      this.ngControl = ngControl;
      this._errorStateTracker.ngControl = ngControl;
    }
  }
  ngAfterContentInit() {
    this._register();
  }
  ngDoCheck() {
    if (this.ngControl) {
      this.updateErrorState();
    }
    this._rawValue.set(this._elementRef.nativeElement.value);
  }
  /** Gets whether the input is empty. */
  isEmpty() {
    return this._rawValue().length === 0;
  }
  /** Gets the placeholder of the input. */
  _getPlaceholder() {
    return this._elementRef.nativeElement.placeholder;
  }
  /** Focuses the input. */
  focus() {
    this._elementRef.nativeElement.focus();
  }
  /** Gets the value that should be used when mirroring the input's size. */
  getMirrorValue() {
    const value = this._rawValue();
    return value.length > 0 ? value : this._getPlaceholder();
  }
  /** Refreshes the error state of the input. */
  updateErrorState() {
    this._errorStateTracker.updateErrorState();
  }
  /** Handles `input` events on the input element. */
  _onInput(event) {
    super._onInput(event);
    this._rangeInput._handleChildValueChange();
  }
  /** Opens the datepicker associated with the input. */
  _openPopup() {
    this._rangeInput._openDatepicker();
  }
  /** Gets the minimum date from the range input. */
  _getMinDate() {
    return this._rangeInput.min;
  }
  /** Gets the maximum date from the range input. */
  _getMaxDate() {
    return this._rangeInput.max;
  }
  /** Gets the date filter function from the range input. */
  _getDateFilter() {
    return this._rangeInput.dateFilter;
  }
  _parentDisabled() {
    return this._rangeInput._groupDisabled;
  }
  _shouldHandleChangeEvent({
    source
  }) {
    return source !== this._rangeInput._startInput && source !== this._rangeInput._endInput;
  }
  _assignValueProgrammatically(value) {
    super._assignValueProgrammatically(value);
    const opposite = this === this._rangeInput._startInput ? this._rangeInput._endInput : this._rangeInput._startInput;
    opposite?._validatorOnChange();
    this._rawValue.set(this._elementRef.nativeElement.value);
  }
  _formatValue(value) {
    super._formatValue(value);
    this._rangeInput._handleChildValueChange();
  }
  /** return the ARIA accessible name of the input element */
  _getAccessibleName() {
    return _computeAriaAccessibleName(this._elementRef.nativeElement);
  }
};
__name(_MatDateRangeInputPartBase, "MatDateRangeInputPartBase");
__publicField(_MatDateRangeInputPartBase, "ɵfac", /* @__PURE__ */ __name(function MatDateRangeInputPartBase_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDateRangeInputPartBase)();
}, "MatDateRangeInputPartBase_Factory"));
__publicField(_MatDateRangeInputPartBase, "ɵdir", ɵɵdefineDirective({
  type: _MatDateRangeInputPartBase,
  inputs: {
    errorStateMatcher: "errorStateMatcher"
  },
  features: [ɵɵInheritDefinitionFeature]
}));
var MatDateRangeInputPartBase = _MatDateRangeInputPartBase;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDateRangeInputPartBase, [{
    type: Directive
  }], () => [], {
    errorStateMatcher: [{
      type: Input
    }]
  });
})();
var _MatStartDate = class _MatStartDate extends MatDateRangeInputPartBase {
  /** Validator that checks that the start date isn't after the end date. */
  _startValidator = /* @__PURE__ */ __name((control) => {
    const start = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(control.value));
    const end = this._model ? this._model.selection.end : null;
    return !start || !end || this._dateAdapter.compareDate(start, end) <= 0 ? null : {
      "matStartDateInvalid": {
        "end": end,
        "actual": start
      }
    };
  }, "_startValidator");
  _validator = Validators.compose([...super._getValidators(), this._startValidator]);
  _register() {
    this._rangeInput._startInput = this;
  }
  _getValueFromModel(modelValue) {
    return modelValue.start;
  }
  _shouldHandleChangeEvent(change) {
    if (!super._shouldHandleChangeEvent(change)) {
      return false;
    } else {
      return !change.oldValue?.start ? !!change.selection.start : !change.selection.start || !!this._dateAdapter.compareDate(change.oldValue.start, change.selection.start);
    }
  }
  _assignValueToModel(value) {
    if (this._model) {
      const range = new DateRange(value, this._model.selection.end);
      this._model.updateSelection(range, this);
      this._rangeInput._handleChildValueChange();
    }
  }
  _onKeydown(event) {
    const endInput = this._rangeInput._endInput;
    const element = this._elementRef.nativeElement;
    const isLtr = this._dir?.value !== "rtl";
    if ((event.keyCode === RIGHT_ARROW && isLtr || event.keyCode === LEFT_ARROW && !isLtr) && element.selectionStart === element.value.length && element.selectionEnd === element.value.length) {
      event.preventDefault();
      endInput._elementRef.nativeElement.setSelectionRange(0, 0);
      endInput.focus();
    } else {
      super._onKeydown(event);
    }
  }
};
__name(_MatStartDate, "MatStartDate");
__publicField(_MatStartDate, "ɵfac", /* @__PURE__ */ (() => {
  let ɵMatStartDate_BaseFactory;
  return /* @__PURE__ */ __name(function MatStartDate_Factory(__ngFactoryType__) {
    return (ɵMatStartDate_BaseFactory || (ɵMatStartDate_BaseFactory = ɵɵgetInheritedFactory(_MatStartDate)))(__ngFactoryType__ || _MatStartDate);
  }, "MatStartDate_Factory");
})());
__publicField(_MatStartDate, "ɵdir", ɵɵdefineDirective({
  type: _MatStartDate,
  selectors: [["input", "matStartDate", ""]],
  hostAttrs: ["type", "text", 1, "mat-start-date", "mat-date-range-input-inner"],
  hostVars: 5,
  hostBindings: /* @__PURE__ */ __name(function MatStartDate_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("input", /* @__PURE__ */ __name(function MatStartDate_input_HostBindingHandler($event) {
        return ctx._onInput($event);
      }, "MatStartDate_input_HostBindingHandler"))("change", /* @__PURE__ */ __name(function MatStartDate_change_HostBindingHandler() {
        return ctx._onChange();
      }, "MatStartDate_change_HostBindingHandler"))("keydown", /* @__PURE__ */ __name(function MatStartDate_keydown_HostBindingHandler($event) {
        return ctx._onKeydown($event);
      }, "MatStartDate_keydown_HostBindingHandler"))("blur", /* @__PURE__ */ __name(function MatStartDate_blur_HostBindingHandler() {
        return ctx._onBlur();
      }, "MatStartDate_blur_HostBindingHandler"));
    }
    if (rf & 2) {
      ɵɵdomProperty("disabled", ctx.disabled);
      ɵɵattribute("aria-haspopup", ctx._rangeInput.rangePicker ? "dialog" : null)("aria-owns", ctx._rangeInput._ariaOwns() || null)("min", ctx._getMinDate() ? ctx._dateAdapter.toIso8601(ctx._getMinDate()) : null)("max", ctx._getMaxDate() ? ctx._dateAdapter.toIso8601(ctx._getMaxDate()) : null);
    }
  }, "MatStartDate_HostBindings"),
  outputs: {
    dateChange: "dateChange",
    dateInput: "dateInput"
  },
  features: [ɵɵProvidersFeature([{
    provide: NG_VALUE_ACCESSOR,
    useExisting: _MatStartDate,
    multi: true
  }, {
    provide: NG_VALIDATORS,
    useExisting: _MatStartDate,
    multi: true
  }]), ɵɵInheritDefinitionFeature]
}));
var MatStartDate = _MatStartDate;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatStartDate, [{
    type: Directive,
    args: [{
      selector: "input[matStartDate]",
      host: {
        "class": "mat-start-date mat-date-range-input-inner",
        "[disabled]": "disabled",
        "(input)": "_onInput($event)",
        "(change)": "_onChange()",
        "(keydown)": "_onKeydown($event)",
        "[attr.aria-haspopup]": '_rangeInput.rangePicker ? "dialog" : null',
        "[attr.aria-owns]": "_rangeInput._ariaOwns() || null",
        "[attr.min]": "_getMinDate() ? _dateAdapter.toIso8601(_getMinDate()!) : null",
        "[attr.max]": "_getMaxDate() ? _dateAdapter.toIso8601(_getMaxDate()!) : null",
        "(blur)": "_onBlur()",
        "type": "text"
      },
      providers: [{
        provide: NG_VALUE_ACCESSOR,
        useExisting: MatStartDate,
        multi: true
      }, {
        provide: NG_VALIDATORS,
        useExisting: MatStartDate,
        multi: true
      }],
      // These need to be specified explicitly, because some tooling doesn't
      // seem to pick them up from the base class. See #20932.
      outputs: ["dateChange", "dateInput"]
    }]
  }], null, null);
})();
var _MatEndDate = class _MatEndDate extends MatDateRangeInputPartBase {
  /** Validator that checks that the end date isn't before the start date. */
  _endValidator = /* @__PURE__ */ __name((control) => {
    const end = this._dateAdapter.getValidDateOrNull(this._dateAdapter.deserialize(control.value));
    const start = this._model ? this._model.selection.start : null;
    return !end || !start || this._dateAdapter.compareDate(end, start) >= 0 ? null : {
      "matEndDateInvalid": {
        "start": start,
        "actual": end
      }
    };
  }, "_endValidator");
  _register() {
    this._rangeInput._endInput = this;
  }
  _validator = Validators.compose([...super._getValidators(), this._endValidator]);
  _getValueFromModel(modelValue) {
    return modelValue.end;
  }
  _shouldHandleChangeEvent(change) {
    if (!super._shouldHandleChangeEvent(change)) {
      return false;
    } else {
      return !change.oldValue?.end ? !!change.selection.end : !change.selection.end || !!this._dateAdapter.compareDate(change.oldValue.end, change.selection.end);
    }
  }
  _assignValueToModel(value) {
    if (this._model) {
      const range = new DateRange(this._model.selection.start, value);
      this._model.updateSelection(range, this);
    }
  }
  _moveCaretToEndOfStartInput() {
    const startInput = this._rangeInput._startInput._elementRef.nativeElement;
    const value = startInput.value;
    if (value.length > 0) {
      startInput.setSelectionRange(value.length, value.length);
    }
    startInput.focus();
  }
  _onKeydown(event) {
    const element = this._elementRef.nativeElement;
    const isLtr = this._dir?.value !== "rtl";
    if (event.keyCode === BACKSPACE && !element.value) {
      this._moveCaretToEndOfStartInput();
    } else if ((event.keyCode === LEFT_ARROW && isLtr || event.keyCode === RIGHT_ARROW && !isLtr) && element.selectionStart === 0 && element.selectionEnd === 0) {
      event.preventDefault();
      this._moveCaretToEndOfStartInput();
    } else {
      super._onKeydown(event);
    }
  }
};
__name(_MatEndDate, "MatEndDate");
__publicField(_MatEndDate, "ɵfac", /* @__PURE__ */ (() => {
  let ɵMatEndDate_BaseFactory;
  return /* @__PURE__ */ __name(function MatEndDate_Factory(__ngFactoryType__) {
    return (ɵMatEndDate_BaseFactory || (ɵMatEndDate_BaseFactory = ɵɵgetInheritedFactory(_MatEndDate)))(__ngFactoryType__ || _MatEndDate);
  }, "MatEndDate_Factory");
})());
__publicField(_MatEndDate, "ɵdir", ɵɵdefineDirective({
  type: _MatEndDate,
  selectors: [["input", "matEndDate", ""]],
  hostAttrs: ["type", "text", 1, "mat-end-date", "mat-date-range-input-inner"],
  hostVars: 5,
  hostBindings: /* @__PURE__ */ __name(function MatEndDate_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("input", /* @__PURE__ */ __name(function MatEndDate_input_HostBindingHandler($event) {
        return ctx._onInput($event);
      }, "MatEndDate_input_HostBindingHandler"))("change", /* @__PURE__ */ __name(function MatEndDate_change_HostBindingHandler() {
        return ctx._onChange();
      }, "MatEndDate_change_HostBindingHandler"))("keydown", /* @__PURE__ */ __name(function MatEndDate_keydown_HostBindingHandler($event) {
        return ctx._onKeydown($event);
      }, "MatEndDate_keydown_HostBindingHandler"))("blur", /* @__PURE__ */ __name(function MatEndDate_blur_HostBindingHandler() {
        return ctx._onBlur();
      }, "MatEndDate_blur_HostBindingHandler"));
    }
    if (rf & 2) {
      ɵɵdomProperty("disabled", ctx.disabled);
      ɵɵattribute("aria-haspopup", ctx._rangeInput.rangePicker ? "dialog" : null)("aria-owns", ctx._rangeInput._ariaOwns() || null)("min", ctx._getMinDate() ? ctx._dateAdapter.toIso8601(ctx._getMinDate()) : null)("max", ctx._getMaxDate() ? ctx._dateAdapter.toIso8601(ctx._getMaxDate()) : null);
    }
  }, "MatEndDate_HostBindings"),
  outputs: {
    dateChange: "dateChange",
    dateInput: "dateInput"
  },
  features: [ɵɵProvidersFeature([{
    provide: NG_VALUE_ACCESSOR,
    useExisting: _MatEndDate,
    multi: true
  }, {
    provide: NG_VALIDATORS,
    useExisting: _MatEndDate,
    multi: true
  }]), ɵɵInheritDefinitionFeature]
}));
var MatEndDate = _MatEndDate;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatEndDate, [{
    type: Directive,
    args: [{
      selector: "input[matEndDate]",
      host: {
        "class": "mat-end-date mat-date-range-input-inner",
        "[disabled]": "disabled",
        "(input)": "_onInput($event)",
        "(change)": "_onChange()",
        "(keydown)": "_onKeydown($event)",
        "[attr.aria-haspopup]": '_rangeInput.rangePicker ? "dialog" : null',
        "[attr.aria-owns]": "_rangeInput._ariaOwns() || null",
        "[attr.min]": "_getMinDate() ? _dateAdapter.toIso8601(_getMinDate()!) : null",
        "[attr.max]": "_getMaxDate() ? _dateAdapter.toIso8601(_getMaxDate()!) : null",
        "(blur)": "_onBlur()",
        "type": "text"
      },
      providers: [{
        provide: NG_VALUE_ACCESSOR,
        useExisting: MatEndDate,
        multi: true
      }, {
        provide: NG_VALIDATORS,
        useExisting: MatEndDate,
        multi: true
      }],
      // These need to be specified explicitly, because some tooling doesn't
      // seem to pick them up from the base class. See #20932.
      outputs: ["dateChange", "dateInput"]
    }]
  }], null, null);
})();
var _MatDateRangePicker = class _MatDateRangePicker extends MatDatepickerBase {
  _forwardContentValues(instance) {
    super._forwardContentValues(instance);
    const input = this.datepickerInput;
    if (input) {
      instance.comparisonStart = input.comparisonStart;
      instance.comparisonEnd = input.comparisonEnd;
      instance.startDateAccessibleName = input._getStartDateAccessibleName();
      instance.endDateAccessibleName = input._getEndDateAccessibleName();
    }
  }
};
__name(_MatDateRangePicker, "MatDateRangePicker");
__publicField(_MatDateRangePicker, "ɵfac", /* @__PURE__ */ (() => {
  let ɵMatDateRangePicker_BaseFactory;
  return /* @__PURE__ */ __name(function MatDateRangePicker_Factory(__ngFactoryType__) {
    return (ɵMatDateRangePicker_BaseFactory || (ɵMatDateRangePicker_BaseFactory = ɵɵgetInheritedFactory(_MatDateRangePicker)))(__ngFactoryType__ || _MatDateRangePicker);
  }, "MatDateRangePicker_Factory");
})());
__publicField(_MatDateRangePicker, "ɵcmp", ɵɵdefineComponent({
  type: _MatDateRangePicker,
  selectors: [["mat-date-range-picker"]],
  exportAs: ["matDateRangePicker"],
  features: [ɵɵProvidersFeature([MAT_RANGE_DATE_SELECTION_MODEL_PROVIDER, MAT_CALENDAR_RANGE_STRATEGY_PROVIDER, {
    provide: MatDatepickerBase,
    useExisting: _MatDateRangePicker
  }]), ɵɵInheritDefinitionFeature],
  decls: 0,
  vars: 0,
  template: /* @__PURE__ */ __name(function MatDateRangePicker_Template(rf, ctx) {
  }, "MatDateRangePicker_Template"),
  encapsulation: 2,
  changeDetection: 0
}));
var MatDateRangePicker = _MatDateRangePicker;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDateRangePicker, [{
    type: Component,
    args: [{
      selector: "mat-date-range-picker",
      template: "",
      exportAs: "matDateRangePicker",
      changeDetection: ChangeDetectionStrategy.OnPush,
      encapsulation: ViewEncapsulation.None,
      providers: [MAT_RANGE_DATE_SELECTION_MODEL_PROVIDER, MAT_CALENDAR_RANGE_STRATEGY_PROVIDER, {
        provide: MatDatepickerBase,
        useExisting: MatDateRangePicker
      }]
    }]
  }], null, null);
})();
var _MatDatepickerApply = class _MatDatepickerApply {
  _datepicker = inject(MatDatepickerBase);
  constructor() {
  }
  _applySelection() {
    this._datepicker._applyPendingSelection();
    this._datepicker.close();
  }
};
__name(_MatDatepickerApply, "MatDatepickerApply");
__publicField(_MatDatepickerApply, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerApply_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerApply)();
}, "MatDatepickerApply_Factory"));
__publicField(_MatDatepickerApply, "ɵdir", ɵɵdefineDirective({
  type: _MatDatepickerApply,
  selectors: [["", "matDatepickerApply", ""], ["", "matDateRangePickerApply", ""]],
  hostBindings: /* @__PURE__ */ __name(function MatDatepickerApply_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("click", /* @__PURE__ */ __name(function MatDatepickerApply_click_HostBindingHandler() {
        return ctx._applySelection();
      }, "MatDatepickerApply_click_HostBindingHandler"));
    }
  }, "MatDatepickerApply_HostBindings")
}));
var MatDatepickerApply = _MatDatepickerApply;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerApply, [{
    type: Directive,
    args: [{
      selector: "[matDatepickerApply], [matDateRangePickerApply]",
      host: {
        "(click)": "_applySelection()"
      }
    }]
  }], () => [], null);
})();
var _MatDatepickerCancel = class _MatDatepickerCancel {
  _datepicker = inject(MatDatepickerBase);
  constructor() {
  }
};
__name(_MatDatepickerCancel, "MatDatepickerCancel");
__publicField(_MatDatepickerCancel, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerCancel_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerCancel)();
}, "MatDatepickerCancel_Factory"));
__publicField(_MatDatepickerCancel, "ɵdir", ɵɵdefineDirective({
  type: _MatDatepickerCancel,
  selectors: [["", "matDatepickerCancel", ""], ["", "matDateRangePickerCancel", ""]],
  hostBindings: /* @__PURE__ */ __name(function MatDatepickerCancel_HostBindings(rf, ctx) {
    if (rf & 1) {
      ɵɵlistener("click", /* @__PURE__ */ __name(function MatDatepickerCancel_click_HostBindingHandler() {
        return ctx._datepicker.close();
      }, "MatDatepickerCancel_click_HostBindingHandler"));
    }
  }, "MatDatepickerCancel_HostBindings")
}));
var MatDatepickerCancel = _MatDatepickerCancel;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerCancel, [{
    type: Directive,
    args: [{
      selector: "[matDatepickerCancel], [matDateRangePickerCancel]",
      host: {
        "(click)": "_datepicker.close()"
      }
    }]
  }], () => [], null);
})();
var _MatDatepickerActions = class _MatDatepickerActions {
  _datepicker = inject(MatDatepickerBase);
  _viewContainerRef = inject(ViewContainerRef);
  _template;
  _portal;
  constructor() {
  }
  ngAfterViewInit() {
    this._portal = new TemplatePortal(this._template, this._viewContainerRef);
    this._datepicker.registerActions(this._portal);
  }
  ngOnDestroy() {
    this._datepicker.removeActions(this._portal);
    if (this._portal && this._portal.isAttached) {
      this._portal?.detach();
    }
  }
};
__name(_MatDatepickerActions, "MatDatepickerActions");
__publicField(_MatDatepickerActions, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerActions_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerActions)();
}, "MatDatepickerActions_Factory"));
__publicField(_MatDatepickerActions, "ɵcmp", ɵɵdefineComponent({
  type: _MatDatepickerActions,
  selectors: [["mat-datepicker-actions"], ["mat-date-range-picker-actions"]],
  viewQuery: /* @__PURE__ */ __name(function MatDatepickerActions_Query(rf, ctx) {
    if (rf & 1) {
      ɵɵviewQuery(TemplateRef, 5);
    }
    if (rf & 2) {
      let _t;
      ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx._template = _t.first);
    }
  }, "MatDatepickerActions_Query"),
  ngContentSelectors: _c1,
  decls: 1,
  vars: 0,
  consts: [[1, "mat-datepicker-actions"]],
  template: /* @__PURE__ */ __name(function MatDatepickerActions_Template(rf, ctx) {
    if (rf & 1) {
      ɵɵprojectionDef();
      ɵɵdomTemplate(0, MatDatepickerActions_ng_template_0_Template, 2, 0, "ng-template");
    }
  }, "MatDatepickerActions_Template"),
  styles: [".mat-datepicker-actions{display:flex;justify-content:flex-end;align-items:center;padding:0 8px 8px 8px}.mat-datepicker-actions .mat-mdc-button-base+.mat-mdc-button-base{margin-left:8px}[dir=rtl] .mat-datepicker-actions .mat-mdc-button-base+.mat-mdc-button-base{margin-left:0;margin-right:8px}\n"],
  encapsulation: 2,
  changeDetection: 0
}));
var MatDatepickerActions = _MatDatepickerActions;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerActions, [{
    type: Component,
    args: [{
      selector: "mat-datepicker-actions, mat-date-range-picker-actions",
      template: `
    <ng-template>
      <div class="mat-datepicker-actions">
        <ng-content></ng-content>
      </div>
    </ng-template>
  `,
      changeDetection: ChangeDetectionStrategy.OnPush,
      encapsulation: ViewEncapsulation.None,
      styles: [".mat-datepicker-actions{display:flex;justify-content:flex-end;align-items:center;padding:0 8px 8px 8px}.mat-datepicker-actions .mat-mdc-button-base+.mat-mdc-button-base{margin-left:8px}[dir=rtl] .mat-datepicker-actions .mat-mdc-button-base+.mat-mdc-button-base{margin-left:0;margin-right:8px}\n"]
    }]
  }], () => [], {
    _template: [{
      type: ViewChild,
      args: [TemplateRef]
    }]
  });
})();
var _MatDatepickerModule = class _MatDatepickerModule {
};
__name(_MatDatepickerModule, "MatDatepickerModule");
__publicField(_MatDatepickerModule, "ɵfac", /* @__PURE__ */ __name(function MatDatepickerModule_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _MatDatepickerModule)();
}, "MatDatepickerModule_Factory"));
__publicField(_MatDatepickerModule, "ɵmod", ɵɵdefineNgModule({
  type: _MatDatepickerModule,
  imports: [MatButtonModule, OverlayModule, A11yModule, PortalModule, MatCommonModule, MatCalendar, MatCalendarBody, MatDatepicker, MatDatepickerContent, MatDatepickerInput, MatDatepickerToggle, MatDatepickerToggleIcon, MatMonthView, MatYearView, MatMultiYearView, MatCalendarHeader, MatDateRangeInput, MatStartDate, MatEndDate, MatDateRangePicker, MatDatepickerActions, MatDatepickerCancel, MatDatepickerApply],
  exports: [CdkScrollableModule, MatCalendar, MatCalendarBody, MatDatepicker, MatDatepickerContent, MatDatepickerInput, MatDatepickerToggle, MatDatepickerToggleIcon, MatMonthView, MatYearView, MatMultiYearView, MatCalendarHeader, MatDateRangeInput, MatStartDate, MatEndDate, MatDateRangePicker, MatDatepickerActions, MatDatepickerCancel, MatDatepickerApply]
}));
__publicField(_MatDatepickerModule, "ɵinj", ɵɵdefineInjector({
  providers: [MatDatepickerIntl, MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY_PROVIDER],
  imports: [MatButtonModule, OverlayModule, A11yModule, PortalModule, MatCommonModule, MatDatepickerContent, MatDatepickerToggle, MatCalendarHeader, CdkScrollableModule]
}));
var MatDatepickerModule = _MatDatepickerModule;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(MatDatepickerModule, [{
    type: NgModule,
    args: [{
      imports: [MatButtonModule, OverlayModule, A11yModule, PortalModule, MatCommonModule, MatCalendar, MatCalendarBody, MatDatepicker, MatDatepickerContent, MatDatepickerInput, MatDatepickerToggle, MatDatepickerToggleIcon, MatMonthView, MatYearView, MatMultiYearView, MatCalendarHeader, MatDateRangeInput, MatStartDate, MatEndDate, MatDateRangePicker, MatDatepickerActions, MatDatepickerCancel, MatDatepickerApply],
      exports: [CdkScrollableModule, MatCalendar, MatCalendarBody, MatDatepicker, MatDatepickerContent, MatDatepickerInput, MatDatepickerToggle, MatDatepickerToggleIcon, MatMonthView, MatYearView, MatMultiYearView, MatCalendarHeader, MatDateRangeInput, MatStartDate, MatEndDate, MatDateRangePicker, MatDatepickerActions, MatDatepickerCancel, MatDatepickerApply],
      providers: [MatDatepickerIntl, MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY_PROVIDER]
    }]
  }], null, null);
})();
var matDatepickerAnimations = {
  // Represents:
  // trigger('transformPanel', [
  //   transition(
  //     'void => enter-dropdown',
  //     animate(
  //       '120ms cubic-bezier(0, 0, 0.2, 1)',
  //       keyframes([
  //         style({opacity: 0, transform: 'scale(1, 0.8)'}),
  //         style({opacity: 1, transform: 'scale(1, 1)'}),
  //       ]),
  //     ),
  //   ),
  //   transition(
  //     'void => enter-dialog',
  //     animate(
  //       '150ms cubic-bezier(0, 0, 0.2, 1)',
  //       keyframes([
  //         style({opacity: 0, transform: 'scale(0.7)'}),
  //         style({transform: 'none', opacity: 1}),
  //       ]),
  //     ),
  //   ),
  //   transition('* => void', animate('100ms linear', style({opacity: 0}))),
  // ])
  /** Transforms the height of the datepicker's calendar. */
  transformPanel: {
    type: 7,
    name: "transformPanel",
    definitions: [{
      type: 1,
      expr: "void => enter-dropdown",
      animation: {
        type: 4,
        styles: {
          type: 5,
          steps: [{
            type: 6,
            styles: {
              opacity: 0,
              transform: "scale(1, 0.8)"
            },
            offset: null
          }, {
            type: 6,
            styles: {
              opacity: 1,
              transform: "scale(1, 1)"
            },
            offset: null
          }]
        },
        timings: "120ms cubic-bezier(0, 0, 0.2, 1)"
      },
      options: null
    }, {
      type: 1,
      expr: "void => enter-dialog",
      animation: {
        type: 4,
        styles: {
          type: 5,
          steps: [{
            type: 6,
            styles: {
              opacity: 0,
              transform: "scale(0.7)"
            },
            offset: null
          }, {
            type: 6,
            styles: {
              transform: "none",
              opacity: 1
            },
            offset: null
          }]
        },
        timings: "150ms cubic-bezier(0, 0, 0.2, 1)"
      },
      options: null
    }, {
      type: 1,
      expr: "* => void",
      animation: {
        type: 4,
        styles: {
          type: 6,
          styles: {
            opacity: 0
          },
          offset: null
        },
        timings: "100ms linear"
      },
      options: null
    }],
    options: {}
  },
  // Represents:
  // trigger('fadeInCalendar', [
  //   state('void', style({opacity: 0})),
  //   state('enter', style({opacity: 1})),
  //   // TODO(crisbeto): this animation should be removed since it isn't quite on spec, but we
  //   // need to keep it until #12440 gets in, otherwise the exit animation will look glitchy.
  //   transition('void => *', animate('120ms 100ms cubic-bezier(0.55, 0, 0.55, 0.2)')),
  // ])
  /** Fades in the content of the calendar. */
  fadeInCalendar: {
    type: 7,
    name: "fadeInCalendar",
    definitions: [{
      type: 0,
      name: "void",
      styles: {
        type: 6,
        styles: {
          opacity: 0
        },
        offset: null
      }
    }, {
      type: 0,
      name: "enter",
      styles: {
        type: 6,
        styles: {
          opacity: 1
        },
        offset: null
      }
    }, {
      type: 1,
      expr: "void => *",
      animation: {
        type: 4,
        styles: null,
        timings: "120ms 100ms cubic-bezier(0.55, 0, 0.55, 0.2)"
      },
      options: null
    }],
    options: {}
  }
};
export {
  DateRange,
  DefaultMatCalendarRangeStrategy,
  MAT_DATEPICKER_SCROLL_STRATEGY,
  MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY,
  MAT_DATEPICKER_SCROLL_STRATEGY_FACTORY_PROVIDER,
  MAT_DATEPICKER_VALIDATORS,
  MAT_DATEPICKER_VALUE_ACCESSOR,
  MAT_DATE_RANGE_SELECTION_STRATEGY,
  MAT_RANGE_DATE_SELECTION_MODEL_FACTORY,
  MAT_RANGE_DATE_SELECTION_MODEL_PROVIDER,
  MAT_SINGLE_DATE_SELECTION_MODEL_FACTORY,
  MAT_SINGLE_DATE_SELECTION_MODEL_PROVIDER,
  MatCalendar,
  MatCalendarBody,
  MatCalendarCell,
  MatCalendarHeader,
  MatDateRangeInput,
  MatDateRangePicker,
  MatDateSelectionModel,
  MatDatepicker,
  MatDatepickerActions,
  MatDatepickerApply,
  MatDatepickerCancel,
  MatDatepickerContent,
  MatDatepickerInput,
  MatDatepickerInputEvent,
  MatDatepickerIntl,
  MatDatepickerModule,
  MatDatepickerToggle,
  MatDatepickerToggleIcon,
  MatEndDate,
  MatMonthView,
  MatMultiYearView,
  MatRangeDateSelectionModel,
  MatSingleDateSelectionModel,
  MatStartDate,
  MatYearView,
  matDatepickerAnimations,
  yearsPerPage,
  yearsPerRow
};
//# sourceMappingURL=@angular_material_datepicker.js.map
