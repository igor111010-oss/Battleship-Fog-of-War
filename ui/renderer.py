"""
Модуль отрисовки игры
"""

import pygame

class Renderer:
    """Класс для отрисовки игровых элементов"""
    
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 30
        self.grid_offset = 50
        
        # Шрифты
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        
        # Цвета
        self.colors = {
            "water": (64, 128, 255),
            "ship": (0, 150, 0),
            "hit": (255, 0, 0),
            "miss": (200, 200, 200),
            "grid": (100, 100, 255),
            "text": (255, 255, 255)
        }
    
    def draw_setup_phase(self, player, selected_ship):
        """Отрисовка фазы расстановки"""
        # Сетка игрока
        self.draw_grid(50, 50, player.grid, show_ships=True)
        
        # Доступные корабли
        y_offset = 50
        for ship in player.available_ships:
            if not ship.placed:
                color = (0, 200, 0) if ship.ship_type == selected_ship else (150, 150, 150)
                self.draw_ship_info(400, y_offset, ship, color)
                y_offset += 40
        
        # Инструкция
        instructions = [
            "Расставьте корабли:",
            "Кликните на корабль, затем на поле",
            "Горизонтально/вертикально - ПКМ",
            "Готово - когда все корабли расставлены"
        ]
        
        y_offset = 400
        for instruction in instructions:
            text = self.font_small.render(instruction, True, (255, 255, 255))
            self.screen.blit(text, (400, y_offset))
            y_offset += 25
        
        # Кнопка готовности
        if player.all_ships_placed():
            self.draw_button("Начать битву!", (650, 500, 100, 40), (0, 150, 0))
    
    def draw_battle_phase(self, player, ai, current_turn, ability_system, turn_count):
        """Отрисовка фазы битвы"""
        # Сетка игрока (слева)
        self.draw_grid(50, 50, player.grid, show_ships=True, show_shots=True)
        
        # Сетка ИИ (справа)
        self.draw_grid(450, 50, ai.grid, show_ships=False, show_shots=True)
        
        # Информация о ходе
        turn_text = f"Ход: {'Игрок' if current_turn == 'player' else 'ИИ'}"
        turn_color = (0, 255, 0) if current_turn == 'player' else (255, 0, 0)
        text = self.font_medium.render(turn_text, True, turn_color)
        self.screen.blit(text, (300, 400))
        
        # Счетчик ходов
        turn_count_text = f"Ходов: {turn_count}"
        text = self.font_small.render(turn_count_text, True, (200, 200, 200))
        self.screen.blit(text, (300, 450))
        
        # Способности
        self.draw_abilities(ability_system)
        
        # Статус игроков
        self.draw_status(player, ai)
    
    def draw_grid(self, x_offset, y_offset, grid, show_ships=True, show_shots=True):
        """Отрисовка игровой сетки"""
        # Рисуем клетки
        for x in range(10):
            for y in range(10):
                cell = grid[x][y]
                rect = pygame.Rect(
                    x_offset + x * self.cell_size,
                    y_offset + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Цвет клетки
                if cell.shot:
                    if cell.has_ship:
                        color = (255, 0, 0)  # Попадание
                    else:
                        color = (100, 100, 100)  # Промах
                elif show_ships and cell.has_ship and cell.ship:
                    color = cell.ship.get_color()  # Цвет корабля
                elif cell.revealed:
                    color = (200, 200, 255)  # Раскрытая клетка
                else:
                    color = (0, 100, 200)  # Вода
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
        
        # Координаты
        for i in range(10):
            # Буквы (A-J) по горизонтали
            letter = chr(65 + i)
            text = self.font_small.render(letter, True, (255, 255, 255))
            self.screen.blit(
                text, 
                (x_offset + i * self.cell_size + 10, y_offset - 20)
            )
            
            # Цифры (1-10) по вертикали
            text = self.font_small.render(str(i + 1), True, (255, 255, 255))
            self.screen.blit(
                text, 
                (x_offset - 20, y_offset + i * self.cell_size + 10)
            )
    
    def draw_ship_info(self, x, y, ship, color):
        """Отрисовка информации о корабле"""
        rect = pygame.Rect(x, y, 150, 30)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=5)
        
        text = self.font_small.render(
            f"{ship.ship_type.value} ({ship.size})", 
            True, 
            (255, 255, 255)
        )
        self.screen.blit(text, (x + 10, y + 5))
    
    def draw_abilities(self, ability_system):
        """Отрисовка панели способностей"""
        y_offset = 500
        
        # Заголовок
        title = self.font_small.render("Способности:", True, (255, 255, 255))
        self.screen.blit(title, (50, y_offset))
        
        # Очки способностей
        points_text = f"Очки: {ability_system.ability_points}"
        points = self.font_small.render(points_text, True, (255, 255, 0))
        self.screen.blit(points, (200, y_offset))
        
        # Список способностей
        y_offset += 30
        for ability_name, ability in ability_system.abilities.items():
            # Цвет в зависимости от доступности
            if ability_system.can_use_ability(ability_name):
                color = (0, 255, 0)
            else:
                color = (150, 150, 150)
            
