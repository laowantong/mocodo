from pathlib import Path
from importlib import import_module

__version__ = "4.2.13"
SCRIPT_DIRECTORY = Path(__file__).resolve().parent


def load_ipython_extension(ipython):
    # This function is called when the extension is loaded in a notebook
    # with %load_ext mocodo or %reload_ext mocodo.
    mocodo = import_module("mocodo.magic").mocodo
    ipython.register_magic_function(mocodo, 'line_cell', 'mocodo')
    print(f"Mocodo {__version__} loaded.")
