# `ipydrawio` labextensions

`ipydrawio` ships, and enables by default, several JupyterLab 3 _federated extensions_.
At some point in the future, these might become smaller packages, and are independently
reusable by other _federated modules_.

- `@deathbeds/ipydrawio-webpack`
    - a mostly-automated re-packaging (and light patching) of the official [drawio]
      repo
- `@deathbeds/ipydrawio`
    - the core renderer library
- `@deathbeds/ipydrawio-widget`
    - the Jupyter Widgets
- `@deathbeds/ipydrawio-notebook`
    - the custom `ipynb` format
- `@deathbeds/ipydrawio-pdf`
    - a **work-in-progress** attempt to provide an easy-to-install PDF toolchain
      for drawio (and more?)

[drawio]: https://github.com/jgraph/drawio
