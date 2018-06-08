import pygame
import time
import resources
import socket

from drawer import Drawer
from entities.object import Object
import intro
from macro_maze_generator import MazeGenerator
from key_event_handler import KeyEventHandler
from player import Player
from sparks import Sparks
from utilities import Utilities


class GameProcessing:
    def __init__(self, window_width=1000, window_height=600, maze_size=3, death_time=5, fullscreen=False,
                 frame_rate=-1, box_w=300, box_h=300, wall_w=40, smooth_f=1, online=False, online_type='-',
                 sock=None, caption='Light'):
        self.caption = caption
        self.online = online
        self.online_type = online_type
        self.fullscreen = fullscreen
        self.frame_rate = frame_rate
        self.resolution = (window_width, window_height)
        if (online and online_type is 'server' and sock is not None) or not online:
            self.death_time = death_time
            self.full_f_time = maze_size * maze_size * 2
            # self.full_f_time = 1000
            self.box_w = box_w
            self.box_h = box_h
            self.maze_size = maze_size
            self.macro_map = MazeGenerator().ret_maze(maze_size)
            self.micro_map, self.micro_map_red = Utilities.make_full_map(self.macro_map, box_width=box_w,
                                                                         box_height=box_h,
                                                                         wall_w=wall_w, smooth_f=smooth_f,
                                                                         part_num=maze_size * maze_size * 2)
            if online:
                self.conn, self.adr = sock.accept()
                sock.setblocking(False)
                Utilities.send_map_data(self.conn, death_time, self.full_f_time, box_w, box_h, maze_size,
                                        self.micro_map, self.micro_map_red)
        elif online and online_type is 'client' and sock is not None:
            self.sock = sock
            sock.setblocking(False)
            self.death_time, self.full_f_time, self.box_w, self.box_h, self.maze_size, self.micro_map, self.micro_map_red = Utilities.get_map_data(
                self.sock)

    def start_game_loop(self):
        pygame.display.init()
        pygame.init()
        pygame.display.set_caption(self.caption)
        pygame.mixer.music.load('resources/rih.mp3')
        pygame.mixer.music.play(-1)

        if self.online_type is 'client':
            Utilities.move_all(self.micro_map_red)
        Utilities.move_all(self.micro_map)

        if self.fullscreen:
            screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(self.resolution)

        go = True

        timer = pygame.time.Clock()

        # pygame.mouse.set_visible(False)

        player = Player(True, full_f_time=self.full_f_time, death_time=self.death_time)
        if self.online:
            another_player = Player(False)
            Utilities.set_players_pos(self.online, self.online_type, player, another_player, self.box_w, self.box_h,
                                      self.resolution, self.maze_size)
        else:
            Utilities.set_players_pos(self.online, self.online_type, player, None, self.box_w, self.box_h,
                                      self.resolution, self.maze_size)


        sparks = Sparks()

        frames = 0
        t = time.time()
        drawer = Drawer()
        enemy_data = ''
        while go:
            if self.frame_rate != -1:
                timer.tick(self.frame_rate)
            player.pos = Utilities.collision_fix(
                player.pos, self.resolution, self.micro_map_red)
            player.pos = [int(player.pos[0]), int(player.pos[1])]
            if self.online:
                if self.online_type is 'client':
                    enemy_data = Utilities.update_another_player_data(self.sock, player, another_player, enemy_data)
                elif self.online_type is 'server':
                    enemy_data = Utilities.update_another_player_data(self.conn, player, another_player, enemy_data)
            sparks.update(player.pos)
            screen.lock()
            # ----------------------------------------------- start of drawing code
            screen.fill((0, 0, 0))
            drawer.draw_light(screen, color=player.color.copy(), full_factor=player.full_factor)
            sparks.draw(screen, relative_point=player.pos)
            if self.online:
                drawer.draw_another_p_light(screen, main_player_pos=player.pos, player_pos=another_player.pos,
                                            color=another_player.color.copy(), full_factor=another_player.full_factor)
                print(another_player.pos)
            drawer.draw_another_light(screen, player_pos=[int(round(player.pos[0])), int(round(player.pos[1]))],
                                      pos=[(self.maze_size // 2 + 1) * self.box_w + 2000 - self.box_w // 2,
                                           (self.maze_size // 2 + 1) * self.box_h + 2000 - self.box_h // 2],
                                      color=[255, 255, 255, 15], full_factor=1, radius=self.box_w // 2)
            if self.online_type is not 'client':
                drawer.draw_another_light(screen, player_pos=[int(round(player.pos[0])), int(round(player.pos[1]))],
                                          pos=[self.box_w + 2000 - self.box_w // 2,
                                               self.box_h + 2000 - self.box_h // 2],
                                          color=[200, 200, 255, 15], full_factor=1, radius=self.box_w // 4, ran=4)
            else:
                drawer.draw_another_light(screen, player_pos=[int(round(player.pos[0])), int(round(player.pos[1]))],
                                          pos=[self.maze_size * self.box_w + 2000 - self.box_w // 2,
                                               self.maze_size * self.box_h + 2000 - self.box_h // 2],
                                          color=[200, 200, 255, 15], full_factor=1, radius=self.box_w // 4, ran=4)

            drawer.draw_objects_and_shadows(screen, self.micro_map, player.pos[0], player.pos[1], frames)

            # ----------------------------------------------- end of drawing draw
            screen.unlock()
            pygame.display.flip()
            frames += 1

            player.update(KeyEventHandler.move_but(), time.time() - t)
            t = time.time()

            player.win = Utilities.check_for_win(player, self.maze_size, self.resolution, self.box_w, self.box_h)
            if Utilities.fulling_check(self.online_type, player, self.box_w, self.box_h,
                                      self.resolution, self.maze_size):
                player.t_of_fulling = time.time()

            if player.game_over:
                go = False
                if player.win:
                    drawer.ending(screen, True, 2)
                else:
                    drawer.ending(screen, False, 2)

            if self.online:
                if another_player.win:
                    drawer.ending(screen, False, 2)
                    go = False

            pygame.event.pump()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                go = False
        pygame.quit()
        intro.Intro.game_intro(self.resolution)
