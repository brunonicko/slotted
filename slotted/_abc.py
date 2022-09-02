import abc
import tippo
import six
import types

try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc  # type: ignore

from tippo import Any, Generic, Dict, List, Set, Tuple, Type, Union
from basicco.generic_meta import GenericMeta
from basicco.mangling import mangle

from ._slotted import Slotted, SlottedMeta

__all__ = [
    "SlottedABCMeta",
    "SlottedABCGenericMeta",
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
    "SlottedCollection",
]

_ABC_ALL = [
    "ABCMeta",
    "Callable",
    "Container",
    "Hashable",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "Mapping",
    "MappingView",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "Sequence",
    "Set",
    "Sized",
    "ValuesView",
]

_ABC_GENERIC = [
    # "Callable",
    "Container",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "Mapping",
    "MappingView",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "Sequence",
    "Set",
    "ValuesView",
]


SlottedCallable = tippo.Callable
SlottedContainer = tippo.Container
SlottedHashable = tippo.Hashable
SlottedItemsView = tippo.ItemsView
SlottedIterable = tippo.Iterable
SlottedIterator = tippo.Iterator
SlottedKeysView = tippo.KeysView
SlottedMapping = tippo.Mapping
SlottedMappingView = tippo.MappingView
SlottedMutableMapping = tippo.MutableMapping
SlottedMutableSequence = tippo.MutableSequence
SlottedMutableSet = tippo.MutableSet
SlottedSequence = tippo.Sequence
SlottedSet = tippo.AbstractSet
SlottedSized = tippo.Sized
SlottedValuesView = tippo.ValuesView


# Try to get 'Collection' if it's available.
try:
    SlottedCollection = collections_abc.Collection
except AttributeError:
    SlottedCollection = None  # type: ignore
else:
    _ABC_ALL.append("Collection")


class SlottedABCMeta(SlottedMeta, abc.ABCMeta):
    """Slotted version of :class:`abc.ABCMeta`."""


if GenericMeta is type:
    SlottedABCGenericMeta = SlottedABCMeta

else:

    class SlottedABCGenericMeta(GenericMeta, SlottedABCMeta):  # type: ignore
        """Slotted version of :class:`typing.GenericMeta`."""


class SlottedABC(six.with_metaclass(SlottedABCMeta, Slotted)):
    """Slotted version of :class:`abc.ABC`."""


# Register 'SlottedABC' as a subclass of 'ABC' if possible.
try:
    from abc import ABC
except ImportError:
    ABC = None  # type: ignore
else:
    ABC.register(SlottedABC)  # type: ignore


_CLASSES = set()  # type: Set[Type]
for cls_name in _ABC_ALL:
    try:
        cls = getattr(collections_abc, cls_name)
    except AttributeError:
        continue
    if not isinstance(cls, abc.ABCMeta) or not issubclass(cls, object):
        continue
    _CLASSES.add(cls)

_CACHE = {
    object: SlottedABC,
    abc.ABCMeta: SlottedABCMeta,
}  # type: Dict[Type[Any], Union[SlottedABCMeta, Type[SlottedABCMeta]]]


def extract_dict(base):
    # type: (Type) -> Tuple[Dict[str, Any], Dict[str, Any]]
    slots = set(mangle(slot, base.__name__) for slot in getattr(base, "__slots__", ()))
    base_dict = {}
    overrides = {}
    for name, value in six.iteritems(base.__dict__):
        if name in slots:
            if isinstance(value, types.MemberDescriptorType):
                if value.__objclass__ is base and value.__name__ == name:
                    continue
            overrides[name] = value
        else:
            base_dict[name] = value
    return base_dict, overrides


def convert_meta(source):
    # type: (Type) -> Type
    """Convert an ABCMeta-based metaclass to a SlottedABCMeta-based metaclass."""
    try:
        return _CACHE[source]
    except KeyError:
        pass

    target_bases_list = []  # type: List[Union[SlottedABCMeta, Type[SlottedABCMeta]]]
    for source_base in source.__bases__:
        target_bases_list.append(tippo.cast(SlottedABCMeta, convert_meta(source_base)))

    source_name = source.__name__
    target_name = "Slotted{}".format(source_name)
    target_bases = tuple(target_bases_list)
    target_dct, overrides = extract_dict(source)
    target_dct["__module__"] = __name__
    target_dct["__doc__"] = "".join(
        (
            "Slotted version of :class:`{}.{}`.".format(source.__module__, source.__name__),
            "\n\n",
            "Inherits from:\n",
            "\n".join(
                "  - :class:`{}.{}`".format(
                    b.__module__.replace("slotted._abc", "slotted").replace("slotted._bases", "slotted"),
                    b.__name__,
                )
                for b in target_bases
            ),
        )
    )

    if hasattr(types, "new_class"):

        def exec_body(ns):
            for k, v in six.iteritems(target_dct):
                ns[k] = v
            return ns

        target = tippo.cast(
            "SlottedABCMeta",
            types.new_class(target_name, target_bases, {"metaclass": SlottedABCMeta}, exec_body),
        )
    else:
        target = SlottedABCMeta(target_name, target_bases, target_dct)

    for name, value in six.iteritems(overrides):
        type.__setattr__(tippo.cast(type, target), name, value)
    _CACHE[source] = target

    return target


def convert(source):
    # type: (abc.ABCMeta) -> Union[SlottedABCMeta, Type[SlottedABCMeta]]
    """Convert an ABC-based class to an SlottedABC-based class."""
    try:
        return _CACHE[source]
    except KeyError:
        pass

    meta = convert_meta(type(source))

    target_bases_list = []  # type: List[Union[SlottedABCMeta, Type[SlottedABCMeta]]]
    for source_base in source.__bases__:
        target_bases_list.append(convert(tippo.cast(abc.ABCMeta, source_base)))

    source_name = source.__name__
    target_name = "Slotted{}".format(source_name)
    target_bases = tuple(target_bases_list)
    target_dct, overrides = extract_dict(source)
    target_dct.pop("__dict__", None)
    target_dct["__module__"] = __name__
    target_dct["__doc__"] = "".join(
        (
            "Slotted version of :class:`{}.{}`.".format(source.__module__, source.__name__),
            "\n\n",
            (
                ".. note::\n"
                "   This class is not available in some older versions of Python. "
                "   When that's the case, `{}` will be set to `None`."
                "\n\n"
            ).format(target_name)
            if source_name == "Collection"
            else "",
            "Metaclass: :class:`slotted.SlottedABCMeta`",
            "\n\n",
            "Inherits from:\n",
            "\n".join(
                "  - :class:`{}.{}`".format(
                    b.__module__.replace("slotted._abc", "slotted").replace("slotted._bases", "slotted"),
                    b.__name__,
                )
                for b in target_bases
            ),
        )
    )

    if hasattr(types, "new_class"):

        def exec_body(ns):
            for k, v in six.iteritems(target_dct):
                ns[k] = v
            return ns

        target = types.new_class(target_name, target_bases, {"metaclass": meta}, exec_body)
    else:
        target = meta(target_name, target_bases, target_dct)

    for name, value in six.iteritems(overrides):
        type.__setattr__(target, name, value)
    _CACHE[source] = target

    if target.__dict__.get("__dict__") is not None:
        error = "class {!r} has a '__dict__'".format(target_name)
        raise AssertionError(error)

    source.register(target)
    return target


# Convert all classes.
for original in _CLASSES:
    converted = convert(tippo.cast(abc.ABCMeta, original))
    globals()[converted.__name__] = converted


_CONVERTED_CLASSES = {o: c for o, c in six.iteritems(_CACHE) if not issubclass(o, type)}  # type: Dict[Type, Type]
for original, converted in _CONVERTED_CLASSES.items():
    assert not issubclass(converted, type)

    # Skip unsupported for now.
    if original.__name__ not in _ABC_GENERIC:
        continue

    # Skip if already generic.
    if (
        hasattr(tippo, "GenericMeta")
        and isinstance(converted, getattr(tippo, "GenericMeta"))
        or hasattr(converted, "__class_getitem__")
        or hasattr(type(converted), "__getitem__")
    ):
        continue

    # Convert to generic.
    generic_original = getattr(tippo, original.__name__)
    if hasattr(generic_original, "__parameters__"):
        parameters = generic_original.__parameters__
        new_class_args = (
            converted.__name__,
            (
                six.with_metaclass(
                    SlottedABCGenericMeta,
                    converted,
                    Generic[parameters],  # type: ignore
                ),
            ),
        )  # type: ignore

        if hasattr(types, "new_class"):
            generic_converted = types.new_class(*new_class_args)  # type: ignore
        else:
            new_class_args += ({},)  # type: ignore
            generic_converted = type(*new_class_args)  # type: ignore

        # Replace class.
        globals()[converted.__name__] = generic_converted
