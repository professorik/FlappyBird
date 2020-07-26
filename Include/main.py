#!/usr/bin/env python

import pygame
import os
from pygame.locals import *  # noqa
import sys
import random
import audioop
import pyaudio

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((1092, 708))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("PycharmProjects/floppy/assets/background.png").convert()
        self.birdSprites = [pygame.image.load("PycharmProjects/floppy/assets/1.png").convert_alpha(),
                            pygame.image.load("PycharmProjects/floppy/assets/2.png").convert_alpha(),
                            pygame.image.load("PycharmProjects/floppy/assets/dead.png")]
        self.wallUp = pygame.image.load("PycharmProjects/floppy/assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("PycharmProjects/floppy/assets/top.png").convert_alpha()
        self.gap = 160
        self.countOfBlocks = 6
        self.walls_x = [400 + i * random.randint(300, 330) for i in range(self.countOfBlocks)]
        self.offsets = [random.randint(-180, 180) for i in range(self.countOfBlocks)]
        self.temp = self.countOfBlocks - 1
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0

    def updateWalls(self):
        for i in range(self.countOfBlocks):
            self.walls_x[i] -= 2
            if self.walls_x[i] < -80:
                self.walls_x[i] = self.walls_x[self.temp] + random.randint(250, 330)
                self.temp = (1 + self.temp) % self.countOfBlocks
                self.counter += 1
                self.offsets[i] = random.randint(-180, 180)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY

        upRect1 = [1]*self.countOfBlocks
        downRect1 = [1]*self.countOfBlocks

        for i in range(self.countOfBlocks):
            upRect1[i] = pygame.Rect(self.walls_x[i],
                                 360 + self.gap - self.offsets[i] + 10,
                                 self.wallUp.get_width() - 10,
                                 self.wallUp.get_height())
            downRect1[i] = pygame.Rect(self.walls_x[i],
                                   0 - self.gap - self.offsets[i] - 10,
                                   self.wallDown.get_width() - 10,
                                   self.wallDown.get_height())
            if upRect1[i].colliderect(self.bird):
                self.dead = True
            if downRect1[i].colliderect(self.bird):
                self.dead = True

        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.temp = self.countOfBlocks - 1
            self.walls_x = [400 + i * random.randint(300, 330) for i in range(self.countOfBlocks)]
            self.offsets = [random.randint(-180, 180) for i in range(self.countOfBlocks)]
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)

        chunk = 1024
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=chunk)

        THRESHOLD = 100
        while True:
            clock.tick(60)

            if audioop.rms(stream.read(chunk), 2) > THRESHOLD and not self.dead:
                self.jump = 17
                self.gravity = 5
                self.jumpSpeed = 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            for i in range(self.countOfBlocks):
                self.screen.blit(self.wallUp,
                                 (self.walls_x[i], 360 + self.gap - self.offsets[i]))
                self.screen.blit(self.wallDown,
                                 (self.walls_x[i],  0 - self.gap - self.offsets[i]))

            self.screen.blit(font.render(str(self.counter), -1,(255, 255, 255)), (546, 50))
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
