#!/usr/bin/env python3

# Missing required key
ERROR_REQUIRED    = 1
# Expected nested key value
ERROR_NESTED      = 2
# Missing key rule
ERROR_MISSINGRULE = 3
# Contains duplicates
ERROR_DUPLICATE   = 4
# Invalid value
ERROR_CONSTRAINT  = 5
# Constraint function failed
ERROR_FUNCTION    = 6
# Invalid tuple format
ERROR_TUPLE       = 7

def parse(data, rules):
    """
    Performs a depth-first search on a dictionary payload and validates all its
    key-value pairs agains a corresponding rule dictionary

    Parameters:

        data

            Payload dictionary.

        rules

            Rule dictionary corresponding to data payload.

    Returns the error code of the first detected error.
    """

    # Check for keys that have no corresponding rule
    if len(set(data.keys()).difference(set(rules))) > 0:
        return ERROR_MISSINGRULE

    # Check for duplicate keys
    if len(data) != len(set(data)):
        return ERROR_DUPLICATE

    error = 0

    for key, value in rules.items():
        if isinstance(value, tuple):
            if len(value) != 2:
                return ERROR_TUPLE
            # Key is required
            elif not data.get(key) and value[0]:
                return ERROR_REQUIRED
            # Key has constraint function
            elif callable(value[1]):
                try:
                    if not value[1](data.get(key)):
                        return ERROR_CONSTRAINT
                except:
                    return ERROR_FUNCTION

            # Key is nested
            elif isinstance(value[1], dict):
                if not isinstance(data.get(key), dict):
                    return ERROR_NESTED
                else:
                    error = parse(data.get(key), value[1])
        else:
            # Key is required
            if not data.get(key) and value:
                return ERROR_REQUIRED

    return error

def print_parse(data, rules, depth=0):
    """
    Prints parser validation results
    """
    # Check for keys that have no corresponding rule
    invalid_keys = set(data.keys()).difference(set(rules))
    if len(invalid_keys) > 0:
        print("[Error] Unspecified keys detected: {}"
            .format(" ".join("'" + x + "'" for x in invalid_keys)))

    # Check for duplicate keys
    if len(data) != len(set(data)):
        print("[Error] Duplicate keys detected")

    error = 0

    for key, value in rules.items():
        if isinstance(value, tuple):
            if len(value) != 2:
                print("[Error] A tuple must have exactly two elements")
            # Key is required
            elif not data.get(key) and value[0]:
                print("[Error] Key '{}' required but not found".format(key))
            # Key has constraint function
            elif callable(value[1]):
                try:
                    if not value[1](data.get(key)):
                        print("[Error] Invalid value detected for key '{}'"
                            .format(key))
                except:
                    print("[Error] Constraint function failed")
            # Key is nested
            elif isinstance(value[1], dict):
                if not isinstance(data.get(key), dict):
                    print("[Error] Key '{}' should be nested".format(key))
                else:
                    error = print_parse(data.get(key), value[1], depth + 1)
        else:
            # Key is required
            if not data.get(key) and value:
                print("[Error] Key '{}' required but not found".format(key))

    return error
