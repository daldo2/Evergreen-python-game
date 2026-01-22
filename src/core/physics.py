import pygame

def move_and_slide(rect, velocity, tiles, dt):
    """
    Move block by a given velocity and a set of tiles,
    while resolving the colissions.

    Returns the updated rect and collisions with indication of side.
    """
    collisions = {'top': False, 'bottom': False, 'left': False, 'right': False}

    rect.x += velocity.x * dt

    hit_list = [tile for tile in tiles if rect.colliderect(tile)]

    for tile in hit_list:
        if velocity.x > 0:
            rect.right = tile.left
            collisions['right'] = True
        elif velocity.x < 0:
            rect.left = tile.right
            collisions['left'] = True

    rect.y += velocity.y * dt

    hit_list = [tile for tile in tiles if rect.colliderect(tile)]

    for tile in hit_list:
        if velocity.y > 0:
            rect.bottom = tile.top
            collisions['bottom'] = True
        elif velocity.y < 0:
            rect.top = tile.bottom
            collisions['top'] = True

    return rect, collisions