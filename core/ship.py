"""
Модуль корабля
"""

from enum import Enum

class ShipType(Enum):
    """Типы кораблей"""
    CARRIER = "Авианосец"
    BATTLESHIP = "Линкор"
    CRUISER = "Крейсер"
    SUBMARINE = "Подлодка"
    DESTROYER = "Эсминец"

class Ship:
    """Класс корабля"""
    
    def __init__(self, ship_type, size):
        self.ship_type = ship_type
        self.size = size
        self.hits = 0
        self.placed = False
        self.cells = []
        self.horizontal = True
    
    def hit(self):
        """Попадание по кораблю"""
        self.hits += 1
    
    def is_destroyed(self):
        """Проверка, уничтожен ли корабль"""
        return self.hits >= self.size
    
    def place(self, cells, horizontal):
        """Размещение корабля"""
        self.cells = cells
        self.horizontal = horizontal
        self.placed = True
        self.hits = 0
    
    def get_color(self):
        """Цвет корабля для отрисовки"""
        if self.is_destroyed():
            return (100, 100, 100)  # Серый для уничтоженных
        elif self.placed:
            return (0, 150, 0)  # Зеленый для размещенных
        else:
            return (150, 150, 150)  # Светло-серый для доступных
    
    def __repr__(self):
        return f"{self.ship_type.value} ({self.size})"
