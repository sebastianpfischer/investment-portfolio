import pytest
import os
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


def test_basic_delete():
    """Delete the above created project"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        # Create the project
        runner.invoke(project_meta, ["create", str(project_path)])
        # Delete it and verify it realy do not exist
        result = runner.invoke(project_meta, ["delete", "-y", str(project_path)])
        assert result.exit_code == 0
        assert not project_path.exists()


def test_delete_containing_several_files():
    """Delete the above created project containing several additional files"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        # Create the project
        result = runner.invoke(project_meta, ["create", str(project_path)])
        # Create a set of dummy files within the project
        for number in range(5):
            with open(project_path / (str(number) + "file.csv"), "w+") as f:
                f.writelines("Hello")
        # Delete it and verify it realy do not exist
        runner.invoke(project_meta, ["delete", "-y", str(project_path)])
        # Check if all the files got deleted
        for number in range(5):
            assert not Path(project_path / (str(number) + "file.csv")).exists()


def test_delete_try_of_no_project():
    """Miss use of the API to try to delete some repository"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        # Create project folder
        project_path.mkdir(parents=True, exist_ok=True)
        # Create a set of dummy files within the project
        for number in range(5):
            with open(project_path / (str(number) + "file.csv"), "w+") as f:
                f.writelines("Hello")
        # Try to delete the project
        result = runner.invoke(project_meta, ["delete", "-y", str(project_path)])
        print(result.stdout)
        assert result.exit_code == os.EX_USAGE
