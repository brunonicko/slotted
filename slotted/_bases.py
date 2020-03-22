# -*- coding: utf-8 -*-

from collections import defaultdict
from types import GetSetDescriptorType, MemberDescriptorType
from six import with_metaclass, iteritems
from typing import Any, Dict, Type, Tuple, AnyStr

SlotsTuple = Tuple[str, ...]
MembersDict = Dict[str, Dict[Type, MemberDescriptorType]]
StateDict = Dict[str, Dict[Type, Any]]


def privatize_name(cls_name, name):
    # type: (str, AnyStr) -> str
    """Privatize an attribute name if necessary."""
    if name.startswith("__") and not name.endswith("__"):
        return "_{}{}".format(cls_name.lstrip("_"), name)
    return name


def update_members(members, members_update):
    # type: (MembersDict, MembersDict) -> None
    """Update members dictionary in place."""
    for name, bases in iteritems(members_update):
        members.setdefault(name, {})
        for base, member in iteritems(bases):
            members[name][base] = member


def scrape_members(base):
    # type: (Type) -> MembersDict
    """Scrape base for members (shallow)."""
    if base is object:
        return {}
    base_members = defaultdict(dict)
    for name in base.__slots__:
        try:
            member = base.__dict__[privatize_name(base.__name__, name)]
        except KeyError:
            continue
        if isinstance(member, MemberDescriptorType):
            if member.__objclass__ is base and member.__name__ == name:
                base_members[name][base] = member
    return base_members


def scrape_all_members(base):
    # type: (Type) -> MembersDict
    """Scrape base for all members (deep)."""
    all_members = defaultdict(dict)
    for base_base in reversed(base.__mro__):
        if base_base is base:
            update_members(all_members, scrape_members(base))
        else:
            update_members(all_members, scrape_all_members(base_base))
    return all_members


def get_state(obj):
    # type: (Slotted) -> StateDict
    """Get state of a slotted object for pickling purposes."""
    state = defaultdict(dict)
    for name, members in iteritems(type(obj).__members__):
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
            member = base.__dict__[name]
            if isinstance(member, MemberDescriptorType):
                if member.__objclass__ is base and member.__name__ == name:
                    member.__set__.__call__(obj, value)


def _make_slotted_class(mcs, name, bases, dct):
    # type: (Type[SlottedMeta], str, Tuple[Type, ...], Dict[str, Any]) -> SlottedMeta
    """Make slotted class."""
    for base in bases:
        if isinstance(base.__dict__.get("__dict__"), GetSetDescriptorType):
            raise TypeError(
                "base '{}' does not enforce '__slots__'".format(base.__name__)
            )
    dct = dict(dct)
    dct["__slots__"] = tuple(dct.get("__slots__", ()))
    return super(SlottedMeta, mcs).__new__(mcs, name, bases, dct)


class SlottedMeta(type):
    """Enforces usage of '__slots__'."""

    __new__ = staticmethod(_make_slotted_class)

    @property
    def __members__(cls):
        # type: () -> MembersDict
        members = {}
        for base in reversed(cls.__mro__):
            if base is cls:
                base_members = scrape_members(cls)
            elif isinstance(base, SlottedMeta):
                base = base  # type: SlottedMeta
                base_members = base.__members__
            else:
                base_members = scrape_all_members(base)
            update_members(members, base_members)
        return members


class Slotted(with_metaclass(SlottedMeta, object)):
    """Enforces usage of '__slots__' and implements pickling methods based on state."""

    __slots__ = ()  # type: SlotsTuple

    def __getstate__(self):
        # type: () -> StateDict
        """Get state for pickling."""
        return get_state(self)

    def __setstate__(self, state):
        # type: (StateDict) -> None
        """Set state for unpickling."""
        set_state(self, state)
