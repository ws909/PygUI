from abc import ABC as _ABC
from enum import Enum as _Enum
import time as _time
import traceback as _traceback

import pygame as _pygame

from PygUI.utilities import weak as _weak
from PygUI.utilities import minimum as _minimum
from PygUI.utilities import maximum as _maximum
from PygUI.event import EventHandler as _EventHandler
from PygUI.maths import *

import PygUI.info as _info


# noinspection PyClassHasNoInit
class Orientation(_Enum):
    Top = 1
    Over = 1
    Bottom = 2
    Below = 2
    Left = 3
    Right = 4
    Center = 5
    Vertical = 6
    Horizontal = 7

    @staticmethod
    def info(write: bool = True):
        return _info.get_info(Orientation, write)


# noinspection PyClassHasNoInit
# Perhaps rename to 'Trigger', or 'TriggerType', or 'TriggerState'.sfv
class Click(_Enum):
    click = 1
    press = 2
    release = 3

    @staticmethod
    def info(write: bool = True):
        return _info.get_info(Click, write)


# noinspection PyClassHasNoInit
class MouseButton(_Enum):
    left = 1
    middle = 2
    right = 3
    scroll_up = 4
    scroll_down = 5
    none = 6

    @staticmethod
    def info(write: bool = True):
        return _info.get_info(MouseButton, write)

# ----------------------------------------------------------------------------------------------------------------------


class Fonts:
    fonts: [_pygame.font] = []

    @staticmethod
    def add(font_name: str, size: int) -> _pygame.font:
        for font in Fonts.fonts:
            if font[1] == font_name and font[2] == size:
                return font[0]
        font = _pygame.font.SysFont(font_name, size)
        Fonts.fonts.append((font, font_name, size))
        return font

    @staticmethod
    def get(font_name: str, size: int) -> _pygame.font:
        for font in Fonts.fonts:
            if font[1] == font_name and font[2] == size:
                return font[0]
        return Fonts.add(font_name, size)

    @staticmethod
    def info(write: bool = True) -> _pygame.font:
        return _info.get_info(Fonts, write)

# ----------------------------------------------------------------------------------------------------------------------


# noinspection PyClassHasNoInit
class UILabel(_ABC):

    @staticmethod
    def info(write: bool = True):
        return _info.get_info(UILabel, write)

# ----------------------------------------------------------------------------------------------------------------------


class Style:

    styles: dict = {}

    @staticmethod
    def new(name: str, target: UILabel.__class__, **properties):
        if Style.styles.get(name) is not None:
            raise KeyError("'" + name + "' already defined")

        initialized_target = target()
        for key, value in properties.items():
            if not hasattr(initialized_target, key):
                raise AttributeError("Existence of attribute in UILabel is absence: {}".format(key))

        del initialized_target
        Style.styles[name] = (target, properties)

    @staticmethod
    def get(name: str) -> dict:
        return Style.styles.get(name)[1]

    @staticmethod
    def update(name: str, **properties):
        if Style.styles.get(name) is None:
            raise KeyError("'" + name + "' not defined")

        for key, value in properties.items():
            if not hasattr(Style.styles.get(name)[0], key):
                raise AttributeError("Existence of attribute in UILabel is absence: {}".format(key))

        Style.styles.get(name[1]).update(properties)

    @staticmethod
    def info(write: bool = True):
        return _info.get_info(Style, write)

# ----------------------------------------------------------------------------------------------------------------------


class UITabBarItem(_info.InfoGetter):
    name: str
    command: object
    command_parameters: list
    initialized: bool

    def __init__(self, name: str, command: object, initialized: bool = False, command_parameters=None):
        self.name = name
        self.command = command
        self.command_parameters = command_parameters if command_parameters is not None else list()
        self.initialized = initialized

# ----------------------------------------------------------------------------------------------------------------------


class UITabBar(UILabel, _info.InfoGetter):
    surface: _pygame.Surface
    color: [3]
    _items: list

    def __init__(self, surface: _pygame.Surface, items: list, **kwargs):
        self.surface = surface
        self.color = (235, 235, 235)
        self.margin = (0, 0, 0, 0)  # (left, right, below, over) TODO: add
        self._items = list()

        forbidden_arguments = \
            ("size", "active_color", "command", "command_parameters", "click_type", "text", "_updated")
        for key, value in kwargs.items():
            if key == "color":
                setattr(self, key, value)
            elif key == "margin":
                setattr(self, key, value)
            elif key in forbidden_arguments:
                raise AttributeError("Forbidden access. Keyword: {}".format(key),
                                     "\n Allowed attributes: highlight_color: [3], "
                                     "execution_type: Click.On_Press or Click.Release, "
                                     "text_color: [3], "
                                     "font: pygame.Font")
        if kwargs.get("margin"):
            kwargs.pop("margin")

        self.surface = _pygame.transform.scale(self.surface,
                                               (self.surface.get_width(),
                                                self.surface.get_height() + self.margin[2] + self.margin[3]))

        items_size = items.__len__()
        item_length = (self.surface.get_width() - self.margin[1] - self.margin[0]) / items_size

        for i in range(0, items_size):

            button = UIButton(**kwargs)
            button.text = items[i].name
            button.command = items[i].command
            button.command_parameters = items[i].command_parameters
            button.size[1] = self.margin[3]
            button.size[3] = self.surface.get_height() - self.margin[2] - self.margin[3]
            button.size[0] = (item_length * i) + self.margin[0]
            button.size[2] = item_length
            button.color = None
            self._items.append(button)

    def __del__(self):
        print("Cleaning UITabBar: " + self.__str__())
        del self._items

    def render(self):
        self.surface.fill(self.color)
        for item in self._items:
            item.render(self.surface)

    def update(self, x: int, y: int):
        for item in self._items:
            item.update(x, y)

    # ------------------------------------------------------------------------------------------------------------------

    # TODO: set up EventHandler.window_resize callback
    def update_dimensions(self, dimensions: [2]):
        dimensions[0] = dimensions[0] if dimensions[0] is not None else self.surface.get_width()
        dimensions[1] = dimensions[1] if dimensions[1] is not None else self.surface.get_height()
        self.surface = _pygame.transform.scale(self.surface, (dimensions[0], dimensions[1]))
        items_size = self._items.__len__()
        item_length = (self.surface.get_width() - self.margin[1]) / items_size
        for i in range(0, items_size):
            self._items[i].size[1] = self.margin[3]
            self._items[i].size[3] = self.surface.get_height() - self.margin[2] - self.margin[3]
            self._items[i].size[0] = (item_length * i) + self.margin[0]
            self._items[i].size[2] = item_length


# TODO: clear the variable lists, to make the code more readable. Fix an error.
class UIButton(UILabel, _info.InfoGetter):

    size: [4]  # (x, y, width, height)
    color: [3]
    highlight_color: [3]
    _active_color: [3]
    _command: object
    command_parameters: list or dict
    click_type: Click
    click_button: MouseButton
    execution_type: Click  # TODO: add this behaviour. <On_Press, Release>
    text: str
    text_color: [3]
    text_highlight_color: [3]
    _active_text_color: [3]
    font: _pygame.font
    _updated: int

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, cmd):
        if cmd is None:
            self._command = None
            self._remove_callbacks()
        else:
            self._command = _weak(cmd)
            self._add_callbacks()

    @property  # Perhaps rename to 'trigger', 'trigger_button', or 'trigger_type'.
    def click_type(self):
        return self._click_type

    @click_type.setter
    def click_type(self, click: Click):

        self._remove_callbacks()
        self._click_type = click
        self._add_callbacks()

    @property
    def operative(self):
        return self._operative

    @operative.setter
    def operative(self, boolean: bool):
        try:
            if boolean and not self._operative:
                _EventHandler.callbacks.add.mouse_motion(self._mouse_motion)
                self._add_callbacks()

            if not boolean and self._operative:
                _EventHandler.callbacks.remove.mouse_motion(self._mouse_motion)
                self._remove_callbacks()

        except ValueError:
            pass

        self._operative = boolean

    def __init__(self, **kwargs):
        self.size = [0, 0, 90, 50]
        self.color = [235, 235, 235]
        self.highlight_color = [160, 160, 160]
        self._active_color = self.color
        self._command = None
        self.command_parameters: list = list()
        self.click_button: MouseButton = MouseButton.left
        self._click_type = Click.click
        self.text: str or None = None
        self.text_color = [25, 25, 25]
        self.text_highlight_color = [100, 100, 100]
        self._active_text_color = self.text_color
        self.font = _pygame.font.Font(_pygame.font.get_default_font(), 20)

        self._operative = True

        for key, value in kwargs.items():
            if key.startswith("_"):
                raise AttributeError("Invalid keyword: {}".format(key))

            elif hasattr(self, key):
                setattr(self, key, value)

            else:
                raise AttributeError("Invalid keyword: {}".format(key))

        self._x_offset: int = 0
        self._y_offset: int = 0

        b = self._operative
        self._operative = False
        self.operative = b

        # This doesn't solve the problem, because the button's parameters haven't been externally set yet.
        # Might need a new callback, that runs on the first loop, and then removes itself.
        self._mouse_motion(_pygame.event.Event(4, {
            "pos": _pygame.mouse.get_pos(),
            "rel": (0, 0),
            "buttons": _pygame.mouse.get_pressed()}))

    def __del__(self):
        print("Cleaning UIButton: " + self.__str__())

        self.operative = False

    # ------------------------------------------------------------------------------------------------------------------

    def render(self, surface: _pygame.Surface):
        _pygame.draw.rect(surface, self._active_color, self.size) if self._active_color is not None else None

        if self.text is not None:
            text = self.font.render(self.text, True, self._active_text_color)
            x = self.size[0] + (self.size[2] / 2) - self.font.size(str(self.text))[0] / 2
            y = self.size[1] + (self.size[3] / 2) - self.font.size(str(self.text))[1] / 2
            surface.blit(text, (x, y))

    # ------------------------------------------------------------------------------------------------------------------
    # TODO: rename these, keeping them private.

    def _remove_callbacks(self):
        try:
            if self._click_type == Click.click:
                _EventHandler.callbacks.remove.mouse_button_down(self._mouse_button_down)

            elif self._click_type == Click.release:
                _EventHandler.callbacks.remove.mouse_button_up(self._mouse_button_up)

            elif self._click_type == Click.press:
                _EventHandler.callbacks.remove.mouse_press(self._mouse_press)

        except ValueError:
            pass

    def _add_callbacks(self):
        if self._operative and self._command is not None and self.click_button != MouseButton.none:
            try:
                if self._click_type == Click.click:
                    _EventHandler.callbacks.add.mouse_button_down(self._mouse_button_down)

                elif self._click_type == Click.release:
                    _EventHandler.callbacks.add.mouse_button_up(self._mouse_button_up)

                elif self._click_type == Click.press:
                    _EventHandler.callbacks.add.mouse_press(self._mouse_press)

            except ValueError:
                pass

    # ------------------------------------------------------------------------------------------------------------------

    def _setup_callback(self):
        """
        <Event(4-MouseMotion {'pos': (280, 250), 'rel': (0, 2), 'buttons': (0, 0, 0)})>
        <Event(5-MouseButtonDown {'pos': (280, 250), 'button': 1})>
        """

    # ------------------------------------------------------------------------------------------------------------------

    def _mouse_press(self, event):
        if within_rectangle(event.pos[0] - self._x_offset, event.pos[1] - self._y_offset, self.size):
            if self.click_button.value in event.buttons:
                self._command()(*self.command_parameters)

    def _mouse_button_up(self, event):

        if within_rectangle(event.pos[0] - self._x_offset, event.pos[1] - self._y_offset, self.size):
            if event.button == self.click_button.value:
                self._command()(*self.command_parameters)

    def _mouse_button_down(self, event):

        if within_rectangle(event.pos[0] - self._x_offset, event.pos[1] - self._y_offset, self.size):
            if event.button == self.click_button.value:
                self._command()(*self.command_parameters)

    def _mouse_motion(self, event):

        if within_rectangle(event.pos[0] - self._x_offset, event.pos[1] - self._y_offset, self.size):

            if self.highlight_color is not None:
                self._active_color = self.highlight_color

            if self.text_highlight_color is not None:
                self._active_text_color = self.text_highlight_color

        else:
            self._active_color = self.color
            self._active_text_color = self.text_color

    # ------------------------------------------------------------------------------------------------------------------

    def update(self, x: int, y: int):  # remove '*remove'.

        self._x_offset = x
        self._y_offset = y

    # ------------------------------------------------------------------------------------------------------------------

    def move(self, x: int, y: int):
        self.size[0] += x
        self.size[1] += y


class UIText(UILabel, _info.InfoGetter):
    _position: [2]
    _text: str
    _text_color: [3]
    _font: _pygame.font

    _horizontal_alignment: Orientation
    _vertical_alignment: Orientation

    _x: int
    _y: int

    _rendered_text: _pygame.font

    # ------------------------------------------------------------------------------------------------------------------

    def _set_x(self):
        if self._horizontal_alignment == Orientation.Center:
            self._x = self._position[0] - self._font.size(str(self._text))[0] / 2

        elif self._horizontal_alignment == Orientation.Right:
            self._x = self._position[0]

        elif self._horizontal_alignment == Orientation.Left:
            self._x = self._position[0] - self._font.size(str(self._text))[0]

        else:
            raise ValueError("Horizontal orientation out of bounds")

    def _set_y(self):
        if self._vertical_alignment == Orientation.Center:
            self._y = self._position[1] - self._font.size(str(self._text))[1] / 2

        elif self._vertical_alignment == Orientation.Below:
            self._y = self._position[1]

        elif self._vertical_alignment == Orientation.Over:
            self._y = self._position[1] - self._font.size(str(self._text))[1]

        else:
            raise ValueError("Vertical orientation out of bounds")

    def _set_text(self):
        self._rendered_text = self.font.render(self.text, True, self.text_color)

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def horizontal_alignment(self):
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, orientation: Orientation):
        self._horizontal_alignment = orientation
        self._set_x()

    @property
    def vertical_alignment(self):
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, orientation: Orientation):
        self._vertical_alignment = orientation
        self._set_x()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p: (int, int)):
        self._position = p
        self._set_x()
        self._set_y()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, string: str):
        self._text = string
        self._set_x()
        self._set_y()
        self._set_text()

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, color: [int, int, int]):
        self._text_color = color
        self._set_text()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, f: _pygame.font.Font):
        self._font = f
        self._set_x()
        self._set_y()
        self._set_text()

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, **kwargs):
        self._position = (0, 0)
        self._text = "UIText"
        self._text_color = [255, 255, 255]
        self._font = _pygame.font.Font(_pygame.font.get_default_font(), 20)

        self._horizontal_alignment: Orientation = Orientation.Center
        self._vertical_alignment: Orientation = Orientation.Center

        self._rendered_text = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError("Invalid keyword: {}".format(key))

        self._set_x()
        self._set_y()

        self._set_text()

    def render(self, surface: _pygame.Surface):
        surface.blit(self._rendered_text, (self._x, self._y))


# Not usable. DON'T USE!
class UIInteractiveText(UILabel, _info.InfoGetter):
    _position: [2]
    _text: str
    _text_color: [3]
    _font: _pygame.font

    _horizontal_alignment: Orientation
    _vertical_alignment: Orientation

    _x: int
    _y: int

    # ------------------------------------------------------------------------------------------------------------------

    def _set_x(self):
        if self._horizontal_alignment == Orientation.Center:
            self._x = self._position[0] - self._font.size(str(self._text))[0] / 2

        elif self._horizontal_alignment == Orientation.Right:
            self._x = self._position[0]

        elif self._horizontal_alignment == Orientation.Left:
            self._x = self._position[0] - self._font.size(str(self._text))[0]

        else:
            raise ValueError("Horizontal orientation out of bounds")

    def _set_y(self):
        if self._vertical_alignment == Orientation.Center:
            self._y = self._position[1] - self._font.size(str(self._text))[1] / 2

        elif self._vertical_alignment == Orientation.Below:
            self._y = self._position[1]

        elif self._vertical_alignment == Orientation.Over:
            self._y = self._position[1] - self._font.size(str(self._text))[1]

        else:
            raise ValueError("Vertical orientation out of bounds")

    def _set_text(self):
        self._rendered_text = self.font.render(self.text, True, self.text_color)

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def horizontal_alignment(self):
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, orientation: Orientation):
        self._horizontal_alignment = orientation
        self._set_x()

    @property
    def vertical_alignment(self):
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, orientation: Orientation):
        self._vertical_alignment = orientation
        self._set_x()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p: (int, int)):
        self._position = p
        self._set_x()
        self._set_y()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, string: str):
        self._text = string
        self._set_x()
        self._set_y()
        self._set_text()
        self._at_text = self._text.__len__()

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, color: [int, int, int]):
        self._text_color = color
        self._set_text()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, f: _pygame.font.Font):
        self._font = f
        self._set_x()
        self._set_y()
        self._set_text()

    @property  # sets/returns if text operates at all. Disconnect everything if false, including mouse/click callbacks.
    def operative(self):
        return self._operative

    @operative.setter
    def operative(self, boolean: bool):
        self._operative = boolean

        self.active = boolean

        # Add callback changes similar to '@property active'. These'll handle (de)activating 'self.active'.

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, boolean: bool):

        try:
            if boolean and not self._active:
                _EventHandler.callbacks.add.keydown(self._keydown)
                _EventHandler.callbacks.add.keyup(self._keyup)
                _EventHandler.callbacks.add.update(self.update)

                self._pressed_keys: {int: [str, float, int]} = {}

            else:
                _EventHandler.callbacks.remove.keydown(self._keydown)
                _EventHandler.callbacks.remove.keyup(self._keyup)
                _EventHandler.callbacks.remove.update(self.update)

                self._pressed_keys = None

        except ValueError:
            pass

        self._active = boolean

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, **kwargs):
        self._position = (0, 0)
        self._text = "UIText"
        self._text_color = [255, 255, 255]
        self._font = _pygame.font.Font(_pygame.font.get_default_font(), 20)

        self._horizontal_alignment: Orientation = Orientation.Center
        self._vertical_alignment: Orientation = Orientation.Center

        self._rendered_text = None

        self._operative = True
        self._active = False

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError("Invalid keyword: {}".format(key))

        self._set_x()
        self._set_y()

        self._set_text()

        # Behaviour setup

        self._pressed_keys = None
        self._at_text = self._text.__len__()

        if _EventHandler.initialized:
            self.operative = self._operative

    def __del__(self):
        print("Cleaning UIInteractiveText: " + self.__str__())

        try:
            self.operative = False

        except ValueError:
            pass

    # ------------------------------------------------------------------------------------------------------------------

    def _keydown(self, event: _pygame.event.Event):
        self._pressed_keys[event.key] = [event.unicode, _time.time(), 0]

    def _keyup(self, event: _pygame.event.Event):
        try:
            self._pressed_keys.pop(event.key)

        except KeyError:
            if self._pressed_keys[event.key]:
                raise KeyError(_traceback.format_exc())

            # A key was released after construction, while pressed before construction.

    def update(self):
        if 310 in self._pressed_keys:
            return

        for code, data in self._pressed_keys.items():

            # print(str(code) + ": '" + str(data[0]) + "'")

            if _time.time() - data[1] > 0.4 or data[2] == 0:
                data[2] += 1
                print()

                if code == 8:
                    if self._at_text != 0:
                        self._text = self._text[:self._at_text - 1] + self._text[self._at_text:]
                        self._set_x()
                        self._set_y()
                        self._set_text()

                    self._at_text = _minimum(0, self._at_text - 1)

                elif data[0] == "":
                    continue

                elif code == 276:
                    self._at_text = _minimum(0, self._at_text - 1)
                    print("1:   ", self._at_text)

                elif code == 275:
                    self._at_text = _maximum(self._text.__len__() + 1, self._at_text + 1)
                    print("2:   ", self._at_text)

                else:
                    self._text += data[0]
                    self._set_x()
                    self._set_y()
                    self._set_text()
                    self._at_text = _maximum(self._text.__len__() + 1, self._at_text + 1)

    def render(self, surface: _pygame.Surface):
        surface.blit(self._rendered_text, (self._x, self._y))


class UIInteractiveTextBlock(UILabel, _info.InfoGetter):
    pass


# TODO: add possibility to move image in size borders, and customize scaling
class UIImage(UILabel, _info.InfoGetter):  # TODO: add possibility to move image in size borders, and customize scaling
    """scale_mode values:
     0 = scale to size. Aspect ratio not kept
     1 = scale to fit width.
     2 = scale to fit height.
     3 = scale width. Aspect ratio not kept
     4 = scale height. Aspect ratio not kept
     5 = scale to fit width, cut at height edge
     6 = scale to fit height, cut at width edge
     7 = scale width, cut at height edge. Aspect ratio not kept
     8 = scale height, cut at width edge. Aspect ratio not kept
     9 = cut width. No scaling
    10 = cut height. No scaling
    11 = clip at width and height. No scaling
    12 = no scaling
    """

    _size: [4]
    _scale_mode: int

    show_size: bool
    visible: bool

    _image: _pygame.Surface
    _loaded_image: _pygame.Surface

    # Drawing values
    _area: [4]

    @property
    def formatted_image(self) -> _pygame.Surface:
        return self._image

    @property
    def image(self) -> _pygame.Surface:
        return self._loaded_image

    @image.setter
    def image(self, surface: _pygame.Surface or str):
        if isinstance(surface, str):
            surface = _pygame.image.load(surface)

        surface = surface.convert()
        self._loaded_image = surface

        self._set_scale()

    @property
    def scale_mode(self) -> int:
        return self._scale_mode

    @scale_mode.setter
    def scale_mode(self, mode: int):
        self._scale_mode = mode
        self._set_scale()

    @property
    def size(self) -> [4]:
        return self._size

    @size.setter
    def size(self, area: [4]):
        self._size = area
        self._set_scale()

    def __init__(self, **kwargs):
        self._size: [4] = [0, 0, 100, 100]
        self._scale_mode: int = 11

        self.show_size: bool = True
        self.visible: bool = True

        self._image: _pygame.Surface = None
        self._loaded_image: _pygame.Surface = None

        # Drawing values
        self._area = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError("Invalid keyword: {}".format(key))

    # ------------------------------------------------------------------------------------------------------------------

    def render(self, surface: _pygame.Surface):
        if self.visible:

            if self._loaded_image is None:

                if self.show_size is False:
                    return

                _pygame.draw.rect(surface, (200, 200, 200), self.size)
                font = _pygame.font.Font(_pygame.font.get_default_font(), 20)
                text = font.render("UIImage", True, (0, 0, 0))
                x = self.size[0] + (self.size[2] / 2) - font.size(str("UIImage"))[0] / 2
                y = self.size[1] + (self.size[3] / 2) - font.size(str("UIImage"))[1] / 2
                surface.blit(text, (x, y))

            else:
                surface.blit(self._image, (self.size[0], self.size[1]), self._area)

    # ------------------------------------------------------------------------------------------------------------------

    def _set_scale(self):

        if self._loaded_image is None:
            return

        if self.scale_mode == 0:  # scale to size. Aspect ratio not kept
            self._image = _pygame.transform.scale(self._loaded_image, (self.size[2], self.size[3]))
            self._area = None

        elif self.scale_mode == 1:  # scale to fit width
            rate = self._loaded_image.get_width() / self.size[2]
            height = int(self._loaded_image.get_height() / rate)
            self._image = _pygame.transform.scale(self._loaded_image, (self.size[2], height))
            self._area = None

        elif self.scale_mode == 2:  # scale to fit height
            rate = self._loaded_image.get_height() / self.size[3]
            width = int(self._loaded_image.get_width() / rate)
            self._image = _pygame.transform.scale(self._loaded_image, (width, self.size[3]))
            self._area = None

        elif self.scale_mode == 3:  # scale width. Aspect ratio not kept
            self._image = _pygame.transform.scale(self._loaded_image, (self.size[2], self._loaded_image.get_height()))
            self._area = None

        elif self.scale_mode == 4:  # scale height. Aspect ratio not kept
            self._image = _pygame.transform.scale(self._loaded_image, (self._loaded_image.get_width(), self.size[3]))
            self._area = None

        elif self.scale_mode == 5:  # scale to fit width, cut at height edge
            rate = self._loaded_image.get_width() / self.size[2]
            height = int(self._loaded_image.get_height() / rate)
            self._image = _pygame.transform.scale(self._loaded_image, (self.size[2], height))
            self._area = (0, 0, self._loaded_image.get_width(), self.size[3])

        elif self.scale_mode == 6:  # scale to fit height, cut at width edge
            rate = self._loaded_image.get_height() / self.size[3]
            width = int(self._loaded_image.get_width() / rate)
            self._image = _pygame.transform.scale(self._loaded_image, (width, self.size[3]))
            self._area = (0, 0, self.size[2], self._loaded_image.get_height())

        elif self.scale_mode == 7:  # scale width, cut at height edge. Aspect ratio not kept
            self._image = _pygame.transform.scale(self._loaded_image, (self.size[2], self._loaded_image.get_height()))
            self._area = (0, 0, self._loaded_image.get_width(), self.size[3])

        elif self.scale_mode == 8:  # scale height, cut at width edge. Aspect ratio not kept
            self._image = _pygame.transform.scale(self._loaded_image, (self._loaded_image.get_width(), self.size[3]))
            self._area = (0, 0, self.size[2], self._loaded_image.get_height())

        elif self.scale_mode == 9:  # cut width. No scaling
            self._image = self._loaded_image
            self._area = (0, 0, self.size[2], self._loaded_image.get_height())

        elif self.scale_mode == 10:  # cut height. No scaling
            self._image = self._loaded_image
            self._area = (0, 0, self._loaded_image.get_width(), self.size[3])

        elif self.scale_mode == 11:  # clip at width and height. No scaling
            self._image = self._loaded_image
            self._area = self.size

        elif self.scale_mode == 12:  # no scaling
            self._image = self._loaded_image
            self._area = None

        else:
            raise ValueError("Scale mode out of bounds. Please use the values between 0 and 12")

        # noinspection PyArgumentList
        self._image = self._image.convert()

    # ------------------------------------------------------------------------------------------------------------------

    def set_current_size(self):
        self.size[2] = self.image.get_size()[0]
        self.size[3] = self.image.get_size()[1]


class UIImageButton(UILabel, _info.InfoGetter):
    pass


class UIPasscodeBlock(UILabel, _info.InfoGetter):
    pass


class UIPasswordBlock(UILabel, _info.InfoGetter):
    pass


class Transform:

    @staticmethod
    def combine_colors(surface: _pygame.Surface, upper_color: [3], lower_color: [3], orientation: Orientation,
                       coordinates: [4] = None):
        background = coordinates if coordinates is not None else surface.get_rect()
        x1 = background[0]
        x2 = x1 + background[2]
        y1 = background[1]
        y2 = y1 + background[3]
        h = x2 - x1 if orientation == Orientation.Vertical else y2 - y1

        rate = (float((lower_color[0] - upper_color[0]) / h),
                (float(lower_color[1] - upper_color[1]) / h),
                (float(lower_color[2] - upper_color[2]) / h))

        if orientation == Orientation.Horizontal:
            for line in range(y1, y2):
                color = (min(max(upper_color[0] + (rate[0] * line), 0), 255),
                         min(max(upper_color[1] + (rate[1] * line), 0), 255),
                         min(max(upper_color[2] + (rate[2] * line), 0), 255))
                _pygame.draw.line(surface, color, (x1, line), (x2, line))
        elif orientation == Orientation.Vertical:
            for line in range(x1, x2):
                color = (min(max(upper_color[0] + (rate[0] * line), 0), 255),
                         min(max(upper_color[1] + (rate[1] * line), 0), 255),
                         min(max(upper_color[2] + (rate[2] * line), 0), 255))
                _pygame.draw.line(surface, color, (line, y1), (line, y2))
        else:
            raise ValueError("Orientation out of bounds")

    @staticmethod
    def info(write: bool = True):
        return _info.get_info(Transform, write)
