import math


class Vector2D:
    """Support for operation on a vector with 2-dimensional components."""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def unit_vector(self):
        return self / self.magnitude

    def rotate(self, degrees: float):
        """
        Rotates vector counter clockwise from its current position to
        the given degrees.

        For more information, see `Rotation Matrix`:
            https://en.wikipedia.org/wiki/Rotation_matrix
        """
        theta = math.radians(degrees)
        self.x = self.x * math.cos(theta) - self.y * math.sin(theta)
        self.y = self.x * math.sin(theta) + self.y * math.cos(theta)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def _arithmethic_operation(self, operation, other):
        if isinstance(other, self.__class__):
            return self.__class__(
                operation(self.x, other.x),
                operation(self.y, other.y),
            )
        elif isinstance(other, (int, float)):
            return self.__class__(
                operation(self.x, other),
                operation(self.y, other),
            )
        return NotImplemented

    def __add__(self, other):
        return self._arithmethic_operation(lambda a, b: a + b, other)

    def __sub__(self, other):
        return self._arithmethic_operation(lambda a, b: a - b, other)

    def __mul__(self, other):
        return self._arithmethic_operation(lambda a, b: a * b, other)

    def __truediv__(self, other):
        return self._arithmethic_operation(lambda a, b: a / b, other)

    def __floordiv__(self, other):
        return self._arithmethic_operation(lambda a, b: a // b, other)
