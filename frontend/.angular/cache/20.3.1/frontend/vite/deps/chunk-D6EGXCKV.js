import {
  APP_ID,
  Injectable,
  inject,
  setClassMetadata,
  ɵɵdefineInjectable
} from "./chunk-L6HAKNJU.js";
import {
  __name,
  __publicField
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/cdk/fesm2022/shadow-dom.mjs
var shadowDomIsSupported;
function _supportsShadowDom() {
  if (shadowDomIsSupported == null) {
    const head = typeof document !== "undefined" ? document.head : null;
    shadowDomIsSupported = !!(head && (head.createShadowRoot || head.attachShadow));
  }
  return shadowDomIsSupported;
}
__name(_supportsShadowDom, "_supportsShadowDom");
function _getShadowRoot(element) {
  if (_supportsShadowDom()) {
    const rootNode = element.getRootNode ? element.getRootNode() : null;
    if (typeof ShadowRoot !== "undefined" && ShadowRoot && rootNode instanceof ShadowRoot) {
      return rootNode;
    }
  }
  return null;
}
__name(_getShadowRoot, "_getShadowRoot");
function _getFocusedElementPierceShadowDom() {
  let activeElement = typeof document !== "undefined" && document ? document.activeElement : null;
  while (activeElement && activeElement.shadowRoot) {
    const newActiveElement = activeElement.shadowRoot.activeElement;
    if (newActiveElement === activeElement) {
      break;
    } else {
      activeElement = newActiveElement;
    }
  }
  return activeElement;
}
__name(_getFocusedElementPierceShadowDom, "_getFocusedElementPierceShadowDom");
function _getEventTarget(event) {
  return event.composedPath ? event.composedPath()[0] : event.target;
}
__name(_getEventTarget, "_getEventTarget");

// node_modules/@angular/cdk/fesm2022/array.mjs
function coerceArray(value) {
  return Array.isArray(value) ? value : [value];
}
__name(coerceArray, "coerceArray");

// node_modules/@angular/cdk/fesm2022/id-generator.mjs
var counters = {};
var __IdGenerator = class __IdGenerator {
  _appId = inject(APP_ID);
  /**
   * Generates a unique ID with a specific prefix.
   * @param prefix Prefix to add to the ID.
   */
  getId(prefix) {
    if (this._appId !== "ng") {
      prefix += this._appId;
    }
    if (!counters.hasOwnProperty(prefix)) {
      counters[prefix] = 0;
    }
    return `${prefix}${counters[prefix]++}`;
  }
};
__name(__IdGenerator, "_IdGenerator");
__publicField(__IdGenerator, "ɵfac", /* @__PURE__ */ __name(function _IdGenerator_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || __IdGenerator)();
}, "_IdGenerator_Factory"));
__publicField(__IdGenerator, "ɵprov", ɵɵdefineInjectable({
  token: __IdGenerator,
  factory: __IdGenerator.ɵfac,
  providedIn: "root"
}));
var _IdGenerator = __IdGenerator;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(_IdGenerator, [{
    type: Injectable,
    args: [{
      providedIn: "root"
    }]
  }], null, null);
})();

// node_modules/@angular/cdk/fesm2022/keycodes2.mjs
var BACKSPACE = 8;
var TAB = 9;
var ENTER = 13;
var SHIFT = 16;
var CONTROL = 17;
var ALT = 18;
var ESCAPE = 27;
var SPACE = 32;
var PAGE_UP = 33;
var PAGE_DOWN = 34;
var END = 35;
var HOME = 36;
var LEFT_ARROW = 37;
var UP_ARROW = 38;
var RIGHT_ARROW = 39;
var DOWN_ARROW = 40;
var ZERO = 48;
var NINE = 57;
var A = 65;
var Z = 90;
var META = 91;
var MAC_META = 224;

// node_modules/@angular/cdk/fesm2022/keycodes.mjs
function hasModifierKey(event, ...modifiers) {
  if (modifiers.length) {
    return modifiers.some((modifier) => event[modifier]);
  }
  return event.altKey || event.shiftKey || event.ctrlKey || event.metaKey;
}
__name(hasModifierKey, "hasModifierKey");

export {
  _getShadowRoot,
  _getFocusedElementPierceShadowDom,
  _getEventTarget,
  coerceArray,
  _IdGenerator,
  BACKSPACE,
  TAB,
  ENTER,
  SHIFT,
  CONTROL,
  ALT,
  ESCAPE,
  SPACE,
  PAGE_UP,
  PAGE_DOWN,
  END,
  HOME,
  LEFT_ARROW,
  UP_ARROW,
  RIGHT_ARROW,
  DOWN_ARROW,
  ZERO,
  NINE,
  A,
  Z,
  META,
  MAC_META,
  hasModifierKey
};
//# sourceMappingURL=chunk-D6EGXCKV.js.map
