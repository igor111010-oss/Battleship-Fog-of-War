"""
Основной игровой модуль
"""

import pygame
import random
from core.player import Player
from core.ai import AI
from core.abilities import AbilitySystem
from ui.renderer import Renderer

class Game:
    """Главный класс игры"""
    
    def __init__(self, screen):
        self.screen = screen
        self.renderer = Renderer(screen)
        
        # Создание игроков
        self.player = Player(is_human=True)
        self.ai = AI(is_human=False)
        
        # Система способностей
        self.ability_system = AbilitySystem()
        
        # Состояние игры
        self.current_turn = "player"  # player или ai
        self.game_over = False
        self.winner = None
        
        # Фазы игры
        self.setup_phase = True
        self.battle_phase = False
        
        # Счетчики
        self.player_score = 0
        self.ai_score = 0
        self.turn_count = 0
        
        # Расстановка кораблей
        self.ship_placement_mode = False
        self.selected_ship = None
        
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                
                if self.setup_phase:
                    self.handle_setup_events(event)
                else:
                    self.handle_battle_events(event)
            
            # Обновление и отрисовка
            self.update()
            self.draw()
            
            # Проверка на окончание игры
            if not self.game_over:
                self.check_game_over()
            
            pygame.display.flip()
        
        return "menu"
    
    def handle_setup_events(self, event):
        """Обработка событий в фазе расстановки"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Проверка клика по сетке игрока
            grid_rect = pygame.Rect(50, 50, 300, 300)
            if grid_rect.collidepoint(mouse_pos):
                grid_x = (mouse_pos[0] - 50) // 30
                grid_y = (mouse_pos[1] - 50) // 30
                
                if self.player.place_ship(grid_x, grid_y, self.selected_ship):
                    self.selected_ship = None
            
            # Кнопка готовности
            ready_button = pygame.Rect(650, 500, 100, 40)
            if ready_button.collidepoint(mouse_pos):
                if self.player.all_ships_placed():
                    self.setup_phase = False
                    self.battle_phase = True
                    self.ai.place_ships_random()
    
    def handle_battle_events(self, event):
        """Обработка событий в фазе битвы"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.current_turn == "player":
            mouse_pos = pygame.mouse.get_pos()
            
            # Проверка клика по сетке ИИ
            ai_grid_rect = pygame.Rect(450, 50, 300, 300)
            if ai_grid_rect.collidepoint(mouse_pos):
                grid_x = (mouse_pos[0] - 450) // 30
                grid_y = (mouse_pos[1] - 50) // 30
                
                # Выстрел по позиции
                result = self.player.shoot(self.ai, grid_x, grid_y)
                
                if result:
                    if result == "hit":
                        self.ability_system.add_points(10)
                    
                    self.current_turn = "ai"
                    self.turn_count += 1
        
        # Обработка способностей
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and self.ability_system.can_use_ability("radar"):
                self.use_ability("radar")
            elif event.key == pygame.K_2 and self.ability_system.can_use_ability("drone"):
                self.use_ability("drone")
            elif event.key == pygame.K_3 and self.ability_system.can_use_ability("double_shot"):
                self.use_ability("double_shot")
    
    def use_ability(self, ability_name):
        """Использование способности"""
        if ability_name == "radar":
            # Логика радара
            mouse_pos = pygame.mouse.get_pos()
            if 450 <= mouse_pos[0] <= 750 and 50 <= mouse_pos[1] <= 350:
                grid_x = (mouse_pos[0] - 450) // 30
                grid_y = (mouse_pos[1] - 50) // 30
                
                # Показываем пустые клетки в области 3x3
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = grid_x + dx, grid_y + dy
                        if 0 <= nx < 10 and 0 <= ny < 10:
                            if nx == grid_x and ny == grid_y:
                                continue
                            if not self.ai.grid[nx][ny].has_ship:
                                self.ai.grid[nx][ny].revealed = True
                
                self.ability_system.use_ability("radar")
        
        elif ability_name == "drone":
            # Дрон находит случайный корабль
            for x in range(10):
                for y in range(10):
                    if self.ai.grid[x][y].has_ship and not self.ai.grid[x][y].revealed:
                        self.ai.grid[x][y].revealed = True
                        self.ability_system.use_ability("drone")
                        return
        
        elif ability_name == "double_shot":
            # Двойной выстрел - следующий ход можно стрелять дважды
            self.player.double_shot_active = True
            self.ability_system.use_ability("double_shot")
    
    def update(self):
        """Обновление состояния игры"""
        if self.battle_phase and self.current_turn == "ai" and not self.game_over:
            # Ход ИИ
            pygame.time.wait(500)  # Задержка для эффекта
            x, y = self.ai.make_move()
            
            if x is not None:
                self.ai.shoot(self.player, x, y)
                self.current_turn = "player"
    
    def draw(self):
        """Отрисовка игры"""
        self.screen.fill((30, 30, 50))  # Темно-синий фон
        
        if self.setup_phase:
            self.renderer.draw_setup_phase(self.player, self.selected_ship)
        else:
            self.renderer.draw_battle_phase(
                self.player, self.ai, 
                self.current_turn, 
                self.ability_system,
                self.turn_count
            )
        
        if self.game_over:
            self.renderer.draw_game_over(self.winner)
    
    def check_game_over(self):
        """Проверка окончания игры"""
        if self.player.all_ships_destroyed():
            self.game_over = True
            self.winner = "ai"
        elif self.ai.all_ships_destroyed():
            self.game_over = True
            self.winner = "player"
