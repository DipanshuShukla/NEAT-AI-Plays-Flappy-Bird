from FlappyBird import *


def main():
    bird = Bird(230, 350)
    base = Base(730)
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

        Draw_Window(WINDOW, bird, pipes, base, Score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
