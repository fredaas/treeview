#!/usr/bin/env python3

class Params():
    def __init__(self, data, required, optional, rules, min_optional=0):
        self.json = data
        self.data = set(data.keys())

        self.rules = rules

        optional = set(optional.split())
        required = set(required.split())

        self.observed_optional = self.data.difference(required)
        self.observed_required = self.data.difference(self.observed_optional)

        self.missing_rules = optional.union(required).difference(set(self.rules))

        self.is_required_valid = len(required.intersection(data)) == len(required)
        self.is_optional_valid = self.observed_optional.issubset(optional) and (len(self.observed_optional) >= min_optional)
        self.is_missing_rules = len(self.missing_rules)

        self.contains_duplicates = len(self.json) == len(self.data)

    def is_valid_params(self):
        return self.is_required_valid and self.is_optional_valid and not self.contains_duplicates

    def is_valid_args(self):
        if is_missing_rules:
            return None

        keys = list(self.observed_optional) + list(self.observed_required)
        for key in keys:
            value = self.json[key]
            if not self.rules[key](value):
                return False
        return True

    def get_optional(self):
        return list(self.observed_optional)

    def get_required(self):
        return list(self.observed_required)

    def show_valid_params(self):
        print("Observed required {} [{}]".format(self.observed_required, self.is_required_valid))
        print("Observed optional {} [{}]".format(self.observed_optional, self.is_optional_valid))

    def show_valid_args(self):
        for key in self.missing_rules:
            print("[WARNING] Missing rule for key '{}'".format(key))

        keys = list(self.observed_optional) + list(self.observed_required)
        for key in keys:
            value = self.json[key]
            if self.rules[key](value):
                print(key, "[True]")
            else:
                print(key, "[False]")

    def show_missing_rules(self):
        print(self.missing_rules)

if __name__ == "__main__":
    data = {
        "a": 10,
        "b": 5,
        "c": 42,
        "d": {
            "x": 1,
            "y": 2,
        }
    }

    rules = {
        "a": lambda x: x in [1, 10, 100],
        "b": lambda x: (x > 0) and (x < 10),
        "c": lambda x: x == 42,
        "d": lambda x: isinstance(x, dict)
    }
    params = Params(data, "a b", "c d e", rules, min_optional=2)
    params.show_valid_params()
    params.show_valid_args()

    rules = {
        "x": lambda x: x == 1,
        "y": lambda x: x == 2,
    }
    params = Params(data["d"], "x", "y z", rules, min_optional=1)
    params.show_valid_params()
    params.show_valid_args()
