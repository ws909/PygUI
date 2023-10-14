import pygame as _pygame
from pygame.locals import *

from PygUI.event import EventHandler as _EventHandler
from PygUI.utilities import minimum as _minimum


class DisplayHandler:

    _monitor: _pygame.display.Info
    display: _pygame.Surface or _pygame.SurfaceType

    width: int
    height: int

    title: str

    def __init__(self, **kwargs):
        self._monitor = _pygame.display.Info()

        self.width:  int = int(self._monitor.current_w - 40)
        self.height: int = int((self.width / 10) * 5.5)

        self.minimum_width:  int = 0
        self.minimum_height: int = 0

        self.display = None
        self.title = None
        self.flags = RESIZABLE | HWSURFACE | HWACCEL | DOUBLEBUF

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError("Invalid keyword: {}".format(key))

    def __del__(self):
        self.clear()

    # ------------------------------------------------------------------------------------------------------------------

    def clear(self):
        print("Cleaning DisplayHandler: " + self.__str__())
        del self.display

    def rebuild(self):
        self._monitor = _pygame.display.Info()
        self.width:  int = self._monitor.current_w - 40
        self.height: int = int((self.width / 10) * 5.5)
        self.display = None

    # ------------------------------------------------------------------------------------------------------------------

    def resize(self, event):

        self.width  = _minimum(self.minimum_width,  event.w)
        self.height = _minimum(self.minimum_height, event.h)

        _pygame.display.set_caption(self.title)
        self.display = _pygame.display.set_mode((self.width, self.height), self.flags)
        self.display.convert()
        self.display.set_alpha(None)

    # ------------------------------------------------------------------------------------------------------------------

    def set_display(self, title: str, width: int = None, height: int = None):
        if self.display is not None:
            self.close_display()

        _pygame.display.init()

        self.title = title if title is not None else self.title if self.title is not None else ""

        self.width = width if width is not None else self.width
        self.height = height if height is not None else self.height

        _pygame.display.set_caption(title)

        self.display = _pygame.display.set_mode((self.width, self.height), self.flags)
        self.display.convert()
        self.display.set_alpha(None)

        _EventHandler.callbacks.add.window_resize(self.resize)

    def close_display(self):
        self.display = None
        _pygame.display.quit()
        _EventHandler.callbacks.remove.window_resize(self.resize)

    def update(self):
        _pygame.display.flip()
