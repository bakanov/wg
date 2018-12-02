from sqlalchemy.inspection import inspect
from dictdiffer import diff
from common.const import OBJECT_NUMBERS, CONSTRAINTS
from common.model import Engine, Hull, Weapon, Ship
from common.table_operartions import populate_child_tables, populate_main_table, randomize_child_tables, \
    randomize_main_table
from common.utils import orm_object_to_dict


def populate_database(dbsession, object_numbers_dict, constraints):
    child_tables_dict = populate_child_tables(dbsession, [Engine, Hull, Weapon], OBJECT_NUMBERS, CONSTRAINTS)
    populate_main_table(dbsession, Ship, child_tables_dict, object_numbers_dict)


def randomize_database(dbsession, object_numbers_dict, constraints):
    randomize_child_tables(dbsession, [Engine, Hull, Weapon], CONSTRAINTS, 5)

    child_tables_dict = {}
    for orm_class in [Engine, Hull, Weapon]:
        primary_key_column = inspect(orm_class).primary_key[0].name
        results = dbsession.query(orm_class).all()
        child_tables_dict[primary_key_column] = results

    randomize_main_table(dbsession, Ship, child_tables_dict, object_numbers_dict, 10)


def get_database_state(dbsession):
    results = dbsession.query(Ship, Engine, Hull, Weapon) \
        .join(Engine).join(Hull).join(Weapon)

    return results


def get_database_state_dict(dbsession):
    results = get_database_state(dbsession)

    result_dicts = []

    for result in results:
        result_dict = {}
        result_dict['main_column'] = orm_object_to_dict('ship', result[0])
        result_dict['child_columns'] = {}
        result_dict['child_columns']['engine'] = orm_object_to_dict('engine', result[1])
        result_dict['child_columns']['hull'] = orm_object_to_dict('hull', result[2])
        result_dict['child_columns']['weapon'] = orm_object_to_dict('weapon', result[3])
        result_dicts.append(result_dict)

    return result_dicts


def pretty_print_ship_diff(ship_name, change_list):
    change_string_all = ''
    for change_tuple in change_list:
        what_changed_tuple = change_tuple[2]
        (old, new) = what_changed_tuple
        change_string = "{}, {} \n    expected {}, was {}".format(ship_name, new, old, new)
        change_string_all += change_string
    return change_string_all


def pretty_print_part_diff(ship_name, part_type, change_list, old_dict, new_dict):
    change_string_all = "{}, {}\n".format(ship_name, new_dict[part_type])
    for change_tuple in change_list:
        changed_type = change_tuple[1]
        what_changed_tuple = change_tuple[2]
        (old, new) = what_changed_tuple
        change_string = "    {}: expected {}, was {}\n".format(changed_type, old, new)
        change_string_all += change_string
    return change_string_all


def compare_ships(dicts1, dicts2):
    for i, dict1 in enumerate(dicts1):
        dict2 = dicts2[i]
        ship_name = dict1['main_column']['ship']
        compare_states(ship_name, dict1, dict2)


def compare_states(ship_name, dict1, dict2):
    res = None
    main_diff = list(diff(dict1['main_column'], dict2['main_column']))
    if main_diff:
        res = pretty_print_ship_diff(ship_name, main_diff)
    else:
        for key, dict1_child_column in dict1['child_columns'].iteritems():
            dict2_child_column = dict2['child_columns'][key]
            child_diff = list(diff(dict1_child_column, dict2_child_column))
            if child_diff:
                res = pretty_print_part_diff(ship_name, key, child_diff, dict1_child_column, dict2_child_column)

    return res
