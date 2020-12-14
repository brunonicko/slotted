# -*- coding: utf-8 -*-
"""Test importing from `slotted`."""

import pytest

__all__ = ["test_import", "test_import_abc"]


def test_import():
    from slotted import Slotted, SlottedMeta, get_state, set_state

    assert all((Slotted, SlottedMeta, get_state, set_state))


def test_import_abc():
    import slotted
    from slotted._abc import __all__ as _collections_all

    assert _collections_all
    for name in _collections_all:
        member = getattr(slotted, name)
        if member is None:
            assert name == "SlottedCollection"
            with pytest.raises(ImportError):
                try:
                    # noinspection PyCompatibility
                    from collections.abc import Collection  # noqa
                except ImportError:
                    from collections import Collection  # noqa
        else:
            assert getattr(slotted, name)


if __name__ == "__main__":
    pytest.main()
