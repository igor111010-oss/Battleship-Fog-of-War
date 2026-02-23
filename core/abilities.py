"""
Модуль системы способностей
"""

class Ability:
    """Класс способности"""
    
    def __init__(self, name, cost, description, key_binding):
        self.name = name
        self.cost = cost
        self.description = description
        self.key_binding = key_binding
        self.available = True

class AbilitySystem:
    """Система управления способностями"""
    
    def __init__(self):
        self.ability_points = 0
        self.abilities = {
            "radar": Ability(
                "🔍 Радар", 
                30, 
                "Показывает пустые клетки в области 3x3", 
                "1"
            ),
            "drone": Ability(
                "🚁 Дрон", 
                50, 
                "Находит одну случайную клетку с кораблем", 
                "2"
            ),
            "double_shot": Ability(
                "💥 Двойной выстрел", 
                40, 
                "Позволяет сделать два выстрела за ход", 
                "3"
            )
        }
    
    def add_points(self, points):
        """Добавление очков способностей"""
        self.ability_points += points
    
    def can_use_ability(self, ability_name):
        """Проверка возможности использования способности"""
        if ability_name in self.abilities:
            ability = self.abilities[ability_name]
            return self.ability_points >= ability.cost and ability.available
        return False
    
    def use_ability(self, ability_name):
        """Использование способности"""
        if self.can_use_ability(ability_name):
            ability = self.abilities[ability_name]
            self.ability_points -= ability.cost
            ability.available = False
            return True
        return False
    
    def reset_abilities(self):
        """Сброс способностей для нового раунда"""
        for ability in self.abilities.values():
            ability.available = True
    
    def get_ability_info(self, ability_name):
        """Получение информации о способности"""
        return self.abilities.get(ability_name)
