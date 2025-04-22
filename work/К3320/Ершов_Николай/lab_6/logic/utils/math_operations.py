from math import sqrt

__all__ = (
    'MathOperations',
)


class MathOperations:
    """Класс содержащий логику математических операций"""

    @classmethod
    def pythagoras(cls, a: float, b: float) -> str:
        """Возвращает гипотенузу треугольника по теореме Пифагора"""
        if a < 0 or b < 0:
            return f"Треугольника с такими сторонами не существует!"
        return f"Гипотенуза этого треугольника: {(a ** 2 + b ** 2) ** 0.5}"

    @classmethod
    def quadratic(cls, a: float, b: float, c: float) -> str:
        """Возвращает решение квадратного уравнения"""
        D = b ** 2 - 4 * a * c
        if D < 0:
            return f"Нет решений"
        elif D == 0:
            return f"Найдено одно решение: x = {-b / (2 * a)}"
        else:
            x1 = (-b + sqrt(D)) / (2 * a)
            x2 = (-b - sqrt(D)) / (2 * a)
            return f"Найдено два решения: x1 = {x1}, x2 = {x2}"

    @classmethod
    def trapezoid_area(cls, a: float, b: float, h: float) -> str:
        """Возвращает площадь трапеции"""
        if a < 0 or b < 0 or h < 0:
            return f"Трапеции с такими сторонами не существует!"
        return f"Площадь трапеции: {(a + b) * h / 2}"

    @classmethod
    def parallelogram_area(cls, a: float, h: float) -> str:
        """Возвращает площадь параллелограмма"""
        if a < 0 or h < 0:
            return f"Параллелограмма с такими сторонами не существует!"
        return f"Площадь параллелограмма: {a * h}"
