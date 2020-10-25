from typing import (
    Callable,
    Container,
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
    Set,
    Sized,
    ValuesView,
)

__all__ = [
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


class SlottedCallable(Callable):
    pass


class SlottedContainer(Container):
    pass


class SlottedHashable(Hashable):
    pass


class SlottedItemsView(ItemsView):
    pass


class SlottedIterable(Iterable):
    pass


class SlottedIterator(Iterator):
    pass


class SlottedKeysView(KeysView):
    pass


class SlottedMapping(Mapping):
    pass


class SlottedMappingView(MappingView):
    pass


class SlottedMutableMapping(MutableMapping):
    pass


class SlottedMutableSequence(MutableSequence):
    pass


class SlottedMutableSet(MutableSet):
    pass


class SlottedSequence(Sequence):
    pass


class SlottedSet(Set):
    pass


class SlottedSized(Sized):
    pass


class SlottedValuesView(ValuesView):
    pass
