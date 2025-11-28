import {
  ApplicationRef,
  EnvironmentInjector,
  Injectable,
  Injector,
  createComponent,
  inject,
  setClassMetadata,
  ɵɵdefineInjectable
} from "./chunk-L6HAKNJU.js";
import {
  __name,
  __publicField
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/cdk/fesm2022/style-loader.mjs
var appsWithLoaders = /* @__PURE__ */ new WeakMap();
var __CdkPrivateStyleLoader = class __CdkPrivateStyleLoader {
  _appRef;
  _injector = inject(Injector);
  _environmentInjector = inject(EnvironmentInjector);
  /**
   * Loads a set of styles.
   * @param loader Component which will be instantiated to load the styles.
   */
  load(loader) {
    const appRef = this._appRef = this._appRef || this._injector.get(ApplicationRef);
    let data = appsWithLoaders.get(appRef);
    if (!data) {
      data = {
        loaders: /* @__PURE__ */ new Set(),
        refs: []
      };
      appsWithLoaders.set(appRef, data);
      appRef.onDestroy(() => {
        appsWithLoaders.get(appRef)?.refs.forEach((ref) => ref.destroy());
        appsWithLoaders.delete(appRef);
      });
    }
    if (!data.loaders.has(loader)) {
      data.loaders.add(loader);
      data.refs.push(createComponent(loader, {
        environmentInjector: this._environmentInjector
      }));
    }
  }
};
__name(__CdkPrivateStyleLoader, "_CdkPrivateStyleLoader");
__publicField(__CdkPrivateStyleLoader, "ɵfac", /* @__PURE__ */ __name(function _CdkPrivateStyleLoader_Factory(__ngFactoryType__) {
  return new (__ngFactoryType__ || __CdkPrivateStyleLoader)();
}, "_CdkPrivateStyleLoader_Factory"));
__publicField(__CdkPrivateStyleLoader, "ɵprov", ɵɵdefineInjectable({
  token: __CdkPrivateStyleLoader,
  factory: __CdkPrivateStyleLoader.ɵfac,
  providedIn: "root"
}));
var _CdkPrivateStyleLoader = __CdkPrivateStyleLoader;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(_CdkPrivateStyleLoader, [{
    type: Injectable,
    args: [{
      providedIn: "root"
    }]
  }], null, null);
})();

export {
  _CdkPrivateStyleLoader
};
//# sourceMappingURL=chunk-3UAARJPV.js.map
