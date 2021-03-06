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
    clock = pygame.time.Clock()
    zombie_counter = 0
    zombie_distance = 100

    def __init__(self):
        # 设定窗口的大小
        pygame.display.init()
        MainGame.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 显示帮助文字
        self.init_points_list()
        self.init_maps_list()
        self.produce_zombie()

        while True:
            MainGame.clock.tick(240)
            self.handle_events()
            MainGame.screen.fill((255, 255, 255))
            self.load_maps_list()
            self.load_plant_list()
            # 每次都要重新绘制
            self.load_help_text()
            self.load_bullets()
            self.load_zombie_list()
            MainGame.zombie_counter += 1
            if MainGame.zombie_counter == MainGame.zombie_distance:
                self.produce_zombie()
                MainGame.zombie_counter = 0
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
            if bullet.live:
                bullet.display()
                bullet.move()
                bullet.hit_zombie()
            else:
                MainGame.bullets.remove(bullet)

    @staticmethod
    def produce_zombie():
        for i in range(1, 7):
            left = randint(1, 5) * 200 + 800
            top = i * 80
            zombie = Zombie(left, top)
            MainGame.zombie_list.append(zombie)

    @staticmethod
    def load_zombie_list():
        for zombie in MainGame.zombie_list:
            if isinstance(zombie, Zombie):
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
        self.price = 50
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
        # 遍历僵尸列表查看该行是否有僵尸存在
        should_shot = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.top == self.rect.top and self.rect.left < zombie.rect.left < 800:
                should_shot = True

        if self.live and should_shot:
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
        self.damage = 100
        self.live = True

    def move(self):
        if self.rect.left < SCREEN_WIDTH:
            self.rect = self.rect.move(self.speed, 0)
        else:
            self.live = False

    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            # 判断是否碰到僵尸
            if pygame.sprite.collide_rect(self, zombie):
                # 减少僵尸的血量
                zombie.hp -= self.damage
                # 把子弹删除掉
                self.live = False
                if zombie.hp <= 0:
                    # 把僵尸的状态设置为死亡，等待 load_zombie_list 中删除僵尸
                    zombie.live = False
                    self.next_level()

    @staticmethod
    def next_level():
        MainGame.score += 20
        MainGame.remnant_score -= 20
        for i in range(1, 100):
            if MainGame.score == i * 100 and MainGame.remnant_score == 0:
                MainGame.remnant_score = 100 * i
                MainGame.level += 1
                MainGame.zombie_distance -= 2

    def display(self):
        MainGame.screen.blit(self.image, self.rect)


class Zombie(pygame.sprite.Sprite):
    # Surface # Rect
    def __init__(self, left, top):
        super(Zombie, self).__init__()
        self.live = True
        self.image = pygame.image.load('./imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.can_move = True
        # 伤害
        self.damage = 20
        self.hp = 1000
        self.speed = 1

    # 僵尸移动
    def move(self):
        if self.can_move:
            self.rect = self.rect.move(self.speed * -1, 0)
            # todo: 到最左边就要结束游戏

    # 碰撞植物
    def hit_plant(self):
        for plant in MainGame.plant_list:
            if pygame.sprite.collide_rect(self, plant):
                self.can_move = False
                # todo: 调整吃的速度
                self.eat_plant(plant)

    def display(self):
        MainGame.screen.blit(self.image, self.rect)

    # 吃植物
    def eat_plant(self, plant):
        plant.hp -= self.damage
        print(plant.hp)
        if plant.hp <= 0:
            self.can_move = True
            left = plant.rect.left // 80
            top = plant.rect.top // 80
            m = MainGame.maps_list[top - 1][left]
            m.can_grow = True
            plant.live = False


if __name__ == '__main__':
    game = MainGame()
