from pathlib import Path
from tempfile import TemporaryDirectory

import json

import pytest

from app.budget import Budget, BudgetStorage, BudgetNotFound


def test_budget_load_not_existing_file_raises_exception(tmpdir, alliance):
  BudgetStorage.base_dir = tmpdir
  with pytest.raises(BudgetNotFound, match = r'Budget for (High|Low|Null) -> .+ not found for \d+/\d+'):
    budget = Budget(alliance, 'High', 'testdepartment', 2020, 11)
    BudgetStorage.load(budget)

def test_budget_load_path_is_correct(alliance, budget_storage, example_budget_2020_11_high_testdepartment):
    budget = Budget(alliance, 'High', 'testdepartment', 2020, 11)
    budget_data = BudgetStorage.load(budget)
    assert isinstance(budget_data, Budget)

def test_budget_2020_11_high_testdepartment_is_loaded_correctly_from_budget(alliance, budget_storage, example_budget_2020_11_high_testdepartment):
  budget = Budget(alliance, 'High', 'testdepartment', 2020, 11)
  b = budget_storage.load(budget)
  assert len(b.entries) == 3
  assert b.state == 'wip'

def test_save(budget_storage, alliance):
  region = 'Low'
  department = 'Industry'
  year = 2020
  month = 12

  dest_path = budget_storage.base_dir / str(year) / str(month) / '{}_{}_{}.json'.format(alliance, region.lower(), department.lower())

  budget = Budget(alliance, region, department, year, month)
  save_file = budget_storage.save(budget)

  assert dest_path.exists() and dest_path.is_file() and save_file == dest_path