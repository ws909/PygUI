"""
Info about PygUI and its parts
"""

import warnings
from enum import Enum
from abc import ABC


class Info(Enum):
    All = ""
    PygUI = ""

    # PygUI.UI.accesories
    Orientation = ""
    Click = ""
    Fonts = ""
    UILabel = ""
    Style = ""
    UITabBarItem = ""
    UITabBar = ""
    UIButton = ""
    UIImageButton = ""  # TODO: construct
    UIText = ""
    UITextBlock = ""
    UIInteractiveTextBlock = ""  # TODO: construct
    UIImage = "This is the UIImage description"
    UIInteractiveImage = ""  # TODO: construct

    # PygUI.UI.viewControllers:
    UIViewController = ""
    UITabBarViewController = ""
    UIScrollViewController = ""


class InfoGetter(ABC):
    @classmethod
    def info(cls, write: bool = True) -> str:
        description = getattr(Info, cls.__name__).value

        print(description) if write else None

        return description


def get_info(name: str or object, write: bool = True) -> str or None:
    if not isinstance(name, str):
        name = name.__name__

    try:
        value = getattr(Info, name).value
        print(value) if write else None
        return value
    except AttributeError:
        warnings.warn("AttributeError: name '" + name + "' not defined")
        return
