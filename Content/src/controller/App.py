import time

import pygame

from Content.src.viewControllers import FifthViewController
from Content.src.viewControllers import FourthViewController
from Content.src.viewControllers import HomeViewController
from Content.src.viewControllers import ScrollViewController
from Content.src.viewControllers import SecondViewController
from Content.src.viewControllers import ThirdViewController
from DisplayHandler import DisplayHandler
from PygUI.UI.accesories import Fonts
from PygUI.UI.accesories import UITabBarItem
from PygUI.UI.viewControllers import UITabBarViewController
from PygUI.UI.viewControllers import UIViewController
from PygUI.additions import Notifications
from PygUI.event import EventHandler
from PygUI.time import Clock

__author__ = "Andreas Ormevik Jansen"
__copyright__ = None
__credits__ = ["Andreas Ormevik Jansen"]

__license__ = None
__version__ = "1.1.0"
__maintainer__ = "Andreas Ormevik Jansen"


class App:

    _displayHandler: DisplayHandler
    _clock: Clock

    _name: str = "App"
    _LPS: int = 30  # Loops per second: "run()" loop
    _active: bool

    _view_controller: UIViewController

    def __init__(self):
        print("App launching")
        pygame.init()

        # Set up event handling
        EventHandler.init()

        # Set up rendering class, and build a display
        self._displayHandler = DisplayHandler()
        self._displayHandler.set_display(self._name)

        # Set up a clock
        self._clock = Clock()

        # Set up a font
        Fonts.add("monospace", 40)

        # Set up UI
        self._initialize_user_interface()

        # Run application
        print("App launched\n")
        self._active = True
        self._run()

    def __del__(self):
        print("App exiting")
        del self._clock
        del self._displayHandler
        del self._view_controller
        Notifications.flush()
        pygame.quit()
        print("App exited\n")

    # ------------------------------------------------------------------------------------------------------------------

    def _initialize_user_interface(self):
        items: [UITabBarItem] = [
            UITabBarItem("Home", HomeViewController),
            UITabBarItem("Second", SecondViewController),
            UITabBarItem("Third", ThirdViewController),
            UITabBarItem("Fourth", FourthViewController),
            UITabBarItem("Fifth", FifthViewController),
            UITabBarItem("Scroll", ScrollViewController)
        ]
        
        self._view_controller = UITabBarViewController(
            pygame.Surface((self._displayHandler.width, self._displayHandler.height)),
            items,
            height=80,
            font=Fonts.get("monospace", 40),
            highlight_color=(180, 180, 180),
            text_highlight_color=(0, 0, 0),
            color=(40, 40, 40),
            text_color=(255, 255, 255)
        )

    # ------------------------------------------------------------------------------------------------------------------

    def _handle_events(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._active = False

    # ------------------------------------------------------------------------------------------------------------------

    # noinspection PyArgumentList
    def _run(self):

        EventHandler.callbacks.add.any(self._handle_events)

        while self._active and pygame.display.get_active():

            self._clock.synchronize_loop(self._LPS)

            # ----------------------------------------------------------------------------------------------------------

            # Input

            EventHandler.update()

            # ----------------------------------------------------------------------------------------------------------

            # Logic
            self._view_controller.update(0, 0, self._clock.delta)

            # ----------------------------------------------------------------------------------------------------------

            # Rendering
            self._view_controller.render()
            self._displayHandler.display.blit(self._view_controller.surface, (0, 0))
            self._clock.render_lps(self._displayHandler.display)
            self._displayHandler.update()

            # ----------------------------------------------------------------------------------------------------------

        EventHandler.callbacks.remove.any(self._handle_events)

        if self._active:
            while self._active and not pygame.display.get_active():
                time.sleep(0.5)
                self._active = not pygame.event.get(pygame.QUIT)
            self._clock.restart()
            self._run()

        print("App ended run session\n")


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

app = App()
