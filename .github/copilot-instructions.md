# Project Guidelines

## Scope

The main active application is `viikko3/login`, a small Flask login and
registration service. Run the commands below from that directory.

## Build and Test

This is a `uv` project. Run project commands with `uv run ...` from
`viikko3/login`. There is no separate build or lint command configured.

Start the application before running browser tests:

```bash
cd viikko3/login
uv run python src/index.py
```

The Flask application listens on port `5001` at
`http://localhost:5001`. Keep the application running in a separate terminal
for the duration of the Robot Framework tests.

Run all Robot Framework acceptance tests while the application is running:

```bash
cd viikko3/login
uv run robot src/tests
```

Run one suite:

```bash
uv run robot src/tests/login.robot
```

Run one test case:

```bash
uv run robot --test "Login With Nonexistent Username" src/tests/login.robot
```

The tests use Robot Framework Browser with Chromium and expect the application
on `http://localhost:5001`. `AppLibrary.py` resets the in-memory user store
through `/tests/reset` and creates test users through the registration endpoint.

## Architecture

- `src/index.py` is the development entry point and starts the Flask app on
  port 5001.
- `src/app.py` defines the HTTP routes, renders Jinja templates, and translates
  service exceptions into flashed messages followed by redirects.
- `src/services/user_service.py` contains both username/password authentication
  checks (`check_credentials`) and registration validation (`validate`),
  including username and password length checks and password confirmation.
  Keep these business rules here rather than in route handlers.
- `src/repositories/user_repository.py` is the in-memory persistence layer;
  `user_repository` is a module-level singleton used by the service and test
  reset endpoint.
- `src/entities/user.py` contains the user entity.
- `src/templates/` contains the page layout and the home, login, registration,
  welcome, and main-page views.
- `src/tests/*.robot` are browser-level acceptance tests. Shared Browser
  variables and keywords belong in `src/tests/resource.robot`; suite-specific
  setup and keywords stay with their suite.

## Conventions

- Run commands from `viikko3/login` using `uv run`; this supplies the project
  environment and dependencies.
- Successful login redirects to `/ohtu`; successful registration redirects to
  `/welcome`. Failed operations flash the exception message and redirect back
  to the corresponding form.
- Registration validation currently requires a username of at least 3
  characters, a password of at least 4 characters, and matching password
  confirmation. Duplicate usernames are rejected by the repository.
- Tests reset application state before each test. Do not rely on test execution
  order or users created by another test.
- Robot selectors rely on the existing element ids (`username`, `password`,
  and `password_confirmation`) and visible button/link text. Preserve these
  when changing templates unless the tests are updated deliberately.
- The test-only reset endpoint is intentionally used by acceptance-test setup;
  keep it available when changing test infrastructure.
