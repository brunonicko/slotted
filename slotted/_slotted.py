import inspect

import six
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
            if not hasattr(base, "__slots__"):
                raise TypeError("base {!r} does not define __slots__".format(base.__name__))

        return cls


class Slotted(six.with_metaclass(SlottedMeta, object)):
    """Enforces __slots__."""

    __slots__ = ()


def slots(cls):
    # type: (Type) -> Set[str]
    """Get all slot names for a class."""
    _slots = set()  # type: Set[str]
    for base in inspect.getmro(cls):
        _slots.update(getattr(base, "__slots__", ()))
    return _slots
