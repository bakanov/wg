from nose import with_setup  # optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.const import OBJECT_NUMBERS, CONSTRAINTS
from common.ships import get_database_state_dict, randomize_database, compare_states


def my_setup_function():
    print("my_setup_function")


def my_teardown_function():
    print("my_teardown_function")


@with_setup(my_setup_function, my_teardown_function)
def test_ships_generator():
    engine = create_engine('sqlite:///Ships.db')
    Session = sessionmaker(bind=engine)

    # create a Session
    dbsession = Session()

    result_dicts_old = get_database_state_dict(dbsession)
    randomize_database(dbsession, OBJECT_NUMBERS, CONSTRAINTS)
    result_dicts_new = get_database_state_dict(dbsession)
    for i, dict1 in enumerate(result_dicts_old):
        dict2 = result_dicts_new[i]
        ship_name = dict1['main_column']['ship']
        check_ship_func = CompareStates(ship_name)
        yield check_ship_func, dict1, dict2


class CompareStates:

    def __init__(self, ship_name):
        self.ship_name = ship_name
        self.description = "Check ship {}".format(ship_name)

    def __call__(self, dict1, dict2):
        res = compare_states(self.ship_name,  dict1, dict2)
        if res is not None:
            raise AssertionError(res)
