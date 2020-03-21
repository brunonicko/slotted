import unittest

__all__ = ["TestBases"]


class TestBases(unittest.TestCase):

    def test_privatize_name(self):
        from slotted._bases import privatize_name

        self.assertEqual(privatize_name("Foo", "bar"), "bar")
        self.assertEqual(privatize_name("Foo", "_bar"), "_bar")
        self.assertEqual(privatize_name("Foo", "__bar__"), "__bar__")
        self.assertEqual(privatize_name("Foo", "__bar"), "_Foo__bar")
        self.assertEqual(privatize_name("_Foo", "__bar"), "_Foo__bar")
        self.assertEqual(privatize_name("__Foo", "__bar"), "_Foo__bar")

    def test_update_slots(self):
        from slotted._bases import update_slots

        class Foo(object):
            __slots__ = ("foo", "bar")

        class Bar(object):
            __slots__ = ("bar", "foobar")

        slots = {"foo": {Foo: Foo.foo}, "bar": {Foo: Foo.bar}}
        update = {"bar": {Bar: Bar.bar}, "foobar": {Bar: Bar.foobar}}

        update_slots(slots, update)
        expected = {
            "foo": {Foo: Foo.foo},
            "bar": {Foo: Foo.bar, Bar: Bar.bar},
            "foobar": {Bar: Bar.foobar}
        }

        self.assertEqual(slots, expected)


if __name__ == '__main__':
    unittest.main()
