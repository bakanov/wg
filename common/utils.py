from random import randint


def get_random_in_range(min, max):
    return randint(min, max)


def get_new_name(name, number):
    return "{}_{}".format(name, number)


def get_random_parameters(constraints):
    params = {}
    for key, value in constraints.iteritems():
        random_value = get_random_in_range(value['min'], value['max'])
        params[key] = random_value

    return params


def orm_object_to_dict(_type, obj):
    obj_dict = {k: v for k, v in obj.__dict__.iteritems() if not str(k).startswith("_")}
    obj_dict['_type'] = _type  # Add type inside to more easily identify type of the object
    return obj_dict
