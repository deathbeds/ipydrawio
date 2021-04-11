# IPyDrawio

[![binder-badge][]][binder] [![install from pypi][pypi-badge]][pypi]
[![reuse from npm][npm-badge]][npm] [![build][workflow-badge]][workflow]
[![coverage][cov-badge]][cov]

> [Drawio][] diagrams for [JupyterLab][]. Forked with ❤️ from
> [QuantStack/jupyterlab-drawio][].

**[Install](#installation)** &middot; **[History]** &middot; **[Roadmap]**
&middot; **[Contribute][contributing]** &middot; **[Open Source](#open-source)**

> > This is BETA software. Native drawio files created with these tools _should_
> > work with any other [drawio][] client, but any UI/API is liable to change at
> > any time.

## Installation

```bash
pip install ipydrawio ipydrawio-export
# TBD: conda install -c conda-forge ipydrawio
```

## Features

- `ipydrawio`
  - Edit multi-page [documents][]
    - with nearly the same UI and features as [diagrams.net][drawio]
    - in many file formats
      - Drawio/mxgraph XML, SVG, PNG
      - or Jupyter Notebooks
  - Jupyter [rich display][] output
  - Jupyter [Widgets][]
- `ipydrawio-export`
  - Export print-quality PDF from diagrams
    - > _BEWARE: some **heavy**, maybe fragile dependencies_
    - optionally include editable Drawio XML as a PDF attachment

## Examples

|                                                        Note | Screenshot/Example               |
| ----------------------------------------------------------: | :------------------------------- |
|       Screenshot of drawio "minimal" UI with export options | [![poster-min]][poster-min]      |
|    The beginning of an interactive computational **poster** | [![poster][]][poster]            |
| A mixed computational/creative **roadmap** for this project | [~~Screenshot Needed~~][roadmap] |

## Usage

- Try on [![binder-badge][]][binder]
  - or follow the [Installation instructions](#installation) and **Start
    JupyterLab**
- Import a `drawio` from [diagrams.net](https://diagrams.net) with the _[File
  Manager][]_
  - or create a new
    <img src="./packages/ipydrawio/style/img/drawio.svg" width="24"/> _Diagram_
    from the [Launcher][]
- Use the _[Command Palette][]_ to _Export Diagram_ to various formats
  - > **NOTE**: some of the built-in UI features of drawio don't work properly
    > inside an IFrame in JupyterLab, and are difficult to robustly disable:
    > please see _Diagram_ options available in the _Command Palette_ and
    > various _Main Menu_ menus.

### PDF: Lab and Server extensions

`ipydrawio-export` can generate print-quality PDF. This approach relies on a
headless browser, powered by [@jgraph/draw-image-export2] and ultimately
`puppeteer` which in turn requires `nodejs`.

- **native dependencies** as required to appease `puppeteer`
  - if running in `docker`, this can be a bit trial-and-error
  - for more, see the [binder][apt-txt] and CI.
- `nodejs>10,<14` from `conda` or your system package manager
  - **NOTE**: this relies on being able to install `puppeteer` (and other
    **arbitrary dependencies** with `jlpm` for now **when first used**
    - _we'll figure out a better approach soon enough_
- `pip install ipydrawio-export`

> For example:
>
> ```bash
> conda install -yc conda-forge nodejs=12
> pip install ipydrawio-export
> ```

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
[roadmap]:
  https://github.com/deathbeds/ipydrawio/blob/master/docs/ROADMAP.dio.ipynb
[npm]: https://npmjs.com/package/@deathbeds/ipydrawio
[pypi-badge]: https://img.shields.io/pypi/v/ipydrawio
[pypi]: https://pypi.org/project/ipydrawio/
[npm-badge]: https://img.shields.io/npm/v/@deathbeds/ipydrawio
[cov-badge]:
  https://codecov.io/gh/deathbeds/ipydrawio/branch/master/graph/badge.svg?token=9B74VKHQDK
[cov]: https://codecov.io/gh/deathbeds/ipydrawio
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
  https://nbviewer.jupyter.org/github/deathbeds/ipydrawio/blob/master/docs/ROADMAP.dio.ipynb
[command palette]:
  https://jupyterlab.readthedocs.io/en/stable/user/commands.html?highlight=command%20palette
[launcher]:
  https://jupyterlab.readthedocs.io/en/stable/user/files.html?highlight=Launcher#creating-files-and-activities
[file manager]: https://jupyterlab.readthedocs.io/en/stable/user/files.html
