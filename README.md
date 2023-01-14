# flake8-mock-spec

Are you using mocks in your code and want to ensure that you are not accessing
or calling methods that the mocked objects don't have? Using mocks incorrectly
can lead to bugs in your code and falsely passing tests. To avoid this,
flake8-mock-spec linter has been created to enforce the use of the spec
argument when creating mocks. This ensures that your use of mocks is compliant
with the interface of the actual object being mocked, and helps you catch
errors early on. Using this linter can save you time and help you write more
robust and maintainable code.

## Getting Started

To start using `flake8-mock-spec`, you need to install the package and run it
on your source code. Here are the steps to get started:

1. Create a virtual environment and activate it:

  ```shell
  python -m venv venv
  source ./venv/bin/activate
  ```

2. Install `flake8-mock-spec`:

  ```shell
  pip install flake8-mock-spec
  ```

3. Run `flake8` on your source code:

  ```shell
  flake8 test_source.py
  ```

For example, consider the following code:

```Python
# test_source.py
from unittest import mock

def test_foo():
    mocked_foo = mock.Mock()
```

Running `flake8` on this code will produce the following warning:

```shell
flake8 test_source.py
test_source.py:5:22: TMS010 unittest.mock.Mock instances should be constructed with the spec or spec_set argument, more information: https://github.com/jdkandersson/flake8-mock-spec#fix-tms010
```

To resolve this warning, you need to specify the `spec` or `spec_set` argument
when creating the mock object:

```Python
# test_source.py
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.Mock(spec=Foo)
```

## Rules

A set of linting rules have been defined to ensure best practices are followed
when using unittest.mock library. These rules allow for selective suppression,
meaning that specific rules can be ignored in certain scenarios. The following
rules have been defined:

* `TMS010`: checks that `unittest.mock.Mock` instances are constructed with the
  `spec` or `spec_set` argument.
* `TMS011`: checks that `unittest.mock.MagicMock` instances are constructed with
  the `spec` or `spec_set` argument.
* `TMS012`: checks that `unittest.mock.NonCallableMock` instances are
  constructed with the `spec` or `spec_set` argument.
* `TMS013`: checks that `unittest.mock.AsyncMock` instances are constructed
  with the `spec` or `spec_set` argument.
* `TMS020`: checks that `unittest.mock.patch` is called with any one or more of
  the `new`, `spec`, `spec_set`, `autospec` or `new_callable` arguments
* `TMS021`: checks that `unittest.mock.patch.object` is called with any one or
  more of the `new`, `spec`, `spec_set`, `autospec` or `new_callable` arguments

### Fix TMS010

This linting rule is triggered when a `unittest.mock.Mock` instance is created
without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.Mock()
```

To fix this issue, you need to provide the `spec` or `spec_set` argument when
creating the mock object. Here are a few examples:

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.Mock(spec=Foo)
```

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.Mock(spec_set=Foo)
```

For more information about `mock.Mock` and how to use it, please refer to the
official documentation:
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock

### Fix TMS011

This linting rule is triggered when a `unittest.mock.MagicMock` instance is
created without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.MagicMock()
```

To fix this issue, you need to provide the `spec` or `spec_set` argument when
creating the mock object. Here are a few examples:

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.MagicMock(spec=Foo)
```

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.MagicMock(spec_set=Foo)
```

For more information about `mock.MagicMock` and how to use it, please refer to the
official documentation:
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock

### Fix TMS012

This linting rule is triggered when a `unittest.mock.NonCallableMock` instance
is created without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.NonCallableMock()
```

To fix this issue, you need to provide the `spec` or `spec_set` argument when
creating the mock object. Here are a few examples:

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.NonCallableMock(spec=Foo)
```

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.NonCallableMock(spec_set=Foo)
```

For more information about `mock.NonCallableMock` and how to use it, please refer to the
official documentation:
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.NonCallableMock

### Fix TMS013

This linting rule is triggered when a `unittest.mock.AsyncMock` instance is
created without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.AsyncMock()
```

To fix this issue, you need to provide the `spec` or `spec_set` argument when
creating the mock object. Here are a few examples:

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.AsyncMock(spec=Foo)
```

```Python
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.AsyncMock(spec_set=Foo)
```

For more information about `mock.AsyncMock` and how to use it, please refer to the
official documentation:
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock

### Fix TMS020

This linting rule is triggered when calling unittest.mock.patch without
including one or more of the following arguments: `new`, `spec`, `spec_set`,
`autospec`, or `new_callable`.

For example, this code will trigger the rule:

```Python
from unittest import mock

@mock.patch("Foo")
def test_foo():
    pass

with mock.patch("Foo") as mocked_foo:
    pass

foo_patcher = patch("Foo")
```

To fix this issue, include one or more of the aforementioned arguments when
calling `mock.patch`. For example:

```Python
from unittest import mock

from foo import Foo

@mock.patch("Foo", spec=Foo)
def test_foo():
    pass

with mock.patch("Foo", spec_set=Foo) as mocked_foo:
    pass

foo_patcher = patch("Foo", autospec=True)
```

For more information about `mock.patch` and how to use it, please refer to the
official documentation:
https://docs.python.org/3/library/unittest.mock.html#patch

### Fix TMS021

This linting rule is triggered when calling unittest.mock.patch.object without
including one or more of the following arguments: `new`, `spec`, `spec_set`,
`autospec`, or `new_callable`.

For example, this code will trigger the rule:

```Python
from unittest import mock

from foo import Foo

@mock.patch.object(Foo, "bar")
def test_foo():
    pass

with mock.patch.object(Foo, "bar") as mocked_foo:
    pass

foo_patcher = patch(Foo, "bar")
```

To fix this issue, include one or more of the aforementioned arguments when
calling `mock.patch.object`. For example:

```Python
from unittest import mock

from foo import Foo

@mock.patch.object(Foo, "bar", spec=Foo.bar)
def test_foo():
    pass

with mock.patch.object(Foo, "bar", spec_set=Foo.bar) as mocked_foo:
    pass

foo_patcher = patch(Foo, "bar", autospec=True)
```

For more information about `mock.patch.object` and how to use it, please refer
to the official documentation:
https://docs.python.org/3/library/unittest.mock.html#patch
