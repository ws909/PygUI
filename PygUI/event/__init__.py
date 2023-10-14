import traceback as _traceback

import pygame as _pygame

from PygUI.utilities import weak as _weak


class EventHandler:

    class Callback:

        class _Add:
            @staticmethod
            def early_update(callback):
                EventHandler.callbacks.early_update.append(_weak(callback))

            @staticmethod
            def update(callback):
                EventHandler.callbacks.update.append(_weak(callback))

            @staticmethod
            def any(callback):
                EventHandler.callbacks.any.append(_weak(callback))

            @staticmethod
            def keydown(callback):
                EventHandler.callbacks.keydown.append(_weak(callback))

            @staticmethod
            def keyup(callback):
                EventHandler.callbacks.keyup.append(_weak(callback))

            @staticmethod
            def mouse_button_down(callback):
                EventHandler.callbacks.mouse_button_down.append(_weak(callback))

            @staticmethod
            def mouse_button_up(callback):
                EventHandler.callbacks.mouse_button_up.append(_weak(callback))

            @staticmethod
            def mouse_motion(callback):
                EventHandler.callbacks.mouse_motion.append(_weak(callback))

            @staticmethod
            def mouse_press(callback):
                EventHandler.callbacks.mouse_press.append(_weak(callback))

            @staticmethod
            def window_resize(callback):
                EventHandler.callbacks.window_resize.append(_weak(callback))

        class _Remove:

            @staticmethod
            def early_update(callback):
                EventHandler.callbacks.early_update.remove(_weak(callback))

            @staticmethod
            def update(callback):
                EventHandler.callbacks.update.remove(_weak(callback))

            @staticmethod
            def any(callback):
                EventHandler.callbacks.any.remove(_weak(callback))

            @staticmethod
            def keydown(callback):
                EventHandler.callbacks.keydown.remove(_weak(callback))

            @staticmethod
            def keyup(callback):
                EventHandler.callbacks.keyup.remove(_weak(callback))

            @staticmethod
            def mouse_button_down(callback):
                EventHandler.callbacks.mouse_button_down.remove(_weak(callback))

            @staticmethod
            def mouse_button_up(callback):
                EventHandler.callbacks.mouse_button_up.remove(_weak(callback))

            @staticmethod
            def mouse_motion(callback):
                EventHandler.callbacks.mouse_motion.remove(_weak(callback))

            @staticmethod
            def mouse_press(callback):
                EventHandler.callbacks.mouse_press.remove(_weak(callback))

            @staticmethod
            def window_resize(callback):
                EventHandler.callbacks.window_resize.remove(_weak(callback))

        add: _Add
        remove: _Remove

        # May need special arrays for weak members. This is for the callback's class to release.
        early_update:      [object]
        update:            [object]

        any:               [object]
        keydown:           [object]
        keyup:             [object]
        mouse_button_down: [object]
        mouse_button_up:   [object]
        mouse_motion:      [object]
        mouse_press:       [object]
        window_resize:     [object]

        def __init__(self):
            self.add = self._Add()
            self.remove = self._Remove()

            self.early_update:      [object] = []
            self.update:            [object] = []

            self.any:               [object] = []
            self.keydown:           [object] = []
            self.keyup:             [object] = []
            self.mouse_button_down: [object] = []
            self.mouse_button_up:   [object] = []
            self.mouse_motion:      [object] = []
            self.mouse_press:       [object] = []
            self.window_resize:     [object] = []

    # ------------------------------------------------------------------------------------------------------------------

    callbacks: Callback

    _mouse_press: {}

    _errors: [str]

    @staticmethod
    def init():
        EventHandler.callbacks = EventHandler.Callback()

        EventHandler._mouse_press = set([])

        EventHandler._errors = []

    @staticmethod
    def flush():
        del EventHandler.Callback
        del EventHandler._mouse_press

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def initialized(self) -> bool:
        return EventHandler.callbacks is not None

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def update():
        for callback in EventHandler.callbacks.early_update:
            callback()()

        for event in _pygame.event.get():

            for callback in EventHandler.callbacks.any:
                callback()(event)

            if event.type == _pygame.KEYDOWN:
                for callback in EventHandler.callbacks.keydown:
                    callback()(event)

            elif event.type == _pygame.KEYUP:
                for callback in EventHandler.callbacks.keyup:
                    callback()(event)

            elif event.type == _pygame.MOUSEBUTTONDOWN:
                for callback in EventHandler.callbacks.mouse_button_down:
                    callback()(event)

                EventHandler._mouse_press.add(event.button)

            elif event.type == _pygame.MOUSEBUTTONUP:
                for callback in EventHandler.callbacks.mouse_button_up:
                    callback()(event)

                try:
                    EventHandler._mouse_press.remove(event.button)

                except KeyError:
                    EventHandler._errors.append(_traceback.format_exc())
                    print("Error occured in EventHandler.")
                    print(_traceback.format_exc())

            elif event.type == _pygame.MOUSEMOTION:
                for callback in EventHandler.callbacks.mouse_motion:
                    callback()(event)

            elif event.type == _pygame.VIDEORESIZE:
                for callback in EventHandler.callbacks.window_resize:
                    callback()(event)

        if EventHandler._mouse_press.__len__() > 0:
            e = _pygame.event.Event(0, {"buttons": EventHandler._mouse_press, "pos": _pygame.mouse.get_pos()})
            for callback in EventHandler.callbacks.mouse_press:
                callback()(e)

        for callback in EventHandler.callbacks.update:
            callback()()
