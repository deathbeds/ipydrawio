# CONTRIBUTING

## Help Wanted

- tackling [roadmap](./docs/ROADMAP.dio.ipynb) issues
- improving testing
- improving (self-hosted) documentation
- improving the binder demo
- improving [continuous integration](./github/workflows/ci.yml) and
  [developer experience](./dodo.py)

## Prerequisites

- `jupyterlab >=3,<4`
- `nodejs >=12`
- `doit >=0.32`

### Recommended: conda

- Get [Miniforge/Mambaforge](https://github.com/conda-forge/miniforge/releases)

```bash
mamba env update --file .github/environment.yml
source activate ipydrawio
```

> or use the demo environment in `.binder`

## Get to a working Lab

```bash
doit
```

## Prepare a Release

```bash
doit dist
```

## Do everything

```bash
doit all
```

## Updating drawio

- update the `version` in `packages/ipydrawio-webpack/package.json`
- update dependencies in other `package.json`

```bash
pushd packages/ipydrawio-webpack/drawio
git fetch
git checkout v<the new version>
popd
doit dist
```

- validate everything looks good!

## Releasing

- [ ] start a release issue with a checklist (maybe like this one)
- [ ] ensure the versions have been bumped (check with `doit test:integrity`)
- [ ] validate on binder
- [ ] wait for a successful build of `master`
- [ ] download the `dist` archive and unpack somewhere (maybe a fresh `dist`)
- [ ] actually upload
  ```bash
  export VERSION=<the next version>
  cd dist
  twine upload ipydrawio*
  npm login
  npm publish deathbeds-ipydrawio-$VERSION.tgz
  npm publish deathbeds-ipydrawio-notebook-$VERSION.tgz
  npm publish deathbeds-ipydrawio-pdf-$VERSION.tgz
  npm publish deathbeds-ipydrawio-webpack-$VERSION.tgz
  npm logout
  ```
- [ ] handle `conda-forge` feedstock tasks
