import pytest
import os
from investporto.portfolio_plan_cli import Portfolio
from click.testing import CliRunner, Result
from pathlib import Path
import collections
from investporto.types_and_vars import portfolio_plan_name

file_content = """
etfs:
  percentage: 30
  subtypes:
    big_market_caps:
      percentage: 100
stocks:
  percentage: 70
  subtypes:
    big_market_caps:
      percentage: 35
    mid_market_caps:
      percentage: 35
"""
dict_content = {
    "stocks": {
        "percentage": 70,
        "subtypes": {
            "big_market_caps": {"percentage": 35},
            "mid_market_caps": {"percentage": 35},
        },
    },
    "etfs": {"percentage": 30, "subtypes": {"big_market_caps": {"percentage": 100}}},
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


def comparaison(base, cmp_with):
    all_keys_found = True
    all_values_found = True
    for key, value in cmp_with.items():
        if isinstance(value, collections.abc.Mapping):
            base[key], returned_key_check, returned_value_check = comparaison(
                base.get(key, {}), value
            )
            all_keys_found &= returned_key_check
            all_values_found &= returned_value_check
        else:
            all_values_found &= value in base.values()
            all_keys_found &= key in base.keys()
    return base, all_keys_found, all_values_found


def test_portfolio_class_add(create_dummy_project):
    """Test the successful addition of several elements
    into the project plan"""
    # Create the dummy project
    _, _, project_plan = create_dummy_project
    # Define different elements to add to the project
    new_asset_type = "Bonds"
    new_asset_percentage = 20
    new_asset_subtype = "State"
    new_asset_subpercentage = 89

    # Test 1: add a type
    with Portfolio(project_plan) as plan:
        plan.add(asset_type=new_asset_type, percentage=new_asset_percentage)
    # Reopen the file and check if the element was really added
    portfolio = Portfolio(project_plan)
    portfolio.open()
    _, all_keys_found, all_values_found = comparaison(
        portfolio._plan, {new_asset_type.lower(): {"percentage": new_asset_percentage}}
    )
    print(f"--> {portfolio._plan}")
    assert all_keys_found
    assert all_values_found
    # Clean resources
    portfolio.close()
    del portfolio

    # Test 2: add a subtype
    with Portfolio(project_plan) as plan:
        plan.add(
            asset_type=new_asset_type,
            asset_subtype=new_asset_subtype,
            subpercentage=new_asset_subpercentage,
        )
    # Reopen the file and check if the element was really added
    portfolio = Portfolio(project_plan)
    portfolio.open()
    _, all_keys_found, all_values_found = comparaison(
        portfolio._plan,
        {
            new_asset_type: {
                "percentage": new_asset_percentage,
                "subtype": {new_asset_subtype: {"percentage": new_asset_subpercentage}},
            }
        },
    )
    print(f"--> {portfolio._plan}")
    assert all_keys_found
    assert all_values_found
    # Clean resources
    portfolio.close()
    del portfolio


def test_portfolio_class_delete(create_dummy_project):
    """Test the deletion of several elements are possible"""
    # Create the dummy project
    _, _, project_plan = create_dummy_project
    # Define different elements to add to the project
    new_asset_type = "ETFs"
    new_asset_subtype = "big_market_caps"

    # Test 1: remove a subtype
    with Portfolio(project_plan) as plan:
        plan.delete(asset_type=new_asset_type, asset_subtype=new_asset_subtype)
    # Reopen the file and check if the element was really added
    portfolio = Portfolio(project_plan)
    portfolio.open()
    _, all_keys_found, all_values_found = comparaison(
        portfolio._plan, {new_asset_type: {new_asset_subtype: None}}
    )
    assert not all_keys_found
    assert not all_values_found
    # Clean resources
    portfolio.close()
    del portfolio

    # Test 2: remove a type
    with Portfolio(project_plan) as plan:
        plan.delete(asset_type=new_asset_type)
    # Reopen the file and check if the element was really added
    portfolio = Portfolio(project_plan)
    portfolio.open()
    _, all_keys_found, all_values_found = comparaison(
        portfolio._plan, {new_asset_type: None}
    )
    assert all_keys_found
    assert all_values_found
    # Clean resources
    portfolio.close()
    del portfolio
