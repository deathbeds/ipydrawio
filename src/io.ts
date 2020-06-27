import { Contents } from "@jupyterlab/services";

import { LabIcon } from "@jupyterlab/ui-components";

import DRAWIO_ICON_SVG from "../style/img/drawio.svg";
import { DrawioWidget } from "./editor";
import { PageConfig } from "@jupyterlab/coreutils";
import { ISettingRegistry } from "@jupyterlab/settingregistry";

export interface IDrawioFormat {
  key: string;
  name: string;
  ext: string;
  label: string;
  icon: LabIcon;
  format: Contents.FileFormat;
  mimetype: string;
  pattern?: string;
  save?: (raw: string) => string;
  load?: (raw: string) => string;
  exporter?: (
    drawio: DrawioWidget,
    key: string,
    settings: ISettingRegistry.ISettings
  ) => Promise<string>;
}

const iconRegEx = /jp-icon-warn0/;

export const drawioIcon = new LabIcon({
  name: "drawio:drawio",
  svgstr: DRAWIO_ICON_SVG,
});

export const drawioSvgIcon = new LabIcon({
  name: "drawio:svg",
  svgstr: DRAWIO_ICON_SVG.replace(iconRegEx, "jp-icon-contrast1"),
});

export const drawioPngIcon = new LabIcon({
  name: "drawio:png",
  svgstr: DRAWIO_ICON_SVG.replace(iconRegEx, "jp-icon-contrast0"),
});

// basically works, but needs a really solid story about where it will be published
// export const drawioHtmlIcon = new LabIcon({
//   name: "drawio:html",
//   svgstr: DRAWIO_ICON_SVG.replace(iconRegEx, "jp-icon-brand0"),
// });

const stripDataURI = (raw: string) => raw.split(",")[1];

const unbase64SVG = (raw: string) => atob(stripDataURI(raw));

export const XML_NATIVE: IDrawioFormat = {
  ext: ".dio",
  format: "text",
  icon: drawioIcon,
  key: "drawio",
  label: "Diagram",
  mimetype: "application/dio",
  name: "dio",
};

export const SVG_PLAIN: IDrawioFormat = {
  ext: ".svg",
  format: "text",
  icon: drawioSvgIcon,
  key: "svg",
  label: "SVG",
  mimetype: "image/svg+xml",
  name: "svg",
  save: unbase64SVG,
};

export const SVG_EDITABLE: IDrawioFormat = {
  ...SVG_PLAIN,
  ext: ".dio.svg",
  key: "xmlsvg",
  label: "SVG (Editable)",
  name: "diosvg",
  pattern: "^.*.dio.svg$",
};

// export const HTML_PLAIN: IDrawioFormat = {
//   ext: ".html",
//   format: "text",
//   icon: drawioHtmlIcon,
//   key: "html2",
//   label: "HTML",
//   mimetype: "text/html",
//   name: "html"
// }

// export const HTML_EDITABLE: IDrawioFormat = {
//   ...HTML_PLAIN,
//   ext: ".dio.html",
//   icon: drawioHtmlIcon,
//   key: "html2",
//   label: "HTML (Editable)",
//   name: "diohtml",
//   pattern: "^.*.dio.html$",
//   save: String
// };

export const PNG_PLAIN: IDrawioFormat = {
  ext: ".png",
  format: "base64",
  icon: drawioPngIcon,
  key: "png",
  label: "PNG",
  mimetype: "image/png",
  name: "png",
  save: stripDataURI,
};

export const PNG_EDITABLE: IDrawioFormat = {
  ...PNG_PLAIN,
  ext: ".dio.png",
  key: "xmlpng",
  label: "PNG (Editable)",
  name: "diopng",
  pattern: "^.*.dio.png$",
};

export const PDF_PLAIN: IDrawioFormat = {
  ext: ".pdf",
  format: "base64",
  icon: drawioPngIcon,
  key: "pdf",
  label: "PDF",
  mimetype: "application/pdf",
  name: "pdf",
  save: stripDataURI,
  exporter: async (widget, key, settings) => {
    let drawioExportUrl = "./drawio-export-demo";
    try {
      drawioExportUrl = (settings.composite["drawioExportDemo"] as any)["url"];
    } catch (err) {
      console.warn(err);
    }
    if (drawioExportUrl.indexOf("./") !== 0) {
      console.error(`don't know how to handle non-relative URLs`);
      return;
    }
    const xml = widget.context.model.toString();
    let url = `${PageConfig.getBaseUrl()}${drawioExportUrl.slice(2)}`;
    url += url.endsWith("/") ? "" : "/";
    const query = new URLSearchParams();
    query.append("xml", xml);
    query.append("format", "pdf");
    query.append("base64", "1");

    const response = await fetch(`${url}?token=${PageConfig.getToken()}`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: query.toString(),
    });

    const text = await response.text();

    return `application/pdf;base64,${text}`;
  },
};

export const EXPORT_FORMATS = [
  // HTML_EDITABLE,
  PNG_EDITABLE,
  PNG_PLAIN,
  SVG_EDITABLE,
  SVG_PLAIN,
  PDF_PLAIN,
];

export const ALL_BINARY_FORMATS = [PNG_PLAIN, PNG_EDITABLE, PDF_PLAIN];

export const ALL_TEXT_FORMATS = [
  // HTML_EDITABLE,
  // HTML_PLAIN,
  SVG_EDITABLE,
  SVG_PLAIN,
  XML_NATIVE,
];

export const DEFAULT_TEXT_FORMATS = [
  // HTML_EDITABLE,
  SVG_EDITABLE,
  XML_NATIVE,
];
export const DEFAULT_BINARY_FORMATS = [PNG_EDITABLE];
export const ALL_FORMATS = [...ALL_BINARY_FORMATS, ...ALL_TEXT_FORMATS];

export const EXPORT_MIME_MAP = new Map<string, IDrawioFormat>([
  [PNG_EDITABLE.mimetype, PNG_EDITABLE],
  [SVG_EDITABLE.mimetype, SVG_EDITABLE],
  // [HTML_EDITABLE.mimetype, HTML_EDITABLE],
  [PDF_PLAIN.mimetype, PDF_PLAIN],
]);
