# CONTRIBUTING

## Help Wanted

- tackling [roadmap](./docs/ROADMAP.dio.ipynb) issues
- improving testing
- improving (self-hosted) documentation
- improving the binder demo
- improving [continuous integration](./github/workflows/ci.yml) and [developer experience](./dodo.py)

## Prerequisites

- `jupyterlab >=2.2,<3`
- `nodejs >=12`
- `doit =0.32`

### Recommended: conda

- Get [Miniconda3](https://repo.anaconda.com/miniconda/)

```bash
conda env update --file environment.yml
source activate jupyterlab-drawio
```

## Get to a working Lab

```bash
doit
```

## Prepare a Release

```bash
doit all
```
