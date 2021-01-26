# jupyter-drawio-export

> PDF export of [drawio](https://www.diagrams.net) diagrams for Jupyter.

See the [project repo](https://github.com/deathbeds/ipydrawio) for more
information.

## Server Extension

`jupyter-drawio-export` runs as a [server extension][serverext]. When installed,
it _should_ be automatically configured. If problems arise, it can be manually
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
pip install jupyter-drawio-export
jupyter drawio-export some_file.dio
```

If needed, the `nodejs` application will be installed into the Jupyter data
path.

```bash
jupyter config --paths  # it uses the one in the environment
```

> In the future, it's hoped this can be packaged more conveniently.

### Provisioning

To ensure the `nodejs` application is installed _without_ exporting a PDF (e.g
when building a docker container).

```bash
jupyter drawio-config provision
```

## Open Source

This work is licensed under the [Apache 2.0](./LICENSE.txt).

The vendored code from
[@jgraph/draw-image-export2](https://github.com/jgraph/draw-image-export2) is
also licensed under the [Apache-2.0](./vendor/draw-image-export2/LICENSE)
License.

[serverext]:
  https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html
