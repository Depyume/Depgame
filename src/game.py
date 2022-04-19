import pygame
import pytmx
import pyscroll

from src import player
from src.player import Player
from src.map import MapManager


class Game:

    def __init__(self):

        # fenetre d jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Depgame - Aventure")
        self.player = Player(60, 60)

        # charger carte
        # tmx_data = pytmx.util_pygame.load_pygame('../maps/world.tmx')
        # map_data = pyscroll.data.TiledMapData(tmx_data)
        # map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # map_layer.zoom = 3
        self.world = MapManager(self.screen, self.player)

        # gene un player
        # player_position = tmx_data.get_object_by_name("Player")
        # self.player = Player(player_position.x, player_position.y)

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
        elif pressed[pygame.K_h]:
            self.player.get_damage()
        elif pressed[pygame.K_k]:
            self.player.get_health()

    def update(self):
        self.world.update()

        # for sprite in self.group.sprites():
        # if sprite.feet.collidelist(self.walls) > -1:
        # sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()
        # boucle du jeux
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.world.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)

        pygame.quit()
        screen = pygame.display.set_mode((800, 600))
