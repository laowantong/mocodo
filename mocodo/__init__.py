import importlib

def load_ipython_extension(ipython):
    # This function is called when the extension is loaded in a notebook
    # with %load_ext mocodo or %reload_ext mocodo.

    mocodo = importlib.import_module("mocodo.magic_command").mocodo
    ipython.register_magic_function(mocodo, 'line_cell', 'mocodo')
    
    pkg_resources = importlib.import_module("pkg_resources")

    try:
        MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
    except pkg_resources.DistributionNotFound:
        MOCODO_VERSION = "(unknown version)"  # For tests during CI
    print(f"Mocodo {MOCODO_VERSION} loaded.")
