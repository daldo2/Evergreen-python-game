import pygame
import pytmx
from src import config

def load_level(filename):
    """
    Parses a Tiled Map Editor file to extract game world data.

    This function loads the map using pytmx and iterates through specific layers
    to generate physics objects, rendering data,
    and spawn coordinates for entities.

    Args:
        filename: The relative file path to the .tmx map file.

    Returns:
        tuple: A collection of level data in the following order:
            1. tmx_data : The raw map object from pytmx.
            2. walls: A list of collision rectangles for solid terrain.
            3. hazards: A list of hazard rectangles.
            4. visuals: A list of tuples for drawing the terrain.
            5. spawn_point: The (x, y) starting coordinates for the player.
            6. slime_spawns: List of (x, y) coordinates for Slime enemies.
            7. frog_spawns: List of (x, y) coordinates for Frog enemies.
            8. mana_spawns: List of (x, y) coordinates for Manas.
            9. win_zone: The collision zone that triggers the win state.
    """
    tmx_data = pytmx.util_pygame.load_pygame(filename)

    walls = []
    visuals = []
    hazards = []
    spawn_point = (0, 0)
    slime_spawns = []
    frog_spawns = []
    mana_spawns = []
    win_zone = None

    layer = tmx_data.get_layer_by_name("Terrain")

    if layer:
        for x, y, gid in layer:
            if gid != 0:
                pixel_x = x * config.TILE_SIZE
                pixel_y = y * config.TILE_SIZE

                rect = pygame.Rect(pixel_x, pixel_y, config.TILE_SIZE, config.TILE_SIZE)
                walls.append(rect)
                image = tmx_data.get_tile_image_by_gid(gid)
                visuals.append((image, rect))


    objects = tmx_data.get_layer_by_name("Spawners")
    for obj in objects:
        if obj.name == "PlayerStart":
            spawn_point = (obj.x, obj.y)

        elif obj.name == "SlimeStart":
            slime_spawns.append((obj.x, obj.y- 32))

        elif obj.name == "FrogStart":
            frog_spawns.append((obj.x, obj.y -32))

        elif obj.name == "ManaStart":
            mana_spawns.append((obj.x, obj.y -32))

        if obj.name == "WinZone":
            win_zone = pygame.Rect(obj.x, obj.y, obj.width, obj.height)


    return tmx_data, walls,hazards, visuals, spawn_point, slime_spawns, frog_spawns, mana_spawns, win_zone