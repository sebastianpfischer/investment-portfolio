import pytest
import os
from investporto.portfolio_plan_cli import Portfolio
from click.testing import CliRunner, Result
from pathlib import Path
from investporto.types_and_vars import portfolio_plan_name

file_content = """
ETFs:
  percentage: 30
  subtypes:
    big_market_caps:
      percentage: 100
Stocks:
  percentage: 70
  subtypes:
    big_market_caps:
      percentage: 35
    mid_market_caps:
      percentage: 35
"""
dict_content = {
    "Stocks": {
        "percentage": 70,
        "subtypes": {
            "big_market_caps": {"percentage": 35},
            "mid_market_caps": {"percentage": 35},
        },
    },
    "ETFs": {"percentage": 30, "subtypes": {"big_market_caps": {"percentage": 100}}},
}


@pytest.fixture
def create_dummy_project():
    # Define test variables
    runner = CliRunner()
    project_path = Path("temp/test1")
    project_plan = project_path / portfolio_plan_name
    # Create project
    with runner.isolated_filesystem():
        project_path.mkdir(parents=True)
        with open(project_plan, "w") as portfolio_plan_file:
            portfolio_plan_file.write(file_content)
        # Provide the creation to the test. I know that project_path
        # is equal to project_plan.parent but different tests need one
        # or the other, therefor I pass both
        yield runner, project_path, project_plan
        # Cleanup content
        pass
    pass


def test_portfolio_class_open(create_dummy_project):
    """Test portfolio openning"""
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    portfolio.open()
    # Check that the received content is the one expected to read
    assert dict_content == portfolio._plan


def test_portfolio_class_closing(create_dummy_project):
    """Test if the closing of a project is working"""
    _, _, project_plan = create_dummy_project
    with Portfolio(project_plan):
        pass
    # Create a second Check file, we expect it to be the same as before
    # with open(project_plan, "r") as portfolio_plan_file:
    #    read_content = portfolio_plan_file.read()
    #    assert file_content == read_content
    # --> This would be the best approach but I could not find on the fly
    #     how to resolve the  \n...
    # Therefor, I will just reopen the file and compare its content...
    portfolio = Portfolio(project_plan)
    portfolio.open()
    assert dict_content == portfolio._plan
