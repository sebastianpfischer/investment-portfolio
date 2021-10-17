"""
Investment portfolio
**************************

:module: cli

:synopsis: Entry point to the tool

.. currentmodule:: cli


:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License

"""
import click

from .project_meta_cli import project_meta
from .portofolio_plan_cli import portofolio_plan


main = click.CommandCollection(sources=[project_meta, portofolio_plan])


if __name__ == "__main__":
    main()
