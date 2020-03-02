#!/usr/bin/env python3

from treeview import ( parse, print_parse )

def pprint(data, depth=0):
    """
    Traverses the dictionary in BFS order and prints its keys and values
    """
    space = 4
    for key, value in data.items():
        print(' ' * space * depth + str(key))
        if isinstance(value, dict):
            pprint(value, depth + 1)
        else:
            print(' ' * space * (depth + 1) + str(value))

def test_treeview():
    data_x = {
        "a": 10,
        "c": 42,
        "d": {
            "x": 1,
            "y": {
                "z": 2,
                "p": 3,
            },
        },
        "q": 123,
    }

    rules_x1 = {
        "a": (1, lambda x: x >= 10),
        "c": 0,
        "d": (1, {
            "x": 1,
            "y": (0, {
                "z": (1, lambda x: x == 2),
                "p": 1,
            }),
        }),
        "q": 0,
    }

    rules_x2 = {
        "a": (1, lambda x: x < 10),
        "b": 1,
        "c": 0,
        "d": (1, {
            "x": 1,
            "y": (0, {
                "z": (1, lambda x: x != 2),
            }),
        }),
    }

    data_y = {
        "a": 1,
        "c": {
            "x": 3,
            "y": 4,
        },
    }

    rules_y1 = {
        "a": 0,
        "b": (0, lambda x: x != 2),
        "c": (0, {
            "x": 0,
            "y": 0,
        }),
    }

    error = 0

    print("TEST 1")
    error = parse(data_x, rules_x1)
    if not error:
        print("OK")
    else:
        print_parse(data_x, rules_x1)
        print("[Error] Code: {}".format(error))

    print("TEST 2")
    error = parse(data_x, rules_x2)
    if not error:
        print("OK")
    else:
        print_parse(data_x, rules_x2)
        print("[Error] Code: {}".format(error))

    print("TEST 3")
    error = parse(data_y, rules_y1)
    if not error:
        print("OK")
    else:
        print_parse(data_y, rules_y1)
        print("[Error] Code: {}".format(error))

if __name__ == "__main__":
    test_treeview()
