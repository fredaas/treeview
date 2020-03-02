#!/usr/bin/env python3

ERROR_REQUIREDKEY  = 1
ERROR_MISSINGVALUE = 2
ERROR_MISSINGRULE  = 3
ERROR_DUPLICATES   = 4
ERROR_CONSTRAINT   = 5

def parse(data, rules):
    """
    Performs a depth-first search on a dictionary payload and validates all its key-value pairs
    agains a corresponding rule dictionary

    Parameters:

        data

            Payload dictionary.

        rules

            Rule dictionary corresponding to data payload.
    """

    # Check for keys that have no corresponding rule
    if len(set(data.keys()).difference(set(rules))) > 0:
        return ERROR_MISSINGRULE

    # Check for duplicate keys
    if len(data) != len(set(data)):
        return ERROR_DUPLICATES

    for key, value in rules.items():
        # Required key not found
        if not data.get(key) and value:
            return ERROR_REQUIREDKEY
        # Key has contraint function
        elif isinstance(value, tuple) and callable(value[1]):
            if not value[1](data.get(key)):
                return ERROR_CONSTRAINT
        # Rule is nested but data is not
        elif isinstance(value, tuple) and not isinstance(data.get(key), dict):
            return ERROR_MISSINGVALUE
        # Follow nested key
        elif isinstance(value, tuple):
            if not data.get(key) and value[0]:
                return ERROR_REQUIREDKEY
            else:
                parse(data.get(key), value[1])

    return 0

def print_parse(data, rules, depth=0):
    """
    Prints parser validation results
    """
    # Check for keys that have no corresponding rule
    invalid_keys = set(data.keys()).difference(set(rules))
    if len(invalid_keys) > 0:
        print("[Error] Unspecified keys detected: {}".format(" ".join("'" + x + "'" for x in invalid_keys)))

    # Check for duplicate keys
    if len(data) != len(set(data)):
        print("[Error] Duplicate keys detected")

    for key, value in rules.items():
        # Required key not found
        if not data.get(key) and value:
            print("[Error] Key '{}' required but not found".format(key))
        # Key has contraint function
        elif isinstance(value, tuple) and callable(value[1]):
            if not value[1](data.get(key)):
                print("[Error] Invalid value detected for key '{}'".format(key))
        # Rule is nested but data is not
        elif isinstance(value, tuple) and not isinstance(data.get(key), dict):
            print("[Error] Key '{}' should be nested".format(key))
        # Follow nested key
        elif isinstance(value, tuple):
            if not data.get(key) and value[0]:
                print("[Error] Key '{}' required but not found".format(key))
            else:
                print_parse(data.get(key), value[1], depth + 1)
