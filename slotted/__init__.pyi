# -*- coding: utf-8 -*-
"""Package stub file."""

from abc import ABC, ABCMeta
from typing import (
    AbstractSet,
    Any,
    Callable,
    Container,
    Dict,
    Hashable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MappingView,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Sized,
    Type,
    ValuesView,
)

__all__ = [
    "get_state",
    "set_state",
    "SlottedMeta",
    "Slotted",
    "SlottedABCMeta",
    "SlottedABC",
    "SlottedCallable",
    "SlottedContainer",
    "SlottedHashable",
    "SlottedItemsView",
    "SlottedIterable",
    "SlottedIterator",
    "SlottedKeysView",
    "SlottedMapping",
    "SlottedMappingView",
    "SlottedMutableMapping",
    "SlottedMutableSequence",
    "SlottedMutableSet",
    "SlottedSequence",
    "SlottedSet",
    "SlottedSized",
    "SlottedValuesView",
]

def get_state(obj):  # type: (Slotted) -> Dict[str, Dict[Type, Any]]
    pass

def set_state(obj, state):  # type: (Slotted, Dict[str, Dict[Type, Any]]) -> None
    pass

class SlottedMeta(type):
    pass

class Slotted(metaclass=SlottedMeta):
    pass

class SlottedABCMeta(SlottedMeta, ABCMeta):
    pass

class SlottedABC(Slotted, ABC, metaclass=SlottedABCMeta):
    pass

SlottedCallable = Callable

class SlottedContainer(Container, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedHashable(Hashable, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedItemsView(ItemsView, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedIterable(Iterable, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedIterator(Iterator, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedKeysView(KeysView, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedMapping(Mapping, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedMappingView(MappingView, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedMutableMapping(MutableMapping, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedMutableSequence(MutableSequence, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedMutableSet(MutableSet, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedSequence(Sequence, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedSet(AbstractSet, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedSized(Sized, SlottedABC, metaclass=ABCMeta):
    pass

class SlottedValuesView(ValuesView, SlottedABC, metaclass=ABCMeta):
    pass
