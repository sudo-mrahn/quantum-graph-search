# Development

The supported local workflow uses the project-local `.venv` managed by the
repository `Makefile`.

## Bootstrap

```bash
make bootstrap
```

This creates `.venv`, upgrades `pip`, installs the package in editable mode
with test dependencies, and installs `flake8` so local linting matches CI.

On Debian/Ubuntu, if `.venv` creation fails because `ensurepip` is missing,
install the matching `python3-venv` package for your interpreter and rerun
`make bootstrap`. The target also falls back to `python3 -m virtualenv` when
that tool is already installed.

## Validation

```bash
make test
make lint
```

These commands run against `.venv/bin/python`, so activating the virtual
environment is optional.
