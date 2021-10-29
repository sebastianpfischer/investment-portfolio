"""
Define some recurring typing definitions
"""

import typing
import pathlib

# Types
PathType = typing.Union[str, pathlib.Path]

# Vars
portfolio_plan_name = pathlib.Path("porto_plan.yaml")
