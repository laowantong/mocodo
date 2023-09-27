import importlib
from time import time
from mocodo.mocodo_error import subarg_error

def run(source, subargs, **kargs):
    algo = subargs.get("algo", "bb")
    try:
        module = importlib.import_module(f".rewrite.arrange_{algo}", package="mocodo")
    except ModuleNotFoundError:
        raise subarg_error("algo", algo)
    timeout = subargs.get("timeout")
    if timeout is None:
        has_expired = lambda: False
    else:
        try:
            timeout = time() + float(timeout)
            has_expired = lambda: time() > timeout
        except Exception:
            raise subarg_error("timeout", timeout)
    return module.arrange(source, subargs, has_expired)
