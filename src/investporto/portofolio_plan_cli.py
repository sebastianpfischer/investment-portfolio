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
@click.argument("name", type=click.STRING, required=True, default="stocks")
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
@click.argument("name", type=click.STRING, required=True, default="stocks")
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
def create_subtype_of_investment(name: str, percentage: float):
    """Add new asset type (Stocks, ETFs, Bonds, ...)"""
    click.echo(f"{name} with {percentage}% was added...")
