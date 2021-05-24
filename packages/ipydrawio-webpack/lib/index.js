import { URLExt, PageConfig } from '@jupyterlab/coreutils';
/**
 * The path on the server to base application HTML, to be served in an iframe
 */
export const DRAWIO_URL = URLExt.join(
  PageConfig.getOption('fullLabextensionsUrl'),
  '@deathbeds/ipydrawio-webpack/static/dio/index.html'
);
