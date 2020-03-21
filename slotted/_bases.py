# -*- coding: utf-8 -*-

from collections import defaultdict
from types import GetSetDescriptorType, MemberDescriptorType
from six import with_metaclass, iteritems
from typing import Any, Dict, Type, Tuple, AnyStr

SlotsTuple = Tuple[str, ...]
AllSlotsDict = Dict[str, Dict[Type, MemberDescriptorType]]
StateDict = Dict[str, Dict[Type, Any]]


def privatize_name(cls_name, name):
    # type: (str, AnyStr) -> str
    """Privatize a member name."""
    if name.startswith("__") and not name.endswith("__"):
        return "_{}{}".format(cls_name.lstrip("_"), name)
    return name


def update_slots(slots, slots_update):
    # type: (AllSlotsDict, AllSlotsDict) -> None
    """Update 'all slots' dictionary in place."""
    for name, members in iteritems(slots_update):
        slots.setdefault(name, {})
        for base, member in iteritems(members):
            slots[name][base] = member


def scrape_slots(base):
    # type: (Type) -> AllSlotsDict
    """Scrape base for slots."""
    b_slots = defaultdict(dict)
    for n, m in iteritems(base.__dict__):
        if isinstance(m, MemberDescriptorType):
            b_slots[n][base] = m
    return b_slots


def scrape_all_slots(base):
    # type: (Type) -> AllSlotsDict
    """Scrape base for all slots."""
    b_all_slots = defaultdict(dict)
    for b_base in reversed(base.__mro__):
        if b_base is base:
            update_slots(b_all_slots, scrape_slots(base))
        else:
            update_slots(b_all_slots, scrape_all_slots(b_base))
    return b_all_slots


def make_slotted_class(mcs, name, bases, dct):
    # type: (Type[SlottedMeta], str, Tuple[Type, ...], Dict[str, Any]) -> SlottedMeta
    """Make slotted class."""

    # Copy dct so we don't mutate the original
    dct = dict(dct)

    # Prevent user from setting '__all_slots__' directly
    if dct.get("__all_slots__"):
        raise ValueError("'{}.__all_slots__' cannot be declared manually")

    # Get slots declared for this class
    __slots__ = dct["__slots__"] = tuple(dct.get("__slots__", ()))

    # Conflict error
    for slot in set(privatize_name(name, s) for s in __slots__):
        if slot in dct:
            raise ValueError(
                "'{}' in __slots__ conflicts with class variable".format(slot)
            )

    # Prepare dictionaries to store all slots for this class
    __all_slots__ = dct["__all_slots__"] = {}  # type: AllSlotsDict

    # Build class
    cls = super(SlottedMeta, mcs).__new__(mcs, name, bases, dct)

    # Collect all slots
    for base in reversed(cls.__mro__):
        if isinstance(base.__dict__.get("__dict__"), GetSetDescriptorType):
            raise TypeError(
                "base '{}' does not enforce '__slots__'".format(base.__name__)
            )
        if base is cls:
            base_all_slots = scrape_slots(cls)
        elif isinstance(base, SlottedMeta):
            base_all_slots = getattr(base, "__all_slots__")
        else:
            base_all_slots = scrape_all_slots(base)
        update_slots(__all_slots__, base_all_slots)

    return cls


def get_state(obj):
    # type: (Slotted) -> StateDict
    """Get state of a slotted object for pickling purposes."""
    state = defaultdict(dict)
    for name, members in iteritems(type(obj).__all_slots__):
        for base, member in iteritems(members):
            try:
                value = member.__get__(obj, base)
            except AttributeError:
                continue
            state[name][base] = value
    return state


def set_state(obj, state):
    # type: (Slotted, StateDict) -> None
    """Set state of a slotted object for unpickling purposes."""
    for name, bases in iteritems(state):
        for base, value in iteritems(bases):
            base.__dict__[name].__set__(obj, value)


class SlottedMeta(type):
    """Enforces usage of '__slots__'."""

    __new__ = staticmethod(make_slotted_class)


class Slotted(with_metaclass(SlottedMeta, object)):
    """Enforces usage of '__slots__' and implement pickling methods."""

    __slots__ = ()  # type: SlotsTuple
    __all_slots__ = {}  # type: AllSlotsDict

    def __getstate__(self):
        # type: () -> StateDict
        """Get state for pickling."""
        return get_state(self)

    def __setstate__(self, state):
        # type: (StateDict) -> None
        """Set state for unpickling."""
        set_state(self, state)
