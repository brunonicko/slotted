# -*- coding: utf-8 -*-
"""Enforces usage of '__slots__' for python classes."""

from ._abc import __all__ as _collections_all

__all__ = ["get_state", "set_state", "SlottedMeta", "Slotted"] + _collections_all
