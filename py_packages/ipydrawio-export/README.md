# IPyDrawio Export

[![binder-badge][]][binder] [![install from pypi][pypi-badge]][pypi]
[![install from conda-forge][conda-badge]][conda]
[![build][workflow-badge]][workflow] [![coverage][cov-badge]][cov]

> PDF export of [drawio](https://www.diagrams.net) diagrams for JupyterLab.

See the [main project repo](https://github.com/deathbeds/ipydrawio) for more
information.

## Installation

> _Note: the `mamba`/`conda` installation method ensures `nodejs` is available_

```bash
mamba install -c conda-forge ipydrawio-export  # recommended, or...
conda install -c conda-forge ipydrawio-export  # or...
pip install ipydrawio-export
```

## Server Extension

`ipydrawio-export` runs as a [server extension][serverext]. When installed, it
_should_ be automatically configured. If problems arise, it can be manually
_enabled_:

```bash
jupyter server extension list   # If you don't see it here...
jupyter server extension enable --sys-prefix --py ipydrawio_export  # run this...
jupyter server extension list   # ... then check it again
```

> Note: If you are starting your server with `jupyter notebook` (not
> `jupyter lab`), the commands above will be `serverextension` instead of
> `server extension`!

## Command-Line Usage

### Exporting PDF

PDF can also be generated from the command line:

```bash
jupyter drawio-export pdf some_file.dio
```

If needed, the `nodejs` application will be installed into the Jupyter data
path.

```bash
jupyter config --paths  # it uses the one in the environment
```

> In the future, it's hoped this can be packaged more conveniently.

### Provisioning

To ensure the `nodejs` application is installed _without_ exporting a PDF (e.g
when building a `docker` container).

```bash
jupyter ipydrawio-export provision
```

### Provision locations

If defined, these environment variables will be respected, and an
`ipydrawio_export` folder will be created within:

- `$JUPYTER_DATA_DIR`
- `$IPYDRAWIO_DATA_DIR`

Otherwise, `ipydrawio-export` will provision its files into
`{sys.prefix}/share/jupyter/ipydrawio_export`.

Of note:

- access to the internet is required
- this location must be writeable by the user
- there must be about 400MiB available, primarily for `puppeteer`'s `chromium`

The effective location can be verified with:

```bash
jupyter ipydrawio-export provision --workdir
```

## Open Source

This work is licensed under the [Apache-2.0] License.

The vendored code from [@jgraph/draw-image-export2][] is also licensed under the
[Apache-2.0][draw2-license] License.

```
Copyright 2021 ipydrawio contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

[@jgraph/draw-image-export2]: https://github.com/jgraph/draw-image-export2
[apache-2.0]:
  https://github.com/deathbeds/ipydrawio/blob/master/py_packages/ipydrawio-export/LICENSE.txt
[draw2-license]:
  https://github.com/jgraph/draw-image-export2/blob/master/LICENSE
[serverext]:
  https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html
[binder]:
  http://mybinder.org/v2/gh/deathbeds/ipydrawio/master?urlpath=lab/tree/docs/Poster.dio.svg
[binder-badge]: https://mybinder.org/badge_logo.svg
[pypi-badge]: https://img.shields.io/pypi/v/ipydrawio-export
[pypi]: https://pypi.org/project/ipydrawio-export
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/ipydrawio-export
[conda]: https://anaconda.org/conda-forge/ipydrawio-export
[workflow-badge]:
  https://github.com/deathbeds/ipydrawio/workflows/.github/workflows/ci.yml/badge.svg
[workflow]:
  https://github.com/deathbeds/ipydrawio/actions?query=branch%3Amaster+workflow%3A.github%2Fworkflows%2Fci.yml
[cov-badge]:
  https://codecov.io/gh/deathbeds/ipydrawio/branch/master/graph/badge.svg?token=9B74VKHQDK
[cov]: https://codecov.io/gh/deathbeds/ipydrawio
