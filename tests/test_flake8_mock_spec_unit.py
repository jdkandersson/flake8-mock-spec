"""Unit tests for plugin."""

from __future__ import annotations

import ast

import pytest

from flake8_mock_spec import MAGIC_MOCK_SPEC_MSG, MOCK_SPEC_MSG, Plugin


def _result(code: str) -> tuple[str, ...]:
    """Generate linting results.

    Args:
        code: The code to check.

    Returns:
        The linting result.
    """
    tree = ast.parse(code)
    plugin = Plugin(tree)
    return tuple(f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run())


@pytest.mark.parametrize(
    "code, expected_result",
    [
        pytest.param("", (), id="trivial"),
        pytest.param(
            """
Mock()
""",
            (f"2:0 {MOCK_SPEC_MSG}",),
            id="module Mock no spec",
        ),
        pytest.param(
            """
MagicMock()
""",
            (f"2:0 {MAGIC_MOCK_SPEC_MSG}",),
            id="module MagicMock no spec",
        ),
        pytest.param(
            """
NonCallableMock()
""",
            (f"2:0 {MAGIC_MOCK_SPEC_MSG}",),
            id="module NonCallableMock no spec",
        ),
        pytest.param(
            """
AsyncMock()
""",
            (f"2:0 {MAGIC_MOCK_SPEC_MSG}",),
            id="module AsyncMock no spec",
        ),
        pytest.param(
            """
mock.Mock()
""",
            (f"2:0 {MOCK_SPEC_MSG}",),
            id="module mock.Mock no spec",
        ),
        pytest.param(
            """
unittest.mock.Mock()
""",
            (f"2:0 {MOCK_SPEC_MSG}",),
            id="module unittest.mock.Mock no spec",
        ),
        pytest.param(
            """
def test_():
    Mock()
""",
            (f"3:4 {MOCK_SPEC_MSG}",),
            id="function Mock no spec",
        ),
        pytest.param(
            """
def test_():
    def test_inner():
        Mock()
""",
            (f"4:8 {MOCK_SPEC_MSG}",),
            id="nested function Mock no spec",
        ),
        pytest.param(
            """
class Test:
    Mock()
""",
            (f"3:4 {MOCK_SPEC_MSG}",),
            id="class Mock no spec",
        ),
        pytest.param(
            """
class Test:
    class TestInner:
        Mock()
""",
            (f"4:8 {MOCK_SPEC_MSG}",),
            id="nested class Mock no spec",
        ),
        pytest.param(
            """
class Test:
    def test_():
        Mock()
""",
            (f"4:8 {MOCK_SPEC_MSG}",),
            id="class method Mock no spec",
        ),
        pytest.param(
            """
Mock(spec=1)
""",
            (),
            id="module Mock spec",
        ),
        pytest.param(
            """
Mock(spec_set=1)
""",
            (),
            id="module Mock spec_set",
        ),
        pytest.param(
            """
MagicMock(spec=1)
""",
            (),
            id="module MagicMock spec",
        ),
        pytest.param(
            """
MagicMock(spec_set=1)
""",
            (),
            id="module MagicMock spec_set",
        ),
        pytest.param(
            """
NonCallableMock(spec=1)
""",
            (),
            id="module NonCallableMock spec",
        ),
        pytest.param(
            """
NonCallableMock(spec_set=1)
""",
            (),
            id="module NonCallableMock spec_set",
        ),
        pytest.param(
            """
AsyncMock(spec=1)
""",
            (),
            id="module AsyncMock spec",
        ),
        pytest.param(
            """
AsyncMock(spec_set=1)
""",
            (),
            id="module AsyncMock spec_set",
        ),
        pytest.param(
            """
Other()
""",
            (),
            id="call not mock",
        ),
        pytest.param(
            """
module.Other()
""",
            (),
            id="nested call not mock",
        ),
    ],
)
def test_plugin(code: str, expected_result: tuple[str, ...]):
    """
    given: code
    when: linting is run on the code
    then: the expected result is returned
    """
    assert _result(code) == expected_result
