"""A linter that checks mocks are constructed with the spec argument."""

from __future__ import annotations

import ast
from typing import Iterator, NamedTuple

MOCK_CLASS = "Mock"
MAGIC_MOCK_CLASS = "MagicMock"
ALL_MOCK_CLASSES = {MOCK_CLASS, MAGIC_MOCK_CLASS}
SPEC_ARGS = {"spec", "spec_set"}

ERROR_CODE_PREFIX = "TMS"
MORE_INFO_BASE = "more information: https://github.com/jdkandersson/flake8-mock-spec"
MOCK_SPEC_MSG_BASE = (
    f"%s unittest.mock.%s instances should be constructed with the {' or '.join(SPEC_ARGS)} "
    f"argument, {MORE_INFO_BASE}#fix-%s"
)
MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}001"
MOCK_SPEC_MSG = MOCK_SPEC_MSG_BASE % (MOCK_SPEC_CODE, MOCK_CLASS, MOCK_SPEC_CODE.lower())
MAGIC_MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}002"
MAGIC_MOCK_SPEC_MSG = MOCK_SPEC_MSG_BASE % (
    MAGIC_MOCK_SPEC_CODE,
    MAGIC_MOCK_CLASS,
    MAGIC_MOCK_SPEC_CODE.lower(),
)


class Problem(NamedTuple):
    """Represents a problem within the code.

    Attrs:
        lineno: The line number the problem occurred on
        col_offset: The column the problem occurred on
        msg: The message explaining the problem
    """

    lineno: int
    col_offset: int
    msg: str


class Visitor(ast.NodeVisitor):
    """Visits AST nodes and check docstrings of test functions.

    Attrs:
        problems: All the problems that were encountered.
    """

    problems: list[Problem]

    def __init__(self) -> None:
        """Construct."""
        self.problems = []

    # The function must be called the same as the name of the node
    def visit_Call(self, node: ast.Call) -> None:  # pylint: disable=invalid-name
        """Visit all Call nodes.

        Args:
            node: The Call node.
        """
        # Get the name of the node that has the call
        name: str | None = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr

        if name is not None and name in ALL_MOCK_CLASSES:
            if not any(keyword.arg in {"spec", "spec_set"} for keyword in node.keywords):
                self.problems.append(
                    Problem(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        msg=MOCK_SPEC_MSG if name == MOCK_CLASS else MAGIC_MOCK_SPEC_MSG,
                    )
                )

        # Ensure recursion continues
        self.generic_visit(node)


class Plugin:
    """Checks test docstrings for the arrange/act/assert structure.

    Attrs:
        name: The name of the plugin.
    """

    name = __name__

    def __init__(self, tree: ast.AST) -> None:
        """Construct.

        Args:
            tree: The AST syntax tree for a file.
        """
        self._tree = tree

    def run(self) -> Iterator[tuple[int, int, str, type["Plugin"]]]:
        """Lint a file.

        Yields:
            All the issues that were found.
        """
        visitor = Visitor()
        visitor.visit(self._tree)
        yield from (
            (problem.lineno, problem.col_offset, problem.msg, type(self))
            for problem in visitor.problems
        )
