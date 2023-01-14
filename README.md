# flake8-mock-spec

Do you use mocks and are concerned you are calling methods or accessing
attributes the mocked objects don't have? If not, you should be as that is a
sure way to inject bugs into your code and still have your tests pass. The
`flake8-mock-spec` linter enforces the use of the `spec` argument on mocks
ensuring that your use of mocks is compliant with the interface of the object
being mocked.

## Getting Started

```shell
python -m venv venv
source ./venv/bin/activate
pip install flake8-mock-spec
flake8 test_source.py
```

On the following code:

```Python
# test_source.py
from unittest import mock

def test_foo():
    mocked_foo = mock.Mock()
```

This will produce warnings such as:

```shell
flake8 test_source.py
test_source.py:5:22: TMS010 unittest.mock.Mock instances should be constructed with the spec or spec_set argument, more information: https://github.com/jdkandersson/flake8-mock-spec#fix-tms010
```

This can be resolved by changing the code to:

```Python
# test_source.py
from unittest import mock

from foo import Foo

def test_foo():
    mocked_foo = mock.Mock(spec=Foo)
```

## Rules

A few rules have been defined to allow for selective suppression:

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

### Fix TMS010

This linting rule is triggered by creating a `unittest.mock.Mock` instance
without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.Mock()
```

This example can be fixed by using the `spec` or `spec_set` argument in the
constructor:

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

### Fix TMS011

This linting rule is triggered by creating a `unittest.mock.MagicMock` instance
without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.MagicMock()
```

This example can be fixed by using the `spec` or `spec_set` argument in the
constructor:

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

### Fix TMS012

This linting rule is triggered by creating a `unittest.mock.NonCallableMock`
instance without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.NonCallableMock()
```

This example can be fixed by using the `spec` or `spec_set` argument in the
constructor:

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

### Fix TMS013

This linting rule is triggered by creating a `unittest.mock.AsyncMock` instance
without the `spec` or `spec_set` argument. For example:

```Python
from unittest import mock

def test_foo():
    mocked_foo = mock.AsyncMock()
```

This example can be fixed by using the `spec` or `spec_set` argument in the
constructor:

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

### Fix TMS020

This linting rule is triggered by calling `unittest.mock.patch` without any one
or more of the `new`, `spec`, `spec_set`, `autospec` or `new_callable`
arguments. For example:

```Python
from unittest import mock

@mock.patch("Foo")
def test_foo():
    pass

with mock.patch("Foo") as mocked_foo:
    pass

foo_patcher = patch("Foo")
```

This example can be fixed by using any one or more of the `new`, `spec`,
`spec_set`, `autospec` or `new_callable` arguments:

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
