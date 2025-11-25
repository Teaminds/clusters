# import uuid


# class Utils:

# @staticmethod
# def uid() -> str:
#     """
#     Генерирует уникальный строковый идентификатор (hex UUID).

#     :return: Уникальная строка
#     """
#     uid = uuid.uuid4().hex
#     return uid

# @staticmethod
# def calculate_trait_income(
#     b: float,
#     n: int,
#     m: int,
#     q: int,
#     w: int,
#     t: float = 1.0,
#     z: float = 1.0,
#     alpha: float = 2.0,
#     beta: float = 1.0,
# ) -> float:
#     """
#     Расчёт дохода от одного признака в группе юнитов.

#     :param b: базовый доход признака
#     :param n: количество уникальных вариантов признака в группе
#     :param m: количество уникальных вариантов признака на уровне (на поле)
#     :param q: количество юнитов в группе
#     :param w: количество юнитов на уровне (на поле)
#     :param alpha: степень влияния гомогенности (по умолчанию 2)
#     :param beta: степень влияния размера группы (по умолчанию 1)
#     :return: доход от признака для юнита
#     """
#     if q <= 1:
#         return 0.0  # Юнит вне группы
#     if n >= m:
#         return 0.0  # Полная разнотипность, доход признака нулевой

#     homogeneity = 1 - (n - 1) / (m - 1)  # Гомогенность от 0 до 1
#     group_size_ratio = q / w  # Размер группы от 0 до 1

#     return b * (homogeneity**alpha) * (group_size_ratio**beta) * t * z
