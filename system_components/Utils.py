import uuid
from typing import Dict, List, Optional, Union
from system_components.ResultCode import ResultCode


class Utils:
    """
    Утилитарные функции для проекта Expedica.

    Содержит:
    - Генератор уникальных идентификаторов
    - Преобразование snake_case в PascalCase
    - Универсальную арифметическую модификацию значений
    - Парсинг конфигурации изменений ресурсов
    """

    @staticmethod
    def uid() -> str:
        """
        Генерирует уникальный строковый идентификатор (hex UUID).

        :return: Уникальная строка
        """
        uid = uuid.uuid4().hex
        return uid

    @staticmethod
    def snake_to_pascal(snake_str: str) -> str:
        """
        Преобразует строку из snake_case в PascalCase.

        :param snake_str: Строка в snake_case
        :return: Строка в PascalCase
        """
        result = "".join(word.capitalize() for word in snake_str.split("_"))
        return result
