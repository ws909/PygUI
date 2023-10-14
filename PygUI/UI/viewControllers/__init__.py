"""
UIViewControllers are User-Interface Controllers that can either be directly used, or inherited from.
"""

from abc import ABC, abstractmethod

import pygame as _pygame

from PygUI.event import EventHandler as _EventHandler
from PygUI.UI.accesories import Orientation as _Orientation
from PygUI.UI.accesories import UITabBar as _UITabBar
from PygUI.UI.accesories import UIText as _UIText
from PygUI.UI.accesories import UIButton  # TODO: temporary
from PygUI.utilities import *  # TODO: change this
from PygUI.maths import *  # TODO: change this
import PygUI.info as _info


class UIViewController(_info.InfoGetter, ABC):

    surface: _pygame.Surface

    def __init__(self, surface: _pygame.Surface):
        self.surface = surface

        self.connect()

    def __del__(self):
        print("Cleaning UIViewController: " + self.__str__())

        self.disconnect()

    # ------------------------------------------------------------------------------------------------------------------

    def connect(self):
        overridden = overridden_methods(self, UIViewController, "did_update", "did_resize")

        try:
            if "did_update" in overridden:
                _EventHandler.callbacks.add.update(self.did_update)

            if "did_resize" in overridden:
                _EventHandler.callbacks.add.window_resize(self.did_resize)

        except ValueError:
            pass  # Event handling has been manually set up

    def disconnect(self):
        overridden = overridden_methods(self, UIViewController, "did_update", "did_resize")

        try:
            if "did_update" in overridden:
                _EventHandler.callbacks.remove.update(self.did_update)

            if "did_resize" in overridden:
                _EventHandler.callbacks.remove.window_resize(self.did_resize)

        except ValueError:
            pass  # Event handling has been manually set up, or the app is quitting

    # ------------------------------------------------------------------------------------------------------------------

    def on_navigated(self):
        """Called after navigation, if navigated to by instantiate_view_controller()"""

    def did_navigate(self):
        """Called after on_navigated, if navigated to by instantiate_view_controller()"""

    def did_resize(self, _):
        """Called after resizing"""

    def did_update(self):
        """Called at the end of the run loop"""

    # ------------------------------------------------------------------------------------------------------------------

    def instantiate_view_controller(self, view_controller: object):  # TODO: find a way to have view_controller be self
        pass

    def update_dimensions(self, dimensions: [2]):
        dimensions[0] = minimum(0, dimensions[0] if dimensions[0] is not None else self.surface.get_width())
        dimensions[1] = minimum(0, dimensions[1] if dimensions[1] is not None else self.surface.get_height())
        self.surface = _pygame.transform.scale(self.surface, dimensions)

    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def render(self):
        """Call from program loop to render ViewController"""
        pass

    @abstractmethod
    def update(self, x: int, y: int, delta: float):
        """Call from program loop to update ViewController"""
        pass

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class UITabBarViewController(UIViewController, _info.InfoGetter):

    _tab_bar: _UITabBar
    _view_controllers: list

    _view_controller: UIViewController

    _view_controller_surface: _pygame.Surface

    def __init__(self, surface: _pygame.Surface, tab_bar_items: list, **tab_bar_kwargs):
        super().__init__(surface)
        tb_height = 80

        for key, value in tab_bar_kwargs.items():
            if key == "height":
                tb_height = value
                tab_bar_kwargs.pop(key)
                break

        self._view_controller_surface = _pygame.Surface((surface.get_width(), surface.get_height() - tb_height))

        self._view_controllers = list()

        for i in range(0, tab_bar_items.__len__()):
            if tab_bar_items[i].initialized:
                self._view_controllers.append(tab_bar_items[i].command(self._view_controller_surface))
            else:
                self._view_controllers.append(tab_bar_items[i].command)
            tab_bar_items[i].command_parameters.append(i)
            tab_bar_items[i].command = self.instantiate_view_controller

        self._tab_bar = _UITabBar(_pygame.Surface((surface.get_width(), tb_height)), tab_bar_items, **tab_bar_kwargs)
        self._view_controller = None
        self.instantiate_view_controller(0)

    def __del__(self):
        del self._tab_bar
        del self._view_controller
        del self._view_controllers

        UIViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        self._view_controller.render()
        self._tab_bar.render()
        self.surface.blit(self._tab_bar.surface, (0, 0))
        self.surface.blit(self._view_controller.surface, (0, self._tab_bar.surface.get_height()))

    def update(self, x, y, delta: float):
        self._tab_bar.update(x, y)
        self._view_controller.update(x, y + self._tab_bar.surface.get_height(), delta)

    # ------------------------------------------------------------------------------------------------------------------

    def instantiate_view_controller(self, view_controller: UIViewController or int):
        if isinstance(view_controller, int):
            view_controller = self._view_controllers[view_controller]
        try:
            if isinstance(self._view_controller, view_controller):
                return
        except TypeError:
            pass

        try:
            self._view_controller = view_controller(self._view_controller_surface)
        except TypeError:
            self._view_controller = view_controller

        self._view_controller.on_navigated()
        self._view_controller.did_navigate()

    # ------------------------------------------------------------------------------------------------------------------

    def did_resize(self, event):
        self.update_dimensions([event.w, event.h])

    def update_dimensions(self, dimensions: [2]):
        dimensions[0] = dimensions[0] if dimensions[0] is not None else self.surface.get_width()
        dimensions[1] = dimensions[1] if dimensions[1] is not None else self.surface.get_height()
        self.surface = _pygame.transform.scale(self.surface, dimensions)
        self._tab_bar.update_dimensions([dimensions[0], None])

        self._view_controller_surface = _pygame.transform.scale(
            self._view_controller_surface,
            (dimensions[0], minimum(0, dimensions[1] - self._tab_bar.surface.get_height())))

        self._view_controller.update_dimensions([dimensions[0], dimensions[1] - self._tab_bar.surface.get_height()])

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class UIScrollViewController(UIViewController, _info.InfoGetter, ABC):

    scroll_surface: _pygame.Surface

    horizontal_scrolling: bool  # Issue with horizontal scrolling. Until issue is fixed, this variable is not for use
    vertical_scrolling: bool    # Issue with horizontal scrolling. Until issue is fixed, this variable is not for use
    direction: _Orientation      # Because of issue with horizontal scrolling from pygame.mouse, this is to be used

    x: int  # Horizontal scroll
    y: int  # Horizontal scroll
    scroll_intensity: float

    # Shared scroller values
    scroller_color: [3]
    scroller_background_color: [3]
    scroller_highlight_color: [3]
    scroller_background_width: int
    scroller_width: int
    scroller_visibility: int  # 0 = never, 1 = on surface focus, 2 = on scrolling, 3 = always
    scroller_mode: int  # 0 = invisible, 1 = panning, 2 = full

    # Vertical scroller
    _vertical_scroller_size: [4]
    _vertical_scroller_active_color: [3]
    _vertical_scroller_within: bool
    _vertical_scroller_drag: bool
    _vertical_scroller_mouse_position: int
    _vertical_scroller_visible: bool

    # Horizontal scroller
    _horizontal_scroller_size: [4]
    _horizontal_scroller_active_color: [3]
    _horizontal_scroller_within: bool
    _horizontal_scroller_drag: bool
    _horizontal_scroller_mouse_position: int
    _horizontal_scroller_visible: bool

    def __init__(self, surface: _pygame.Surface):
        super().__init__(surface)
        self.scroll_surface = _pygame.Surface((surface.get_width(), surface.get_height()))
        # self.horizontal_scrolling = False
        # self.vertical_scrolling = False
        self.direction = _Orientation.Vertical
        self.x = 0
        self.y = 0
        self.scroll_intensity = 3.0

        # Shared scroller values
        self.scroller_color = (80, 80, 80)
        self.scroller_background_color = (200, 200, 200)
        self.scroller_highlight_color = [130, 130, 130]
        self.scroller_background_width = 24
        self.scroller_width = 16
        self.scroller_timeout = 600
        self.scroller_visibility = 2  # 3  # 0 = never, 1 = on surface focus, 2 = on scrolling, 3 = always
        # TODO: set up functionality of these. That includes a new panning mode. Defaults: 2, 1
        # self.scroller_mode = 2  # 0 = invisible, 1 = panning, 2 = full

        # Vertical scroller
        self._vertical_scroller_size = [0, 0, 0, 0]
        self._vertical_scroller_background_size = [0, 0, 0, 0]
        self._vertical_scroller_active_color = self.scroller_color
        self._vertical_scroller_within = False
        self._vertical_scroller_drag = False
        self._vertical_scroller_mouse_position = 0
        self._vertical_scroller_visible = False
        self._vertical_scroller_visibility_timeout = 0

        # Horizontal scroller
        self._horizontal_scroller_size = [0, 0, 0, 0]
        self._horizontal_scroller_background_size = [0, 0, 0, 0]
        self._horizontal_scroller_active_color = self.scroller_color
        self._horizontal_scroller_within = False
        self._horizontal_scroller_drag = False
        self._horizontal_scroller_mouse_position = 0
        self._horizontal_scroller_visible = False
        self._horizontal_scroller_visibility_timeout = 0

        # new:

        self._x_offset = 0
        self._y_offset = 0

        self._delta = 0

        self.length = 0

        # Callback setup
        try:
            _EventHandler.callbacks.add.window_resize(self.resize)

            _EventHandler.callbacks.add.mouse_motion(self._mouse_motion)
            _EventHandler.callbacks.add.mouse_press(self._mouse_press)
            _EventHandler.callbacks.add.mouse_button_down(self._mouse_button_down)
            _EventHandler.callbacks.add.mouse_button_up(self._mouse_button_up)

        except ValueError:
            pass  # EventHandler wasn't set up.

        # Current problems:
            # Scroller colour not highlighted when the mouse goes off, with mouse pressed.
            # Scrollers become smaller after each resize. This is due to to subtracting a certain self.length value.
            # Missing ways of change the behaviour, from the client's side.

            # There should be a UIScroller class. When one side isn't active, it should be released. When the widths
            # comply, the scroller should be remade. Do this in the 'resize()' function.

            # A possible solution, would be to dynamically set callbacks.

    def __del__(self):
        del self.scroll_surface

        try:
            _EventHandler.callbacks.remove.window_resize(self.resize)

            _EventHandler.callbacks.remove.mouse_motion(self._mouse_motion)
            _EventHandler.callbacks.remove.mouse_press(self._mouse_press)
            _EventHandler.callbacks.remove.mouse_button_down(self._mouse_button_down)
            _EventHandler.callbacks.remove.mouse_button_up(self._mouse_button_up)

        except ValueError:
            pass  # As in every other deinit, this fails if the program quits. TODO: find out why.

        UIViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def did_navigate(self):
        self.resize(None)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        """First render to self.scroll_surface, then UIScrollViewController.render(self), then self.surface"""
        self.surface.blit(self.scroll_surface, (self.x, self.y))

        # Vertical scroller
        if self._vertical_scroller_visible:
            _pygame.draw.rect(self.surface, self.scroller_background_color, self._vertical_scroller_background_size)
            _pygame.draw.rect(self.surface, self._vertical_scroller_active_color, self._vertical_scroller_size)

        # Horizontal scroller
        if self._horizontal_scroller_visible:
            _pygame.draw.rect(self.surface, self.scroller_background_color, self._horizontal_scroller_background_size)
            _pygame.draw.rect(self.surface, self._horizontal_scroller_active_color, self._horizontal_scroller_size)

    def resize(self, _):

        del self._vertical_scroller_background_size
        del self._horizontal_scroller_background_size

        v = [None] * 4
        h = [None] * 4

        v[0] = self.surface.get_width() - self.scroller_background_width
        v[1] = 0
        v[2] = self.scroller_background_width
        v[3] = self.surface.get_height()

        h[0] = 0
        h[1] = self.surface.get_height() - self.scroller_background_width
        h[2] = self.surface.get_width()
        h[3] = self.scroller_background_width

        self._vertical_scroller_background_size = v
        self._horizontal_scroller_background_size = h

        self._build_scroller()

    def _build_scroller(self):

        del self._vertical_scroller_size
        del self._horizontal_scroller_size

        vertical   = self.surface.get_height() >= self.scroll_surface.get_height()
        horizontal = self.surface.get_width()  >= self.scroll_surface.get_width()

        length = self.scroller_background_width if not vertical and not horizontal else 0

        scroller_start = self.scroller_background_width - (self.scroller_background_width - self.scroller_width) / 2

        v = [None] * 4
        h = [None] * 4

        v[0] = self.surface.get_width() - scroller_start
        v[1] = -(self.y / (self.scroll_surface.get_height() / self.surface.get_height()))
        v[2] = self.scroller_width
        v[3] = (self.surface.get_height() * (self.surface.get_height() / self.scroll_surface.get_height())) - length

        h[0] = -(self.x / (self.scroll_surface.get_width() / self.surface.get_width()))
        h[1] = self.surface.get_height() - scroller_start
        h[2] = (self.surface.get_width() * (self.surface.get_width() / self.scroll_surface.get_width())) - length
        h[3] = self.scroller_width

        self._vertical_scroller_size = v
        self._horizontal_scroller_size = h

        self.length = length

    def _evaluate_scroller(self):

        length = self.length

        a = [None] * 4

        a[0] = -(self.x / (self.scroll_surface.get_width() / self.surface.get_width()))
        a[1] = -(self.y / (self.scroll_surface.get_height() / self.surface.get_height()))
        a[2] = (self.surface.get_width()  * (self.surface.get_width()  / self.scroll_surface.get_width()))  - length
        a[3] = (self.surface.get_height() * (self.surface.get_height() / self.scroll_surface.get_height())) - length

        self._vertical_scroller_size[1] = a[1]
        self._vertical_scroller_size[3] = a[3]

        self._horizontal_scroller_size[0] = a[0]
        self._horizontal_scroller_size[2] = a[2]

    def _mouse_press(self, event):
        if self._vertical_scroller_drag:

            y = event.pos[1] - self._y_offset - self._vertical_scroller_mouse_position

            scroll = -(y * (self.scroll_surface.get_height() / self.surface.get_height()))
            minimum_scroll = min(scroll, 0)
            self.y = max(minimum_scroll, 0 - self.scroll_surface.get_height() + self.surface.get_height())

            self._evaluate_scroller()

        elif self._horizontal_scroller_drag:

            x = event.pos[0] - self._x_offset - self._horizontal_scroller_mouse_position

            scroll = -(x * (self.scroll_surface.get_width() / self.surface.get_width()))
            minimum_scroll = min(scroll, 0)
            self.x = max(minimum_scroll, 0 - self.scroll_surface.get_width() + self.surface.get_width())

            self._evaluate_scroller()

    def _mouse_button_up(self, _):
        if not self._vertical_scroller_within:
            self._vertical_scroller_active_color = self.scroller_color

        elif not self._horizontal_scroller_within:
            self._horizontal_scroller_active_color = self.scroller_color

        self._vertical_scroller_drag = False
        self._horizontal_scroller_drag = False

    # Perhaps use this to make the scroller backgrounds clickable, to teleport the surface to that place.
    def _mouse_button_down(self, event):
        if event.button == 1:  # Left mouse button

            x = event.pos[0] - self._x_offset
            y = event.pos[1] - self._y_offset

            if within_rectangle(x, y, self._vertical_scroller_size):
                self._vertical_scroller_drag = True
                self._vertical_scroller_mouse_position = y - self._vertical_scroller_size[1]

            elif within_rectangle(x, y, self._horizontal_scroller_size):
                self._horizontal_scroller_drag = True
                self._horizontal_scroller_mouse_position = x - self._horizontal_scroller_size[0]

        if event.button == 4:
            # Drag down
            move = self.scroll_intensity * self._delta

            if self.direction == _Orientation.Vertical:
                self.y = min(self.y + move, 0)
                self._vertical_scroller_visibility_timeout = self.scroller_timeout
            else:
                self.x = min(self.x + move, 0)
                self._horizontal_scroller_visibility_timeout = self.scroller_timeout

        elif event.button == 5:
            # Drag up
            move = self.scroll_intensity * self._delta

            if self.direction == _Orientation.Vertical:
                self.y = max(self.y - move, 0 - self.scroll_surface.get_height() + self.surface.get_height())
                self._vertical_scroller_visibility_timeout = self.scroller_timeout
            else:
                self.x = max(self.x - move, 0 - self.scroll_surface.get_width() + self.surface.get_width())
                self._horizontal_scroller_visibility_timeout = self.scroller_timeout

        self._evaluate_scroller()

    def _mouse_motion(self, event):

        x = event.pos[0] - self._x_offset
        y = event.pos[1] - self._y_offset

        if within_rectangle(x, y, self._vertical_scroller_background_size):
            self._vertical_scroller_within = True

            if within_rectangle(x, y, self._vertical_scroller_size):
                self._vertical_scroller_active_color = self.scroller_highlight_color

            else:
                if not self._vertical_scroller_drag:
                    self._vertical_scroller_active_color = self.scroller_color

        else:
            self._vertical_scroller_within = False
            if not self._vertical_scroller_drag:
                self._vertical_scroller_active_color = self.scroller_color

        if within_rectangle(x, y, self._horizontal_scroller_background_size):
            self._horizontal_scroller_within = True

            if within_rectangle(x, y, self._horizontal_scroller_size):
                self._horizontal_scroller_active_color = self.scroller_highlight_color

            else:
                if not self._horizontal_scroller_drag:
                    self._horizontal_scroller_active_color = self.scroller_color

        else:
            self._horizontal_scroller_within = False
            if not self._horizontal_scroller_drag:
                self._horizontal_scroller_active_color = self.scroller_color

    def update(self, x: int, y: int, delta: float):

        self._x_offset = x
        self._y_offset = y

        self._delta = delta

        self._vertical_scroller_visibility_timeout = max(self._vertical_scroller_visibility_timeout - delta, 0)
        self._horizontal_scroller_visibility_timeout = max(self._horizontal_scroller_visibility_timeout - delta, 0)

        self._vertical_scroller_visible  = self._vertical_scroller_visibility_timeout > 0
        self._vertical_scroller_visible |= self._vertical_scroller_within
        self._vertical_scroller_visible |= self._vertical_scroller_drag
        self._vertical_scroller_visible &= self.surface.get_height() < self.scroll_surface.get_height()

        self._horizontal_scroller_visible  = self._horizontal_scroller_visibility_timeout > 0
        self._horizontal_scroller_visible |= self._horizontal_scroller_within
        self._horizontal_scroller_visible |= self._horizontal_scroller_drag
        self._horizontal_scroller_visible &= self.surface.get_width() < self.scroll_surface.get_width()

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class UIScrollMenuViewController(UIScrollViewController, _info.InfoGetter):

    title: _UIText
    background: [3]
    side: _Orientation.Right or _Orientation.Left

    def __init__(self, surface: _pygame.Surface, **kwargs):
        UIScrollViewController.__init__(self, surface)
        # self.parent_surface = self.surface

        self.title = _UIText()
        self.title.text = "title"
        self.background = (50, 50, 50)
        self.width = 400
        self.side = _Orientation.Right
        self.x = self.surface.get_width() - self.width
        self.scroll_surface = _pygame.Surface((self.width, self.surface.get_height() + 1000))

        self.test_button = UIButton()

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError("Invalid keyword: {}".format(key))

        # self.surface = pygame.Surface((self.width, self.parent_surface.get_height()))

    # ------------------------------------------------------------------------------------------------------------------

    def on_navigated(self):
        self.scroll_surface.fill(self.background)
        self.test_button.render(self.scroll_surface)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        UIScrollViewController.render(self)
        self.title.render(self.surface)
        # self.parent_surface.blit(self.surface, (0, 0))

    def update(self, x, y, delta):
        UIScrollViewController.update(self, x, y, delta)
        self.title.position = (self.scroll_surface.get_width() - self.width / 2, 40)

    # ------------------------------------------------------------------------------------------------------------------

    def update_dimensions(self, dimensions: [2]):
        UIScrollViewController.update_dimensions(self, dimensions)
        self.on_navigated()
