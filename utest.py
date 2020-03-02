#!/usr/bin/env python3

import treeview

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
    data = {
        "a": 10,
        "c": 42,
        "d": {
            "x": 1,
            "y": {
                "z": 2,
            },
        },
    }
    rules = {
        "a": 1,
        "b": 1,
        "c": 0,
        "d": (1, {
            "x": 1,
            "y": (0, {
                "p": 1
            }),
        }),
    }

    pprint(data)
    treeview.print_parse(data, rules)

if __name__ == "__main__":
    test_treeview()
