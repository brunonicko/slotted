def mangle(name, owner_name):
    # type: (str, str) -> str
    if name.startswith("__") and not name.endswith("__"):
        return "_{}{}".format(owner_name.lstrip("_"), name)
    return name
