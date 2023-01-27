import pygame

from constant.constants import BLOCK_SIZE, WINDOW_SIZE
from entity.robot.Battery import Battery
from entity.robot.Trash import Trash


class Robot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.trash = Trash()
        self.battery = Battery()

        self.img_can = pygame.image.load("src/resources/can.png")
        self.img_can = pygame.transform.scale(self.img_can, (3 * BLOCK_SIZE, 3 * BLOCK_SIZE))

        self.img_robot = pygame.image.load("src/resources/robot.png")
        self.img_robot = pygame.transform.scale(self.img_robot, (3 * BLOCK_SIZE, 3 * BLOCK_SIZE))

        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def getCurrentPosition(self):
        return self.x, self.y

    def collectCan(self):
        self.trash.add()

    def canCollectCan(self):
        return self.trash.isNotFull()

    def cleanCans(self):
        self.trash.clean()

    def isTrashEmpty(self):
        return self.trash.isEmpty()

    def update(self, display):
        self.basicTrash(display)
        self.basicBattery(display)

    def dyingDamage(self, amount):
        self.battery.damage(amount)

    def getBattery(self, amount):
        self.battery.charge(amount)

    def basicBattery(self, display):
        pygame.draw.rect(display, self.getBatteryColor(self.battery.getCurrent()),
                         (10, 25, self.battery.getCurrent() / self.battery.getRatio(), 25))
        pygame.draw.rect(display, (255, 255, 255), (10, 25, self.battery.getBarLen(), 25), 4)

    def basicTrash(self, display):
        display.blit(self.img_can, (WINDOW_SIZE // 2 - 100, 10))

        text = self.font.render(f': {self.trash.getCurrentSize()} / {self.trash.getMaxSize()}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_SIZE // 2, 40)
        display.blit(text, text_rect)

    def getBatteryColor(self, battery):
        if battery < self.battery.getMax() // 3:
            return 255, 0, 0
        if battery > self.battery.getMax() // 3 * 2:
            return 127, 255, 0
        return 255, 255, 0

    def main(self, display):
        display.blit(self.img_robot, ((self.x - 1) * BLOCK_SIZE, (self.y - 1) * BLOCK_SIZE))

    def canMove(self):
        return self.battery.canMove()

    def moveTo(self, position):
        self.x = position[0]
        self.y = position[1]
