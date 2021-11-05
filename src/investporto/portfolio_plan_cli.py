"""
Investment portfolio
**************************

:module: portfolio_plan_cli

:synopsis: CLI section for portfolio configuration

.. currentmodule:: portfolio_plan_cli


:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License

"""

import click
import os

from .types_and_vars import portfolio_plan_name
from pathlib import Path
import yaml
import collections.abc
import pandas as pd


#  Create the portfolio plan
@click.group()
def portfolio_plan():
    """"""
    pass


def project_path_option(function):
    """Define the common project path option"""
    function = click.option(
        "-pp",
        "--projet_path",
        type=click.Path(
            dir_okay=True, file_okay=False, writable=True, resolve_path=True
        ),
        required=False,
        help="Path to the project",
    )(function)
    return function


def percentage_option(function):
    """Define the common percentage option"""
    function = click.option(
        "-p",
        "--percentage",
        type=click.FLOAT,
        required=True,
        help="Percentage you want to invest in.",
    )(function)
    return function


class Portfolio:
    """Manage the portfolio plan you define"""

    def __init__(self, path_to_yaml: Path):
        """open the yaml file and store the config"""
        self._path_to_yaml = path_to_yaml
        self._plan = {}
        self.dataframe = None
        pass

    def open(self):
        self.__enter__()

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        with open(self._path_to_yaml, "r") as portfolio_plan_file:
            self._plan = yaml.load(portfolio_plan_file, Loader=yaml.SafeLoader)
            # if yaml file is empty, instead of None, provide an empty dict
            # for consistency
            if not self._plan:
                self._plan = {}
        # If the open was successful, return us
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        # If the received values are different to None, an error occurred!
        if exc_type != exc != exc_tb != None:
            click.echo(f"Error occure: {exc_type}, {exc}, {exc_tb}")
        # No, error found, we try to save the configuration
        with open(self._path_to_yaml, "w") as portfolio_plan_file:
            yaml.dump(self._plan, portfolio_plan_file, default_flow_style=False)

    def _update_dict(
        self, dict_to_update: dict, dict_to_update_with: dict, *, remove: bool = False
    ):
        """Update the configuration with the request

        .. warning::
            This algorithm is not smart and cannot detect today if the elements
            to add or delete already exist in the dict_to_update.
        """
        for key, value in dict_to_update_with.items():
            if isinstance(value, collections.abc.Mapping):
                # If value is a dict, we have to have a recursion
                dict_to_update[key] = self._update_dict(
                    dict_to_update.get(key, {}), value, remove=remove
                )
            else:
                if not remove:
                    dict_to_update[key] = value
                else:
                    del dict_to_update[key]
        return dict_to_update

    def update_dict(self, dict_to_update_with: dict, *, remove: bool = False):
        """Update the current configuration with a provided dict"""
        return self._update_dict(self._plan, dict_to_update_with, remove=remove)

    def add(
        self,
        asset_class: str,
        percentage: float = 0,
        asset_subclass: str = "",
        subpercentage: float = 0,
    ):
        element_to_add = None
        # Set the assets to lowercase (to minimize typos)
        asset_class = asset_class.lower()
        asset_subclass = asset_subclass.lower()
        # Separate in 2 cases with prio:
        # 1 - class was given
        # 2 - subclass was given
        if asset_subclass:
            element_to_add = {
                asset_class: {
                    "subclasss": {asset_subclass: {"percentage": subpercentage}}
                }
            }
        elif asset_class:
            element_to_add = {asset_class: {"percentage": percentage}}
        # If none of the above cases was valid, we raise an error
        if element_to_add:
            self._update_dict(self._plan, element_to_add)
        else:
            raise IOError

    def remove(self, asset_class: str, asset_subclass: str = ""):
        element_to_remove = None
        # Set the assets to lowercase (to minimize typos)
        asset_class = asset_class.lower()
        asset_subclass = asset_subclass.lower()
        # Separate in 2 cases with prio:
        # 1 - class was given
        # 2 - subclass was given
        if asset_subclass:
            element_to_remove = {asset_class: {"subclasss": {asset_subclass: None}}}
        elif asset_class:
            element_to_remove = {asset_class: None}
        # If none of the above cases was valid, we raise an error
        if element_to_remove:
            self._update_dict(self._plan, element_to_remove, remove=True)
        else:
            raise IOError

    def load_dataframe(self):
        """The idea is to reduce load if we do not manipulate the frame"""
        if self._plan:
            self.dataframe = pd.DataFrame.from_dict(self._plan)

    def check_allocation(self):
        pass

    def visualize_allocation(self):
        return repr(self.dataframe)

    def __str__(self) -> str:
        return f"{self._plan}"

    def __repr__(self) -> str:
        return self.__str__()


@portfolio_plan.command("add-asset-class")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@percentage_option
@project_path_option
def create_class_of_investment(name: str, percentage: float, projet_path: str):
    """Add new asset class (Stocks, ETFs, Bonds, ...)"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.add(asset_class=name, percentage=percentage)
            click.echo(ppn)
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with the config access!")
        exit(os.EX_OSERR)


@portfolio_plan.command("add-asset-subclass")
@click.argument("name", type=click.STRING, required=True, default="Large Caps")
@percentage_option
@project_path_option
@click.option(
    "-ac",
    "--asset-class",
    type=click.STRING,
    required=True,
    default="Stocks",
    help="Class to allocate the subclass",
)
def create_subclass_of_investment(
    name: str, percentage: float, projet_path: str, asset_class: str
):
    """Add new asset subclass (Large Caps, Mid Caps, ...)"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.add(
                asset_class=asset_class, asset_subclass=name, subpercentage=percentage
            )
            click.echo(ppn)
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with the config access!")
        exit(os.EX_OSERR)


@portfolio_plan.command("remove-asset-class")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@percentage_option
@project_path_option
def remove_class_of_investment(name: str, percentage: float, projet_path: str):
    """Remove new asset class (Stocks, ETFs, Bonds, ...)"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.remove(asset_class=name)
            click.echo(ppn)
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with the config access!")
        exit(os.EX_OSERR)


@portfolio_plan.command("remove-asset-subclass")
@click.argument("name", type=click.STRING, required=True, default="Large Caps")
@percentage_option
@project_path_option
@click.option(
    "-ac",
    "--asset-class",
    type=click.STRING,
    required=True,
    help="Class to allocate the subclass",
)
def remove_subclass_of_investment(
    name: str, percentage: float, projet_path: str, asset_class: str
):
    """Remove asset subclass (Large Caps, Mid Caps, ...)"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.remove(asset_class=asset_class, asset_subclass=name)
            click.echo(ppn)
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with the config access!")
        exit(os.EX_OSERR)


@portfolio_plan.command("assign-budget")
@click.argument("budget", type=click.FLOAT, required=True, default=0)
@project_path_option
def assign_budget(budget: float, projet_path: str):
    """Assign a budget to the portfolio"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.update_dict({"budget": budget})
            click.echo(ppn)
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with the config access!")
        exit(os.EX_OSERR)


@portfolio_plan.command("verify-allocation")
@project_path_option
def verify_allocation(projet_path: str):
    """Verify if the allocation reach really the 100% per class
    and the same per subclass"""
    click.echo("Will soon be available!")


@portfolio_plan.command("visualize-allocation")
@project_path_option
def visualize_allocation(projet_path: str):
    """Visualize the project allocation"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.load_dataframe()
            click.echo(ppn.visualize_allocation())
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with the config access!")
        exit(os.EX_OSERR)
