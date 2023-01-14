"""Integration tests for plugin."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from flake8_mock_spec import (
    ASYNC_MOCK_SPEC_CODE,
    MAGIC_MOCK_SPEC_CODE,
    MOCK_SPEC_CODE,
    MOCK_SPEC_MSG,
    NON_CALLABLE_MOCK_SPEC_CODE,
    PATCH_CODE,
    PATCH_OBJECT_CODE,
    PATCH_MULTIPLE_CODE,
)


def test_help():
    """
    given: linter
    when: the flake8 help message is generated
    then: plugin is registered with flake8
    """
    with subprocess.Popen(
        f"{sys.executable} -m flake8 --help",
        stdout=subprocess.PIPE,
        shell=True,
    ) as proc:
        stdout = proc.communicate()[0].decode(encoding="utf-8")

        assert "flake8-mock-spec" in stdout


def create_code_file(code: str, base_path: Path) -> Path:
    """Create the code file with the given code.

    Args:
        code: The code to write to the file.
        base_path: The path to create the file within

    Returns:
        The path to the code file.
    """
    (code_file := base_path / "test_source.py").write_text(f'"""Docstring."""\n\n{code}')
    return code_file


def test_fail(tmp_path: Path):
    """
    given: file with Python code that fails the linting
    when: flake8 is run against the code
    then: the process exits with non-zero code and includes the error message
    """
    code_file = create_code_file("from unittest import mock\n\nmock.Mock()\n", tmp_path)

    with subprocess.Popen(
        f"{sys.executable} -m flake8 {code_file}",
        stdout=subprocess.PIPE,
        shell=True,
    ) as proc:
        stdout = proc.communicate()[0].decode(encoding="utf-8")

        assert MOCK_SPEC_MSG in stdout
        assert proc.returncode


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            """
from unittest import mock

mock.Mock(spec=1)
""",
            id="default",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.Mock()  # noqa: {MOCK_SPEC_CODE}
""",
            id=f"{MOCK_SPEC_CODE} disabled",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.MagicMock()  # noqa: {MAGIC_MOCK_SPEC_CODE}
""",
            id=f"{MAGIC_MOCK_SPEC_CODE} disabled",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.NonCallableMock()  # noqa: {NON_CALLABLE_MOCK_SPEC_CODE}
""",
            id=f"{NON_CALLABLE_MOCK_SPEC_CODE} disabled",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.AsyncMock()  # noqa: {ASYNC_MOCK_SPEC_CODE}
""",
            id=f"{ASYNC_MOCK_SPEC_CODE} disabled",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.patch()  # noqa: {PATCH_CODE}
""",
            id=f"{PATCH_CODE} disabled",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.patch.object()  # noqa: {PATCH_OBJECT_CODE}
""",
            id=f"{PATCH_OBJECT_CODE} disabled",
        ),
        pytest.param(
            f"""
from unittest import mock

mock.patch.multiple()  # noqa: {PATCH_MULTIPLE_CODE}
""",
            id=f"{PATCH_MULTIPLE_CODE} disabled",
        ),
    ],
)
def test_pass(code: str, tmp_path: Path):
    """
    given: file with Python code that passes the linting
    when: flake8 is run against the code
    then: the process exits with zero code and empty stdout
    """
    code_file = create_code_file(code, tmp_path)
    (config_file := tmp_path / ".flake8").touch()

    with subprocess.Popen(
        (f"{sys.executable} -m flake8 {code_file} " f"--config {config_file}"),
        stdout=subprocess.PIPE,
        shell=True,
    ) as proc:
        stdout = proc.communicate()[0].decode(encoding="utf-8")

        assert not stdout, stdout
        assert not proc.returncode
