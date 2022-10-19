import pytest
from investporto.portfolio_plan_cli import Portfolio, portfolio_plan
from click.testing import CliRunner, Result
from pathlib import Path
import collections
from investporto.types_and_vars import portfolio_plan_name

file_content = """
'name': 'entry'
'children':
    - 'name': 'etfs'
      'percentage': 30
      'children':
          - 'name': 'big_market_caps'
            'percentage': 100
    - 'name': 'stocks'
      'percentage': 70
      'children':
          - 'name': 'big_market_caps'
            'percentage': 50
          - 'name': 'mid_market_caps'
            'percentage': 40.0
"""


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


def test_portfolio_tree_class_open(create_dummy_project):
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    portfolio.open()
    # Check that the received content is the one expected to read
    to_get_class_name = ["etfs", "stocks"]
    to_get_class_percentage = [30, 70]
    for child in portfolio._plan.children:
        assert child.name in to_get_class_name
        assert child.percentage in to_get_class_percentage


def test_portfolio_tree_class_closing(create_dummy_project):
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
    # Check that the received content is the one expected to read
    to_get_class_name = ["etfs", "stocks"]
    to_get_class_percentage = [30, 70]
    for child in portfolio._plan.children:
        assert child.name in to_get_class_name
        assert child.percentage in to_get_class_percentage


def test_portfolio_tree_class_empty_start(create_dummy_project):
    _, _, project_plan = create_dummy_project
    # First we need to empty the repo
    with open(project_plan, "w") as portfolio_plan_file:
        portfolio_plan_file.write("")
    # Let us open the project
    portfolio = Portfolio(project_plan)
    portfolio.open()
    assert portfolio._plan.name == "entry"
    # Let us close it now:
    portfolio.close()
    # And verify if the create file
    expected_file_content = """name: entry
"""
    with open(project_plan, "r") as portfolio_plan_file:
        assert portfolio_plan_file.read() == expected_file_content


def test_add_asset_class(create_dummy_project):
    # Asset to add
    asset_class_to_add = "bonds"
    asset_class_percentage_to_add = 15
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # Allocate
    with portfolio as p:
        p.add(asset_class_to_add, asset_class_percentage_to_add)
    # Verify allocation
    with portfolio as p:
        allocated_node = None
        for node in p._plan.children:
            if node.name == asset_class_to_add:
                allocated_node = node
                break
        assert allocated_node.name == asset_class_to_add
        assert allocated_node.percentage == asset_class_percentage_to_add


def test_add_asset_class_allocation(create_dummy_project):
    # Asset allocation to add
    asset_class_to_add = "etfs"
    asset_class_allocation_to_add = "mid_market_caps"
    allocation_percentage = 15
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # Allocate
    with portfolio as p:
        p.add(
            asset_class_to_add,
            None,
            asset_class_allocation_to_add,
            allocation_percentage,
        )
    # Verify allocation
    with portfolio as p:
        allocated_node = None
        # Find asset-class
        for node in p._plan.children:
            if node.name == asset_class_to_add:
                allocated_node = node
                break
        # Find allocation
        for node in allocated_node.children:
            if node.name == asset_class_allocation_to_add:
                allocated_node = node
                break

        assert allocated_node.name == asset_class_allocation_to_add
        assert allocated_node.percentage == allocation_percentage


def test_overwrite_asset_class_allocation(create_dummy_project):
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # Allocate
    with portfolio as p:
        p.add("etfs", None, "mid_market_caps", 15)
    # Overwrite
    with portfolio as p:
        p.add("etfs", 15, "mid_market_caps", 80)
    # Verify allocation
    with portfolio as p:
        allocated_node = None
        # Find asset-class
        for node in p._plan.children:
            if node.name == "etfs":
                allocated_node = node
                break
        assert allocated_node.name == "etfs"
        assert allocated_node.percentage == 15
        # Find allocation
        for node in allocated_node.children:
            if node.name == "mid_market_caps":
                allocated_node = node
                break
        assert allocated_node.name == "mid_market_caps"
        assert allocated_node.percentage == 80


def test_remove_asset_class(create_dummy_project):
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # Remove action
    with portfolio as p:
        p.remove("etfs")
    # Verify that the removal occurred
    with portfolio as p:
        allocated_node = None
        # Find asset-class
        for node in p._plan.children:
            if node.name == "etfs":
                allocated_node = node
                break
        assert allocated_node == None


def test_remove_asset_class_allocation(create_dummy_project):
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # Remove action
    with portfolio as p:
        p.remove("stocks", "mid_market_caps")
    # Verify that the removal occurred
    with portfolio as p:
        asset_class_node = None
        allocated_node = None
        # Find asset-class
        for node in p._plan.children:
            if node.name == "stocks":
                asset_class_node = node
                break
        # Find allocation
        for node in asset_class_node.children:
            if node.name == "mid_market_caps":
                allocated_node = node
                break
        assert allocated_node == None


def test_validate_rendering(create_dummy_project, capsys):
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # print (to be called with pytest -s to see it)
    with portfolio as p:
        p.visualize_allocation()

    captured = capsys.readouterr()
    assert (
        captured.out
        == "entry\n├── ( etfs , 30 )\n│   └── ( big_market_caps , 100 )\n└── ( stocks , 70 )\n    ├── ( big_market_caps , 50 )\n    └── ( mid_market_caps , 40.0 )\n"
    )


def test_validate_allocation(create_dummy_project, capsys):
    # Project opening
    _, _, project_plan = create_dummy_project
    portfolio = Portfolio(project_plan)
    # print (to be called with pytest -s to see it)
    with portfolio as p:
        p.check_allocation()

    captured = capsys.readouterr()
    assert (
        captured.out
        == "entry -> ok!\n├── etfs -> ok!\n└── stocks -> allocation error!\n"
    )
