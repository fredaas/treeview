DESCRIPTION
--------------------------------------------------------------------------------

Treeview is lightweight dictionary parser.

USAGE
--------------------------------------------------------------------------------

A rule can be written in three ways,

    1. { <key>: <required> },

    2. { <key>: (<required>, <func>) }, and

    3. { <key>: (<required>, <dict>) }.

A key can either be required on optional. This is controlled by setting
the <required> field to True or False.

A key value can be validated using a constraint function. The constraint
function is specified by the <func> field.

A key value can be nested if the value itself is a dictionary. The <dict> field
specifies a nested key value.

EXAMPLE

    data = {
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

    rules = {
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

    treeview.parse(data, rules)
