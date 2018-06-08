import pygame
import pygame.gfxdraw


class Object:
    def __init__(self, point_list, shadow_type=0):
        self.shadow_type = shadow_type
        self.point_list = point_list

    def fix_position(self, x, y):
        if x != 0 and y != 0:
            for point in self.point_list:
                point[0] += x
                point[1] += y
        elif x != 0:
            for point in self.point_list:
                point[0] += x
        elif y != 0:
            for point in self.point_list:
                point[1] += y

    def draw_polygon(self, screen, color=(0, 0, 0), width=0, relative_point=(0, 0), gfx=False):
        if len(color) == 4:
            gfx = True
        right_plist = []
        for point in self.point_list:
            right_plist.append(
                (point[0] - relative_point[0], point[1] - relative_point[1]))
        if not gfx:
            pygame.draw.polygon(screen, color, right_plist, width,)
        else:
            pygame.gfxdraw.filled_polygon(screen, right_plist, color)

    def draw_lines(self, screen, color=(0, 0, 0), width=1, relative_point=(0, 0), aa=False):
        right_plist = []
        for point in self.point_list:
            right_plist.append((point[0] - relative_point[0], point[1] - relative_point[1]))
        if not aa:
            pygame.draw.lines(screen, color, 1, right_plist, width,)
        else:
            pygame.draw.aalines(screen, color, 1, right_plist, width, )

    def __str__(self):
        return str(self.shadow_type) + "&" + str(self.point_list)