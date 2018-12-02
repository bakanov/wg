from common.utils import get_random_in_range, get_new_name
from sqlalchemy.inspection import inspect


def get_random_parameters(constraints):
    params = {}
    for key, value in constraints.iteritems():
        random_value = get_random_in_range(value['min'], value['max'])
        params[key] = random_value

    return params


def get_main_random_parameters(columns, child_tables_dict):
    params = {}
    for column in columns:
        objects = child_tables_dict[column]
        random_value = get_random_in_range(0, len(objects) - 1)
        obj = objects[random_value]
        primary_key = getattr(obj, column)
        params[column] = primary_key
    return params


def get_primary_key_args(primary_key_column, primary_key_index):
    primary_key_name = get_new_name(primary_key_column, primary_key_index)
    args = {primary_key_column: primary_key_name}
    return args


def populate_child_object(orm_class, table_name,
                          primary_key_column, primary_key_index, constraints):
    args = get_primary_key_args(primary_key_column, primary_key_index)
    current_constraints = constraints[table_name]

    random_parameters = get_random_parameters(current_constraints)
    for key, value in random_parameters.iteritems():
        args[key] = value

    class_instance = orm_class(**args)

    return class_instance


def populate_child_tables(dbsession, orm_classes, object_numbers_dict, constraints):
    child_tables_dict = {}

    for orm_class in orm_classes:
        table_name = orm_class.__table__.name
        primary_key_column = inspect(orm_class).primary_key[0].name
        object_number = object_numbers_dict[table_name]

        for i in range(object_number):
            object_instance = populate_child_object(orm_class, table_name,
                                                    primary_key_column, i, constraints)
            if primary_key_column in child_tables_dict:
                child_tables_dict[primary_key_column].append(object_instance)
            else:
                child_tables_dict[primary_key_column] = [object_instance]

            dbsession.add(object_instance)
            dbsession.commit()

    return child_tables_dict


def randomize_child_tables(dbsession, orm_classes, constraints, change_every_nth):
    for orm_class in orm_classes:
        table_name = orm_class.__table__.name
        primary_key_column = inspect(orm_class).primary_key[0].name
        current_constraints = constraints[table_name]
        results = dbsession.query(orm_class).all()
        for i, result in enumerate(results):
            if i % change_every_nth == 0:
                random_parameters = get_random_parameters(current_constraints)
                kwargs = {primary_key_column: getattr(result, primary_key_column)}
                dbsession.query(orm_class).filter_by(**kwargs).update(random_parameters)
                dbsession.commit()


def randomize_main_table(dbsession, orm_class, child_tables_dict, object_numbers_dict, change_every_nth):
    table_name = orm_class.__table__.name
    primary_key_column = inspect(orm_class).primary_key[0].name
    param_columns = get_main_table_param_columns(orm_class, primary_key_column)

    results = dbsession.query(orm_class).all()
    for i, result in enumerate(results):
        if i % change_every_nth == 0:
            random_parameters = get_main_random_parameters(param_columns, child_tables_dict)
            kwargs = {primary_key_column: getattr(result, primary_key_column)}
            dbsession.query(orm_class).filter_by(**kwargs).update(random_parameters)
            dbsession.commit()


def populate_main_object(orm_class, primary_key_column, primary_key_index,
                         param_columns, child_tables_dict):
    args = get_primary_key_args(primary_key_column, primary_key_index)
    random_parameters = get_main_random_parameters(param_columns, child_tables_dict)
    for key, value in random_parameters.iteritems():
        args[key] = value

    class_instance = orm_class(**args)

    return class_instance


def get_main_table_param_columns(orm_class, primary_key_column):
    param_columns = []

    for column in orm_class.__table__.columns:
        if primary_key_column == column.name:
            continue
        param_columns.append(column.name)

    return param_columns


def populate_main_table(dbsession, orm_class, child_tables_dict, object_numbers_dict):
    table_name = orm_class.__table__.name
    primary_key_column = inspect(orm_class).primary_key[0].name
    param_columns = get_main_table_param_columns(orm_class, primary_key_column)
    object_number = object_numbers_dict[table_name]

    for i in range(object_number):
        object_instance = populate_main_object(orm_class, primary_key_column,
                                               i, param_columns, child_tables_dict)
        dbsession.add(object_instance)
        dbsession.commit()
