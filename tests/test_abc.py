from abc import ABCMeta

try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc  # type: ignore

import pytest
import tippo

from slotted import _abc as slotted_abc  # noqa
from slotted._abc import __all__ as slotted_abc_all  # noqa
from slotted._slotted import Slotted, SlottedMeta  # noqa


collections_all = getattr(collections_abc, "__all__")

T = tippo.TypeVar("T")
KT = tippo.TypeVar("KT")
VT = tippo.TypeVar("VT")


def test_import_abc():
    import slotted
    from slotted._abc import __all__ as _collections_all  # noqa

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


def test_converted():
    not_converted = {"SlottedABCMeta", "SlottedABC"}

    for name in set(slotted_abc_all).difference(not_converted):
        assert name.startswith("Slotted")
        assert hasattr(slotted_abc, name)

        original_name = name[len("Slotted") :]
        if original_name not in collections_all:
            if original_name == "ABCGenericMeta":
                continue
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


def test_generics():
    generics = {
        # slotted_abc.SlottedCallable: (),
        slotted_abc.SlottedContainer: (T,),
        slotted_abc.SlottedItemsView: (KT, VT),
        slotted_abc.SlottedIterable: (T,),
        slotted_abc.SlottedIterator: (T,),
        slotted_abc.SlottedKeysView: (T,),
        slotted_abc.SlottedMapping: (KT, VT),
        slotted_abc.SlottedMappingView: (T,),
        slotted_abc.SlottedMutableMapping: (KT, VT),
        slotted_abc.SlottedMutableSequence: (T,),
        slotted_abc.SlottedMutableSet: (T,),
        slotted_abc.SlottedSequence: (T,),
        slotted_abc.SlottedSet: (T,),
        slotted_abc.SlottedValuesView: (T,),
    }
    for generic_cls, type_vars in generics.items():
        assert generic_cls[type_vars]

    metaclasses = set(type(g) for g in generics)
    assert len(metaclasses) == 1
    assert next(iter(metaclasses)) is slotted_abc.SlottedABCGenericMeta


if __name__ == "__main__":
    pytest.main()
