import pygame

import sys
sys.path.append('..')

import constants      as c
import localConstants as lc

from abc import ABC, abstractmethod

class REINFORCEMENT(ABC):

    def __init__(self,ID,robots,color,numUndigestedReinforcements,username):

        self.ID = ID

        self.color = color

        self.Assign_Robot(robots)

        self.numUndigestedReinforcements = numUndigestedReinforcements

        self.username = username 

        self.font     = pygame.font.Font("anonymous-pro.bold.ttf",lc.userNameFontSize)

        self.text = self.font.render(self.username, True, c.colorLetterToPygameColor[self.color])

        self.textrect = self.text.get_rect()

        self.Rotate_Text()

        self.textrect = self.text.get_rect()

        self.width = self.textrect.width

        self.height = self.textrect.height

        self.Set_Position()

        self.textrect.centerx = self.x

        self.textrect.centery = self.y

    def Assign_Robot(self,robots):

        self.robot = robots.Get_Robot_Of_Color(self.color)

    def Digest(self,database):

        database.Digest_Reinforcement(self.ID)

    def Draw_To(self,screen):

        self.textrect.centerx = self.x

        self.textrect.centery = self.y

        screen.blit(self.text, self.textrect)

    @abstractmethod
    def Add_To_Robot(self):

        raise NotImplementedError()

    @abstractmethod
    def Done(self):

        raise NotImplementedError()

    @abstractmethod
    def Draw_Robots_Wins_Or_Losses(self):

        raise NotImplementedError()

    @abstractmethod
    def Finished_Pushing_Robot(self):

        raise NotImplementedError()

    @abstractmethod
    def Rotate_Text(self):

        raise NotImplementedError()

    @abstractmethod
    def Set_Position(self):

        raise NotImplementedError()

    @abstractmethod
    def Update(self):

        raise NotImplementedError()

