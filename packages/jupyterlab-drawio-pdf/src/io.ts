import { PageConfig } from '@jupyterlab/coreutils';
import {
  IDiagramManager,
  DRAWIO_ICON_CLASS_RE,
  DRAWIO_ICON_SVG,
  DEBUG,
} from '@deathbeds/jupyterlab-drawio/lib/tokens';

import { stripDataURI } from '@deathbeds/jupyterlab-drawio/lib/utils';

import { LabIcon } from '@jupyterlab/ui-components';

export const drawioPdfIcon = new LabIcon({
  name: 'drawio:pdf',
  svgstr: DRAWIO_ICON_SVG.replace(DRAWIO_ICON_CLASS_RE, 'jp-icon-contrast2'),
});

export const PDF_PLAIN: IDiagramManager.IFormat = {
  ext: '.pdf',
  format: 'base64',
  factoryName: `Diagram (PDF)`,
  icon: drawioPdfIcon,
  key: 'pdf',
  label: 'PDF',
  mimetype: 'application/pdf',
  modelName: 'base64',
  name: 'pdf',
  isExport: true,
  isBinary: true,
  save: stripDataURI,
  exporter: async (widget, key, settings) => {
    let drawioExportUrl = './drawio/export/';
    try {
      drawioExportUrl = (settings.composite['drawioExportUrl'] as any)['url'];
    } catch (err) {
      DEBUG && console.warn('using fallback url', err);
    }
    if (drawioExportUrl.indexOf('./') !== 0) {
      console.error(`don't know how to handle non-relative URLs`);
      return null;
    }
    const currentFormat = widget.format;

    const xml = currentFormat?.toXML
      ? currentFormat.toXML(widget.context.model)
      : widget.context.model.toString();

    let url = `${PageConfig.getBaseUrl()}${drawioExportUrl.slice(2)}`;
    url += url.endsWith('/') ? '' : '/';
    const query = new URLSearchParams();
    // TODO: expose, understand, schematize this form API
    query.append('xml', xml);
    query.append('format', 'pdf');
    query.append('base64', '1');

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-XSRFToken': getCookie('_xsrf') || '',
      },
      body: query.toString(),
    });

    const text = await response.text();

    return `application/pdf;base64,${text}`;
  },
};

export const PDF_BRANDED = {
  ...PDF_PLAIN,
  factoryName: `Diagram (Editable PDF)`,
  key: 'pdf-editable',
  ext: '.dio.pdf',
};

function getCookie(name: string): string | undefined {
  // From http://www.tornadoweb.org/en/stable/guide/security.html
  const matches = document.cookie.match('\\b' + name + '=([^;]*)\\b');
  return matches?.[1];
}
