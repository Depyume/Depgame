import pygame
import pytmx
import pyscroll

from src.player import Player
from src.map import Map


class Game:

    def __init__(self):

        # fenetre d jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Depgame - Aventure")

        # charger carte
        tmx_data = pytmx.util_pygame.load_pygame('world.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # gene un player
        player_position = tmx_data.get_object_by_name("Player")
        self.player = Player(player_position.x, player_position.y)

        # def un lister pour stocker le hitbox et les collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de claque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

        # definir le rect de coli pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        self.group.update()

        # verif de la collision
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()
        #for sprite in self.group.sprites():
            #if sprite.feet.collidelist(self.walls) > -1:
               # sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()
        # boucle du jeux
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)

        pygame.quit()
