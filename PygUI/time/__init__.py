from time import sleep as _sleep
from time import time as _time
import pygame
from PygUI.UI.accesories import Fonts
from PygUI.UI.accesories import UIText


class Clock:

    _last_frame_time: int
    _last_time: int
    delta: float
    framecount: int
    lps: int

    def __init__(self):
        self._last_frame_time = int(_time() * 100)
        self._last_time = int(_time() * 100)
        self.delta = None
        self.frameCount = 0
        self.lps = 0

        self.pygame_clock = pygame.time.Clock()
        self.lps_text = UIText()
        self.lps_text.font = Fonts.get("monospace", 40)
        self.lps_text.position = [1000, 140]

        # Test
        self.old_time = pygame.time.get_ticks()
        self.old = _time()

        self.t = 0.0
        self.dt = 0.01

        self.current_time = _time()
        self.accumulator = 0.0

    def synchronize_loop(self, loops_per_second: int):
        self.pygame_clock.tick(loops_per_second)

        current_frame_time = int(_time() * 100)
        self.delta = (current_frame_time * 10 - self._last_frame_time * 10)
        # sleep = (loops_per_second - self.delta) * 6

        self.frameCount += 1
        if self._last_frame_time - self._last_time >= 100:
            self._last_time = int(_time() * 100)
            self.lps = self.frameCount
            self.frameCount = 0
        # if not sleep <= 0:
        #     time.sleep(1 / sleep)
        self._last_frame_time = int(_time() * 100)

    def test(self):
        new_time = pygame.time.get_ticks()
        waited = new_time - self.old_time
        self.old_time = new_time
        if waited < 60:
            _sleep(1.0 / (60 - waited))

    def restart(self):
        self._last_frame_time = int(_time() * 100)
        self.delta = None

    def render_lps(self, surface: pygame.Surface):
        self.lps_text.text = str(self.lps)
        self.lps_text.render(surface)
