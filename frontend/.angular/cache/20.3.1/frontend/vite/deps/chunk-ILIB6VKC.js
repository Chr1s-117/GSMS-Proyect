import {
  Injectable,
  setClassMetadata,
  ɵɵdefineInjectable
} from "./chunk-L6HAKNJU.js";
import {
  __name,
  __publicField
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/cdk/fesm2022/unique-selection-dispatcher.mjs
var _UniqueSelectionDispatcher = class _UniqueSelectionDispatcher {
  _listeners = [];
  /**
   * Notify other items that selection for the given name has been set.
   * @param id ID of the item.
   * @param name Name of the item.
   */
  notify(id, name) {
    for (let listener of this._listeners) {
      listener(id, name);
    }
  }
  /**
   * Listen for future changes to item selection.
   * @return Function used to deregister listener
   */
  listen(listener) {
    this._listeners.push(listener);
    return () => {
      this._listeners = this._listeners.filter((registered) => {
        return listener !== registered;
      });
    };
  }
  ngOnDestroy() {
    this._listeners = [];
  }
};
__name(_UniqueSelectionDispatcher, "UniqueSelectionDispatcher");
__publicField(_UniqueSelectionDispatcher, "ɵfac", /* @__PURE__ */ __name(function UniqueSelectionDispatcher_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _UniqueSelectionDispatcher)();
}, "UniqueSelectionDispatcher_Factory"));
__publicField(_UniqueSelectionDispatcher, "ɵprov", ɵɵdefineInjectable({
  token: _UniqueSelectionDispatcher,
  factory: _UniqueSelectionDispatcher.ɵfac,
  providedIn: "root"
}));
var UniqueSelectionDispatcher = _UniqueSelectionDispatcher;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(UniqueSelectionDispatcher, [{
    type: Injectable,
    args: [{
      providedIn: "root"
    }]
  }], null, null);
})();

export {
  UniqueSelectionDispatcher
};
//# sourceMappingURL=chunk-ILIB6VKC.js.map
