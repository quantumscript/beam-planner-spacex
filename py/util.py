import collections
import enum
import math


class Vector3:
    """A 3-dimensional vector."""
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float, y: float, z: float) -> None:
        """Create a new vector."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        """Pretty print a vector."""
        return 'Vector3(%.3f, %.3f, %.3f)' % (self.x, self.y, self.z)

    def __add__(self, other: 'Vector3') -> 'Vector3':
        """Add two vectors."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        """Subtract two vectors."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def mag(self) -> float:
        """Return the magnitude (length) of a vector."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def unit(self) -> 'Vector3':
        """
        Return the unit-vector in the same direction as a vector.

        WARNING: Undefined for zero-length vectors.
        """
        m = self.mag()
        return Vector3(self.x / m, self.y / m, self.z / m)

    def dot(self, other: 'Vector3') -> float:
        """Return the dot product of two vectors."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def angle_between(self, a: 'Vector3', c: 'Vector3') -> float:
        r"""
        Return the angle in degrees between (a - self) and (c - self):

        a       c
         \     /
          \.·./
           \ /
          self
        """
        m = (a - self).unit()
        n = (c - self).unit()
        r = m.dot(n)

        return math.degrees(math.acos(r))


class Color(enum.Enum):
    """A unique set of frequencies used to talk with a user."""
    A = 1
    B = 2
    C = 3
    D = 4


class Sat(int):
    """A unique satellite."""


class User(int):
    """A unique user."""
