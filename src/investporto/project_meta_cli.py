"""
Investment portfolio
**************************

:module: project_meta_cli

:synopsis: Entry point to the tool

.. currentmodule:: project_meta_cli


:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License

"""

import pathlib
import click

from .types_and_vars import PathType, portofolio_plan_name


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
    default="my_finantial_portofolio",
)
def create(projectname: PathType):
    """Create a project as folder structure"""
    # Create project
    projectname = pathlib.Path(projectname)
    projectname.mkdir(parents=True, exist_ok=True)
    # Create portofolio plan (draft)
    with open((projectname / portofolio_plan_name), "w+") as porto_plan:
        porto_plan.write("hello")
    click.echo(f"{projectname} was created...")


@project_meta.command("delete")
@click.argument(
    "projectname",
    type=click.Path(dir_okay=True, file_okay=True, writable=True, resolve_path=True),
    required=False,
    default="my_finantial_portofolio",
)
@click.option("-y", "--yes", is_flag=True, required=False)
def delete(projectname: PathType, yes: bool):
    """Delete the project"""
    projectname = pathlib.Path(projectname)
    # Confirm what the user wants to do
    if not yes:
        if input(f"are you sure you want to delete {projectname}? (y/n)") != "y":
            exit()
    if not (projectname / portofolio_plan_name).is_file():
        click.echo("This seems not to be a supported project!")
        exit()
    # Search first if any content exist in the projectstructure and delete it
    project_content = projectname.rglob("*")
    for file in project_content:
        file.unlink()
    # Delete the project
    projectname.rmdir()
    click.echo(f"{projectname} was definitely deleted...")
