# Contributing to AGIP Reference

## Development setup

```bash
python -m pip install -e ".[dev]"
make check
```

## Workflow

1. Create a focused feature branch from `main`.
2. Keep changes small and covered by tests.
3. Run `make check` before opening a pull request.
4. Explain the goal, risks, and verification steps in the pull request.

## Quality gates

All changes must pass Ruff, MyPy, and Pytest. Public APIs require documentation and tests.
