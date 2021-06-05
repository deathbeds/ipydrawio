# IPyDrawio

|            demo             |            docs             |                                                            install                                                             |                               build                                |
| :-------------------------: | :-------------------------: | :----------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------: |
| [![binder-badge][]][binder] | [![docs][docs-badge]][docs] | [![install from pypi][pypi-badge]][pypi] [![install from conda-forge][conda-badge]][conda] [![reuse from npm][npm-badge]][npm] | [![build][workflow-badge]][workflow] [![coverage][cov-badge]][cov] |

> [Drawio][] diagrams for [JupyterLab][]. Forked with ❤️ from
> [QuantStack/jupyterlab-drawio][].

**[Install](#installation)** &middot; **[History]** &middot; **[Roadmap]**
&middot; **[Contribute][contributing]** &middot; **[Open Source](#open-source)**

> > This is BETA software. Native drawio files created with these tools _should_
> > work with any other [drawio][] client, but any UI/API is liable to change at
> > any time.

## Installation

```bash
mamba install -c conda-forge ipydrawio  # recommended, or...
conda install -c conda-forge ipydrawio  # or...
pip install ipydrawio
```

## Features

- `ipydrawio`
  - Edit multi-page [documents][]
    - with nearly the same UI and features as [diagrams.net][drawio]
    - in many file formats
      - Drawio/mxgraph XML, SVG, PNG
      - or Jupyter Notebooks
    - with all the Drawio templates
      - plus some Jupyter ones
  - Jupyter [rich display][] output
  - Jupyter [Widgets][]
- `ipydrawio-export`
  - Export print-quality PDF from diagrams
    - optionally include editable Drawio XML as a PDF attachment
    - > _BEWARE: some **heavy**, maybe fragile dependencies, `mamba`
      > recommended_
      ```bash
      mamba install -c conda-forge ipydrawio-export  # recommended, or...
      conda install -c conda-forge ipydrawio-export  # or...
      pip install ipydrawio ipydrawio-export
      ```

## Examples

|                                                        Note | Screenshot/Example               |
| ----------------------------------------------------------: | :------------------------------- |
|       Screenshot of drawio "minimal" UI with export options | [![poster-min]][poster-min]      |
|    The beginning of an interactive computational **poster** | [![poster][]][poster]            |
| A mixed computational/creative **roadmap** for this project | [~~Screenshot Needed~~][roadmap] |

## Usage

> Please see the [docs] for full information

- Try on [![binder-badge][]][binder]
  - or follow the [Installation instructions](#installation) and **Start
    JupyterLab**
- Open a diagram, by doing one of:
  - Creating a
    <img src="https://raw.githubusercontent.com/deathbeds/ipydrawio/master/packages/ipydrawio/style/img/drawio.svg" width="24"/>
    Diagram\_ from the [Launcher][]
  - Uploading a diagram created on [diagrams.net](https://diagrams.net) with the
    _[File Manager][]_ and double clicking it
  - Building diagrams by interactively computing in `IPython` with
    `ipydrawio.Diagram`
  - Use the `application/x-drawio` MIME renderer
- Use the _[Command Palette][]_ to _Export Diagram_ to various formats
  - > **NOTE**: some of the built-in UI features of drawio don't work properly
    > inside an IFrame in JupyterLab, and are difficult to robustly disable:
    > please see _Diagram_ options available in the _Command Palette_ and
    > various _Main Menu_ menus.

## Configuring

### UI Themes

Your default theme can be changed in the JupyterLab Main Menu:

- open _Settings_
- open _Diagram Theme_
- select your theme
- all open documents will change to this theme (prompting if not saved)
- all future documents will use this theme

The different themes have some advantages and disadvantages:

| theme     | default | full menu | layers | pages | light | dark | rough |
| --------- | :-----: | :-------: | :----: | :---: | :---: | :--: | :---: |
| `atlas`   |         |    ✔️     |   ✔️   |  ✔️   |  ✔️   |      |       |
| `dark`    |         |    ✔️     |   ✔️   |  ✔️   |       |  ✔️  |       |
| `kennedy` |         |    ✔️     |   ✔️   |  ✔️   |  ✔️   |      |       |
| `min`     |   ✔️    |           |   ✔️   |  ✔️   |  ✔️   |  ⚙️  |       |
| `sketch`  |         |           |   ✔️   |       |  ✔️   |  ⚙️  |  ✔️   |

> Note that `rough` will change how many shapes look

### Drawio Configuration and URL parameters

Use _Advanced Settings_ to modify drawio embedding parameters

> See the [schema] for full details of the (known) supported options as well as
> the [upstream docs] for all parameters, though IPyDrawio might not support
> them... yet.

[schema]: https://ipydrawio.readthedocs.io/en/stable/api/schema.html
[upstream docs]: https://www.diagrams.net/doc/faq/supported-url-parameters

### PDF: Lab and Server extensions

`ipydrawio-export` can generate print-quality PDF. This approach relies on a
headless browser, powered by [@jgraph/draw-image-export2], `puppeteer`, and
`nodejs`.

- **native dependencies** as required to appease `puppeteer`
  - if running in `docker`, this can be a bit trial-and-error
  - for more, see the [binder][apt-txt] and CI.
- `nodejs>10,<14` from `conda` or your system package manager
  - **NOTE**: this relies on being able to install `puppeteer` (and other
    **arbitrary dependencies** with `jlpm` for now **when first used**
    - _we'll figure out a better approach soon enough_
- `pip install ipydrawio-export` or
  `conda install -c conda-forge ipydrawio-export`

> For example to install all the dependencies:
>
> ```bash
> conda install -yc conda-forge ipydrawio-export
> ```

Once installed, you can use the in-browser tools _Export Diagram as PDF_ as well
as the command line:

```bash
jupyter ipydrawio-export <name of document>
```

## Open Source

### License

All files herein, unless otherwise noted, are free software licensed under
[Apache 2.0].

### Copyright

The copyright holders of this extension are the [contributors][] to this
repository.

Portions of the JupyterLab components are derived from
[QuantStack/jupyterlab-drawio][].

The copyright holders of drawio and drawio-export is
[jgraph](http://www.jgraph.com).

The original source code vendored in this package from:

- [@jgraph/drawio][]
- [@jgraph/draw-image-export2][]

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

[apache 2.0]: https://github.com/deathbeds/ipydrawio/blob/master/LICENSE.txt
[@jgraph/drawio]: https://github.com/jgraph/drawio
[@jgraph/draw-image-export2]: https://github.com/jgraph/draw-image-export2
[jupyterlab]: https://github.com/jupyterlab/jupyterlab
[drawio]: https://www.diagrams.net
[quantstack/jupyterlab-drawio]: https://github.com/QuantStack/jupyterlab-drawio
[contributors]: https://github.com/deathbeds/ipydrawio/graphs/contributors
[history]: https://github.com/deathbeds/ipydrawio/blob/master/CHANGELOG.md
[binder]:
  http://mybinder.org/v2/gh/deathbeds/ipydrawio/master?urlpath=lab/tree/docs/Poster.dio.svg
[binder-badge]: https://mybinder.org/badge_logo.svg
[workflow-badge]:
  https://github.com/deathbeds/ipydrawio/workflows/.github/workflows/ci.yml/badge.svg
[workflow]:
  https://github.com/deathbeds/ipydrawio/actions?query=branch%3Amaster+workflow%3A.github%2Fworkflows%2Fci.yml
[roadmap]: https://github.com/deathbeds/ipydrawio/blob/master/docs/ROADMAP.ipynb
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/ipydrawio
[conda]: https://anaconda.org/conda-forge/ipydrawio
[pypi-badge]: https://img.shields.io/pypi/v/ipydrawio
[pypi]: https://pypi.org/project/ipydrawio/
[npm]: https://npmjs.com/package/@deathbeds/ipydrawio
[npm-badge]: https://img.shields.io/npm/v/@deathbeds/ipydrawio
[cov-badge]:
  https://codecov.io/gh/deathbeds/ipydrawio/branch/master/graph/badge.svg?token=9B74VKHQDK
[cov]: https://codecov.io/gh/deathbeds/ipydrawio
[docs-badge]: https://readthedocs.org/projects/ipydrawio/badge/?version=latest
[docs]: https://ipydrawio.rtfd.io
[contributing]:
  https://github.com/deathbeds/ipydrawio/blob/master/CONTRIBUTING.md
[documents]:
  https://github.com/deathbeds/ipydrawio/blob/master/docs/Diagram%20Document.ipynb
[rich display]:
  https://github.com/deathbeds/ipydrawio/blob/master/docs/Diagram%20Rich%20Display.ipynb
[widgets]:
  https://github.com/deathbeds/ipydrawio/blob/master/docs/Diagram%20Widgets.ipynb
[puppeteer]: https://github.com/puppeteer/puppeteer
[@jgraph/draw-image-export2]: https://github.com/jgraph/draw-image-export2
[apt-txt]: https://github.com/deathbeds/ipydrawio/blob/master/.binder/apt.txt
[poster-min]:
  https://raw.githubusercontent.com/deathbeds/ipydrawio/master/docs/_static/images/poster.png
[poster]:
  https://raw.githubusercontent.com/deathbeds/ipydrawio/master/docs/Poster.dio.svg
[roadmap]:
  https://nbviewer.jupyter.org/github/deathbeds/ipydrawio/blob/master/docs/ROADMAP.ipynb
[command palette]:
  https://jupyterlab.readthedocs.io/en/stable/user/commands.html?highlight=command%20palette
[launcher]:
  https://jupyterlab.readthedocs.io/en/stable/user/files.html?highlight=Launcher#creating-files-and-activities
[file manager]: https://jupyterlab.readthedocs.io/en/stable/user/files.html
