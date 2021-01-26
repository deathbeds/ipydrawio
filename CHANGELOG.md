# CHANGELOG

## Unreleased

### ipydrawio 1.0.0-alpha0

- ipywidgets support
- Supports JupyterLab 3
- `pip` primary distribution
- Contains all previous packages
  - PDF export is tenuous, due to `nodejs` dependencies, and may be temporarily
    unavailable
- A future release may unpack various dependencies into sub-packages

---

### jupyter-drawio-export 0.8.0-alpha2

### @deathbeds/jupyterlab-drawio 0.8.0-alpha2

### @deathbeds/jupyterlab-drawio-notebook 0.8.0-alpha2

### @deathbeds/jupyterlab-drawio-shapes-jupyterlab 0.8.0-alpha2

### @deathbeds/jupyterlab-drawio-pdf 0.8.0-alpha2

### @deathbeds/jupyterlab-drawio-webpack 13.6.10-alpha2

- Drawio v13.6.10

---

## Released 2020-08-16

- basic functionality now tested with robotframework in Firefox on
  - Linux, Ubunut, MacOs
  - Python 3.6 and 3.8

### jupyter-drawio-export 0.8.0-alpha1

- adds statusbar item for PDF export server
- adds status and provision endpoints
- adds export CLI
- requires `lxml`, `pillow`, `pypdf2` and `requests_cache`
  - and, of course, `nodejs`
- CLI functionality tested with pytest

### @deathbeds/jupyterlab-drawio-pdf 0.8.0-alpha1

- removes non-functioning editable PDF for now

### @deathbeds/jupyterlab-drawio-notebook 0.8.0-alpha1

### @deathbeds/jupyterlab-drawio 0.8.0-alpha1

### @deathbeds/jupyterlab-drawio-webpack 13.6.2-alpha1

- Drawio v13.6.2

---

## Released 2020-08-09

### jupyter-drawio-export 0.8.0-alpha0

- wraps/vendors `drawio-image-export2`
- optionally supports
  - PDF caching with `requests_cache`
  - XML embedding with `PyPDF2`

### @deathbeds/jupyterlab-drawio-pdf 0.8.0-alpha0

- depends on `@deathbeds/jupyterlab-drawio`

### @deathbeds/jupyterlab-drawio-notebook 0.8.0-alpha0

- depends on `@deathbeds/jupyterlab-drawio`

### @deathbeds/jupyterlab-drawio 0.8.0-alpha0

- depends on `@deathbeds/jupyterlab-drawio-webpack`

### @deathbeds/jupyterlab-drawio-webpack 13.6.1-alpha0

- Drawio v13.6.1
