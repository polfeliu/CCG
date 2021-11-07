from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style


class CExpression(ABC):

    @abstractmethod
    def render(self, style: 'Style' = default_style) -> str:
        raise NotImplemented

    def __add__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.Sum(self, other)

    def __sub__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.Subtract(self, other)

    def __mul__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.Multiply(self, other)

    def __truediv__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.Divide(self, other)

    def __mod__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.Modulus(self, other)

    def __lshift__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.BitWiseLeftShift(self, other)

    def __rshift__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Arithmetic.BitWiseRightShift(self, other)

    def __and__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Logic.And(self, other)

    def __or__(self, other: 'CExpression') -> 'CExpression':
        return COperators.Logic.Or(self, other)

    def __pos__(self) -> 'CExpression':
        return COperators.Arithmetic.UnaryPlus(self)

    def __neg__(self) -> 'CExpression':
        return COperators.Arithmetic.UnaryMinus(self)

    def __invert__(self) -> 'CExpression':
        return COperators.Logic.Not(self)


class CExpressionFreeStyle(CExpression):

    def __init__(self, content: str):
        self.content = content

    def render(self, style: 'Style' = default_style) -> str:
        return self.content


# Dependency for operator overloading
from .Coperators import COperators
