from FlappyBird import *
import neat

GEN = 0


def Draw_Window(win, birds, pipes, base, SCORE, GEN):
    WINDOW.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.Draw(win)

    text = STAT_FONT.render("Score: " + str(SCORE), 1, WHITE)
    WINDOW.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(GEN-1), 1, WHITE)
    WINDOW.blit(text, (10, 10))

    base.Draw(win)

    for bird in birds:
        bird.Draw(win)

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird())
        ge.append(genome)

    base = Base()
    pipes = [Pipe()]

    run = True
    clock = pygame.time.Clock()

    Score = 0

    while run:
        clock.tick(30)

        if len(birds) <= 0:
            run = False
            break

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.Move()

            output = nets[x].activate((bird.Ypos, abs(bird.Ypos - pipes[-1].height), abs(bird.Ypos - pipes[-1].bottom)))

            if output[0] > 0.5:
                bird.Jump()

        base.Move()

        rem = []
        add_pipe = False

        for pipe in pipes:
            for x, bird in enumerate(birds):

                if pipe.Collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < bird.Xpos:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.Move()

        if add_pipe:
            Score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe())

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):

            if bird.Ypos + bird.img.get_height() >= 730 or bird.Ypos < 0:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        Draw_Window(WINDOW, birds, pipes, base, Score, GEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()


def Run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    Run(config_path)
