import pytest
from investporto.project_meta_cli import project_meta
from click.testing import CliRunner
from pathlib import Path


def test_create():
    """Verify if the project creation was successfull or not"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        result = runner.invoke(project_meta, ["create", str(project_path)])
        assert result.exit_code == 0
        assert project_path.exists()


def test_delete():
    """Delete the above created project"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        # Create the project
        result = runner.invoke(project_meta, ["create", str(project_path)])
        # Delete it and verify it realy do not exist
        result = runner.invoke(project_meta, ["delete", "-y", str(project_path)])
        print(f"{result}")
        assert result.exit_code == 0
        assert not project_path.exists()
