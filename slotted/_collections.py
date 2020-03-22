# -*- coding: utf-8 -*-

from abc import ABCMeta as _ABCMeta

try:
    import collections.abc as _collections
except ImportError:
    import collections as _collections
    from collections import *
else:
    # noinspection PyCompatibility
    from collections.abc import *

from typing import Dict as _Dict
from typing import Type as _Type
from typing import Set as _Set

from ._bases import SlottedMeta as _SlottedMeta
from ._bases import Slotted as _Slotted

__all__ = []


class _SlottedABCMeta(_SlottedMeta, _ABCMeta):
    pass


_collections_all = set(getattr(_collections, "__all__"))
_classes = set()  # type: _Set[_Type]
_cache = {object: _Slotted, _ABCMeta: _SlottedABCMeta}  # type: _Dict[_Type, _Type]

for _cls_name in _collections_all:
    try:
        _cls = locals()[_cls_name]
    except (KeyError, AttributeError):
        continue
    if not isinstance(_cls, _ABCMeta) or not issubclass(_cls, object):
        continue
    _classes.add(_cls)


def _convert_meta(source):
    # type: (_Type) -> _Type
    """Convert a metaclass to a slotted metaclass."""
    try:
        return _cache[source]
    except KeyError:
        pass

    target_bases = []
    for source_base in source.__bases__:
        target_bases.append(_convert_meta(source_base))

    source_name = source.__name__
    target_name = "Slotted{}".format(source_name)
    target_bases = tuple(target_bases)
    target_dct = dict(source.__dict__)
    target_dct["__module__"] = __name__

    target = type(target_name, target_bases, target_dct)
    _cache[source] = target

    if source_name in _collections_all:
        __all__.append(target_name)
    return target


def _convert(source):
    # type: (_ABCMeta) -> _SlottedABCMeta
    """Convert a class to slotted."""
    try:
        return _cache[source]
    except KeyError:
        pass

    meta = _convert_meta(type(source))

    target_bases = []
    for source_base in source.__bases__:
        target_bases.append(_convert(source_base))

    source_name = source.__name__
    target_name = "Slotted{}".format(source_name)
    target_bases = tuple(target_bases)
    target_dct = dict(source.__dict__)
    target_dct.pop("__dict__", None)
    target_dct["__module__"] = __name__

    target = meta(target_name, target_bases, target_dct)
    _cache[source] = target

    if target.__dict__.get("__dict__") is not None:
        raise AssertionError("class '{}' has a '__dict__'".format(target_name))

    source.register(target)
    if source_name in _collections_all:
        __all__.append(target_name)
    return target


# Convert all classes
for _c in _classes:
    _converted = _convert(_c)
    locals()[_converted.__name__] = _converted
