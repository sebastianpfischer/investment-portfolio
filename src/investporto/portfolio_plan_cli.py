"""
Investment portfolio
**************************

:module: portfolio_plan_cli_tree

:synopsis: CLI section for portfolio configuration (resolved with tree)

.. currentmodule:: portfolio_plan_cli_tree


:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License

"""

import click
import os

from .types_and_vars import portfolio_plan_name
from typing import Optional
from pathlib import Path
import yaml
from anytree.importer import DictImporter
from anytree.exporter import DictExporter
from anytree import Node, RenderTree
from anytree.resolver import Resolver, ChildResolverError


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
        help="Amount you want to invest in.",
    )(function)
    return function


class Portfolio:
    """Manage the portfolio plan you define"""

    def __init__(self, path_to_yaml: Path):
        """open the yaml file and store the config"""
        self._path_to_yaml = path_to_yaml
        self._plan = {}
        self.tree = None
        pass

    def open(self):
        self.__enter__()

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        with open(self._path_to_yaml, "r") as portfolio_plan_file:
            # Load the yaml into a dict
            dict_plan = yaml.load(portfolio_plan_file, Loader=yaml.SafeLoader)
            if dict_plan:
                # Transform the dict into a tree
                importer = DictImporter()
                self._plan = importer.import_(dict_plan)
                # if yaml file is empty, instead of None, provide an empty dict
                # for consistency
            else:
                self._plan = Node("entry")
        # If the open was successful, return us
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        # If the received values are different to None, an error occurred!
        if exc_type != exc != exc_tb != None:
            click.echo(f"Error occurred: {exc_type}, {exc}, {exc_tb}")
        # No, error found, we try to save the configuration
        with open(self._path_to_yaml, "w") as portfolio_plan_file:
            # Convert tree to dict
            exporter = DictExporter()
            yaml.dump(
                exporter.export(self._plan),
                portfolio_plan_file,
                default_flow_style=False,
            )

    def add(
        self,
        asset_class_name: str,
        percentage: Optional[float] = None,
        asset_class_allocation_name: str = "",
        allocation_percentage: Optional[float] = None,
    ):
        # Set the assets to lowercase (to minimize typos)
        asset_class_name = asset_class_name.lower()
        asset_class_allocation_name = asset_class_allocation_name.lower()

        def allocate(name: str, parent: Node, percentage: float):
            asset = None
            for node in parent.children:
                if node.name == name:
                    asset = node
            if not percentage and asset:
                # Case where percentage was not given
                return asset
            elif not (0.0 < percentage <= 100.0):
                # Not allowed case
                raise TypeError(f" percentage = {percentage} is not allowed")
            if not asset:
                asset = Node(name, parent, percentage=percentage)
                print(f"{name} was allocated")
            elif asset.percentage != percentage:
                print(
                    f"{name} percentage updated from {asset.percentage} to {percentage}"
                )
                asset.percentage = percentage
            return asset

        # Allocate assets
        asset_class = None
        if asset_class_name:
            asset_class = allocate(asset_class_name, self._plan, percentage)
        if asset_class_allocation_name and asset_class:
            _ = allocate(
                asset_class_allocation_name, asset_class, allocation_percentage
            )

    def remove(self, asset_class_name: str, asset_class_allocation_name: str = ""):
        # Set the assets to lowercase (to minimize typos)
        asset_class_name = asset_class_name.lower()
        asset_class_allocation_name = asset_class_allocation_name.lower()
        # Create resolver
        resolver = Resolver("name")
        # Case 1: only asset class was given
        if asset_class_name and not asset_class_allocation_name:
            try:
                asset: Node = resolver.get(self._plan, asset_class_name)
                asset.parent = None
                print(f"{asset_class_name} was successfully deleted")
            except ChildResolverError:
                print(f"{asset_class_name} was not found!")
        # Case 2: allocation was also provided
        elif asset_class_name and asset_class_allocation_name:
            try:
                asset: Node = resolver.get(
                    self._plan, asset_class_name + "/" + asset_class_allocation_name
                )
                asset.parent = None
                print(f"{asset_class_allocation_name} was successfully deleted")
            except ChildResolverError:
                print(f"{asset_class_allocation_name} was not found!")

    def check_allocation(self):
        # We will check that each children contain the right percentage
        def pre_order_verification(node: Node):
            # Return in case of no children
            if not node.children:
                return
            # calculate percentage of the children
            total = 0.0
            for child in node.children:
                total += child.percentage
            if total == 100.0:
                node.allocation_check = "-> ok!"
            else:
                node.allocation_check = "-> allocation error!"
            # Proceed with the kids
            for child in node.children:
                pre_order_verification(child)

        # Apply pre-order-verification
        pre_order_verification(self._plan)
        # Render
        for pre, _, node in RenderTree(self._plan):
            if hasattr(node, "allocation_check"):
                print(f"{pre}{node.name} {node.allocation_check}")
            else:
                continue

    def visualize_allocation(self):
        for pre, _, node in RenderTree(self._plan):
            if hasattr(node, "percentage"):
                print(f"{pre}( {node.name} , {node.percentage} )")
            else:
                print(f"{pre}{node.name}")

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
