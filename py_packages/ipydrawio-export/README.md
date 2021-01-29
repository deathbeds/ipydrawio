# ipydrawio-export

> PDF export of [drawio](https://www.diagrams.net) diagrams for Jupyter.

See the [project repo](https://github.com/deathbeds/ipydrawio) for more
information.

## Installation

```bash
pip install ipydrawio-export
```

## Server Extension

`ipydrawio-export` runs as a [server extension][serverext]. When installed, it
_should_ be automatically configured. If problems arise, it can be manually
_enabled_:

```bash
jupyter serverextension list   # If you don't see it here...
jupyter serverextension enable --sys-prefix --py ipydrawio_export  # run this...
jupyter serverextension list   # ... then check it again
```

## Command-Line Usage

### Exporting PDF

PDF can also be generated from the command line:

```bash
pip install ipydrawio-export
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

## Open Source

This work is licensed under the [Apache-2.0] License.

The vendored code from [@jgraph/draw-image-export2][] is also licensed under the
[Apache-2.0][draw2-license] License.

[@jgraph/draw-image-export2]: https://github.com/jgraph/draw-image-export2
[apache-2.0]:
  https://github.com/deathbeds/ipydrawio/blob/master/py_packages/ipydrawio-export/LICENSE.txt
[draw2-license]:
  https://github.com/jgraph/draw-image-export2/blob/master/LICENSE
[serverext]:
  https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html
