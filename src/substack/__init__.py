from substack.version import VERSION, VERSION_NAME

__version__ = VERSION


def hello() -> str:
    return f"Welcome to substack-python - {VERSION_NAME} : {VERSION}!"
