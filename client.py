import pygame
from network import Network

pygame.font.init()
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) -
                        round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(win, game, p, score):
    win.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 300))

        text = font.render("Opponent", 1, (0, 255, 255))
        win.blit(text, (380, 300))

        text = font.render("Your Score", 1, (0, 255, 255))
        win.blit(text, (80, 100))

        text = font.render("Opponent", 1, (0, 255, 255))
        win.blit(text, (380, 100))

        font = pygame.font.SysFont("comicsans", 90)
        if p == 0:
            text_1 = font.render("{0}".format(score[0]), 1, (0, 0, 255))
            text_2 = font.render("{0}".format(score[1]), 1, (0, 0, 255))

        else:
            text_1 = font.render("{0}".format(score[1]), 1, (0, 0, 255))
            text_2 = font.render("{0}".format(score[0]), 1, (0, 0, 255))

        win.blit(text_1, (160, 185))
        win.blit(text_2, (470, 185))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        font = pygame.font.SysFont("comicsans", 60)
        if game.both_went():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 400))
            win.blit(text1, (400, 400))
        else:
            win.blit(text1, (100, 400))
            win.blit(text2, (400, 400))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Cheat", 100, 500, (0, 0, 0)), Button("Cooperate", 410, 500, (255, 0, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print("You are player ", player)
    score = [0, 0]
    round_count = 0

    while run:
            clock.tick(60)
            try:
                game = n.send("get")
            except:
                run = False
                print("Couldn't get game")
                break

            if game.both_went():
                redraw_window(win, game, player, score)
                pygame.time.delay(500)
                try:
                    game = n.send("reset")
                except:
                    run = False
                    print("Couldn't get game")
                    break

                font = pygame.font.SysFont("comicsans", 90)
                if game.winner() == 3 and player == 0:
                    text = font.render("+3", 1, (255, 0, 0))
                    score[0] += 3
                    score[1] -= 1
                elif game.winner() == 3 and player == 1:
                    text = font.render("-1", 1, (255, 0, 0))
                    score[0] += 3
                    score[1] -= 1
                elif game.winner() == 2:
                    text = font.render("+2", 1, (255, 0, 0))
                    score[0] += 2
                    score[1] += 2
                elif game.winner() == -1 and player == 0:
                    text = font.render("-1", 1, (255, 0, 0))
                    score[0] -= 1
                    score[1] += 3
                elif game.winner() == -1 and player == 1:
                    text = font.render("+3", 1, (255, 0, 0))
                    score[0] -= 1
                    score[1] += 3
                elif game.winner() == 0:
                    text = font.render("+0", 1, (255, 0, 0))

                round_count += 1

                win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.click(pos) and game.connected():
                            if player == 0:
                                if not game.p1Went:
                                    n.send(btn.text)
                            else:
                                if not game.p2Went:
                                    n.send(btn.text)

            if round_count == 6:
                font = pygame.font.SysFont("comicsans", 40)
                if score[0] > score[1] and player == 0:
                    text = font.render("You Won! Final score: [{0}] - [{1}]".format(score[0], score[1]), 1, (255, 0, 0))
                elif score[0] < score[1] and player == 1:
                    text = font.render("You Won! Final score: [{0}] - [{1}]".format(score[1], score[0]), 1, (255, 0, 0))
                elif score[0] > score[1] and player == 1:
                    text = font.render("You Lost! Final score: [{0}] - [{1}]".format(score[1], score[0]), 1, (255, 0, 0))
                elif score[0] < score[1] and player == 0:
                    text = font.render("You Lost! Final score: [{0}] - [{1}]".format(score[0], score[1]), 1, (255, 0, 0))
                else:
                    text = font.render("Tie Game! Final score: [{0}] - [{1}]".format(score[0], score[1]), 1, (255, 0, 0))
                win.blit(text, (150, 50))
                pygame.display.update()
                pygame.time.delay(5000)
                run = False

            redraw_window(win, game, player, score)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (200, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
