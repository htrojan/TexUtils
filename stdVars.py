"""
This file defines a global unit registry that can be imported everywhere.
Two unit registries defined separately do not work together and can not recognize each others units
"""
import pint

ureg = pint.UnitRegistry()
