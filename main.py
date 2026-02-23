"""
Battleship: Fog of War
Главный модуль запуска игры
"""

import pygame
import sys
from core.game import Game
from ui.menu import Menu

def main():
    """Основная функция запуска игры"""
    pygame.init()
    
    # Настройки экрана
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Battleship: Fog of War 🌊")
    
    # Загрузка иконки (если есть)
    # icon = pygame.image.load('assets/icon.png')
    # pygame.display.set_icon(icon)
    
    clock = pygame.time.Clock()
    
    # Создание меню
    menu = Menu(screen)
    
    # Главный цикл
    running = True
    game_started = False
    game = None
    
    while running:
        if not game_started:
            # Показываем меню
            action = menu.handle_events()
            
            if action == "start":
                game_started = True
                game = Game(screen)
            elif action == "quit":
                running = False
                
            menu.draw()
        else:
            # Запускаем игру
            result = game.run()
            
            if result == "menu":
                game_started = False
                game = None
            elif result == "quit":
                running = False
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
