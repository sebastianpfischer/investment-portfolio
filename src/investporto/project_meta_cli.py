"""
Investment portfolio
**************************

:module: project_meta_cli

:synopsis: CLI section for the project mamagement

.. currentmodule:: project_meta_cli


:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License

"""

import os
import click
import pyzipper
from pathlib import Path
from shutil import rmtree

from .types_and_vars import PathType, portfolio_plan_name


# Create command
@click.group()
def project_meta():
    """"""
    pass


@project_meta.command("create")
@click.argument(
    "projectname",
    type=click.Path(dir_okay=True, file_okay=True, writable=True, resolve_path=True),
    required=False,
    default="my_finantial_portfolio",
)
def create_project(projectname: PathType):
    """Create a project as folder structure"""
    # Create project
    projectname = Path(projectname)
    projectname.mkdir(parents=True, exist_ok=True)
    # Create portfolio plan (draft)
    with open((projectname / portfolio_plan_name), "w+") as porto_plan:
        porto_plan.write("hello")
    click.echo(f"{projectname} was created...")


@project_meta.command("delete")
@click.argument(
    "projectname",
    type=click.Path(dir_okay=True, file_okay=True, writable=True, resolve_path=True),
    required=False,
    default="my_finantial_portfolio",
)
@click.option("-y", "--yes", is_flag=True, required=False)
def delete_project(projectname: PathType, yes: bool):
    """Delete the project"""
    projectname = Path(projectname)
    # Confirm what the user wants to do
    if not yes:
        if input(f"are you sure you want to delete {projectname}? (y/n)") != "y":
            exit()
    if not (projectname / portfolio_plan_name).is_file():
        click.echo("This seems not to be a supported project!")
        exit(os.EX_USAGE)
    # Delete the project with all it contains
    rmtree(projectname.resolve())
    click.echo(f"{projectname} was definitely deleted...")


@project_meta.command("close")
@click.argument(
    "projectname",
    type=click.Path(dir_okay=True, file_okay=True, writable=True, resolve_path=True),
    required=True,
)
@click.password_option()
def close_project(projectname: PathType, password: str):
    """Create an encrypt zip file out of the project and delete the worked one"""
    projectname = Path(projectname).resolve()
    contents = os.walk(projectname)
    # Zip the project
    with pyzipper.AESZipFile(
        f"{projectname}.zip",
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zip_file:
        zip_file.setpassword(password.encode())
        for root, _, files in contents:
            for file_name in files:
                zip_file.write(
                    (Path(root) / file_name),
                    arcname=(Path(root).relative_to(projectname) / file_name),
                )
    # Delete the unziped project
    rmtree(projectname.resolve())


@project_meta.command("open")
@click.argument(
    "projectname",
    type=click.Path(dir_okay=True, file_okay=True, writable=True, resolve_path=True),
    required=True,
)
@click.password_option()
def open_project(projectname: PathType, password: str):
    """Extract from the zip all the project back to the basic project structur"""
    projectname = Path(projectname).resolve()
    with pyzipper.AESZipFile(
        projectname,
        "r",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zip_file:
        zip_file.setpassword(password.encode())
        zip_file.extractall(path=(projectname.parent / projectname.stem))
    # Delete the unziped project
    Path(projectname).unlink()
