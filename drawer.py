import random
import time
import pygame

from light_engine import LightMath


class Drawer:
    def __init__(self):
        self.light_point_list = []
        self.small_obj_list = []
        self.object_list_for_shadows = []
        pass

    def draw_objects_and_shadows(self, screen, object_list, x_pos, y_pos, frames=0, object_list_red=None):
        display_width = screen.get_width()
        display_height = screen.get_height()
        # display_width = 0
        # display_height = 0

        if frames % 15 == 0:
            self.small_obj_list = []
            for obj in object_list:
                j = False
                min_len = 100000
                for dot in obj.point_list:
                    if pygame.math.Vector2(dot[0] - (display_width // 2 + x_pos),
                                           dot[1] - (display_height // 2 + y_pos)).length() < 350:
                        if pygame.math.Vector2(dot[0] - (display_width // 2 + x_pos),
                                               dot[1] - (display_height // 2 + y_pos)).length() < min_len:
                            dot1 = dot
                            min_len = pygame.math.Vector2(dot[0] - (display_width // 2 + x_pos),
                                                          dot[1] - (display_height // 2 + y_pos)).length()
                        j = True

                if j:
                    self.small_obj_list.append(obj)

            self.object_list_for_shadows = []
            for obj in self.small_obj_list:
                j = False
                for dot in obj.point_list:
                    if pygame.math.Vector2(dot[0] - (display_width // 2 + x_pos),
                                           dot[1] - (display_height // 2 + y_pos)).length() < 400:
                        j = True
                if j:
                    self.object_list_for_shadows.append(obj)

        if frames % 2 == 0:
            self.light_point_list = LightMath.make_beams_reduced(self.object_list_for_shadows,
                                                                 ((display_width // 2 + x_pos),
                                                                  (display_height // 2 + y_pos)),
                                                                 display_height + y_pos, display_width + x_pos)

        for obj in self.small_obj_list:
            if obj.shadow_type == 1:
                obj.draw_polygon(screen, relative_point=(x_pos, y_pos), color=(30, 30, 30, 200))
        for obj in self.light_point_list:
            if obj.shadow_type == 0:
                obj.draw_polygon(screen, color=(0, 0, 0), relative_point=(x_pos, y_pos))
            else:
                obj.draw_polygon(screen, color=(0, 0, 0, 100), relative_point=(x_pos, y_pos))

    @staticmethod
    def ending(screen, f, t=2):
        font = pygame.font.SysFont("tahoma", 50)
        text = font.render("YOU WIN", True, (255, 255, 255))
        bfont = pygame.font.SysFont("tahoma", 50)
        text2 = bfont.render("YOU LOSE", True, (255, 255, 255))
        w = screen.get_width()
        h = screen.get_height()
        screen.fill((20, 20, 20))
        if f:
            screen.blit(text,
                        (w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2))
        else:
            screen.blit(text2,
                        (w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(t)


    @staticmethod
    def draw_light(screen, ran=20, radius=300, color=[255, 150, 40, 9].copy(), full_factor=1):
        if full_factor > 0.01:
            display_width = screen.get_width()
            display_height = screen.get_height()
            if full_factor > 1:
                full_factor = 1
            elif full_factor > 0.5:
                ran *= full_factor * full_factor
                ran = round(ran)
            else:
                ran = round(0.5 * ran)
            y = round(radius / ran)
            col_f = random.random()
            for i in range(3):
                color[i] += round(col_f * 4)
                if full_factor > 0.5:
                    color[i] = round(color[i] * full_factor)
                else:
                    color[i] = round(color[i] * 0.5)
                if color[i] > 255:
                    color[i] = 255

            for i in range(ran):
                pygame.gfxdraw.filled_circle(screen, display_width // 2, display_height // 2, y * i + round(col_f * 2),
                                             color)
            pygame.gfxdraw.filled_circle(screen, display_width // 2, display_height // 2, 5, (255, 255, 255))

    @staticmethod
    def draw_another_p_light(screen, main_player_pos, player_pos, ran=20, radius=300,
                             full_factor=1, color=[255, 150, 40, 9].copy()):
        if full_factor > 0.01:
            display_width = screen.get_width()
            display_height = screen.get_height()
            if full_factor > 1:
                full_factor = 1
            elif full_factor > 0.5:
                ran *= full_factor * full_factor
                ran = round(ran)
            else:
                ran = round(0.5 * ran)
            y = round(radius / ran)
            col_f = random.random()
            for i in range(3):
                color[i] += round(col_f * 4)
                if full_factor > 0.5:
                    color[i] = round(color[i] * full_factor)
                else:
                    color[i] = round(color[i] * 0.5)
                if color[i] > 255:
                    color[i] = 255

            for i in range(ran):
                pygame.gfxdraw.filled_circle(screen, round(player_pos[0] - main_player_pos[0]) + display_width // 2,
                                             round(player_pos[1] - main_player_pos[1]) + display_height // 2, y * i + round(col_f * 2),
                                             color)
            pygame.gfxdraw.filled_circle(screen, round(player_pos[0] - main_player_pos[0]) + display_width // 2,
                                         round(player_pos[1] - main_player_pos[1]) + display_height // 2, 5,
                                         (255, 255, 255))


    @staticmethod
    def draw_another_light(screen, player_pos, pos, ran=25, radius=300, color=[255, 150, 40, 9].copy(), full_factor=1):
        if full_factor > 1:
            full_factor = 1
        if full_factor > 0.5:
            ran *= full_factor * full_factor
            ran = round(ran)
        else:
            ran = round(0.5 * ran)
        y = round(radius / ran)
        col_f = random.random()
        for i in range(3):
            color[i] += round(col_f * 4)
            if full_factor > 0.5:
                color[i] = round(color[i] * full_factor)
            else:
                color[i] = round(color[i] * 0.5)
            if color[i] > 255:
                color[i] = 255
        for i in range(ran):
            pygame.gfxdraw.filled_circle(screen, round(pos[0] - player_pos[0]),
                                         round(pos[1] - player_pos[1]),
                                         round(y * i + round(col_f * 2)),
                                         color)
        pygame.gfxdraw.filled_circle(screen, round(pos[0] - player_pos[0]),
                                     round(pos[1] - player_pos[1]), 5,
                                     (255, 255, 255))
