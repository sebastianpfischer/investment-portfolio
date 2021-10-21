import pytest
import os
from investporto.project_meta_cli import project_meta
from click.testing import CliRunner, Result
from pathlib import Path
from investporto.types_and_vars import portofolio_plan_name


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
        # Close the project
        result = runner.invoke(
            project_meta, ["close", "--password=abcd", str(project_path)]
        )
        assert result.exit_code == os.EX_OK
        # Check if the zip file exist
        assert Path(f"{project_path}.zip").is_file()
        # Check if the project initial files are still present
        assert not project_path.is_dir()


def test_open_a_project():
    """Open a project out of a zip files"""
    runner = CliRunner()
    project_path = Path("temp/test1")
    # Run test isolated
    with runner.isolated_filesystem():
        create_dummy_project(runner, project_path)
        # Close the project
        runner.invoke(project_meta, ["close", "--password=abcd", str(project_path)])
        # Open the project
        result = runner.invoke(
            project_meta, ["open", "--password=abcd", f"{project_path}.zip"]
        )
        assert result.exit_code == os.EX_OK
        # Check if the zip file was deleted
        assert not Path(f"{project_path}.zip").is_file()
        # Check if the project files are back and complete
        assert project_path.is_dir()
        assert (project_path / portofolio_plan_name).is_file()
        for number in range(5):
            assert Path(project_path / (str(number) + "file.csv")).is_file()
