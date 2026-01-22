import sys
import pygame
from src import config
from src.scenes.game_scene import GameScene
from src.scenes.menu_scene import MenuScene
from src.scenes.dead_scene import DeadScene
from src.scenes.win_scene import WinScene

def main():
    pygame.init()

    monitor_info = pygame.display.Info()
    MONITOR_WIDTH = monitor_info.current_w
    MONITOR_HEIGHT = monitor_info.current_h


    screen = pygame.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT), pygame.FULLSCREEN)
    game_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


    scale_w = MONITOR_WIDTH / config.SCREEN_WIDTH
    scale_h = MONITOR_HEIGHT / config.SCREEN_HEIGHT
    scale = min(scale_w, scale_h)
    new_width = int(config.SCREEN_WIDTH * scale)
    new_height = int(config.SCREEN_HEIGHT * scale)
    offset_x = (MONITOR_WIDTH - new_width) // 2
    offset_y = (MONITOR_HEIGHT - new_height) // 2

    clock = pygame.time.Clock()

    current_state = "MENU"
    menu_scene = MenuScene()
    game_scene = None
    dead_scene = None
    win_scene = None

    running = True


    while running:
        dt = clock.tick(config.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == "MENU":
                menu_scene.handle_input(event)
            elif current_state == "GAME":
                 game_scene.handle_input(event)
            elif current_state == "DEAD":
                dead_scene.handle_input(event)
            elif current_state == "WIN":
                win_scene.handle_input(event)

        if current_state == "MENU":
            if menu_scene.finished:
                game_scene = GameScene()
                current_state = "GAME"
                menu_scene.finished = False

        if current_state == "DEAD":
            if dead_scene.finished:
                game_scene = GameScene()
                current_state = "GAME"
                dead_scene.finished = False


        if current_state == "GAME":
            if game_scene.char_is_dead:
                game_scene = None
                dead_scene = DeadScene()
                current_state = "DEAD"
            elif game_scene.has_won:
                game_scene = None
                win_scene = WinScene()
                current_state = "WIN"

        if current_state == "WIN":
            if win_scene.finished:
                pygame.quit()
                sys.exit()



        if current_state == "MENU":
            menu_scene.update(dt)
        elif current_state == "GAME":
            game_scene.update(dt)
        elif current_state == "DEAD":
            dead_scene.update(dt)
        elif current_state == "WIN":
            win_scene.update(dt)

        game_surface.fill((0, 0, 0))

        if current_state == "MENU":
            menu_scene.draw(game_surface)
        elif current_state == "GAME":
            game_scene.draw(game_surface)
        elif current_state == "DEAD":
            dead_scene.draw(game_surface)
        elif current_state == "WIN":
            win_scene.draw(game_surface)

        screen.fill((0, 0, 0))
        scaled_surface = pygame.transform.scale(game_surface, (new_width, new_height))
        screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()