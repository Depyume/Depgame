from dataclasses import dataclass

import pygame
import pyscroll
import pytmx


@dataclass
class Warp:
    name: str
    target_world: str
    teleport_point: str
    rect: pygame.rect


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    warps: list[Warp]
    group: pyscroll.PyscrollGroup

    class MapManager:

        def __init__(self, screen, player):
            self.maps = dict()
            self.screen = screen
            self.player = player
            self.current_map = "world"

            self.register_map("world")
            self.register_map("house 1")

        def check_collision(self):
            # warps
            #for warps in self.get_map().warps:
             #   if warps.from_world == self.current_map:
              #      point = self.get_object(warps.origin_point)
               #     rect = pygame.Rect(point.x, point.y, point.width, point.height)

#                    if self.player.feet.colliderect(rect):
 #                       copy_warps = warps
  #                      self.current_map = warps.target_world
   #                     self.teleport_player(copy_warps.warps_point)
            # collision
            for sprite in self.get_group().sprites():
                if sprite.feet.collidelist(self.get_walls()) > -1:
                    sprite.move_back()

        def teleport_player(self, name):
            point = self.get_object(name)
            self.player.position[0] = point.x
            self.player.position[1] = point.y
            self.player.save_location()

        def register_map(self, name):
            # charger map
            tmx_data = pytmx.util_pygame.load_pygame(f"../{name}.tmx")
            map_data = pyscroll.data.TiledMapData(tmx_data)
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
            map_layer.zoom = 3

            # lister les zones de collisions de la map
            walls = []
            warps = []
            for obj in tmx_data.objects:
                if obj.type == "collision":
                    walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    continue
                if obj.type == "warp":
                    warps.append(Warp(
                        obj.name,
                        obj.properties["warp_to"],
                        obj.properties["warp_point"],
                        pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    ))

            # dessiner le groupe de calqque
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
            group.add(self.player)

            # creer un obj map
            self.maps[name] = Map(name, walls, group, tmx_data, warps)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_wall(self):
        return self.get_map().walls

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
