#!/usr/bin/env python3

ERROR_REQUIREDKEY = 1
ERROR_MISSINGVALUE = 2
ERROR_MISSINGRULE = 3
ERROR_DUPLICATES = 4

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

    for key, required in rules.items():
        # Required key not found
        if not data.get(key) and required:
            return ERROR_REQUIREDKEY
        # Rule is nested but data is not
        elif isinstance(required, tuple) and not isinstance(data.get(key), dict):
            return ERROR_MISSINGVALUE
        # Follow nested key
        elif isinstance(required, tuple):
            if not data.get(key) and required[0]:
                return ERROR_REQUIREDKEY
            else:
                parse(data.get(key), required[1])

    return 0

def print_parse(data, rules, depth=0):
    """
    Prints parser validation results
    """
    # Check for keys that have no corresponding rule
    if len(set(data.keys()).difference(set(rules))) > 0:
        print("[Error] Unspecified keys detected")

    # Check for duplicate keys
    if len(data) != len(set(data)):
        print("[Error] Duplicate keys detected")

    for key, required in rules.items():
        # Required key not found
        if not data.get(key) and required:
            print("[Error] Key '{}' required but not found".format(key))
        # Rule is nested but data is not
        elif isinstance(required, tuple) and not isinstance(data.get(key), dict):
            print("[Error] Key '{}' should be nested".format(key))
        # Follow nested key
        elif isinstance(required, tuple):
            if not data.get(key) and required[0]:
                print("[Error] Key '{}' required but not found".format(key))
            else:
                print_parse(data.get(key), required[1], depth + 1)