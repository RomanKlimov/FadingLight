import pygame
import time
import socket

from game_processing import GameProcessing


class Intro:
    @staticmethod
    def game_intro(resolution=[1000, 600]):
        pygame.init()
        screen = pygame.display.set_mode(resolution)



        clock = pygame.time.Clock()
        gameIcon = pygame.image.load('resources/LightIcon.png')
        pygame.display.set_icon(gameIcon)
        pygame.display.set_caption('FL')
        check_sound = pygame.mixer.Sound('resources/tumbler.wav')
        intro_music = pygame.mixer.music.load('resources/dune.mp3')

        font = pygame.font.SysFont("tahoma", 50)
        text = font.render("Fading Light", True, (255, 255, 255))

        bfont = pygame.font.SysFont('tahoma', 20)
        btext = bfont.render('Single', True, (20, 20, 20))

        b1font = pygame.font.SysFont('tahoma', 20)
        b1text = b1font.render('S', True, (20, 20, 20))

        b2font = pygame.font.SysFont('tahoma', 20)
        b2text = b2font.render('M', True, (20, 20, 20))

        b3font = pygame.font.SysFont('tahoma', 20)
        b3text = b3font.render('L', True, (20, 20, 20))

        b4font = pygame.font.SysFont('tahoma', 20)
        b4text = b4font.render('Multi', True, (20, 20, 20))


        w = screen.get_width()
        h = screen.get_height()

        t = time.time()

        intro = True
        i = 30
        j = 30
        k = 30
        s = False
        m = False
        l = False
        single = False
        multi = False
        ip_address = ''

        pygame.mixer.music.play(-1)

        sound1 = False
        sound2 = False
        while intro:
            pygame.event.pump()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                quit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            screen.fill((20, 20, 20))

            screen.blit(text,
                        (w//2 - text.get_width() // 2, h//2 - text.get_height() // 2))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if round(w/2)-round(w/6)-i < mouse[0] < round(w/2)-round(w/6)+i and round(h - 1/7 * h)-i < mouse[1] < round(h - 1/7 * h)+i:
                if not sound1:
                    pygame.mixer.Sound.play(check_sound)
                    # pygame.mixer.music.stop()
                    sound1 = True
                if i < 45:
                    i += 3
                pygame.draw.circle(screen, (255, 255, 153), (round(w/2)-round(w/6), round(h - 1 / 7 * h)), i)
                if click[0]:
                    # pygame.quit()
                    # quit()
                    # single = True
                    # multi = False
                    pygame.quit()
                    n = 10
                    if s:
                        n = 5
                    if m:
                        n = 11
                    if l:
                        n = 17
                    gp = GameProcessing(maze_size=n)
                    gp.start_game_loop()

            else:
                if i > 30:
                    i -= 4
                sound1 = False
                pygame.draw.circle(screen, (255, 255, 255), (round(w/2)-round(w/6), round(h - 1/7 * h)), i)

            screen.blit(btext, (round(w/2)-round(w/6) - btext.get_width() // 2, round(h - 1/7 * h) - btext.get_height() // 2))

            if w-(2 * round(w / 6))-k < mouse[0] < w-(2 * round(w / 6))+k and round(h - 1/7 * h)-k < mouse[1] < round(h - 1/7 * h)+k:
                if not sound2:
                    pygame.mixer.Sound.play(check_sound)
                    # pygame.mixer.music.stop()
                    sound2 = True
                if k < 45:
                    k += 3
                pygame.draw.circle(screen, (255, 255, 153), (w-2*round(w / 6), round(h - 1 / 7 * h)), k)
                if click[0]:
                    pygame.quit()
                    # quit()
                    # pygame.quit()
                    n = 11
                    if s:
                        n = 5
                    if m:
                        n = 11
                    if l:
                        n = 17

                    if len(ip_address) == 0:
                        HOST = ''
                    else:
                        HOST = ip_address
                    PORT = 3301
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if len(ip_address) > 0:
                        online_type = 'client'
                        s.connect((HOST, PORT))
                    else:
                        s.bind((HOST, PORT))
                        s.listen(1)
                        online_type = 'server'

                    gp = GameProcessing(maze_size=n, online=True, online_type=online_type, sock=s, caption=online_type)
                    gp.start_game_loop()



                    # if multi:
                    # multi = True
                    # else:
                    #     multi = True
                    # ipfont = pygame.font.SysFont('tahoma', 20)
                    # iptext = ipfont.render(ipinput, True, (20, 20, 20))
                    # screen.blit(iptext,
                    #             (w // 2 - text.get_width() // 2, h -(h//2 + h // 3) - text.get_height() // 2))
                    # action(s, m, l, single, multi)

            else:
                if k > 30:
                    k -= 4
                sound2 = False
                pygame.draw.circle(screen, (255, 255, 255), (w-2*round(w / 6), round(h - 1/7 * h)), k)

            screen.blit(b4text, (w-2*round(w / 6) - b4text.get_width() // 2, round(h - 1/7 * h) - b4text.get_height() // 2))

            if time.time() - t > 0.15:
                pygame.event.pump()
                if pygame.key.get_pressed()[pygame.K_0]:
                    ip_address += str(0)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_1]:
                    ip_address += str(1)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_2]:
                    ip_address += str(2)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_3]:
                    ip_address += str(3)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_4]:
                    ip_address += str(4)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_5]:
                    ip_address += str(5)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_6]:
                    ip_address += str(6)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_7]:
                    ip_address += str(7)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_8]:
                    ip_address += str(8)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_9]:
                    ip_address += str(9)
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    ip_address = ip_address[:len(ip_address) - 1]
                    t = time.time()

                if pygame.key.get_pressed()[pygame.K_COMMA]:
                    ip_address += '.'
                    t = time.time()
                # if multi:
                #     if pygame.key.get_pressed()[pygame.K_SPACE]:
                #         pygame.quit()
                #         quit()
                #         # action(s,m,l,single,multi,ip_address)


                t = time.time()

            if round(w/6)-j < mouse[0] < round(w/6)+j and round(h - 1/3 * h)-j < mouse[1] < round(h - 1/3 * h)+j:
                pygame.draw.circle(screen, (255, 255, 255), (round(w / 6), round(h - 1 / 3 * h)), j)
                if click[0]:
                    s = True
                    m = False
                    l = False
                    pygame.draw.circle(screen, (255, 255, 153), (round(w / 6), round(h - 1 / 3 * h)), j)
                if s == True:
                    pygame.draw.circle(screen, (255, 255, 153), (round(w / 6), round(h - 1 / 3 * h)), j)
            else:
                if s == True:
                    pygame.draw.circle(screen, (255, 255, 153), (round(w / 6), round(h - 1 / 3 * h)), j)
                else:
                    pygame.draw.circle(screen, (255, 255, 255), (round(w / 6), round(h - 1 / 3 * h)), j)

            screen.blit(b1text, (round(w/6) - b1text.get_width() // 2, round(h - 1/3 * h) - b1text.get_height() // 2))

            if round(w / 2) - j < mouse[0] < round(w / 2) + j and round(h - 1 / 3 * h) - j < mouse[1] < round(h - 1 / 3 * h) + j:

                pygame.draw.circle(screen, (255, 255, 255), (round(w / 2), round(h - 1 / 3 * h)), j)
                if click[0]:
                    m = True
                    s = False
                    l = False
                    pygame.draw.circle(screen, (255, 255, 153), (round(w / 2), round(h - 1 / 3 * h)), j)
                if m == True:
                    pygame.draw.circle(screen, (255, 255, 153), (round(w / 2), round(h - 1 / 3 * h)), j)
            else:
                if m == True:
                    pygame.draw.circle(screen, (255, 255, 153), (round(w / 2), round(h - 1 / 3 * h)), j)
                else:
                    pygame.draw.circle(screen, (255, 255, 255), (round(w / 2), round(h - 1 / 3 * h)), j)
            screen.blit(b2text,
                        (round(w / 2) - b2text.get_width() // 2, round(h - 1 / 3 * h) - b2text.get_height() // 2))

            if (w-round(w / 6)) - j < mouse[0] < (w-round(w / 6)) + j and round(h - 1 / 3 * h) - j < mouse[1] < round(h - 1 / 3 * h) + j:

                pygame.draw.circle(screen, (255, 255, 255), (w-round(w / 6), round(h - 1 / 3 * h)), j)
                if click[0]:
                    l = True
                    s = False
                    m = False
                    pygame.draw.circle(screen, (255, 255, 153), (w-round(w / 6), round(h - 1 / 3 * h)), j)
                if l == True:
                    pygame.draw.circle(screen, (255, 255, 153), (w-round(w / 6), round(h - 1 / 3 * h)), j)
            else:
                if l == True:
                    pygame.draw.circle(screen, (255, 255, 153), (w-round(w / 6), round(h - 1 / 3 * h)), j)
                else:
                    pygame.draw.circle(screen, (255, 255, 255), (w-round(w / 6), round(h - 1 / 3 * h)), j)

            screen.blit(b3text,
                        (w-round(w / 6) - b2text.get_width() // 2, round(h - 1 / 3 * h) - b2text.get_height() // 2))

            ipfont = pygame.font.SysFont('tahoma', 20)
            iptext = ipfont.render(ip_address, True, (100, 100, 100))
            screen.blit(iptext,
                        (w // 2 - text.get_width() // 2, h - (h // 2 + h // 3) - text.get_height() // 2))
            pygame.display.flip()
            clock.tick(60)


# screen = pygame.display.set_mode((1000, 600))
# Intro.game_intro(screen)






