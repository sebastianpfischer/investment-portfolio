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
        pass

    def open(self):
        self.__enter__()

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        with open(self._path_to_yaml, "r") as portfolio_plan_file:
            self._plan = yaml.load(portfolio_plan_file, Loader=yaml.SafeLoader)
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
        self, dict_to_update: dict, dict_to_update_with: dict, *, delete: bool = False
    ):
        for key, value in dict_to_update_with.items():
            if isinstance(value, collections.abc.Mapping):
                # If value is a dict, we have to have a recursion
                dict_to_update[key] = self._update_dict(
                    dict_to_update.get(key, {}), value, delete=delete
                )
            else:
                if not delete:
                    dict_to_update[key] = value
                else:
                    del dict_to_update[key]
        return dict_to_update

    def add(
        self,
        asset_type: str,
        percentage: float = 0,
        asset_subtype: str = "",
        subpercentage: float = 0,
    ):
        element_to_add = None
        # Set the assets to lowercase (to minimize typos)
        asset_type = asset_type.lower()
        asset_subtype = asset_subtype.lower()
        # Separate in 2 cases with prio:
        # 1 - type was given
        # 2 - subtype was given
        if asset_subtype:
            element_to_add = {
                asset_type: {"subtypes": {asset_subtype: {"percentage": subpercentage}}}
            }
        elif asset_type:
            element_to_add = {asset_type: {"percentage": percentage}}
        # If none of the above cases was valid, we raise an error
        if element_to_add:
            self._update_dict(self._plan, element_to_add)
        else:
            raise IOError

    def delete(self, asset_type: str, asset_subtype: str = ""):
        element_to_delete = None
        # Set the assets to lowercase (to minimize typos)
        asset_type = asset_type.lower()
        asset_subtype = asset_subtype.lower()
        # Separate in 2 cases with prio:
        # 1 - type was given
        # 2 - subtype was given
        if asset_subtype:
            element_to_delete = {asset_type: {"subtypes": {asset_subtype: None}}}
        elif asset_type:
            element_to_delete = {asset_type: None}
        # If none of the above cases was valid, we raise an error
        if element_to_delete:
            self._update_dict(self._plan, element_to_delete, delete=True)
        else:
            raise IOError

    def __str__(self) -> str:
        return f"{self._plan}"

    def __repr__(self) -> str:
        print(f"{self._plan}")
        return self.__str__()


@portfolio_plan.command("add-asset-type")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@percentage_option
@project_path_option
def create_type_of_investment(name: str, percentage: float, projet_path: str):
    """Add new asset type (Stocks, ETFs, Bonds, ...)"""
    # Load the configuration stored in the yaml file
    try:
        with Portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
            ppn.add(asset_type=name, percentage=percentage)
            click.echo(ppn)
    except OSError:
        # Exception to be better defined later on
        click.echo("Oups, something went really wrong with close!")
        exit(os.EX_OSERR)


@portfolio_plan.command("add-asset-subtype")
@click.argument("name", type=click.STRING, required=True, default="Large Caps")
@percentage_option
@project_path_option
@click.option(
    "-t",
    "--type",
    type=click.STRING,
    required=True,
    default="Stocks",
    help="Type to allocate the subtype",
)
def create_subtype_of_investment(name: str, percentage: float, projet_path: str):
    """Add new asset subtype (Large Caps, Mid Caps, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
    # Normalized the naming in lower cap


@portfolio_plan.command("remove-asset-type")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@percentage_option
@project_path_option
def remove_type_of_investment(name: str, percentage: float, projet_path: str):
    """Remove new asset type (Stocks, ETFs, Bonds, ...)"""
    click.echo(
        f"{portfolio_plan_name}, \
               {name} with {percentage}% was added..."
    )


@portfolio_plan.command("remove-asset-subtype")
@click.argument("name", type=click.STRING, required=True, default="Large Caps")
@percentage_option
@project_path_option
@click.option(
    "-t",
    "--type",
    type=click.STRING,
    required=True,
    help="Type to allocate the subtype",
)
def remove_subtype_of_investment(name: str, percentage: float, projet_path: str):
    """Remove asset subtype (Large Caps, Mid Caps, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
    # Normalized the naming in lower cap


@portfolio_plan.command("assign-budget")
@click.argument("budget", type=click.FLOAT, required=True, default=0)
@project_path_option
def assign_budget(budget: float, projet_path: str):
    """Assign a budget to the portfolio"""
    click.echo(f"{budget} was assign to the project!")


@portfolio_plan.command("verify-allocation")
@project_path_option
def verify_allocation(projet_path: str):
    """Verify if the allocation reach really the 100% per type
    and the same per subtype"""
    click.echo("Will soon be available!")


@portfolio_plan.command("visualize-allocation")
@project_path_option
def visualize_allocation(projet_path: str):
    """Visualize the project allocation"""
    click.echo("Will soon be available!")
