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


if __name__ == '__main__':
    unittest.main()
