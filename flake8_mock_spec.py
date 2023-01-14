"""A linter that checks mocks are constructed with the spec argument."""

from __future__ import annotations

import ast
from typing import Iterator, NamedTuple

ERROR_CODE_PREFIX = "TMS"
MORE_INFO_BASE = "more information: https://github.com/jdkandersson/flake8-mock-spec"
MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}001"
MOCK_SPEC_MSG = (
    f"{MOCK_SPEC_CODE} unittest.mock.Mock instances should be constructed with the spec or "
    f"spec_set argument, {MORE_INFO_BASE}#fix-{MOCK_SPEC_CODE.lower()}"
)
MAGIC_MOCK_SPEC_CODE = f"{ERROR_CODE_PREFIX}002"
MAGIC_MOCK_SPEC_MSG = (
    f"{MAGIC_MOCK_SPEC_CODE} unittest.mock.MagicMock instances should be constructed with the spec "
    f"argument, {MORE_INFO_BASE}#fix-{MAGIC_MOCK_SPEC_CODE.lower()}"
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
