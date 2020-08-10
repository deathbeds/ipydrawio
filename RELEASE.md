# Releasing

```bash
git clean -dxf
jlpm cache clean
conda clean -yaf
doit all
# nothing but submodule cruft
python -m scripts.tag
python -m scripts.upload
FOR_REAL=1 python -m scripts.tag
FOR_REAL=1 python -m scripts.upload
```
