# -*- coding: utf-8 -*-

from types import GetSetDescriptorType, MemberDescriptorType
from typing import TYPE_CHECKING, cast

from six import iteritems, with_metaclass

if TYPE_CHECKING:
    from typing import Any, Dict, Tuple, Type

    SlotsTuple = Tuple[str, ...]
    MembersDict = Dict[str, Dict[Type, MemberDescriptorType]]
    StateDict = Dict[str, Dict[Type, Any]]


def privatize_name(cls_name, name):
    # type: (str, str) -> str
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
    base_members = {}  # type: MembersDict
    for name in base.__slots__:
        private_name = privatize_name(base.__name__, cast(str, name))
        try:
            member = base.__dict__[private_name]
        except KeyError:
            continue
        if isinstance(member, MemberDescriptorType):
            if member.__objclass__ is base and member.__name__ == private_name:
                base_members.setdefault(private_name, {})
                base_members[private_name][base] = member
    return base_members


def scrape_all_members(base):
    # type: (Type) -> MembersDict
    """Scrape base for all members (deep)."""
    all_members = {}  # type: MembersDict
    for base_base in reversed(base.__mro__):
        if base_base is base:
            update_members(all_members, scrape_members(base))
        else:
            update_members(all_members, scrape_all_members(base_base))
    return all_members


def get_state(obj):
    # type: (Slotted) -> StateDict
    """
    Get state of a slotted object.

    .. code:: python

        >>> from six import with_metaclass
        >>> from slotted import SlottedMeta, get_state

        >>> class A(with_metaclass(SlottedMeta, object)):
        ...     __slots__ = ("a", "b")
        ...
        >>> a = A()
        >>> a.a = 1
        >>> a.b = 2
        >>> get_state(a) == {
        ...     "a": {A: 1}, "b": {A: 2}
        ... }
        True

    :param obj: Slotted object (metaclass inherits from :class:`slotted.SlottedMeta`).

    :return: State.
    :rtype: dict
    """
    state = {}  # type: StateDict
    for name, members in iteritems(type(obj).__members__):
        for base, member in iteritems(members):
            try:
                value = member.__get__(obj, base)
            except AttributeError:
                continue
            state.setdefault(name, {})
            state[name][base] = value
    return state


def set_state(obj, state):
    # type: (Slotted, StateDict) -> None
    """
    Set state of a slotted object.

    .. code:: python

        >>> from six import with_metaclass
        >>> from slotted import SlottedMeta, set_state

        >>> class A(with_metaclass(SlottedMeta, object)):
        ...     __slots__ = ("a", "b")
        ...
        >>> a = A()
        >>> set_state(a, {
        ...     "a": {A: 1}, "b": {A: 2}
        ... })
        >>> a.a
        1
        >>> a.b
        2

    :param obj: Slotted object (metaclass inherits from :class:`slotted.SlottedMeta`).

    :param state: State.
    :type state: dict
    """
    for name, bases in iteritems(state):
        for base, value in iteritems(bases):
            member = base.__dict__[name]
            if isinstance(member, MemberDescriptorType):
                if member.__objclass__ is base and member.__name__ == name:
                    getattr(member, "__set__")(obj, value)


class SlottedMeta(type):
    """
    Enforces usage of '__slots__'.

    Inherits from:
      - :class:`type`
    """

    @staticmethod
    def __new__(
        mcs,  # type: Type[SlottedMeta]
        name,  # type: str
        bases,  # type: Tuple[Type, ...]
        dct,  # type: Dict[str, Any]
    ):
        # type: (...) -> SlottedMeta
        """Make slotted class."""
        for base in bases:
            if isinstance(base.__dict__.get("__dict__"), GetSetDescriptorType):
                error = "base '{}' does not enforce '__slots__'".format(base.__name__)
                raise TypeError(error)
        dct = dict(dct)
        dct["__slots__"] = tuple(dct.get("__slots__", ()))
        return cast(SlottedMeta, super(SlottedMeta, mcs).__new__(mcs, name, bases, dct))

    @property
    def __members__(cls):
        # type: () -> MembersDict
        """
        Get slot members by name and base. Can be used for pickling purposes.

        .. code:: python

            >>> from six import with_metaclass
            >>> from slotted import SlottedMeta

            >>> class A(with_metaclass(SlottedMeta, object)):
            ...     __slots__ = ("a", "b")
            ...
            >>> class B(A):
            ...     __slots__ = ("b", "c")
            ...
            >>> B.__members__ == {
            ...     "a": {A: A.a},
            ...     "b": {A: A.b, B: B.b},
            ...     "c": {B: B.c},
            ... }
            True

        :rtype: dict
        """
        members = {}  # type: MembersDict
        for base in reversed(cls.__mro__):
            if base is cls:
                base_members = scrape_members(cls)
            elif isinstance(base, SlottedMeta):
                base_members = base.__members__
            else:
                base_members = scrape_all_members(base)
            update_members(members, base_members)
        return members


class Slotted(with_metaclass(SlottedMeta, object)):
    """
    Enforces usage of '__slots__' and implements pickling methods based on state.

    Metaclass: :class:`slotted.SlottedABCMeta`

    Inherits from:
      - :class:`object`
    """

    __slots__ = ()  # type: SlotsTuple

    def __getstate__(self):
        # type: () -> StateDict
        """
        Get state for pickling.

        .. code:: python

            >>> from slotted import Slotted

            >>> class A(Slotted):
            ...     __slots__ = ("a", "b")
            ...
            >>> a = A()
            >>> a.a = 1
            >>> a.b = 2
            >>> a.__getstate__() == {
            ...     "a": {A: 1}, "b": {A: 2}
            ... }
            True

        :return: Pickled state.
        :rtype: dict
        """
        return get_state(self)

    def __setstate__(self, state):
        # type: (StateDict) -> None
        """
        Set state for unpickling.

        .. code:: python

            >>> from slotted import Slotted

            >>> class A(Slotted):
            ...     __slots__ = ("a", "b")
            ...
            >>> a = A()
            >>> a.__setstate__({
            ...     "a": {A: 1}, "b": {A: 2}
            ... })
            >>> a.a
            1
            >>> a.b
            2

        :param state: Pickled state.
        :type state: dict
        """
        set_state(self, state)
