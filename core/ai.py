"""
Модуль ИИ
"""

import random
from core.player import Player

class AI(Player):
    """Класс ИИ с различными стратегиями"""
    
    def __init__(self, difficulty="medium"):
        super().__init__(is_human=False)
        self.difficulty = difficulty
        self.last_hits = []  # Последние попадания
        self.target_mode = False  # Режим поиска оставшихся частей корабля
        self.target_direction = None  # Направление поиска
        self.possible_targets = []
        
        # Счетчик уровня сложности
        self.level = 1
        self.hits_count = 0
        self.misses_count = 0
    
    def make_move(self):
        """Принятие решения о ходе"""
        if self.difficulty == "easy":
            return self.easy_ai_move()
        elif self.difficulty == "medium":
            return self.medium_ai_move()
        else:  # hard
            return self.hard_ai_move()
    
    def easy_ai_move(self):
        """Простой ИИ - случайные выстрелы"""
        attempts = 0
        while attempts < 100:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            
            if not self.grid[x][y].shot:
                return x, y
            
            attempts += 1
        
        return None, None
    
    def medium_ai_move(self):
        """Средний ИИ - поиск пострадавших кораблей"""
        # Если есть непроверенные попадания, ищем вокруг
        if self.last_hits:
            # Ищем вокруг последнего попадания
            last_x, last_y = self.last_hits[-1]
            
            # Проверяем соседние клетки
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = last_x + dx, last_y + dy
                if 0 <= nx < 10 and 0 <= ny < 10 and not self.grid[nx][ny].shot:
                    return nx, ny
        
        # Если нет попаданий - случайный выстрел
        return self.easy_ai_move()
    
    def hard_ai_move(self):
        """Сложный ИИ - адаптивная стратегия"""
        # Анализ вероятностей
        if self.target_mode and self.possible_targets:
            # Выбираем следующую цель
            target = self.possible_targets.pop(0)
            if not self.grid[target[0]][target[1]].shot:
                return target
        
        # Поиск непроверенных клеток с высокой вероятностью
        candidates = []
        
        for x in range(10):
            for y in range(10):
                if not self.grid[x][y].shot:
                    # Оценка вероятности наличия корабля
                    probability = self.calculate_probability(x, y)
                    candidates.append((probability, x, y))
        
        if candidates:
            # Сортируем по вероятности
            candidates.sort(reverse=True)
            return candidates[0][1], candidates[0][2]
        
        return self.easy_ai_move()
    
    def calculate_probability(self, x, y):
        """Расчет вероятности наличия корабля в клетке"""
        probability = 1.0
        
        # Учитываем соседние попадания
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                if self.grid[nx][ny].shot and self.grid[nx][ny].has_ship:
                    probability *= 2.0
                elif self.grid[nx][ny].shot:
                    probability *= 0.5
        
        return probability
    
    def update_difficulty(self):
        """Обновление сложности на основе прогресса"""
        if self.hits_count > self.misses_count * 2:
            self.level += 1
            if self.level > 3:
                self.level = 3
        
        difficulties = ["easy", "medium", "hard"]
        self.difficulty = difficulties[self.level - 1]
    
    def shoot(self, opponent, x, y):
        """Переопределение метода shoot для ИИ"""
        result = super().shoot(opponent, x, y)
        
        if result == "hit":
            self.last_hits.append((x, y))
            self.hits_count += 1
            
            # Обновляем режим цели
            if len(self.last_hits) >= 2:
                self.target_mode = True
                
                # Определяем направление
                if len(self.last_hits) >= 2:
                    dx = self.last_hits[-1][0] - self.last_hits[-2][0]
                    dy = self.last_hits[-1][1] - self.last_hits[-2][1]
                    
                    # Добавляем следующую цель в направлении
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        self.possible_targets.append((nx, ny))
        else:
            self.misses_count += 1
        
        # Обновляем сложность
        self.update_difficulty()
        
        return result
