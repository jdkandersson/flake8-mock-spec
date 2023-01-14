"""A linter that checks mocks are constructed with the spec argument."""

from __future__ import annotations

import ast
from typing import Iterator, NamedTuple
from unittest import mock

MOCK_CLASS: str = mock.Mock.__name__
MAGIC_MOCK_CLASS: str = mock.MagicMock.__name__
NON_CALLABLE_MOCK_CLASS: str = mock.NonCallableMock.__name__
ASYNC_MOCK_CLASS: str = mock.AsyncMock.__name__
SPEC_ARGS = frozenset(("spec", "spec_set"))

ERROR_CODE_PREFIX = "TMS"
MORE_INFO_BASE = "more information: https://github.com/jdkandersson/flake8-mock-spec"
MOCK_SPEC_MSG_BASE = (
    f"%s unittest.mock.%s instances should be constructed with the {' or '.join(SPEC_ARGS)} "
    f"argument, {MORE_INFO_BASE}#fix-%s"
)
MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}010"
MOCK_SPEC_MSG = MOCK_SPEC_MSG_BASE % (MOCK_SPEC_CODE, MOCK_CLASS, MOCK_SPEC_CODE.lower())
MAGIC_MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}011"
MAGIC_MOCK_SPEC_MSG = MOCK_SPEC_MSG_BASE % (
    MAGIC_MOCK_SPEC_CODE,
    MAGIC_MOCK_CLASS,
    MAGIC_MOCK_SPEC_CODE.lower(),
)
NON_CALLABLE_MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}012"
NON_CALLABLE_MOCK_SPEC_MSG = MOCK_SPEC_MSG_BASE % (
    NON_CALLABLE_MOCK_SPEC_CODE,
    NON_CALLABLE_MOCK_CLASS,
    NON_CALLABLE_MOCK_SPEC_CODE.lower(),
)
ASYNC_MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}013"
ASYNC_MOCK_SPEC_MSG = MOCK_SPEC_MSG_BASE % (
    ASYNC_MOCK_SPEC_CODE,
    ASYNC_MOCK_CLASS,
    ASYNC_MOCK_SPEC_CODE.lower(),
)
MOCK_MSG_LOOKUP = {
    MOCK_CLASS: MOCK_SPEC_MSG,
    MAGIC_MOCK_CLASS: MAGIC_MOCK_SPEC_MSG,
    NON_CALLABLE_MOCK_CLASS: NON_CALLABLE_MOCK_SPEC_MSG,
    ASYNC_MOCK_CLASS: ASYNC_MOCK_SPEC_MSG,
}

# The attribute actually does exist, mypy reports that it doesn't
PATCH_FUNCTION: str = mock.patch.__name__  # type: ignore
PATCH_ARGS = frozenset(("new", "spec", "spec_set", "autospec", "new_callable"))
PATCH_MSG_BASE = (
    f"%s unittest.mock.%s should be called with any of the {', '.join(PATCH_ARGS)} arguments, "
    f"{MORE_INFO_BASE}#fix-%s"
)
PATCH_CODE = f"{ERROR_CODE_PREFIX}020"
PATCH_MSG = PATCH_MSG_BASE % (PATCH_CODE, PATCH_FUNCTION, PATCH_CODE.lower())
PATCH_OBJECT_CODE = f"{ERROR_CODE_PREFIX}021"
PATCH_OBJECT_FUNCTION = (PATCH_FUNCTION, "object")
PATCH_OBJECT_MSG = PATCH_MSG_BASE % (
    PATCH_OBJECT_CODE,
    ".".join(PATCH_OBJECT_FUNCTION),
    PATCH_OBJECT_CODE.lower(),
)
PATCH_MULTIPLE_FUNCTION = (PATCH_FUNCTION, "multiple")
PATCH_MULTIPLE_CODE = f"{ERROR_CODE_PREFIX}022"
PATCH_MULTIPLE_MSG = PATCH_MSG_BASE % (
    PATCH_MULTIPLE_CODE,
    ".".join(PATCH_MULTIPLE_FUNCTION),
    PATCH_MULTIPLE_CODE.lower(),
)
PATCH_MSG_LOOKUP = {
    PATCH_FUNCTION: PATCH_MSG,
    PATCH_OBJECT_FUNCTION: PATCH_OBJECT_MSG,
    PATCH_MULTIPLE_FUNCTION: PATCH_MULTIPLE_MSG,
}


class Problem(NamedTuple):
    """Represents a problem found in the code.

    Attrs:
        lineno: The line number on which the problem was found.
        col_offset: The column on which the problem was found.
        msg: The message describing the problem.
    """

    lineno: int
    col_offset: int
    msg: str


def _get_fully_qualified_name(node: ast.expr) -> tuple[str, ...]:
    """Retrieve the fully qualified name of a call func node.

    Args:
        node: The node to get the name of.

    Returns:
        Tuple containing all the elements of the fully qualified name of the node.
    """
    if isinstance(node, ast.Name):
        return (node.id,)
    if isinstance(node, ast.Attribute):
        fully_qualified_parent = _get_fully_qualified_name(node.value)
        if fully_qualified_parent:
            return (*fully_qualified_parent, node.attr)
    return ()


class Visitor(ast.NodeVisitor):
    """Visits AST nodes and checks use of mock objects and patch calls.

    Attrs:
        problems: A list of all the problems encountered while visiting the AST nodes.
    """

    problems: list[Problem]

    def __init__(self) -> None:
        """Construct."""
        self.problems = []

    # The function must be called the same as the name of the node
    def visit_Call(self, node: ast.Call) -> None:  # pylint: disable=invalid-name
        """Visit all Call nodes in the AST tree.

        Args:
            node: The Call node being visited.
        """
        # Get the name of the node that has the call
        fully_qualified_name = _get_fully_qualified_name(node=node.func)
        name = fully_qualified_name[-1] if fully_qualified_name else None

        if name in MOCK_MSG_LOOKUP:
            if not any(keyword.arg in SPEC_ARGS for keyword in node.keywords):
                self.problems.append(
                    Problem(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        msg=MOCK_MSG_LOOKUP[name],
                    )
                )

        patch_msg_lookup_key = next(
            (key for key in (name, fully_qualified_name[-2:]) if key in PATCH_MSG_LOOKUP),
            None,
        )
        if patch_msg_lookup_key in PATCH_MSG_LOOKUP:
            if not any(keyword.arg in PATCH_ARGS for keyword in node.keywords):
                self.problems.append(
                    Problem(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        msg=PATCH_MSG_LOOKUP[patch_msg_lookup_key],
                    )
                )

        # Ensure recursion continues
        self.generic_visit(node)


class Plugin:
    """Checks that construction of mocks and calling of patch.

    Attrs:
        name: The name of the plugin.
    """

    # flake8 requires this class to exist
    # pylint: disable=too-few-public-methods

    name = __name__

    def __init__(self, tree: ast.AST) -> None:
        """Initialize the plugin.

        Args:
            tree: The AST syntax tree for the file to be linted.
        """
        self._tree = tree

    def run(self) -> Iterator[tuple[int, int, str, type["Plugin"]]]:
        """Lint a file and yield any issues found.

        Yields:
            A tuple containing the line number, column and error message of the issues found.
        """
        visitor = Visitor()
        visitor.visit(self._tree)
        yield from (
            (problem.lineno, problem.col_offset, problem.msg, type(self))
            for problem in visitor.problems
        )
