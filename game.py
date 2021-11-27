import sys
from random import randint

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 560


class MainGame:
    zombie_list = []
    bullets = []
    maps_list = []
    plant_list = []
    points_list = []
    money = 200
    remnant_score = 100
    score = 0
    level = 1
    screen = None

    def __init__(self):
        # 设定窗口的大小
        pygame.display.init()
        MainGame.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 显示帮助文字
        self.init_points_list()
        self.init_maps_list()
        self.produce_zombie()

        while True:
            self.handle_events()
            MainGame.screen.fill((255, 255, 255))
            self.load_maps_list()
            self.load_plant_list()
            # 每次都要重新绘制
            self.load_help_text()
            self.load_bullets()
            self.load_zombie()
            pygame.display.update()

    # font_style 需要通过元组(name, size, color)的形式传入
    # 我们需要得到一个已经加工好的 Surface 文本
    @staticmethod
    def text_render(content, font_style):
        (name, size, color) = font_style
        pygame.font.init()
        font = pygame.font.SysFont(name, size)
        text = font.render(content, True, color)
        return text

    def load_help_text(self):
        name = "Microsoft YaHei UI"
        size = 26
        color = (255, 0, 0)
        text = self.text_render("1.左键种植向日葵，2.右键种植豌豆射手", (name, size, color))
        MainGame.screen.blit(text, (5, 0))
        text = self.text_render(
            "当前关数：{}， 当前得分：{}，距离下关还差：{}，金钱：{}".format(
                MainGame.level, MainGame.score, MainGame.remnant_score, MainGame.money
            ), (name, size, color)
        )
        MainGame.screen.blit(text, (5, 40))

    @staticmethod
    def init_points_list():
        for top in range(1, 7):
            points = []
            for left in range(10):
                points.append((left, top))
            MainGame.points_list.append(points)
            print(points)

    @staticmethod
    def init_maps_list():
        # 通过坐标点的二维列表得到二维的所以地图
        for points in MainGame.points_list:
            maps = []
            for point in points:
                (left, top) = point
                # 通过坐标点生成地图实例
                m = Map(left, top)
                maps.append(m)
            MainGame.maps_list.append(maps)

    @staticmethod
    def load_maps_list():
        for maps in MainGame.maps_list:
            for m in maps:
                m.display()

    @staticmethod
    def handle_events():
        event_list = pygame.event.get()
        for e in event_list:
            if e.type == pygame.MOUSEBUTTONDOWN:
                print(e.pos)
                (left, top) = e.pos
                left = left // 80
                top = top // 80
                if top == 0:
                    continue
                m = MainGame.maps_list[top - 1][left]
                if m.can_grow:
                    if e.button == pygame.BUTTON_LEFT:
                        plant = SunFlower(left * 80, top * 80)
                        m.can_grow = False
                        MainGame.plant_list.append(plant)
                        print("种植向日葵")
                        pass
                    elif e.button == pygame.BUTTON_RIGHT:
                        plant = PeaShooter(left * 80, top * 80)
                        m.can_grow = False
                        MainGame.plant_list.append(plant)
                        print("种植豌豆射手")
                        pass

    @staticmethod
    def load_plant_list():
        for plant in MainGame.plant_list:
            # 如果植物活着
            if plant.live:
                if isinstance(plant, SunFlower):
                    plant.produce_money()
                elif isinstance(plant, PeaShooter):
                    # 发射子弹
                    plant.shot()
                plant.display()
            else:
                MainGame.plant_list.remove(plant)

    @staticmethod
    def load_bullets():
        for bullet in MainGame.bullets:
            bullet.move()
            bullet.display()

    @staticmethod
    def produce_zombie():
        for i in range(1, 7):
            distance = randint(1, 4) * 200
            zombie = Zombie(800 + distance, i * 80)
            MainGame.zombie_list.append(zombie)

    @staticmethod
    def load_zombie():
        for zombie in MainGame.zombie_list:
            if zombie.live:
                zombie.display()
                zombie.move()
                zombie.hit_plant()
            else:
                MainGame.zombie_list.remove(zombie)


class Map:
    def __init__(self, left, top):
        #
        index = (left + top) % 2 + 1
        self.image = pygame.image.load('imgs/map{}.png'.format(index))
        self.position = (left * 80, top * 80)
        self.can_grow = True

    def display(self):
        MainGame.screen.blit(self.image, self.position)


class Plant(pygame.sprite.Sprite):
    def __init__(self, left, top, image):
        super(Plant, self).__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 200

    def display(self):
        MainGame.screen.blit(self.image, self.rect)


class SunFlower(Plant):
    def __init__(self, left, top):
        super(SunFlower, self).__init__(left, top, 'imgs/sun-flower.png')
        self.time_counter = 0

    def produce_money(self):
        if self.live:
            self.time_counter += 1
            if self.time_counter == 25:
                MainGame.money += 5
                self.time_counter = 0


class PeaShooter(Plant):
    def __init__(self, left, top):
        super(PeaShooter, self).__init__(left, top, 'imgs/pea-shooter.png')
        self.time_counter = 0

    def shot(self):
        self.time_counter += 1
        if self.time_counter == 25:
            # 生成子弹
            bullet = PeaShooterBullet(self)
            # 加入到列表中
            MainGame.bullets.append(bullet)
            self.time_counter = 0


# 定义豌豆射手子弹
class PeaShooterBullet(pygame.sprite.Sprite):
    def __init__(self, pea_shooter: PeaShooter):
        super(PeaShooterBullet, self).__init__()
        self.image = pygame.image.load('imgs/pea-bullet.png')
        self.rect = self.image.get_rect()
        self.rect.left = pea_shooter.rect.left + 40
        self.rect.top = pea_shooter.rect.top + 20
        self.speed = 10

    def move(self):
        if self.rect.left < SCREEN_WIDTH:
            self.rect = self.rect.move(self.speed, 0)
        else:
            # 子弹移出列表
            MainGame.bullets.remove(self)
            pass

    def display(self):
        MainGame.screen.blit(self.image, self.rect)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, left, top):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('./imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.hp = 200
        self.speed = 1
        self.live = True
        self.can_move = True

    def move(self):
        if self.live:
            if self.can_move:
                self.rect =  self.rect.move(self.speed * -1, 0)
                if self.rect.right < 0:
                    sys.exit()

    def hit_plant(self):
        for plant in MainGame.plant_list:
            if pygame.sprite.collide_rect(self, plant):
                self.eat_plant(plant)

    def display(self):
        MainGame.screen.blit(self.image, self.rect)


if __name__ == '__main__':
    game = MainGame()
