# Repository Guidelines

## Scope and layout

This repository contains independent weekly Python exercises under `viikko1/`
through `viikko4/`; each exercise with a `pyproject.toml` has its own `uv`
environment and lockfile. Run commands from the directory of the exercise
being changed, not from the repository root. The current `viikko4/tdd-ostoskori`
exercise is a small test-driven shopping-cart implementation.

## Build, test, and lint

The `viikko4/tdd-ostoskori` project requires Python 3.14+ and declares pytest
as its development dependency. From that directory:

```bash
uv sync
uv run pytest
```

Run the cart test module or an individual test with:

```bash
uv run pytest src/tests/ostoskori_test.py
uv run pytest src/tests/ostoskori_test.py::TestOstoskori::test_ostoskorin_hinta_ja_tavaroiden_maara_alussa
```

There is no configured build or lint command. Other weekly exercises follow
the same per-directory pattern; check their local `pyproject.toml` before
choosing a test runner or entry point.

## Architecture

The cart exercise keeps the domain model split into small classes:

- `src/tuote.py` defines `Tuote`, the named product and its unit price.
- `src/ostos.py` defines `Ostos`, which wraps one product and tracks its
  quantity; quantity changes are clamped at zero and the line total is
  calculated from the product price.
- `src/ostoskori.py` is the aggregate under development. `Ostoskori` owns the
  cart-level operations (adding/removing products, clearing, counting items,
  calculating the total, and exposing purchases).
- `src/tests/ostoskori_test.py` is the pytest/unittest-style test entry point
  for the cart behavior. Imports expect the `src` directory to be on pytest's
  import path.

Keep product-level behavior in `Tuote`/`Ostos` and cart aggregation in
`Ostoskori`; do not duplicate quantity or price calculations in tests or
callers.

## Conventions

- Use `uv run` for project commands so the selected exercise's locked
  dependencies and Python version are used.
- Preserve the existing Finnish domain names and public method names unless a
  coordinated test/API change requires otherwise.
- Tests use `unittest.TestCase` assertions even though they are run by pytest;
  follow that style in the existing cart test module.
- Keep generated files (`__pycache__`, `.pytest_cache`, coverage output, and
  virtual environments) out of changes; the exercise-local `.gitignore`
  already lists them.
