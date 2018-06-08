import pygame


class KeyEventHandler:
    @staticmethod
    def check_for_exit():
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return True
        return False

    @staticmethod
    def move_but():
        w = False
        s = False
        d = False
        a = False
        caps = False

        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_CAPSLOCK]:
            caps = True
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_w]:
            w = True
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_d]:
            d = True
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_a]:
            a = True
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_s]:
            s = True
        pygame.event.pump()

        return {'w': w, 'a': a, 's': s, 'd': d, 'caps': caps}
