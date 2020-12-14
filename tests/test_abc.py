# -*- coding: utf-8 -*-
"""Tests for `slotted._abc`."""

from abc import ABCMeta

try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc  # type: ignore

import pytest

from slotted import _abc as slotted_abc
from slotted._abc import __all__ as slotted_abc_all
from slotted._bases import Slotted, SlottedMeta

collections_all = getattr(collections_abc, "__all__")

__all__ = ["test_all"]


def test_all():
    """Test converted ABC classes."""
    not_converted = {"SlottedABCMeta", "SlottedABC"}

    for name in set(slotted_abc_all).difference(not_converted):
        assert name.startswith("Slotted")
        assert hasattr(slotted_abc, name)

        original_name = name[len("Slotted") :]
        if original_name not in collections_all:
            assert original_name == "Collection"
            with pytest.raises(ImportError):
                try:
                    # noinspection PyCompatibility
                    from collections.abc import Collection  # noqa
                except ImportError:
                    from collections import Collection  # noqa
            assert getattr(slotted_abc, name) is None
            continue

        assert original_name in collections_all

        cls = getattr(slotted_abc, name)
        assert isinstance(cls, ABCMeta)
        assert isinstance(cls, SlottedMeta)
        assert issubclass(cls, Slotted)

        original_cls = getattr(collections_abc, original_name)
        assert issubclass(type(cls), type(original_cls))
        assert issubclass(cls, original_cls)


if __name__ == "__main__":
    pytest.main()
