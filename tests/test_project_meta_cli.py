import pytest
import os
from investporto.project_meta_cli import project_meta
from click.testing import CliRunner, Result
from pathlib import Path


def create_dummy_project(runner: CliRunner, project_path: Path) -> Result:
    """Create a dummy project with different files in
    This is a helper function"""
    # Create the project
    result = runner.invoke(project_meta, ["create", str(project_path)])
    # Create a set of dummy files within the project
    for number in range(5):
        with open(project_path / (str(number) + "file.csv"), "w+") as f:
            f.writelines("Hello")
    return result


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
        runner.invoke(project_meta, ["create", str(project_path)])
        # Delete it and verify it realy do not exist
        result = runner.invoke(project_meta, ["delete", "-y", str(project_path)])
        assert result.exit_code == 0
        assert not project_path.exists()


def test_close_a_project():
    """Close a created project -> create a zip file and delete the project folder"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        create_dummy_project(runner, project_path)
        # Try to delete the project
        # result = runner.invoke(project_meta, ["delete", "-y", str(project_path)])
        # print(result.stdout)
        # assert result.exit_code == os.EX_USAGE
