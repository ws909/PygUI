

class UIScrollViewControllerOld(UIViewController, info.InfoGetter, ABC):

    scroll_surface: pygame.Surface

    horizontal_scrolling: bool  # Issue with horizontal scrolling. Until issue is fixed, this variable is not for use
    vertical_scrolling: bool    # Issue with horizontal scrolling. Until issue is fixed, this variable is not for use
    direction: Orientation      # Because of issue with horizontal scrolling from pygame.mouse, this is to be used

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

    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self.scroll_surface = pygame.Surface((surface.get_width(), surface.get_height()))
        # self.horizontal_scrolling = False
        # self.vertical_scrolling = False
        self.direction = Orientation.Vertical
        self.x = 0
        self.y = 0
        self.scroll_intensity = 30

        # Shared scroller values
        self.scroller_color = (80, 80, 80)
        self.scroller_background_color = (200, 200, 200)
        self.scroller_highlight_color = [130, 130, 130]
        self.scroller_background_width = 24
        self.scroller_width = 16
        self.scroller_timeout = 60
        # TODO: set up functionality of these. That includes a new panning mode. Defaults: 2, 1
        self.scroller_visibility = 2  # 3  # 0 = never, 1 = on surface focus, 2 = on scrolling, 3 = always
        self.scroller_mode = 2  # 0 = invisible, 1 = panning, 2 = full

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

    def __del__(self):
        del self.scroll_surface
        UIViewController.__del__(self)

    # ------------------------------------------------------------------------------------------------------------------

    def render(self):
        """First render to self.scroll_surface, then UIScrollViewController.render(self), then self.surface"""
        self.surface.blit(self.scroll_surface, (self.x, self.y))

        # Vertical scroller
        if self._vertical_scroller_visible:
            pygame.draw.rect(self.surface, self.scroller_background_color, self._vertical_scroller_background_size)
            pygame.draw.rect(self.surface, self._vertical_scroller_active_color, self._vertical_scroller_size) \
                if self._vertical_scroller_active_color is not None else None

        # Horizontal scroller
        if self._horizontal_scroller_visible:
            pygame.draw.rect(self.surface, self.scroller_background_color, self._horizontal_scroller_background_size)
            pygame.draw.rect(self.surface, self._horizontal_scroller_active_color, self._horizontal_scroller_size) \
                if self._horizontal_scroller_active_color is not None else None

    def update(self, x, y, delta, mouse: (0, 0, [0, 0, 0], 0)):
        if not self.scroller_visibility == 0:
            # Shared scroller values
            # Scroller visibility, 1st stage
            if self.scroller_visibility == 1:
                vertical_scroller_visibility = within_rectangle(mouse[0] - x, mouse[1] - y, (0, 0, self.surface.get_width(), self.surface.get_height()))
                horizontal_scroller_visibility = vertical_scroller_visibility

            elif self.scroller_visibility == 2:
                if mouse[3] == 4 or mouse[3] == 5:
                    self._vertical_scroller_visibility_timeout = self.scroller_timeout
                    self._horizontal_scroller_visibility_timeout = self.scroller_timeout

                else:
                    self._vertical_scroller_visibility_timeout\
                        = max(self._vertical_scroller_visibility_timeout - delta / 10, 0)\
                        if not self._vertical_scroller_drag else self.scroller_timeout
                    self._horizontal_scroller_visibility_timeout\
                        = max(self._horizontal_scroller_visibility_timeout - delta / 10, 0)\
                        if not self._horizontal_scroller_drag else self.scroller_timeout

                if self._vertical_scroller_visibility_timeout > 0:
                    if within_rectangle(mouse[0] - x, mouse[1] - y, self._vertical_scroller_background_size):
                        self._vertical_scroller_visibility_timeout = self.scroller_timeout

                if self._horizontal_scroller_visibility_timeout > 0:
                    if within_rectangle(mouse[0] - x, mouse[1] - y, self._horizontal_scroller_background_size):
                        self._horizontal_scroller_visibility_timeout = self.scroller_timeout

                vertical_scroller_visibility = True if self._vertical_scroller_visibility_timeout > 0 else True if within_rectangle(mouse[0] - x, mouse[1] - y, self._vertical_scroller_background_size) else False
                horizontal_scroller_visibility = True if self._horizontal_scroller_visibility_timeout > 0 else True if within_rectangle(mouse[0] - x, mouse[1] - y, self._horizontal_scroller_background_size) else False

            elif self.scroller_visibility == 3:
                vertical_scroller_visibility = True
                horizontal_scroller_visibility = True

            else:
                raise ValueError("Scroller visibility out of bounds. Please use the values between 0 and 3")

            # Scroller visibility, 2nd stage
            self._horizontal_scroller_visible = False \
                if self.surface.get_width() >= self.scroll_surface.get_width() else True

            self._vertical_scroller_visible = False \
                if self.surface.get_height() >= self.scroll_surface.get_height() else True

            length = self.scroller_background_width \
                if self._vertical_scroller_visible and self._horizontal_scroller_visible else 0

            if not vertical_scroller_visibility:
                self._vertical_scroller_visible = False if not self._vertical_scroller_drag else True

            if not horizontal_scroller_visibility:
                self._horizontal_scroller_visible = False if not self._horizontal_scroller_drag else True

            scroller_start = self.scroller_background_width - (self.scroller_background_width - self.scroller_width) / 2

            # Vertical scroller
            if self._vertical_scroller_visible:
                self._vertical_scroller_size = [self.surface.get_width() - scroller_start,
                                                -(self.y / (self.scroll_surface.get_height() / self.surface.get_height())),
                                                self.scroller_width,
                                                (self.surface.get_height()
                                                * (self.surface.get_height() / self.scroll_surface.get_height())) - length]

                self._vertical_scroller_background_size = (self.surface.get_width() - self.scroller_background_width,
                                                           0,
                                                           self.scroller_background_width,
                                                           self.surface.get_height())

                if not self._horizontal_scroller_drag:
                    if within_rectangle(mouse[0] - x, mouse[1] - y, self._vertical_scroller_size):
                        self._vertical_scroller_within = True
                        self._vertical_scroller_active_color = self.scroller_highlight_color if self.scroller_highlight_color is not None else self.scroller_color
                    else:
                        self._vertical_scroller_within = False
                        self._vertical_scroller_active_color = self.scroller_color if self._vertical_scroller_drag is False else self.scroller_highlight_color
                    if mouse[2][0] > 0:
                        if self._vertical_scroller_within:
                            if not self._vertical_scroller_drag:
                                self._vertical_scroller_mouse_position = (mouse[1] - y) - self._vertical_scroller_size[1]
                            self._vertical_scroller_drag = True
                    else:
                        self._vertical_scroller_drag = False

            # Horizontal scroller
            if self._horizontal_scroller_visible:
                self._horizontal_scroller_size = [-(self.x / (self.scroll_surface.get_width() / self.surface.get_width())),
                                                  self.surface.get_height() - scroller_start,
                                                  (self.surface.get_width()
                                                  * (self.surface.get_width() / self.scroll_surface.get_width())) - length,
                                                  self.scroller_width]

                self._horizontal_scroller_background_size = (0,
                                                             self.surface.get_height() - self.scroller_background_width,
                                                             self.surface.get_width(),
                                                             self.scroller_background_width)

                if not self._vertical_scroller_drag:
                    if within_rectangle(mouse[0] - x, mouse[1] - y, self._horizontal_scroller_size):
                        self._horizontal_scroller_within = True
                        self._horizontal_scroller_active_color = self.scroller_highlight_color if self.scroller_highlight_color is not None else self.scroller_color
                    else:
                        self._horizontal_scroller_within = False
                        self._horizontal_scroller_active_color = self.scroller_color if self._horizontal_scroller_drag is False else self.scroller_highlight_color
                    if mouse[2][0] > 0:
                        if self._horizontal_scroller_within:
                            if not self._horizontal_scroller_drag:
                                self._horizontal_scroller_mouse_position = (mouse[0] - x) - self._horizontal_scroller_size[0]
                            self._horizontal_scroller_drag = True
                    else:
                        self._horizontal_scroller_drag = False

            # Sroll calls
            if self._vertical_scroller_drag:
                self.scroll(None, mouse[1] - y - self._vertical_scroller_mouse_position)
            elif self._horizontal_scroller_drag:
                self.scroll(mouse[0] - x - self._horizontal_scroller_mouse_position, None)
        else:
            self._vertical_scroller_visible = False
            self._horizontal_scroller_visible = False

        # Scroll button evaluation
        if self.direction == Orientation.Horizontal:
            if mouse[3] == 4:
                self.x = min(self.x + self.scroll_intensity * delta / 10, 0)
            elif mouse[3] == 5:
                self.x = max(self.x - self.scroll_intensity * delta / 10, 0 - self.scroll_surface.get_width() + self.surface.get_width())
            else:
                return
        elif self.direction == Orientation.Vertical:
            if mouse[3] == 4:
                self.y = min(self.y + self.scroll_intensity * delta / 10, 0)
            elif mouse[3] == 5:
                self.y = max(self.y - self.scroll_intensity * delta / 10, 0 - self.scroll_surface.get_height() + self.surface.get_height())
            else:
                return
        else:
            raise ValueError('Orientation out of bounds. Please use "Orientation.Horizontal" or "Orientation.Vertical"')

    def scroll(self, x: float or None, y: float or None):
        if x is not None:
            scroll = -(x * (self.scroll_surface.get_width() / self.surface.get_width()))
            minimum_scroll = min(scroll, 0)
            self.x = max(minimum_scroll, 0 - self.scroll_surface.get_width() + self.surface.get_width())

        if y is not None:
            scroll = -(y * (self.scroll_surface.get_height() / self.surface.get_height()))
            minimum_scroll = min(scroll, 0)
            self.y = max(minimum_scroll, 0 - self.scroll_surface.get_height() + self.surface.get_height())
