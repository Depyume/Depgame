from dataclasses import dataclass
from sys import warnoptions

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
    walls: list
    group: pyscroll.PyscrollGroup
    warps: list
    lzs: dict


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
        # for warps in self.get_map().warps:
        #   if warps.from_world == self.current_map:
        #      point = self.get_object(warps.origin_point)
        #     rect = pygame.Rect(point.x, point.y, point.width, point.height)

        #                    if self.player.feet.colliderect(rect):
        #                       copy_warps = warps
        #                      self.current_map = warps.target_world
        #                     self.teleport_player(copy_warps.warps_point)
        # collision
        if self.player.feet.collidelist(self.get_wall()) > -1:
            self.player.move_back()
            return

        for warpzone in self.get_warps():
            if self.player.feet.colliderect(warpzone.rect):
                self.current_map = warpzone.warp_to
                landing_zone = self.get_lzs()[warpzone.warp_point]
                self.player.teleport_to(landing_zone[0], landing_zone[1])
                self.update()
                break

        #for sprite in self.get_group().sprites():
            #if sprite.feet.collidelist(self.get_walls()) > -1:
                #sprite.move_back()

    def register_map(self, name):
        # charger map
        tmx_data = pytmx.util_pygame.load_pygame(f"maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # lister les zones de collisions de la map
        walls = []
        warps = []
        lzs = {}
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                continue
            if obj.type == "lz":
                lzs[obj.name] = [obj.x, obj.y]
                continue
            if obj.type == "warp":
                warps.append(Warp(
                    obj.name,
                    obj.properties.get("warp_to"),
                    obj.properties.get("warp_point"),
                    pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                ))

        # dessiner le groupe de calqque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        group.add(self.player)

        # creer un obj map
        self.maps[name] = Map(name, walls, group, warps, lzs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_wall(self):
        return self.get_map().walls

    def get_warps(self):
        return self.get_map().warps

    def get_lzs(self):
        return self.get_map().lzs

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
