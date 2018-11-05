import sys

__version__ = '1.0.3'

if sys.version_info >= (3, 0):
    from mocodo_magic.mocodo_magic import *
else:
    from mocodo_magic import *

__all__ = ['mocodo_magic']
