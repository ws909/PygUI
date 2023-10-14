import pygame

# from OpenGL.GL import *
# from OpenGL.GLU import *


class ObjectViewer:  # TODO: progress

    background: [3]
    item: []

    def __init__(self):
        self.background = [0, 0, 0]
        self.item = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))

    def update(self, size: [4], display: pygame.display):
        display.fill(self.background, size)
        for i in self.item:
            pygame.draw.polygon(display, (0, 0, 0), [(0, 0), (0, 0), (0, 0)])

    def load(self, file: str):
        """
        .txt
        :return:
        """
        f = open(file, "r")
        f.close()





# --------------------------
# Test

pygame.init()

this_display = pygame.display.set_mode((1440, 810))
viewer = ObjectViewer()
viewer.background = [255, 100, 100]
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    viewer.update([350, 35, 740, 740], this_display)

    pygame.display.flip()

pygame.quit()
