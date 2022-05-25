import abc
import inspect
from typing import Set, Type

__all__ = ["SlottedMeta", "Slotted", "SlottedABCMeta", "SlottedABC", "slots"]


class SlottedMeta(type):
    """Metaclass that enforces __slots__."""

    @staticmethod
    def __new__(mcs, name, bases, dct, **kwargs):

        # Force slots when constructing this class.
        if "__slots__" not in dct:
            dct = dict(dct)
            dct["__slots__"] = ()
        cls = super().__new__(mcs, name, bases, dct, **kwargs)

        # All bases are required to have slots.
        for base in inspect.getmro(cls)[1:-1]:
            if not hasattr(base, "__slots__"):
                raise TypeError(f"{base} does not define __slots__")

        return cls


class Slotted(metaclass=SlottedMeta):
    """Enforces __slots__."""

    __slots__ = ()


class SlottedABCMeta(abc.ABCMeta, SlottedMeta):
    """Mix-in of abc.ABCMeta and SlottedMeta."""


class SlottedABC(abc.ABC, Slotted, metaclass=SlottedABCMeta):
    """Mix-in of abc.ABC and Slotted."""

    __slots__ = ()


def slots(cls: Type) -> Set[str]:
    """Get all slot names for a class."""
    _slots: Set[str] = set()
    for base in inspect.getmro(cls)[:-1]:
        _slots.update(getattr(base, "__slots__", ()))
    return _slots
