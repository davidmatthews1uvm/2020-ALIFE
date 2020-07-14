import constantsPassiveGame as cpg

import pygame

class SCREEN:

    def __init__(self):

        pygame.init()

        numOptions = len(cpg.options)

        depth = int( cpg.depth / numOptions )

        self.screen = pygame.display.set_mode((cpg.width,depth)) # Set screen size of pygame window

        pygame.font.init()

        self.myfont = pygame.font.Font(cpg.font,cpg.fontSize)

        self.done = False

    def Done(self):

        return self.done

    def Handle_Events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.done = True

    def Prepare(self):

        self.screen.fill(cpg.backgroundColor)

    def Reveal(self):

        pygame.display.flip()

