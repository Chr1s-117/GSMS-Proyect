import {
  Injectable,
  setClassMetadata,
  ɵɵdefineInjectable
} from "./chunk-L6HAKNJU.js";
import {
  __name,
  __publicField
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/material/fesm2022/error-state.mjs
var __ErrorStateTracker = class __ErrorStateTracker {
  _defaultMatcher;
  ngControl;
  _parentFormGroup;
  _parentForm;
  _stateChanges;
  /** Whether the tracker is currently in an error state. */
  errorState = false;
  /** User-defined matcher for the error state. */
  matcher;
  constructor(_defaultMatcher, ngControl, _parentFormGroup, _parentForm, _stateChanges) {
    this._defaultMatcher = _defaultMatcher;
    this.ngControl = ngControl;
    this._parentFormGroup = _parentFormGroup;
    this._parentForm = _parentForm;
    this._stateChanges = _stateChanges;
  }
  /** Updates the error state based on the provided error state matcher. */
  updateErrorState() {
    const oldState = this.errorState;
    const parent = this._parentFormGroup || this._parentForm;
    const matcher = this.matcher || this._defaultMatcher;
    const control = this.ngControl ? this.ngControl.control : null;
    const newState = matcher?.isErrorState(control, parent) ?? false;
    if (newState !== oldState) {
      this.errorState = newState;
      this._stateChanges.next();
    }
  }
};
__name(__ErrorStateTracker, "_ErrorStateTracker");
var _ErrorStateTracker = __ErrorStateTracker;

// node_modules/@angular/material/fesm2022/error-options.mjs
var _ShowOnDirtyErrorStateMatcher = class _ShowOnDirtyErrorStateMatcher {
  isErrorState(control, form) {
    return !!(control && control.invalid && (control.dirty || form && form.submitted));
  }
};
__name(_ShowOnDirtyErrorStateMatcher, "ShowOnDirtyErrorStateMatcher");
__publicField(_ShowOnDirtyErrorStateMatcher, "ɵfac", /* @__PURE__ */ __name(function ShowOnDirtyErrorStateMatcher_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _ShowOnDirtyErrorStateMatcher)();
}, "ShowOnDirtyErrorStateMatcher_Factory"));
__publicField(_ShowOnDirtyErrorStateMatcher, "ɵprov", ɵɵdefineInjectable({
  token: _ShowOnDirtyErrorStateMatcher,
  factory: _ShowOnDirtyErrorStateMatcher.ɵfac
}));
var ShowOnDirtyErrorStateMatcher = _ShowOnDirtyErrorStateMatcher;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(ShowOnDirtyErrorStateMatcher, [{
    type: Injectable
  }], null, null);
})();
var _ErrorStateMatcher = class _ErrorStateMatcher {
  isErrorState(control, form) {
    return !!(control && control.invalid && (control.touched || form && form.submitted));
  }
};
__name(_ErrorStateMatcher, "ErrorStateMatcher");
__publicField(_ErrorStateMatcher, "ɵfac", /* @__PURE__ */ __name(function ErrorStateMatcher_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _ErrorStateMatcher)();
}, "ErrorStateMatcher_Factory"));
__publicField(_ErrorStateMatcher, "ɵprov", ɵɵdefineInjectable({
  token: _ErrorStateMatcher,
  factory: _ErrorStateMatcher.ɵfac,
  providedIn: "root"
}));
var ErrorStateMatcher = _ErrorStateMatcher;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(ErrorStateMatcher, [{
    type: Injectable,
    args: [{
      providedIn: "root"
    }]
  }], null, null);
})();

export {
  _ErrorStateTracker,
  ShowOnDirtyErrorStateMatcher,
  ErrorStateMatcher
};
//# sourceMappingURL=chunk-I3J5DV5L.js.map
