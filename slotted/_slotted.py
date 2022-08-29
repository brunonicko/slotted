import inspect
import sys

import six
from basicco import state, mangling
from tippo import Set, Type

__all__ = ["SlottedMeta", "Slotted", "slots"]


class SlottedMeta(type):
    """Metaclass that enforces __slots__."""

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

        # Add state reducer method for older Python versions.
        if sys.version_info[0:2] < (3, 4):
            if getattr(cls, "__reduce__", None) is object.__reduce__:
                type.__setattr__(cls, "__reduce__", state.reducer)

        return cls


class Slotted(six.with_metaclass(SlottedMeta, object)):
    """Enforces __slots__."""

    __slots__ = ()


def slots(cls, mangled=False):
    # type: (Type, bool) -> Set[str]
    """Get all slot names for a class."""
    _slots = set()  # type: Set[str]
    for base in inspect.getmro(cls):
        _slots.update(mangling.mangle(s, base.__name__) if mangled else s for s in getattr(base, "__slots__", ()))
    return _slots
