# -*- coding: utf-8 -*-
"""Enforces usage of '__slots__' for python classes."""

from ._abc import (
    SlottedABC,
    SlottedABCMeta,
    SlottedCallable,
    SlottedContainer,
    SlottedHashable,
    SlottedItemsView,
    SlottedIterable,
    SlottedIterator,
    SlottedKeysView,
    SlottedMapping,
    SlottedMappingView,
    SlottedMutableMapping,
    SlottedMutableSequence,
    SlottedMutableSet,
    SlottedSequence,
    SlottedSet,
    SlottedSized,
    SlottedValuesView,
)
from ._bases import Slotted, SlottedMeta, get_state, set_state

__all__ = [
    "get_state",
    "set_state",
    "SlottedMeta",
    "Slotted",
    "SlottedABC",
    "SlottedABCMeta",
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
