import pygame
import random
import os

pygame.font.init()
WIN_WIDTH, WIN_HEIGHT = 500, 800

# IMAGES
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

# COLORS
Yellow = [255, 255, 0]
WHITE = [255, 255, 255]

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


class Base:
    vel = 5
    width = BASE_IMG.get_width()
    img = BASE_IMG

    def __init__(self):
        self.y = 730
        self.x1 = 0
        self.x2 = self.width

    def Move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def Draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

    def Collide(self, bird):
        if bird.Ypos + bird.img.get_height() >= self.y:
            return True

        return False


class Bird:
    IMG = BIRD_IMG
    max_rot = 30
    rot_vel = 20
    animation_time = 5

    def __init__(self):
        self.Xpos = 230
        self.Ypos = 350
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.Ypos
        self.img_count = 0
        self.img = self.IMG[0]

    def Jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.Ypos

    def Move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.Ypos += d

        if d < 0 or self.Ypos < self.height + 50:
            if self.tilt < self.max_rot:
                self.tilt = self.max_rot
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel

    def Draw(self, win):
        self.img_count += 1
        if self.img_count < self.animation_time:
            self.img = self.IMG[0]
        elif self.img_count < self.animation_time * 2:
            self.img = self.IMG[1]
        elif self.img_count < self.animation_time * 3:
            self.img = self.IMG[2]
        elif self.img_count < self.animation_time * 4:
            self.img = self.IMG[1]
        elif self.img_count < self.animation_time * 4 + 1:
            self.img = self.IMG[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMG[1]
            self.img_count = self.animation_time * 2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.Xpos, round(self.Ypos))).center)
        win.blit(rotated_img, new_rect.topleft)

    def Get_Mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    gap = 200
    vel = 5

    def __init__(self):
        self.x = 600
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.Set_Height()

    def Set_Height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def Move(self):
        self.x -= self.vel

    def Draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def Collide(self, bird):
        bird_mask = bird.Get_Mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.Xpos, self.top - round(bird.Ypos))
        bottom_offset = (self.x - bird.Xpos, self.bottom - round(bird.Ypos))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


def Draw_Window(win, bird, pipes, base, SCORE):
    WINDOW.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.Draw(win)

    text = STAT_FONT.render("Score: " + str(SCORE), 1, WHITE)
    WINDOW.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.Draw(win)
    bird.Draw(win)
    pygame.display.update()


if __name__ == "__main__":
    def main():
        bird = Bird()
        base = Base()
        pipes = [Pipe()]

        run = True
        clock = pygame.time.Clock()

        Score = 0

        while run:
            clock.tick(30)

            # bird.Move()
            base.Move()

            rem = []
            add_pipe = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bird.Jump()

            for pipe in pipes:
                pipe.Move()
                if pipe.Collide(bird):
                    pass
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < bird.Xpos:
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                Score += 1
                pipes.append(Pipe())

            for r in rem:
                pipes.remove(r)

            if bird.Ypos + bird.img.get_height() > 730:
                pass

            bird.Move()
            Draw_Window(WINDOW, bird, pipes, base, Score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            if pipe.Collide(bird) or base.Collide(bird):
                run = False
        return True

    play = main()
    while play:
        play = main()

