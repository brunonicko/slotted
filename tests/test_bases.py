# -*- coding: utf-8 -*-

import unittest
import six

__all__ = ["TestBases"]


class TestBases(unittest.TestCase):
    """Tests for '_bases' module."""

    def test_privatize_name(self):
        from slotted._bases import privatize_name

        self.assertEqual(privatize_name("Foo", "bar"), "bar")
        self.assertEqual(privatize_name("Foo", "_bar"), "_bar")
        self.assertEqual(privatize_name("Foo", "__bar__"), "__bar__")
        self.assertEqual(privatize_name("Foo", "__bar"), "_Foo__bar")
        self.assertEqual(privatize_name("_Foo", "__bar"), "_Foo__bar")
        self.assertEqual(privatize_name("__Foo", "__bar"), "_Foo__bar")

    def test_update_members(self):
        from slotted._bases import update_members

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
        self.assertEqual(members, expected)

    def test_scrape_members(self):
        from slotted._bases import scrape_members

        class Foo(object):
            __slots__ = ("foo",)

        class Bar(Foo):
            __slots__ = ("foo", "_bar")

        members = scrape_members(Bar)
        expected = {"foo": {Bar: Bar.foo}, "_bar": {Bar: Bar._bar}}
        self.assertEqual(members, expected)

    def test_scrape_all_members(self):
        from slotted._bases import scrape_all_members

        class Foo(object):
            __slots__ = ("foo",)

        class Bar(Foo):
            __slots__ = ("foo", "_bar")

        members = scrape_all_members(Bar)
        expected = {"foo": {Foo: Foo.foo, Bar: Bar.foo}, "_bar": {Bar: Bar._bar}}
        self.assertEqual(members, expected)

    def test_slotted_meta(self):
        from slotted._bases import SlottedMeta

        class Foo(object):
            __slots__ = ("foo", "foobar")

        class Bar(six.with_metaclass(SlottedMeta, Foo)):
            __slots__ = ("foo", "bar")

        Foo.foobar = 1

        class FooBar(Bar, Foo):
            pass

        self.assertTrue(hasattr(FooBar, "__slots__"))
        self.assertEqual(FooBar.__slots__, ())
        self.assertEqual(Bar.__slots__, ("foo", "bar"))
        expected = {
            "foo": {Foo: Foo.__dict__["foo"], Bar: Bar.__dict__["foo"],},
            "bar": {Bar: Bar.__dict__["bar"],},
        }
        self.assertEqual(Bar.__members__, expected)

        class BarBar(object):
            pass

        self.assertRaises(TypeError, SlottedMeta, ("FooBarBar", (BarBar, FooBar), {}))

    def test_slotted(self):
        from slotted._bases import Slotted

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

        self.assertEqual(bar.foo, new_bar.foo)
        self.assertEqual(Foo.foo.__get__(bar), Foo.foo.__get__(new_bar))
        self.assertEqual(bar.bar, new_bar.bar)
        self.assertEqual(bar.foobar, new_bar.foobar)


if __name__ == "__main__":
    unittest.main()
