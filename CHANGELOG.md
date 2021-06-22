# CHANGELOG

## Unreleased

### ipydrawio 1.1.1

- adds `jupyter ipydrawio clean` for removing `host`, `agent`, `modified`
  attributes and pretty printing, restoring `lxml` as a dependency [#44]

#### @deathbeds/ipydrawio 1.1.1

- revert default theme from `sketch` back to `min` [#41]

#### @deathbeds/ipydrawio-notebook 1.1.1

#### @deathbeds/ipydrawio-webpack 14.8.000

- upgrade to drawio v14.8.0 for layer enhancements and various bugfixes [#51]

#### @deathbeds/ipydrawio-jupyter-templates 1.1.1

- adds some (unofficial) Jupyter-branded templates [#44]

### ipydrawio-export 1.1.1

- upgrades `draw-image-export` for `xmldom` version and bugfixes [#44]

#### @deathbeds/ipydrawio-pdf 1.1.1

[#41]: https://github.com/deathbeds/ipydrawio/issues/41
[#44]: https://github.com/deathbeds/ipydrawio/issues/44

---

## Releases

### ipydrawio 1.1.0

- new documentation site at https://ipydrawio.rtfd.io [#40]
- no longer depends on `lxml`, future XML-based features will hopefully support
  the standard library `xml` module [#40]

#### @deathbeds/ipydrawio 1.1.0

- the `sketch` theme is now available as the `ui` [#40]
- the _Custom Diagram..._ Launcher card offers all the themes, templates, and
  editable formats [#40]
  - templates can be added by extensions [#41]
- additional configuration defaults added to `urlParams` [#40]
- the <kbd>Esc</kbd> button now shifts focus back to the main application
  allowing for use of more keyboard shortcuts. [#40]
  - the previous inescapable behavior can be restored in _Adanced Settings_ by
    setting `"disableEscapeFocus": true`

#### @deathbeds/ipydrawio-notebook 1.1.0

#### @deathbeds/ipydrawio-webpack 14.7.100

- drawio 14.7.1 [#41]

### ipydrawio-export 1.1.0

- depends on `lxml` [#40]

#### @deathbeds/ipydrawio-pdf 1.1.0

[#40]: https://github.com/deathbeds/ipydrawio/pull/40
[#41]: https://github.com/deathbeds/ipydrawio/pull/41

---

### ipydrawio 1.0.1

- [#32] on-disk file paths are shorter to avoid Windows issues
- [#31] `install.json` is properly placed

#### @deathbeds/ipydrawio 1.0.1

#### @deathbeds/ipydrawio-notebook 1.0.1

#### @deathbeds/ipydrawio-webpack 14.5.901

- [#32] drawio assets are copied into a shorter path
- changing version scheme to allow for patch releases.
  - going forward, the upstream patch release will be multiplied by 100

### ipydrawio-export 1.0.1

- [#32] on-disk file paths are shorter to avoid Windows issues
- [#31] `install.json` is properly placed

#### @deathbeds/ipydrawio-pdf 1.0.1

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

#### @deathbeds/ipydrawio 1.0.0

- [#22] adds more _Main Menu_ options and _Command Palette_ Commands
- [#22] new file names created by _Export Diagram as..._ commands use
  best-effort, two-digit numbers (if needed) incrementer instead of timestamp
- [#20] add `allow-downloads` sandbox exception for the drawio `iframe`,
  enabling some more built-in features

#### @deathbeds/ipydrawio-notebook 1.0.0

- [#21] fixes overload of default _Notebook_ activity for _Edit with_ for
  `.ipynb` files

#### @deathbeds/ipydrawio-webpack 14.5.9

### ipydrawio-export 1.0.0

- [#22] correctly handle finding/resolving `node.*` on windows
- [#22] upgrade to newer `puppeteer`-based `draw-image-export`

#### @deathbeds/ipydrawio-pdf 1.0.0

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

#### @deathbeds/ipydrawio 1.0.0-alpha0

#### @deathbeds/ipydrawio-notebook 1.0.0-alpha0

#### @deathbeds/ipydrawio-webpack 14.2.6-alpha0

### ipydrawio-export 1.0.0a0

#### @deathbeds/ipydrawio-pdf 1.0.0-alpha0

---

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
