# CONTRIBUTING

## Help Wanted

- tackling [roadmap](./docs/ROADMAP.ipynb) issues
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
- [ ] create a new release through the GitHub UI
  - [ ] paste in the relevant CHANGELOG entries
  - [ ] upload the artifacts
- [ ] actually upload to npm.com, pypi.org
  ```bash
  cd dist
  twine upload ipydrawio*
  npm login
  npm publish deathbeds-ipydrawio-$VERSION.tgz
  npm publish deathbeds-ipydrawio-notebook-$VERSION.tgz
  npm publish deathbeds-ipydrawio-pdf-$VERSION.tgz
  npm publish deathbeds-ipydrawio-webpack-$OTHER_VERSION.tgz
  npm logout
  ```
- [ ] postmortem
  - [ ] handle `conda-forge` feedstock tasks
  - [ ] validate on binder via simplest-possible gists
  - [ ] bump to next development version

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
