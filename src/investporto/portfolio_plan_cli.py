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


#  Create the portfolio plan
@click.group()
def portfolio_plan():
    """"""
    pass


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
        self.__exit__()

    def __enter__(self):
        try:
            with open(self._path_to_yaml, "r") as portfolio_plan_file:
                self._plan = yaml.load(portfolio_plan_file, Loader=yaml.SafeLoader)
            # If the open was successful, return us
            return self
        except OSError:
            # Exception to be better defined later on
            click.echo("Oups, something went really wrong!")

    def __exit__(self, exc_type, exc, exc_tb):
        # If the received values are different to None, an error occurred!
        if exc_type != exc != exc_tb != None:
            click.echo(f"Error occure: {exc_type}, {exc}, {exc_tb}")
            exit(os.EX_IOERR)
        # No, error found, we try to save the configuration
        try:
            with open(self._path_to_yaml, "w") as portfolio_plan_file:
                yaml.dump(self._plan, portfolio_plan_file, default_flow_style=False)
        except OSError:
            # Exception to be better defined later on
            click.echo("Oups, something went really wrong!")

    def add(
        self,
        asset_type: str,
        percentage: float = 0,
        asset_subtype: str = "",
        subpercentage: float = 0,
    ):
        raise NotImplementedError

    def delete(
        self,
        asset_type: str,
        percentage: float = 0,
        asset_subtype: str = "",
        subpercentage: float = 0,
    ):
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self._plan}"

    def __repr__(self) -> str:
        print(f"{self._plan}")
        return self.__str__()


@portfolio_plan.command("add-asset-type")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@click.option(
    "-p",
    "--percentage",
    type=click.FLOAT,
    required=True,
    help="Percentage you want to invest in.",
)
@click.option(
    "-pp",
    "--projet_path",
    type=click.Path(dir_okay=True, file_okay=False, writable=True, resolve_path=True),
    required=False,
    help="with to the project",
)
def create_type_of_investment(name: str, percentage: float, projet_path: str):
    """Add new asset type (Stocks, ETFs, Bonds, ...)"""
    # Load the configuration stored in the yaml file
    with portfolio(Path(projet_path / portfolio_plan_name).resolve()) as ppn:
        click.echo(ppn)


@portfolio_plan.command("add-asset-subtype")
@click.argument("name", type=click.STRING, required=True, default="Large Caps")
@click.option(
    "-t",
    "--type",
    type=click.STRING,
    required=True,
    default="Stocks",
    help="Type to allocate the subtype",
)
@click.option(
    "-p",
    "--percentage",
    type=click.FLOAT,
    required=True,
    help="Percentage you want to invest in.",
)
def create_subtype_of_investment(name: str, percentage: float):
    """Add new asset subtype (Large Caps, Mid Caps, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
    # Normalized the naming in lower cap


@portfolio_plan.command("remove-asset-type")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@click.option(
    "-p",
    "--percentage",
    type=click.FLOAT,
    required=True,
    help="Percentage you want to invest in.",
)
def remove_type_of_investment(name: str, percentage: float):
    """Remove new asset type (Stocks, ETFs, Bonds, ...)"""
    click.echo(
        f"{portfolio_plan_name}, \
               {name} with {percentage}% was added..."
    )


@portfolio_plan.command("remove-asset-subtype")
@click.argument("name", type=click.STRING, required=True, default="Large Caps")
@click.option(
    "-t",
    "--type",
    type=click.STRING,
    required=True,
    help="Type to allocate the subtype",
)
@click.option(
    "-p",
    "--percentage",
    type=click.FLOAT,
    required=True,
    help="Percentage you want to invest in.",
)
def remove_subtype_of_investment(name: str, percentage: float):
    """Remove asset subtype (Large Caps, Mid Caps, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
    # Normalized the naming in lower cap


@portfolio_plan.command("assign-budget")
@click.argument("budget", type=click.FLOAT, required=True, default=0)
def assign_budget(budget: float):
    """Assign a budget to the portfolio"""
    click.echo(f"{budget} was assign to the project!")


@portfolio_plan.command("verify-allocation")
def verify_allocation():
    """Verify if the allocation reach really the 100% per type
    and the same per subtype"""
    click.echo("Will soon be available!")


@portfolio_plan.command("visualize-allocation")
def visualize_allocation():
    """Visualize the project allocation"""
    click.echo("Will soon be available!")