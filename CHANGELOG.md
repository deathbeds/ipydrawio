# CHANGELOG

## Unreleased

### ipydrawio 1.0.2

### ipydrawio-export 1.0.2

### @deathbeds/ipydrawio 1.0.2

### @deathbeds/ipydrawio-notebook 1.0.2

### @deathbeds/ipydrawio-pdf 1.0.2

### @deathbeds/ipydrawio-webpack 14.6.1000

- drawio 14.6.10

---

### ipydrawio 1.0.1

- [#32] on-disk file paths are shorter to avoid Windows issues
- [#31] `install.json` is properly placed

### ipydrawio-export 1.0.1

- [#32] on-disk file paths are shorter to avoid Windows issues
- [#31] `install.json` is properly placed

### @deathbeds/ipydrawio 1.0.1

### @deathbeds/ipydrawio-notebook 1.0.1

### @deathbeds/ipydrawio-pdf 1.0.1

### @deathbeds/ipydrawio-webpack 14.5.901

- [#32] drawio assets are copied into a shorter path
- changing version scheme to allow for patch releases.
  - going forward, the upstream patch release will be multiplied by 100

[#31]: https://github.com/deathbeds/ipydrawio/issues/31
[#32]: https://github.com/deathbeds/ipydrawio/issues/32

---

### ipydrawio 1.0.0

- ipywidgets support
- Supports JupyterLab 3
- `pip` primary distribution
- Contains all previous packages
  - PDF export is tenuous, due to `nodejs` dependencies, and may be temporarily
    unavailable
- A future release may unpack various dependencies into sub-packages

### ipydrawio-export 1.0.0

- [#22] correctly handle finding/resolving `node.*` on windows
- [#22] upgrade to newer `puppeteer`-based `draw-image-export`

### @deathbeds/ipydrawio 1.0.0

- [#22] adds more _Main Menu_ options and _Command Palette_ Commands
- [#22] new file names created by _Export Diagram as..._ commands use
  best-effort, two-digit numbers (if needed) incrementer instead of timestamp
- [#20] add `allow-downloads` sandbox exception for the drawio `iframe`,
  enabling some more built-in features

### @deathbeds/ipydrawio-notebook 1.0.0

- [#21] fixes overload of default _Notebook_ activity for _Edit with_ for
  `.ipynb` files

### @deathbeds/ipydrawio-pdf 1.0.0

### @deathbeds/ipydrawio-webpack 14.5.9

- [#22] improved PDF export

[#20]: https://github.com/deathbeds/ipydrawio/issues/20
[#21]: https://github.com/deathbeds/ipydrawio/issues/21
[#22]: https://github.com/deathbeds/ipydrawio/pull/22

---

### ipydrawio 1.0.0a0

- ipywidgets support
- Supports JupyterLab 3
- `pip` primary distribution
- Contains all previous packages
  - PDF export is tenuous, due to `nodejs` dependencies, and may be temporarily
    unavailable
- A future release may unpack various dependencies into sub-packages

### ipydrawio-export 1.0.0a0

### @deathbeds/ipydrawio 1.0.0-alpha0

### @deathbeds/ipydrawio-notebook 1.0.0-alpha0

### @deathbeds/ipydrawio-pdf 1.0.0-alpha0

### @deathbeds/ipydrawio-webpack 14.2.6-alpha0

## Historic Releases

For pre-releases of the previously-named package, see the [old CHANGELOG][]

[old changelog]:
  https://github.com/deathbeds/ipydrawio/tree/3a577ac/CHANGELOG.md

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
