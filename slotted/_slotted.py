import inspect

import six
from tippo import Set, Type

from ._utils import mangle as _mangle

__all__ = ["SlottedMeta", "Slotted", "slots"]


class SlottedMeta(type):
    """Metaclass that enforces `__slots__`."""

    @staticmethod
    def __new__(mcs, name, bases, dct, **kwargs):

        # Force slots when constructing this class.
        if "__slots__" not in dct:
            dct = dict(dct)
            dct["__slots__"] = ()
        cls = super(SlottedMeta, mcs).__new__(mcs, name, bases, dct, **kwargs)

        # All bases are required to have slots.
        for base in inspect.getmro(cls)[1:-1]:
            if not hasattr(base, "__slots__") or "__dict__" in base.__dict__:
                raise TypeError("base {!r} does not define __slots__".format(base.__name__))

        return cls


class Slotted(six.with_metaclass(SlottedMeta, object)):
    """Enforces `__slots__`."""

    __slots__ = ()


def slots(cls, mangled=False):
    # type: (Type[Slotted] | SlottedMeta, bool) -> Set[str]
    """
    Get all slot names for a slotted class.

    :param cls: Slotted class.
    :param mangled: Whether to mangle the protected names.
    :return: A set of slot names.
    """
    _slots = set()  # type: Set[str]
    for base in inspect.getmro(cls):
        _slots.update(_mangle(s, base.__name__) if mangled else s for s in getattr(base, "__slots__", ()))
    return _slots
