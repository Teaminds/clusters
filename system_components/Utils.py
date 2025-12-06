import uuid
from system_components.ResultCode import ResultCode


class Utils:

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

    @staticmethod
    def sort_dict_recursive(d):
        if isinstance(d, dict):
            result = {}
            for k in sorted(d):
                result[k] = Utils.sort_dict_recursive(d[k])
            return result
        elif isinstance(d, list):
            return [Utils.sort_dict_recursive(i) for i in d]
        else:
            return d

    @staticmethod
    def get_2d_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    @staticmethod
    def get_next_item_of_dict(dictionary, current_key):
        keys = list(dictionary.keys())
        idx = keys.index(current_key)
        if idx + 1 < len(keys):
            next_key = keys[idx + 1]
            return (next_key, dictionary[next_key])
        return (None, None)

    @staticmethod
    def get_next_item_of_list(lst, current_item):
        if current_item in lst:
            idx = lst.index(current_item)
            if idx + 1 < len(lst):
                return lst[idx + 1]
        return None
