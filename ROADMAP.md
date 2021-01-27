# ROADMAP

- [ ] support mimerenderer
- [ ] rework distribution for JupyterLab 3
- [ ] support (ipy)widgets
- [ ] rebrand as `ipydrawio`
- [ ] pypi release
- [ ] conda-forge release
- [ ] docs on `gh-pages`

## Jupyter Widget

### MVP

```py
import ipywidgets as W, traitlets as T

class Drawio(W.Box):
    value = T.Unicode().tag(sync=True)
    scroll_x = T.Float().tag(sync=True)
    scroll_y = T.Float().tag(sync=True)
    zoom = T.Float().tag(sync=True)
    selected = W.trait_types.TraitTuple(T.Unicode()).tag(sync=True)
```
