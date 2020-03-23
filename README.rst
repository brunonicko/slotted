Slotted
=======
Enforces usage of ``__slots__`` for python classes and provides pickling capabilities.

Examples
--------
When defining a ``Slotted`` class with no ``__slots__`` declaration, it assumes it has
empty slots, which is equivalent of declaring ``__slots__ = ()``.

.. code:: python

    >>> from slotted import Slotted
    >>> class Foo(Slotted):
    ...     pass  # implicit declaration of __slots__ = ()
    ...
    >>> foo = Foo()
    >>> foo.bar = 1
    Traceback (most recent call last):
    AttributeError: 'Foo' object has no attribute 'bar'

Slotted classes have pickling support:

.. code:: python

    >>> from slotted import Slotted
    >>> from pickle import dumps, loads
    >>> class Foo(Slotted):
    ...     __slots__ = ("bar", "foobar")
    ...
    >>> foo = Foo()
    >>> foo.bar = 1
    >>> foo.foobar = 2
    >>> another_foo = loads(dumps(foo))
    >>> print(another_foo.bar, another_foo.foobar)
    (1, 2)

Slotted classes can be mixed with regular classes as long as they and all of their bases
implement ``__slots__``.

.. code:: python

    >>> from slotted import Slotted
    >>> class Bar(object):
    ...     __slots__ = ("bar",)
    >>> class Foo(Bar, Slotted):
    ...     __slots__ = ("foo",)
    ...
    >>> foo = Foo()

If any non-``Slotted`` class anywhere in the chain does not implement ``__slots__``, a
``TypeError`` exception is raised.

.. code:: python

    >>> from slotted import Slotted
    >>> class Bar(object):
    ...     pass
    >>> class Foo(Bar, Slotted):
    ...     __slots__ = ("foo",)
    ...
    TypeError: base 'Bar' does not enforce '__slots__'

``Slotted`` behavior can also be achieved by using the ``SlottedMeta`` metaclass.

.. code:: python

    >>> from slotted import SlottedMeta
    >>> from six import add_metaclass
    >>> @add_metaclass(SlottedMeta)
    ... class Foo(object):
    ...     pass  # implicit declaration of __slots__ = ()
    ...
    >>> foo = Foo()
    >>> foo.bar = 1
    Traceback (most recent call last):
    AttributeError: 'Foo' object has no attribute 'bar'

In Python 3, ``Slotted`` can be mixed with ``collections.abc`` classes without any
issues. However, those classes do not define slots in Python 2. In order to work around
that limitation, you can utilize automatically converted ``SlottedABC`` classes like so:

.. code:: python

    >>> from collections import Mapping
    >>> from slotted import SlottedMapping
    >>> issubclass(SlottedMapping, Mapping)
    True
    >>> class FooMapping(SlottedMapping):
    ...     __slots__ = ("_d",)
    ...     def __init__(self):
    ...         self._d = {"a": 1, "b": 2}
    ...     def __getitem__(self, item):
    ...         return self._d[item]
    ...     def __iter__(self):
    ...         for key in self._d:
    ...             yield key
    ...     def __len__(self):
    ...         return len(self._d)
    ...
    >>> m = FooMapping()
    >>> isinstance(m, Mapping)
    True
    >>> print(m["a"])
    1
    >>> m.bar = "foo"
    Traceback (most recent call last):
    AttributeError: 'FooMapping' object has no attribute 'bar'
