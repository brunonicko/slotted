import pytest
import pickle
import six

import slotted


class Foo(object):
    __slots__ = ("foo",)


class Bar(Foo):
    __slots__ = ("bar",)


class FooBar(Foo):
    __slots__ = ("__foobar",)


class ForcedBarM(six.with_metaclass(slotted.SlottedMeta, Bar)):
    pass


class ForcedBar(Bar, slotted.Slotted):
    pass


class ForcedFooBar(FooBar, slotted.Slotted):
    pass


def test_import():
    from slotted import Slotted, SlottedMeta, slots

    assert all((Slotted, SlottedMeta, slots))


def test_slots():
    assert slotted.slots(Foo) == {"foo"}
    assert slotted.slots(Bar) == {"foo", "bar"}
    for forced_cls in (ForcedBarM, ForcedBar):
        assert hasattr(forced_cls, "__slots__")
        assert slotted.slots(forced_cls) == {"foo", "bar"}

    assert slotted.slots(ForcedFooBar, mangled=True) == {"foo", "_FooBar__foobar"}


def test_non_slotted():
    class NonSlotted:
        pass

    with pytest.raises(TypeError):
        slotted.SlottedMeta("NonSlotted", (NonSlotted,), {})

    with pytest.raises(TypeError):
        slotted.SlottedABCMeta("NonSlotted", (NonSlotted,), {})

    with pytest.raises(TypeError):
        type("NonSlotted", (NonSlotted, slotted.Slotted), {})

    with pytest.raises(TypeError):
        type("NonSlotted", (NonSlotted, slotted.SlottedABC), {})


def test_pickle():
    bar = ForcedBar()
    bar.foo = 1
    bar.bar = 2

    pickled_bar = pickle.loads(pickle.dumps(bar))
    assert pickled_bar.foo == 1
    assert pickled_bar.bar == 2


if __name__ == "__main__":
    pytest.main()
