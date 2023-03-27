import inspect

import six
from tippo import Set

__all__ = ["SlottedMeta", "Slotted", "slots"]


class SlottedMeta(type):
    """Metaclass that enforces `__slots__`."""

    @staticmethod
    def __new__(mcs, name, bases, dct, **kwargs):
        # All bases are required to inherit from object and to have slots.
        for base in bases:
            if not issubclass(base, object):
                error = "{!r} is not a subclass of object".format(base.__name__)
                raise TypeError(error)
            if "__dict__" in base.__dict__:
                error = "base {!r} is not slotted".format(base.__name__)
                raise TypeError(error)

        # Force slots when constructing this class.
        if "__slots__" not in dct:
            dct = dict(dct)
            dct["__slots__"] = ()

        return super(SlottedMeta, mcs).__new__(mcs, name, bases, dct, **kwargs)


class Slotted(six.with_metaclass(SlottedMeta, object)):
    """Enforces `__slots__`."""

    __slots__ = ()


def _mangle(name, owner_name):
    # type: (str, str) -> str
    if name.startswith("__") and not name.endswith("__"):
        return "_{}{}".format(owner_name.lstrip("_"), name)
    return name


def slots(cls, mangled=False):
    # type: (type, bool) -> Set[str]
    """
    Get all slot names for a class.

    :param cls: Class.
    :param mangled: Whether to mangle the protected names.
    :return: A set of slot names.
    """
    _slots = set()  # type: Set[str]
    for base in inspect.getmro(cls):
        _slots.update(
            _mangle(s, base.__name__) if mangled else s
            for s in getattr(base, "__slots__", ())
        )
    return _slots
