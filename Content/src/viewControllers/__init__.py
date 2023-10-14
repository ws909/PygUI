import pygame

import PygUI

from PygUI.UI.viewControllers import UIViewController
from PygUI.UI.viewControllers import UIScrollViewController
from PygUI.UI.viewControllers import UIScrollMenuViewController

from PygUI.UI.accesories import Orientation
from PygUI.UI.accesories import Click
from PygUI.UI.accesories import Transform
from PygUI.UI.accesories import UIButton
from PygUI.UI.accesories import UIText
from PygUI.UI.accesories import UIInteractiveText
from PygUI.UI.accesories import UIImage
from PygUI.UI.accesories import Fonts

import Content


class HomeViewController(UIViewController):

    _test_button: UIButton
    _test_button2: UIButton

    _background: list

    def __init__(self, surface: pygame.Surface):
        UIViewController.__init__(self, surface)

        self._background = (255, 180, 50)
        self._test_button = UIButton(text="mhm")
        self._test_button.size = [200, 300, 80, 40]
        self._test_button.color = (140, 140, 140)

        self._test_button2 = UIButton()
        self._test_button2.size = (500, 200, 110, 60)
        self._test_button2.color = (40, 40, 40)
        self._test_button2.highlight_color = (250, 250, 250)
        self._test_button2.command = self.write
        PygUI.Notifications.beep(5)

    def __del__(self):
        UIViewController.__del__(self)
        del self._test_button
        del self._test_button2

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        self.surface.fill(self._background)
        self._test_button.render(self.surface)
        self._test_button2.render(self.surface)

    def update(self, x, y, delta: float):
        self._test_button.move(int(1 * (delta / 10)), 0)
        self._test_button.update(x, y)
        self._test_button2.update(x, y)

    # ------------------------------------------------------------------------------------------------------------------
    # Private functions

    def write(self):
        print("Did someone say mhm?")


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class SecondViewController(UIViewController):

    _text: UIText
    _test_button: UIButton
    _text_block: UIInteractiveText

    def __init__(self, surface: pygame.Surface):
        UIViewController.__init__(self, surface)
        self._text = UIText()
        self._text.position = [100, 200]
        self._text.horizontal_alignment = Orientation.Right
        self._text.text_color = [0, 0, 0]
        self._text.text = "Look at me! I'm some lovely text!"

        self._test_button = UIButton()
        self._test_button.size = [300, 320, 90, 50]
        self._test_button.command = self.click
        self._test_button.click_type = Click.press

        self._text_block = UIInteractiveText()
        self._text_block.position = [200, 400]
        self._text_block.horizontal_alignment = Orientation.Center
        self._text_block.text_color = [0, 0, 0]
        self._text_block.text = "..."

    def __del__(self):
        UIViewController.__del__(self)
        del self._text
        del self._test_button

    # ------------------------------------------------------------------------------------------------------------------

    def on_navigated(self):
        self.surface.fill((255, 255, 255))
        self._text.render(self.surface)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        self.surface.fill((255, 255, 255))  # Remake this, so only the portion where the text was deleted, will redraw.
        self._test_button.render(self.surface)
        self._text_block.render(self.surface)

    def update(self, x, y, delta: float):
        self._test_button.update(x, y)

    # ------------------------------------------------------------------------------------------------------------------

    def update_dimensions(self, dimensions: [2]):
        UIViewController.update_dimensions(self, dimensions)
        self.on_navigated()

    # ------------------------------------------------------------------------------------------------------------------
    # Private functions

    def click(self):
        print("clicked")


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class ThirdViewController(UIScrollViewController):

    title: UIText
    image: UIImage

    def __init__(self, surface: pygame.Surface):
        UIScrollViewController.__init__(self, surface)
        self.direction = Orientation.Horizontal

        self.title = UIText()
        self.title.position = [160, 80]
        self.title.text_color = [255, 255, 255]
        self.title.text = "HUB"
        self.title.font = Fonts.get("monospace", 60)
        self.title.horizontal_alignment = Orientation.Right

        self.image = UIImage(image=Content.get_path() + "/assets/image.png")
        self.image.size = (160, 160, 500, 300)

    def __del__(self):
        UIScrollViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def on_navigated(self):
        self.scroll_surface = pygame.Surface((self.surface.get_width() + 1200, self.surface.get_height()))
        self.scroll_surface.fill((20, 20, 20))
        self.image.render(self.scroll_surface)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        UIScrollViewController.render(self)
        self.title.render(self.surface)

    def update(self, x, y, delta: float):
        UIScrollViewController.update(self, x, y, delta)

    # ------------------------------------------------------------------------------------------------------------------

    def update_dimensions(self, dimensions: [2]):
        UIScrollViewController.update_dimensions(self, dimensions)
        self.on_navigated()

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class FourthViewController(UIViewController):

    _background: [3]

    def __init__(self, surface: pygame.Surface):
        UIViewController.__init__(self, surface)
        self._background = [0, 255, 0]
        self.menu = UIScrollMenuViewController(self.surface)
        self.menu.title.font = Fonts.get("monospace", 50)
        self.menu.on_navigated()

        PygUI.Notifications.notify("PygUI", "You just entered the fourth view controller", True)

        decoded = PygUI.Notifications.decode(PygUI.Notifications.notifications[-1])
        encoded = PygUI.Notifications.encode(decoded)

        print("decoded =", decoded)
        print("encoded =", encoded)

    def __del__(self):
        UIViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        self.surface.fill(self._background)
        self.menu.render()

    def update(self, x, y, delta: float):
        self.menu.update(x, y, delta)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class FifthViewController(UIScrollViewController):

    button: UIButton

    def __init__(self, surface: pygame.Surface):
        UIScrollViewController.__init__(self, surface)

        self.direction = Orientation.Horizontal

        self.button = UIButton()
        self.button.size = [100, 200, 120, 80]
        self.button.color = [100, 200, 120]

    def __del__(self):
        UIScrollViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def on_navigated(self):
        self.set_surface()

    def did_resize(self, _):
        self.set_surface()

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        self.button.render(self.scroll_surface)
        UIScrollViewController.render(self)

    def update(self, x, y, delta: float):
        UIScrollViewController.update(self, x, y, delta)
        self.button.update(x - self.x, y - self.y)

    # ------------------------------------------------------------------------------------------------------------------

    def set_surface(self):
        self.scroll_surface = pygame.Surface((self.surface.get_width() + 1200, self.surface.get_height()))
        Transform.combine_colors(self.scroll_surface, (255, 255, 0), (0, 100, 0), Orientation.Vertical)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class ScrollViewController(UIScrollViewController):

    button: UIButton

    def __init__(self, surface: pygame.Surface):
        UIScrollViewController.__init__(self, surface)

        self.button = UIButton()
        self.button.size = [100, 200, 120, 80]
        self.button.color = [100, 200, 120]

    def __del__(self):
        UIScrollViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def on_navigated(self):
        self.scroll_surface = pygame.Surface((self.surface.get_width() + 200, self.surface.get_height() + 1200))
        Transform.combine_colors(self.scroll_surface, (255, 255, 0), (0, 100, 0), Orientation.Horizontal)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        self.button.render(self.scroll_surface)
        UIScrollViewController.render(self)

    def update(self, x, y, delta: float):
        UIScrollViewController.update(self, x, y, delta)
        self.button.update(x - self.x, y - self.y)
