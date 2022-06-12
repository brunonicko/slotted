import pytest

import slotted


class Foo:
    __slots__ = ("foo",)


class Bar(Foo):
    __slots__ = ("bar",)


class ForcedBarM(Bar, metaclass=slotted.SlottedMeta):
    pass


class ForcedBar(Bar, slotted.Slotted):
    pass


class ForcedBarABCM(ForcedBarM, metaclass=slotted.SlottedABCMeta):
    pass


class ForcedBarABC(ForcedBar, slotted.SlottedABC):
    pass


def test_slots():
    assert slotted.slots(Foo) == {"foo"}
    assert slotted.slots(Bar) == {"foo", "bar"}
    for forced_cls in (ForcedBarM, ForcedBar, ForcedBarABCM, ForcedBarABC):
        assert hasattr(forced_cls, "__slots__")
        assert slotted.slots(forced_cls) == {"foo", "bar"}


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


if __name__ == "__main__":
    pytest.main()
