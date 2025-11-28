import {
  __name
} from "./chunk-KQSGOR2U.js";

// node_modules/@angular/cdk/fesm2022/coercion.mjs
function coerceBooleanProperty(value) {
  return value != null && `${value}` !== "false";
}
__name(coerceBooleanProperty, "coerceBooleanProperty");
function coerceStringArray(value, separator = /\s+/) {
  const result = [];
  if (value != null) {
    const sourceValues = Array.isArray(value) ? value : `${value}`.split(separator);
    for (const sourceValue of sourceValues) {
      const trimmedString = `${sourceValue}`.trim();
      if (trimmedString) {
        result.push(trimmedString);
      }
    }
  }
  return result;
}
__name(coerceStringArray, "coerceStringArray");

export {
  coerceBooleanProperty,
  coerceStringArray
};
//# sourceMappingURL=chunk-CGUWAHN6.js.map
