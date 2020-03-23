# -*- coding: utf-8 -*-

from abc import ABCMeta
from types import MemberDescriptorType
from six import with_metaclass, iteritems

try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc

from typing import Any
from typing import Dict
from typing import Type
from typing import Set
from typing import Tuple

from ._bases import privatize_name
from ._bases import SlottedMeta
from ._bases import Slotted

__all__ = ["SlottedABCMeta", "SlottedABC"]


class SlottedABCMeta(SlottedMeta, ABCMeta):
    """Metaclass for 'SlottedABC'. Combines 'SlottedMeta' and 'ABCMeta'."""


class SlottedABC(with_metaclass(SlottedABCMeta, Slotted)):
    """Slotted 'ABC' base class."""


_ABC_ALL = set(getattr(collections_abc, "__all__"))

_CLASSES = set()  # type: Set[Type]
for cls_name in _ABC_ALL:
    try:
        cls = getattr(collections_abc, cls_name)
    except AttributeError:
        continue
    if not isinstance(cls, ABCMeta) or not issubclass(cls, object):
        continue
    _CLASSES.add(cls)

_CACHE = {object: SlottedABC, ABCMeta: SlottedABCMeta}  # type: Dict[Type, Type]


def extract_dict(base):
    # type: (Type) -> Tuple[Dict[str, Any], Dict[str, Any]]
    slots = set(
        privatize_name(base.__name__, slot) for slot in getattr(base, "__slots__", ())
    )
    base_dict = {}
    overrides = {}
    for name, value in iteritems(base.__dict__):
        if name in slots:
            if isinstance(value, MemberDescriptorType):
                if value.__objclass__ is base and value.__name__ == name:
                    continue
            overrides[name] = value
        else:
            base_dict[name] = value
    return base_dict, overrides


def convert_meta(source):
    # type: (Type) -> Type
    """Convert an ABCMeta-based metaclass to a SlottedABCMeta-based metaclass."""
    try:
        return _CACHE[source]
    except KeyError:
        pass

    target_bases = []
    for source_base in source.__bases__:
        target_bases.append(convert_meta(source_base))

    source_name = source.__name__
    target_name = "Slotted{}".format(source_name)
    target_bases = tuple(target_bases)
    target_dct, overrides = extract_dict(source)
    target_dct["__module__"] = __name__

    target = type(target_name, target_bases, target_dct)
    for name, value in iteritems(overrides):
        type.__setattr__(target, name, value)
    _CACHE[source] = target

    if source_name in _ABC_ALL:
        __all__.append(target_name)
    return target


def convert(source):
    # type: (ABCMeta) -> SlottedABCMeta
    """Convert an ABC-based class to an SlottedABC-based class."""
    try:
        return _CACHE[source]
    except KeyError:
        pass

    meta = convert_meta(type(source))

    target_bases = []
    for source_base in source.__bases__:
        target_bases.append(convert(source_base))

    source_name = source.__name__
    target_name = "Slotted{}".format(source_name)
    target_bases = tuple(target_bases)
    target_dct, overrides = extract_dict(source)
    target_dct.pop("__dict__", None)
    target_dct["__module__"] = __name__

    target = meta(target_name, target_bases, target_dct)
    for name, value in iteritems(overrides):
        type.__setattr__(target, name, value)
    _CACHE[source] = target

    if target.__dict__.get("__dict__") is not None:
        raise AssertionError("class '{}' has a '__dict__'".format(target_name))

    source.register(target)
    if source_name in _ABC_ALL:
        __all__.append(target_name)
    return target


# Convert all classes
for cls in _CLASSES:
    converted = convert(cls)
    locals()[converted.__name__] = converted
