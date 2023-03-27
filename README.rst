.. logo_start
.. raw:: html

   <p align="center">
     <a href="https://github.com/brunonicko/slotted">
         <picture>
            <object data="./_static/slotted.svg" type="image/png">
                <source
                    srcset="./docs/source/_static/slotted_white.svg"
                    media="(prefers-color-scheme: dark)"
                />
                <img
                    src="./docs/source/_static/slotted.svg"
                    width="60%"
                    alt="slotted"
                />
            </object>
         </picture>
     </a>
   </p>
.. logo_end

.. image:: https://github.com/brunonicko/slotted/workflows/MyPy/badge.svg
   :target: https://github.com/brunonicko/slotted/actions?query=workflow%3AMyPy

.. image:: https://github.com/brunonicko/slotted/workflows/Lint/badge.svg
   :target: https://github.com/brunonicko/slotted/actions?query=workflow%3ALint

.. image:: https://github.com/brunonicko/slotted/workflows/Tests/badge.svg
   :target: https://github.com/brunonicko/slotted/actions?query=workflow%3ATests

.. image:: https://readthedocs.org/projects/slotted/badge/?version=stable
   :target: https://slotted.readthedocs.io/en/stable/

.. image:: https://img.shields.io/github/license/brunonicko/slotted?color=light-green
   :target: https://github.com/brunonicko/slotted/blob/master/LICENSE

.. image:: https://static.pepy.tech/personalized-badge/slotted?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads
   :target: https://pepy.tech/project/slotted

.. image:: https://img.shields.io/pypi/pyversions/slotted?color=light-green&style=flat
   :target: https://pypi.org/project/slotted/

Overview
--------
Enforces usage of ``__slots__`` for Python classes.

Motivation
----------
Besides the performance benefits, using ``__slots__`` also prevents the client code from
setting attributes that were not initially defined for instances of classes, which
usually happens by mistake especially in environments where static type checking is not
being performed.

So forcing it upon a class and its subclasses might be a desirable thing to do for
classes that are part of an API, for example.

Examples
--------
When defining a ``Slotted`` class with no ``__slots__`` declaration, it assumes it has
empty slots, which is equivalent to declaring ``__slots__ = ()``.

.. code:: python

    >>> from slotted import Slotted

    >>> class Foo(Slotted):
    ...     pass  # implicit declaration of __slots__ = ()
    ...
    >>> foo = Foo()
    >>> foo.bar = 1
    Traceback (most recent call last):
    AttributeError: 'Foo' object has no attribute 'bar'

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
    Traceback (most recent call last):
    TypeError: base 'Bar' is not slotted

``Slotted`` behavior can also be achieved by using the ``SlottedMeta`` metaclass.

.. code:: python

    >>> from six import with_metaclass
    >>> from slotted import SlottedMeta

    >>> class Foo(with_metaclass(SlottedMeta, object)):
    ...     pass  # implicit declaration of __slots__ = ()
    ...
    >>> foo = Foo()
    >>> foo.bar = 1
    Traceback (most recent call last):
    AttributeError: 'Foo' object has no attribute 'bar'
