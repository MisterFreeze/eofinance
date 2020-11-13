from flask import Blueprint
from flask.blueprints import BlueprintSetupState
from pathlib import Path


BUDGET_STORAGE_DIR=''

bp = Blueprint('auth', __name__, url_prefix='/budget')

BUDGET_STATES = ['wip', 'requested', 'confirmed']


class BudgetNotFound(Exception):
  pass


class BudgetEntry(object):
  def __init__(self, budget):
    self._budget = budget


class Budget(object):
  def __init__(self, alliance, region, dpt, year, month):
    self.alliance = alliance
    self.region = region
    self.department = dpt
    self.year = year
    self.month = month
    self.entries = []
    self.state = BUDGET_STATES[0]


class BudgetStorage(object):
  base_dir = BUDGET_STORAGE_DIR
  json_decoder = None
  json_encoder = None
  
  @staticmethod
  def __path_for_budget(budget:Budget) -> Path:
    alliance = budget.alliance
    year = budget.year
    month = budget.month
    region = budget.region
    dpt = budget.department
    p = Path(BudgetStorage.base_dir) / str(year) / str(month) / '{}_{}_{}.json'.format(alliance, region.lower(), dpt.lower())
    return p

  @staticmethod
  def load(budget:Budget) -> Budget:
    file_name = BudgetStorage.__path_for_budget(budget)
    budget_data = None
    p = Path(file_name)
    print(p)
    try:
      with p.open() as lf:
        budget_data = lf.read()
    except FileNotFoundError:
      raise BudgetNotFound('Budget for {} -> {} not found for {}/{}'.format(budget.region, budget.department, budget.year, budget.month))
    budget_data = BudgetStorage.json_decoder.loads(budget_data)
    if 'state' in budget_data.keys():
      budget.state = budget_data['state']
    budget.entries = budget_data['entries']
    return budget

  @staticmethod
  def save(budget:Budget) -> Budget:
    save_file = BudgetStorage.__path_for_budget(budget)
    save_dir = save_file.parent
    if not save_dir.exists():
      save_dir.mkdir(mode=0o775, parents=True, exist_ok=True)
    budget_data_to_save = {
      'state': budget.state,
      'entries': budget.entries
    }
    budget_json = BudgetStorage.json_decoder.dumps(budget_data_to_save)
    with save_file.open(mode='w') as sf:
      sf.write(budget_json)
    return save_file


@bp.route('/<int:year>/<int:alliance>/<string:region>/<string:department>/', methods=['GET'])
def list_department_budget_for_year(alliance, region, department, year):
  pass


@bp.route('/<int:year>/<int:month>/<int:alliance>/<string:region>/<string:department>/', methods=['GET'])
def get_budget(alliance, region, department, year, month):
  pass


@bp.route('/<int:year>/<int:month>/<int:alliance>/<string:region>/<string:department>/', methods=['POST'])
def create_budget(alliance, region, department, year, month):
  pass


def __setup_blueprint(state:BlueprintSetupState):
  BudgetStorage.base_dir = state.options['BUDGET_STORAGE_DIR']

bp.record_once(__setup_blueprint)
