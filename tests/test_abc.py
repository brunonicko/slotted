# -*- coding: utf-8 -*-

import unittest

from abc import ABCMeta
try:
    import collections.abc as collections
except ImportError:
    import collections as collections
collections_all = getattr(collections, "__all__")

__all__ = ["TestCollections"]


class TestCollections(unittest.TestCase):
    """Tests for '_collections' module."""

    def test_all(self):
        from slotted._bases import SlottedMeta, Slotted
        from slotted import _abc as slotted_abc
        from slotted._abc import __all__ as slotted_abc_all
        not_converted = {"SlottedABCMeta", "SlottedABC"}

        for name in set(slotted_abc_all).difference(not_converted):
            self.assertTrue(name.startswith("Slotted"))
            self.assertTrue(hasattr(slotted_abc, name))

            original_name = name[len("Slotted"):]
            self.assertIn(original_name, collections_all)

            cls = getattr(slotted_abc, name)
            self.assertIsInstance(cls, ABCMeta)
            self.assertIsInstance(cls, SlottedMeta)
            self.assertTrue(issubclass(cls, Slotted))

            original_cls = getattr(collections, original_name)
            self.assertTrue(issubclass(type(cls), type(original_cls)))
            self.assertTrue(issubclass(cls, original_cls))


if __name__ == "__main__":
    unittest.main()
