import { ReadonlyPartialJSONObject } from '@lumino/coreutils';
import { NotebookModel } from '@jupyterlab/notebook';
import { Contents } from '@jupyterlab/services';

import {
  IFormat,
  DRAWIO_ICON_CLASS_RE,
  DRAWIO_ICON_SVG,
  JSON_FACTORY,
  DRAWIO_METADATA,
} from '@deathbeds/ipydrawio';

import { LabIcon } from '@jupyterlab/ui-components';

export const drawioIpynbIcon = new LabIcon({
  name: 'drawio:ipynb',
  svgstr: DRAWIO_ICON_SVG.replace(DRAWIO_ICON_CLASS_RE, 'jp-icon-contrast3'),
});

export const IPYNB_EDITABLE: IFormat<any> = {
  ext: '.dio.ipynb',
  factoryName: `${JSON_FACTORY} (Notebook)`,
  key: 'ipynb',
  format: 'json',
  icon: drawioIpynbIcon,
  label: 'Diagram Notebook',
  mimetype: 'application/x-ipynb+json',
  name: 'dionotebook',
  pattern: '.*.dio.ipynb$',
  contentType: 'notebook',
  modelName: 'notebook',
  isJson: true,
  isEditable: true,
  isExport: true,
  isDefault: true,
  isTransformed: true,
  wantsModel(contentsModel: Contents.IModel) {
    return contentsModel.type === 'notebook';
  },
  save: (raw) => {
    return raw;
  },
  fromXML: (model: NotebookModel, xml) => {
    const meta = model.metadata.get(
      DRAWIO_METADATA
    ) as ReadonlyPartialJSONObject;
    model.metadata.set(DRAWIO_METADATA, { ...(meta || {}), xml });
  },
  toXML: (model: NotebookModel) => {
    const meta = model.metadata.get(
      DRAWIO_METADATA
    ) as ReadonlyPartialJSONObject;
    return meta?.xml ? `${meta.xml}` : '';
  },
  exporter: async (widget, key, settings) => {
    const xml = widget.adapter.toXML();
    const newModel = new NotebookModel();
    newModel.metadata.set(DRAWIO_METADATA, { xml });
    return newModel.toJSON();
  },
};
