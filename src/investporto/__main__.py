"""
Is used when investporto is called as a module.

It redirects to investporto.cli.main.

.. command-output:: python -m investporto --help
    :ellipsis: 4



:module: __main__

:Copyright: Copyright (c) 2010-2021 sebastianpfischer

    MIT License
"""

from .cli import main

if __name__ == "__main__":
    main()
