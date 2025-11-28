import {
  NgModule,
  setClassMetadata,
  ɵɵdefineInjector,
  ɵɵdefineNgModule
} from "./chunk-L6HAKNJU.js";
import {
  __name,
  __publicField
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/cdk/fesm2022/platform.mjs
var _PlatformModule = class _PlatformModule {
};
__name(_PlatformModule, "PlatformModule");
__publicField(_PlatformModule, "ɵfac", /* @__PURE__ */ __name(function PlatformModule_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || _PlatformModule)();
}, "PlatformModule_Factory"));
__publicField(_PlatformModule, "ɵmod", ɵɵdefineNgModule({
  type: _PlatformModule
}));
__publicField(_PlatformModule, "ɵinj", ɵɵdefineInjector({}));
var PlatformModule = _PlatformModule;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(PlatformModule, [{
    type: NgModule,
    args: [{}]
  }], null, null);
})();
var supportedInputTypes;
var candidateInputTypes = [
  // `color` must come first. Chrome 56 shows a warning if we change the type to `color` after
  // first changing it to something else:
  // The specified value "" does not conform to the required format.
  // The format is "#rrggbb" where rr, gg, bb are two-digit hexadecimal numbers.
  "color",
  "button",
  "checkbox",
  "date",
  "datetime-local",
  "email",
  "file",
  "hidden",
  "image",
  "month",
  "number",
  "password",
  "radio",
  "range",
  "reset",
  "search",
  "submit",
  "tel",
  "text",
  "time",
  "url",
  "week"
];
function getSupportedInputTypes() {
  if (supportedInputTypes) {
    return supportedInputTypes;
  }
  if (typeof document !== "object" || !document) {
    supportedInputTypes = new Set(candidateInputTypes);
    return supportedInputTypes;
  }
  let featureTestInput = document.createElement("input");
  supportedInputTypes = new Set(candidateInputTypes.filter((value) => {
    featureTestInput.setAttribute("type", value);
    return featureTestInput.type === value;
  }));
  return supportedInputTypes;
}
__name(getSupportedInputTypes, "getSupportedInputTypes");

export {
  getSupportedInputTypes
};
//# sourceMappingURL=chunk-55OABCSW.js.map
