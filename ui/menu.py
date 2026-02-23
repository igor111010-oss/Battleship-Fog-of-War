"""
Модуль меню
"""

import pygame

class Menu:
    """Класс меню"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Кнопки
        self.buttons = {
            "start": pygame.Rect(300, 250, 200, 50),
            "settings": pygame.Rect(300, 320, 200, 50),
            "quit": pygame.Rect(300, 390, 200, 50)
        }
        
        # Анимация
        self.wave_offset = 0
        self.clock = pygame.time.Clock()
    
    def handle_events(self):
        """Обработка событий меню"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                for button_name, button_rect in self.buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        if button_name == "quit":
                            return "quit"
                        elif button_name == "start":
                            return "start"
                        elif button_name == "settings":
                            return "settings"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
        
        return None
    
    def draw(self):
        """Отрисовка меню"""
        self.screen.fill((20, 40, 80))  # Темно-синий фон
        
        # Анимированные волны
        self.wave_offset += 1
        self.draw_waves()
        
        # Заголовок
        title = self.font_large.render("BATTLESHIP", True, (255, 255, 255))
        subtitle = self.font_medium.render("Fog of War", True, (200, 200, 255))
        
        title_rect = title.get_rect(center=(400, 150))
        subtitle_rect = subtitle.get_rect(center=(400, 200))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Кнопки
        self.draw_button("Начать игру", self.buttons["start"], (0, 150, 0))
        self.draw_button("Настройки", self.buttons["settings"], (150, 150, 0))
        self.draw_button("Выход", self.buttons["quit"], (150, 0, 0))
        
        # Подсказка
        hint = self.font_small.render("Нажмите ESC для выхода", True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(400, 550))
        self.screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def draw_button(self, text, rect, color):
        """Отрисовка кнопки"""
        # Проверка наведения мыши
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            color = tuple(min(c + 50, 255) for c in color)
            rect = rect.inflate(10, 10)
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=10)
        
        text_surf = self.font_medium.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def draw_waves(self):
        """Отрисовка анимированных волн"""
        for i in range(10):
            wave_y = 400 + i * 20 + pygame.math.Vector2(1, 0).rotate(self.wave_offset + i * 36).y * 10
            pygame.draw.line(
                self.screen, 
                (50, 100, 200), 
                (0, wave_y), 
                (800, wave_y), 
                2
            )
