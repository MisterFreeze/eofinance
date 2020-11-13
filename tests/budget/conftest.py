import pytest
import json

from app import create_app, init_db

from app.budget import BudgetStorage

@pytest.fixture
def web_client(tmp_path_factory):
  tmp_db_dir = tmp_path_factory.mktemp('instance', False)
  db_file = tmp_db_dir / 'db.sqlite'
  app_config = {
    'instance_path': tmp_db_dir 
  }
  app = create_app(app_config)
  app.config['DATABASE'] = db_file
  app.config['TESTING'] = True

  with app.test_client() as client:
      with app.app_context():
          init_db
      yield client

@pytest.fixture
def alliance():
  return 99009104

@pytest.fixture
def budgets_dir(tmp_path_factory):
  budgets_folder = None
  try:
    budgets_folder = tmp_path_factory.mktemp('budgets', False)
  except FileExistsError:
    budgets_folder = tmp_path_factory.getbasetemp() / 'budgets'
  return budgets_folder

@pytest.fixture
def example_budget_2020_11_high_testdepartment(budgets_dir, alliance):
  budget_dir_2020_11 = budgets_dir / '2020' / '11'
  budget_dir_2020_11.mkdir(parents=True, exist_ok=True)
  file_path = budget_dir_2020_11 / '{}_high_testdepartment.json'.format(alliance)
  dummy_budget_json = '''
{
  "state": "wip",
  "entries": [
      1,2,3
    ]
}
  '''
  with file_path.open('w') as bf:
    bf.write(dummy_budget_json)

@pytest.fixture
def budget_storage(budgets_dir):
  BudgetStorage.base_dir = budgets_dir
  BudgetStorage.json_encoder = json
  BudgetStorage.json_decoder = json
  return BudgetStorage
