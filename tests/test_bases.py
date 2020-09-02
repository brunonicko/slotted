# -*- coding: utf-8 -*-
"""Tests for `slotted._abc`."""

import pytest
import six

from slotted._bases import (
    Slotted,
    SlottedMeta,
    privatize_name,
    scrape_all_members,
    scrape_members,
    update_members,
)

__all__ = [
    "test_privatize_name",
    "test_update_members",
    "test_scrape_members",
    "test_scrape_all_members",
    "test_slotted_meta",
    "test_slotted",
]


def test_privatize_name():
    """Test the `privatize_name` function."""
    assert privatize_name("Foo", "bar") == "bar"
    assert privatize_name("Foo", "_bar") == "_bar"
    assert privatize_name("Foo", "__bar__") == "__bar__"
    assert privatize_name("Foo", "__bar") == "_Foo__bar"
    assert privatize_name("_Foo", "__bar") == "_Foo__bar"
    assert privatize_name("__Foo", "__bar") == "_Foo__bar"


def test_update_members():
    """Test the `update_members` function."""

    class Foo(object):
        __slots__ = ("foo", "bar")

    class Bar(object):
        __slots__ = ("bar", "foobar")

    members = {"foo": {Foo: Foo.foo}, "bar": {Foo: Foo.bar}}
    update = {"bar": {Bar: Bar.bar}, "foobar": {Bar: Bar.foobar}}
    update_members(members, update)
    expected = {
        "foo": {Foo: Foo.foo},
        "bar": {Foo: Foo.bar, Bar: Bar.bar},
        "foobar": {Bar: Bar.foobar},
    }
    assert members == expected


def test_scrape_members():
    """Test the `scrape_members` function."""

    class Foo(object):
        __slots__ = ("foo",)

    class Bar(Foo):
        __slots__ = ("foo", "_bar")

    members = scrape_members(Bar)
    expected = {"foo": {Bar: Bar.foo}, "_bar": {Bar: Bar._bar}}
    assert members == expected


def test_scrape_all_members():
    """Test the `scrape_all_members` function."""

    class Foo(object):
        __slots__ = ("foo",)

    class Bar(Foo):
        __slots__ = ("foo", "_bar")

    members = scrape_all_members(Bar)
    expected = {"foo": {Foo: Foo.foo, Bar: Bar.foo}, "_bar": {Bar: Bar._bar}}
    assert members == expected


def test_slotted_meta():
    """Test the `SlottedMeta` meta class."""

    class Foo(object):
        __slots__ = ("foo", "foobar")

    class Bar(six.with_metaclass(SlottedMeta, Foo)):
        __slots__ = ("foo", "bar")

    Foo.foobar = 1

    class FooBar(Bar, Foo):
        pass

    assert hasattr(FooBar, "__slots__")
    assert FooBar.__slots__ == ()
    assert Bar.__slots__ == ("foo", "bar")
    expected = {
        "foo": {Foo: Foo.__dict__["foo"], Bar: Bar.__dict__["foo"]},
        "bar": {Bar: Bar.__dict__["bar"], },
    }
    assert Bar.__members__ == expected

    class BarBar(object):
        pass

    with pytest.raises(TypeError):
        SlottedMeta("FooBarBar", (BarBar, FooBar), {})


def test_slotted():
    """Test the `SlottedMeta` class."""

    class Foo(object):
        __slots__ = ("foo", "__foobar")

        def __init__(self):
            self.__foobar = None

        @property
        def foobar(self):
            if self.__foobar is None:
                raise ValueError("'__foobar' never set")
            return self.__foobar

        @foobar.setter
        def foobar(self, value):
            self.__foobar = value

    class Bar(Slotted, Foo):
        __slots__ = ("foo", "bar")

    Foo.foobar = 1

    bar = Bar()
    bar.foo = 2
    bar.bar = 3
    Foo.foo.__set__.__call__(bar, 4)

    new_bar = Bar()
    new_bar.__setstate__(bar.__getstate__())

    assert bar.foo == new_bar.foo
    assert Foo.foo.__get__(bar) == Foo.foo.__get__(new_bar)
    assert bar.bar == new_bar.bar
    assert bar.foobar == new_bar.foobar


if __name__ == "__main__":
    pytest.main()
