def stand_for(
    candidate,
    *keys,
    options={
        "ascii": ["ascii"],
        "camel": ["camel", "camel_case", "camelCase"],
        "capitalize": ["capitalize"],
        "casefold": ["casefold"],
        "create": ["create", "add", "insert", "make"],
        "delete": ["del", "delete", "suppress", "erase", "remove"],
        "fix": ["fix"],
        "guess": ["guess", "infer"],
        "lower": ["lower", "lowercase", "lower_case"],
        "obfuscate": ["obfuscate", "obscure"],
        "randomize": ["rand", "random", "randomize", "randomise"],
        "snake": ["snake", "snake_case"],
        "swapcase": ["swapcase"],
        "title": ["title"],
        "upper": ["upper", "uppercase", "upper_case"],
    }
):
    for key in keys:
        if candidate in options[key]:
            return True
    return False
