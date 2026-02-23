"""
Модуль игрока
"""

import random
from core.ship import Ship, ShipType

class Cell:
    """Класс клетки игрового поля"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_ship = False
        self.shot = False
        self.revealed = False
        self.ship = None
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y}, ship={self.has_ship})"

class Player:
    """Базовый класс игрока"""
    
    def __init__(self, is_human=False):
        self.is_human = is_human
        self.grid = [[Cell(x, y) for y in range(10)] for x in range(10)]
        self.ships = []
        self.placed_ships = []
        self.double_shot_active = False
        
        # Создание кораблей
        self.available_ships = [
            Ship(ShipType.CARRIER, 5),
            Ship(ShipType.BATTLESHIP, 4),
            Ship(ShipType.CRUISER, 3),
            Ship(ShipType.SUBMARINE, 3),
            Ship(ShipType.DESTROYER, 2)
        ]
    
    def place_ship(self, x, y, ship_type, horizontal=True):
        """Размещение корабля на поле"""
        if ship_type is None:
            return False
        
        # Поиск корабля среди доступных
        ship = None
        for s in self.available_ships:
            if s.ship_type == ship_type and not s.placed:
                ship = s
                break
        
        if not ship:
            return False
        
        # Проверка возможности размещения
        if not self.can_place_ship(x, y, ship.size, horizontal):
            return False
        
        # Размещение корабля
        cells = []
        for i in range(ship.size):
            cx = x + (i if horizontal else 0)
            cy = y + (0 if horizontal else i)
            
            self.grid[cx][cy].has_ship = True
            self.grid[cx][cy].ship = ship
            cells.append((cx, cy))
        
        ship.place(cells, horizontal)
        self.placed_ships.append(ship)
        
        return True
    
    def can_place_ship(self, x, y, size, horizontal):
        """Проверка возможности размещения корабля"""
        # Проверка границ
        if horizontal and x + size > 10:
            return False
        if not horizontal and y + size > 10:
            return False
        
        # Проверка соседних клеток (корабль не должен касаться других)
        for dx in range(-1, size + 1):
            for dy in range(-1, 2):
                nx = x + (dx if horizontal else 0)
                ny = y + (0 if horizontal else dy)
                
                if not horizontal:
                    nx = x + dy
                    ny = y + dx
                
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if horizontal:
                        if dy == 0 and 0 <= dx < size:
                            continue
                    
                    if self.grid[nx][ny].has_ship:
                        return False
        
        return True
    
    def all_ships_placed(self):
        """Проверка, все ли корабли размещены"""
        return len(self.placed_ships) == len(self.available_ships)
    
    def shoot(self, opponent, x, y):
        """Выстрел по противнику"""
        if x < 0 or x >= 10 or y < 0 or y >= 10:
            return None
        
        target_cell = opponent.grid[x][y]
        
        if target_cell.shot:
            return None  # Уже стреляли сюда
        
        target_cell.shot = True
        
        if target_cell.has_ship:
            # Попадание
            ship = target_cell.ship
            ship.hit()
            
            # Проверка на уничтожение корабля
            if ship.is_destroyed():
                # Отмечаем все клетки вокруг уничтоженного корабля
                self.mark_around_ship(opponent, ship)
            
            return "hit"
        else:
            # Промах
            return "miss"
    
    def mark_around_ship(self, opponent, ship):
        """Отмечает клетки вокруг уничтоженного корабля"""
        for cell_x, cell_y in ship.cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cell_x + dx, cell_y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        opponent.grid[nx][ny].shot = True
    
    def all_ships_destroyed(self):
        """Проверка, все ли корабли уничтожены"""
        for ship in self.placed_ships:
            if not ship.is_destroyed():
                return False
        return True
    
    def place_ships_random(self):
        """Автоматическая расстановка кораблей"""
        for ship in self.available_ships:
            placed = False
            attempts = 0
            
            while not placed and attempts < 100:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                horizontal = random.choice([True, False])
                
                if self.place_ship(x, y, ship.ship_type, horizontal):
                    placed = True
                
                attempts += 1
