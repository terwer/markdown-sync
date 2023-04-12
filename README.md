# markdown-sync

convert from vuepress1， siyuan-note docs to vuepress2, hexo

## Install poetry

```bash
pip install poetry==1.2.0
```

## Create new python project

```bash
## https://python-poetry.org/docs/cli/
## poetry new markdown-sync
poetry new markdown-sync --name src
## poetry new --src markdown-sync
```

## Prepare

```bash
## Install pytest
nx add zhi-markdown-sync pytest
nx add zhi-markdown-sync pytest-cov
nx add zhi-markdown-sync pytest-html

## Install pydoc-markdown
nx add zhi-markdown-sync pydoc-markdown

## Install tox
nx add zhi-markdown-sync tox
```

## Install

```bash
poetry install
```

## Add dependency

```bash
poetry add pydoc-markdown
poetry add pytest
poetry add pytest-cov
poetry add pytest-html
poetry add tox
poetry add flake8
```

## Lint

```
flake8
```

## Build

```bash
poetry build -f wheel
```

## Test

```bash
poetry run pytest tests/
```

## Docs

```bash
pydoc-markdown -p zhi_vuepress1_to_vuepress2 --render-toc > docs/source/api.md
```

## Tox

```bash
tox
```