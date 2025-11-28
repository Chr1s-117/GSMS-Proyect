import {
  MatFormFieldModule
} from "./chunk-RU2IYAIA.js";
import {
  MAT_ERROR,
  MAT_FORM_FIELD,
  MAT_FORM_FIELD_DEFAULT_OPTIONS,
  MAT_PREFIX,
  MAT_SUFFIX,
  MatError,
  MatFormField,
  MatFormFieldControl,
  MatHint,
  MatLabel,
  MatPrefix,
  MatSuffix,
  getMatFormFieldDuplicatedHintError,
  getMatFormFieldMissingControlError,
  getMatFormFieldPlaceholderConflictError
} from "./chunk-XPIMXOAB.js";
import "./chunk-55OABCSW.js";
import "./chunk-CGUWAHN6.js";
import "./chunk-BGN7QJKV.js";
import "./chunk-GXIY53OB.js";
import "./chunk-ZGDQ3GWN.js";
import "./chunk-6BKD3BMU.js";
import "./chunk-D6EGXCKV.js";
import "./chunk-HAI453QW.js";
import "./chunk-U5634LHI.js";
import "./chunk-3UAARJPV.js";
import "./chunk-I6BOHX6S.js";
import "./chunk-GXOWEAQE.js";
import "./chunk-WMCYXEPE.js";
import "./chunk-L6HAKNJU.js";
import "./chunk-AHFTOZG5.js";
import "./chunk-GR6CC6I7.js";
import "./chunk-YRHOY6S2.js";
import "./chunk-QQHXZCUH.js";
import "./chunk-KQSGOR2U.js";

// node_modules/@angular/material/fesm2022/form-field.mjs
var matFormFieldAnimations = {
  // Represents:
  // trigger('transitionMessages', [
  //   // TODO(mmalerba): Use angular animations for label animation as well.
  //   state('enter', style({opacity: 1, transform: 'translateY(0%)'})),
  //   transition('void => enter', [
  //     style({opacity: 0, transform: 'translateY(-5px)'}),
  //     animate('300ms cubic-bezier(0.55, 0, 0.55, 0.2)'),
  //   ]),
  // ])
  /** Animation that transitions the form field's error and hint messages. */
  transitionMessages: {
    type: 7,
    name: "transitionMessages",
    definitions: [
      {
        type: 0,
        name: "enter",
        styles: {
          type: 6,
          styles: { opacity: 1, transform: "translateY(0%)" },
          offset: null
        }
      },
      {
        type: 1,
        expr: "void => enter",
        animation: [
          { type: 6, styles: { opacity: 0, transform: "translateY(-5px)" }, offset: null },
          { type: 4, styles: null, timings: "300ms cubic-bezier(0.55, 0, 0.55, 0.2)" }
        ],
        options: null
      }
    ],
    options: {}
  }
};
export {
  MAT_ERROR,
  MAT_FORM_FIELD,
  MAT_FORM_FIELD_DEFAULT_OPTIONS,
  MAT_PREFIX,
  MAT_SUFFIX,
  MatError,
  MatFormField,
  MatFormFieldControl,
  MatFormFieldModule,
  MatHint,
  MatLabel,
  MatPrefix,
  MatSuffix,
  getMatFormFieldDuplicatedHintError,
  getMatFormFieldMissingControlError,
  getMatFormFieldPlaceholderConflictError,
  matFormFieldAnimations
};
//# sourceMappingURL=@angular_material_form-field.js.map
