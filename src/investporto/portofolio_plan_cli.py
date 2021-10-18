"""
Investment portfolio
**************************

:module: portofolio_plan_cli

:synopsis: Entry point to the tool

.. currentmodule:: portofolio_plan_cli


:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License

"""

import click

from .types_and_vars import portofolio_plan_name


#  Create the portofolio plan
@click.group()
def portofolio_plan():
    """"""
    pass


@portofolio_plan.command("add-asset-type")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@click.option(
    "-p",
    "--percentage",
    type=click.FLOAT,
    required=True,
    help="Percentage you want to invest in.",
)
def create_type_of_investment(name: str, percentage: float):
    """Add new asset type (Stocks, ETFs, Bonds, ...)"""
    click.echo(
        f"{portofolio_plan_name}, \
               {name} with {percentage}% was added..."
    )


@portofolio_plan.command("add-asset-subtype")
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
    """Add new asset type (Large Caps, Mid Caps, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
    # Normalized the naming in lower cap


@portofolio_plan.command("remove-asset-type")
@click.argument("name", type=click.STRING, required=True, default="Stocks")
@click.option(
    "-p",
    "--percentage",
    type=click.FLOAT,
    required=True,
    help="Percentage you want to invest in.",
)
def remove_type_of_investment(name: str, percentage: float):
    """Add new asset type (Stocks, ETFs, Bonds, ...)"""
    click.echo(
        f"{portofolio_plan_name}, \
               {name} with {percentage}% was added..."
    )


@portofolio_plan.command("remove-asset-subtype")
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
    """Add new asset type (Large Caps, Mid Caps, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
    # Normalized the naming in lower cap


@portofolio_plan.command("assign-budget")
@click.argument("budget", type=click.FLOAT, required=True, default=0)
def assign_budget(budget: float):
    """Assign a budget to the portofolio"""
    click.echo(f"{budget} was assign to the project!")


@portofolio_plan.command("verify-allocation")
def verify_allocation():
    """Verify if the allocation reach really the 100% per type
    and the same per subtype"""
    click.echo("Will soon be available!")


@portofolio_plan.command("visualize-allocation")
def visualize_allocation():
    """Visualize the project allocation"""
    click.echo("Will soon be available!")
