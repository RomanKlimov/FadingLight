import time


class Player:
    def __init__(self, main=True, pos=[0, 0], full_factor=1.0, full_f_time=1000, color=[255, 150, 40, 9].copy(),
                 death_time=5):
        self.main = main,
        self.color = color
        self.pos = pos
        self.full_factor = full_factor
        self.t_of_fulling = time.time()
        self.full_f_time = full_f_time
        self.win = False
        self.death_time = death_time
        self.game_over = False

    def update(self, buttons, t):
        self.full_factor = 1 - (time.time() - self.t_of_fulling) / self.full_f_time
        if self.full_factor < 0:
            self.full_factor = 0
        if 0.5 < self.full_factor < 0.65:
            self.full_factor = 0.65
        elif 0.5 > self.full_factor > 0.15:
            self.full_factor = 0.65 - self.full_factor / 10
        if self.win:
            self.game_over = True
        if time.time() - self.t_of_fulling > self.full_f_time + self.death_time:
            self.game_over = True
            self.win = False

        q = 1
        if buttons['caps']:
            q = 1.8
        if buttons['d']:
            self.pos[0] += t * 100 * q
        if buttons['a']:
            self.pos[0] -= t * 100 * q
        if buttons['s']:
            self.pos[1] += t * 100 * q
        if buttons['w']:
            self.pos[1] -= t * 100 * q
