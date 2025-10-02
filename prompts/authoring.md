# Test Authoring Rules (Playwright + pytest, Python)

## Fixtures & State
- UI tests use fixtures: `page`, `base_url`.
- To reset state: call `reset_cart(page.request)` at the start of each UI test.

## Selectors (stability first)
- Prefer `page.get_by_test_id("<id>")` if the app provides test IDs.
- Otherwise, use `page.get_by_role("<role>", name="...")` with accessible names.
- `get_by_text("...")` is acceptable if role/name aren’t available.
- Avoid nth-child, XPath, or brittle CSS.

## Structure
- Place pure UI tests in `tests/ui/`.
- Place cross-layer (API→DB→UI) tests in `tests/e2e/`.
- Filenames: `test_<slug>.py`.
- Docstring should include the requirement or intent.

## Assertions & Helpers
- Use `expect_*` assertions, no sleeps/timeouts.
- Extract repeated steps into `utils/ui_helpers.py` and import them.
- Keep tests idempotent (start fresh, don’t depend on others).
