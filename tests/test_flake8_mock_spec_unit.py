"""Unit tests for plugin."""

from __future__ import annotations

import ast
from unittest import mock

import pytest

from flake8_mock_spec import MAGIC_MOCK_SPEC_MSG, MOCK_CLASSES, MOCK_SPEC_MSG, Plugin, PATCH_MSG


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
def test_plugin_mock(code: str, expected_result: tuple[str, ...]):
    """
    given: code
    when: linting is run on the code
    then: the expected result is returned
    """
    assert _result(code) == expected_result


@pytest.mark.parametrize(
    "code, expected_result",
    [
        pytest.param(
            """
@patch()
def function_1():
    pass
""",
            (f"2:1 {PATCH_MSG}",),
            id="decorator no arg",
        ),
        pytest.param(
            """
@mock.patch()
def function_1():
    pass
""",
            (f"2:1 {PATCH_MSG}",),
            id="module decorator no arg",
        ),
        pytest.param(
            """
@unittest.mock.patch()
def function_1():
    pass
""",
            (f"2:1 {PATCH_MSG}",),
            id="nested module decorator no arg",
        ),
        pytest.param(
            """
class Class1:
    @patch()
    def function_1(self):
        pass
""",
            (f"3:5 {PATCH_MSG}",),
            id="method decorator no arg",
        ),
        pytest.param(
            """
@patch(other=1)
def function_1():
    pass
""",
            (f"2:1 {PATCH_MSG}",),
            id="decorator single arg not expected",
        ),
        pytest.param(
            """
@patch(other=1, another=2)
def function_1():
    pass
""",
            (f"2:1 {PATCH_MSG}",),
            id="decorator multiple arg not expected",
        ),
        pytest.param(
            """
with patch():
    pass
""",
            (f"2:5 {PATCH_MSG}",),
            id="context manager no arg",
        ),
        pytest.param(
            """
patcher = patch()
""",
            (f"2:10 {PATCH_MSG}",),
            id="assignment no arg",
        ),
        pytest.param(
            """
@patch(new=1)
def function_1():
    pass
""",
            (),
            id="decorator new arg",
        ),
        pytest.param(
            """
@mock.patch(new=1)
def function_1():
    pass
""",
            (),
            id="module decorator new arg",
        ),
        pytest.param(
            """
@unittest.mock.patch(new=1)
def function_1():
    pass
""",
            (),
            id="nested module decorator new arg",
        ),
        pytest.param(
            """
@patch(spec=1)
def function_1():
    pass
""",
            (),
            id="decorator spec arg",
        ),
        pytest.param(
            """
@patch(spec_set=1)
def function_1():
    pass
""",
            (),
            id="decorator spec_set arg",
        ),
        pytest.param(
            """
@patch(autospec=1)
def function_1():
    pass
""",
            (),
            id="decorator autospec arg",
        ),
        pytest.param(
            """
@patch(new_callable=1)
def function_1():
    pass
""",
            (),
            id="decorator new_callable arg",
        ),
        pytest.param(
            """
@patch(new=1, other=2)
def function_1():
    pass
""",
            (),
            id="decorator multiple args first expected",
        ),
        pytest.param(
            """
@patch(other=1, spec=2)
def function_1():
    pass
""",
            (),
            id="decorator multiple args second expected",
        ),
        pytest.param(
            """
@patch(new=1, spec=2)
def function_1():
    pass
""",
            (),
            id="decorator multiple args all expected",
        ),
        pytest.param(
            """
class Class1:
    @patch(new=1)
    def function_1(self):
        pass
""",
            (),
            id="method decorator new arg",
        ),
        pytest.param(
            """
with patch(new=1):
    pass
""",
            (),
            id="context manager new arg",
        ),
        pytest.param(
            """
patcher = patch(new=1)
""",
            (),
            id="assignment manager new arg",
        ),
    ],
)
def test_plugin_patch(code: str, expected_result: tuple[str, ...]):
    """
    given: code
    when: linting is run on the code
    then: the expected result is returned
    """
    assert _result(code) == expected_result


@pytest.mark.parametrize(
    "class_", [pytest.param(class_, id=f"{class_} class") for class_ in MOCK_CLASSES]
)
def test_mock_classes_exist(class_: str):
    """
    given: mock class
    when: the existence of the class on unittest.mock is checked
    then: the class exists in mock and can be instantiated
    """
    assert hasattr(mock, class_)
    getattr(mock, class_)()
