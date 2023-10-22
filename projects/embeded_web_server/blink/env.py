"""Module for loading and retrieving enviromental variables."""


_env_variables = {}
_env_variables_path = "/.env"
_env_loaded = False


def set_env_path(path):
    """Path for the file to source enviromental varibles from."""
    global _env_variables_path
    _env_variables_path = path


def _load_envs(path=None):
    if path is None:
        path = _env_variables_path
    env_vars = {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.rstrip() for line in file]
    except OSError:
        raise OSError(f"No file with path '{path}'")

    for line in lines:
        if line.startswith("#"):
            continue
        key, val = line.split("=")
        env_vars[key.strip()] = val.strip()
    return env_vars


def getenv(var: str) -> str:
    """Return enviromental variable with name 'var'."""
    global _env_loaded, _env_variables

    if not _env_loaded:
        _env_variables = _load_envs()
        _env_loaded = True

    value = _env_variables.get(var, None)
    if value is None:
        raise ValueError(f"Enviromental variable '{var}' was not set")
    return value
