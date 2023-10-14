"""
PygUI is a high-level module for use on top of Pygame. It features user interface view controllers,
and a set of different UI labels, which make it easy to build apps.
For more info, use PygUI.info.get_info("PygUI")
"""

import sys
import warnings

__author__ = "Andreas Ormevik Jansen"
__copyright__ = None
__credits__ = ["Andreas Ormevik Jansen"]

__license__ = "LGPL"
__version__ = "1.0.1"
__maintainer__ = "Andreas Ormevik Jansen"


if __name__ == "__main__":
    sys.exit()

# Module imports

_missing_modules = list()


# Required modules

try:
    from PygUI.utilities import *
except (ImportError, IOError):
    _missing_modules.append("utilities")

try:
    import PygUI.maths as maths
except (ImportError, IOError):
    _missing_modules.append("maths")

try:
    from PygUI.UI.accesories import *
except (ImportError, IOError):
    _missing_modules.append("UI.accesories")

try:
    from PygUI.UI.viewControllers import *
except (ImportError, IOError):
    _missing_modules.append("UI.viewControllers")


# Exit if imports failed
if _missing_modules:
    error = "couldn't import: "
    for m in _missing_modules:
        error += m
        error += ", "

    error = error[:-2]
    raise ImportError(error)


# Standard modules

try:
    import PygUI.info as info
except (ImportError, IOError):
    _missing_modules.append("info")

try:
    from PygUI.additions import Notifications as Notifications
    Notifications.init()
except (ImportError, IOError):
    _missing_modules.append("Notifications")

try:
    import PygUI.file as file
except (ImportError, IOError):
    _missing_modules.append("file")


# Warn if imports failed
if _missing_modules:
    error = "couldn't import "
    for m in _missing_modules:
        error += m
        error += ", "

    error = error[:-2]
    warnings.warn(error)

del sys
del warnings
