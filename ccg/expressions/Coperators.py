from abc import abstractmethod
from typing import TYPE_CHECKING, Callable
from enum import Enum

from .Cexpression import CExpression
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style


class COperation(CExpression):

    @abstractmethod
    def render(self, style: 'Style' = default_style) -> str:
        raise NotImplementedError


class CUnaryOperation(COperation):

    def __init__(self,
                 render_function: Callable[['Style', 'CExpression'], str],
                 a: 'CExpression'
                 ):
        self.render_function = render_function
        self.a = a

    def render(self, style: 'Style' = default_style) -> str:
        return self.render_function(style, self.a)


class CBinaryOperation(COperation):

    def __init__(self,
                 render_function: Callable[['Style', 'CExpression', 'CExpression'], str],
                 a: 'CExpression',
                 b: 'CExpression'
                 ):
        self.render_function = render_function
        self.a = a
        self.b = b

    def render(self, style: 'Style' = default_style) -> str:
        return self.render_function(style, self.a, self.b)


class COperator:
    pass


class CUnaryOperator(COperator):
    def __init__(self, render_function: Callable[['Style', 'CExpression'], str]):
        self.render_function = render_function

    def __call__(self, a: 'CExpression') -> 'CUnaryOperation':
        return CUnaryOperation(self.render_function, a)


class CBinaryOperator(COperator):

    def __init__(self, render_function: Callable[['Style', 'CExpression', 'CExpression'], str]):
        self.render_function = render_function

    def __call__(self, a: 'CExpression', b: 'CExpression') -> 'COperation':
        return CBinaryOperation(self.render_function, a, b)


class CUnaryOperatorToken(CUnaryOperator):
    class Order(Enum):
        Before = 0
        After = 1

    def __init__(self, operator_token: str, order: Order):
        self.operator_token = operator_token
        self.order = order

        if self.order == self.Order.Before:
            def generator(style: 'Style', a: 'CExpression') -> 'str':
                return (
                    f"{operator_token}"
                    f"{style.vspace_unary_operator}"
                    f"{a.render(style)}"
                )
        elif self.order == self.Order.After:
            def generator(style: 'Style', a: 'CExpression') -> 'str':
                return (
                    f"{a.render(style)}"
                    f"{style.vspace_unary_operator}"
                    f"{operator_token}"
                )
        else:
            raise ValueError

        super(CUnaryOperatorToken, self).__init__(generator)


class CBinaryOperatorToken(CBinaryOperator):
    def __init__(self, operator_token: str):
        def generator(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
            return (
                f"{a.render(style)}"
                f"{style.vspace_before_binary_operator}"
                f"{operator_token}"
                f"{style.vspace_after_binary_operator}"
                f"{b.render(style)}"
            )

        super(CBinaryOperatorToken, self).__init__(generator)


def subscript_render(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
    return f"{a.render(style)}[{b.render(style)}]"


def parentheses_render(style: 'Style', a: 'CExpression') -> str:
    return (
        f"{style.vspace_before_parentheses_operator}"
        f"({a.render(style)})"
        f"{style.vspace_after_parentheses_operator}"
    )


class COperators:
    class IncrementDecrement:
        PreIncrement = CUnaryOperatorToken("++", order=CUnaryOperatorToken.Order.Before)
        PreDecrement = CUnaryOperatorToken("--", order=CUnaryOperatorToken.Order.Before)
        PostIncrement = CUnaryOperatorToken("++", order=CUnaryOperatorToken.Order.After)
        PostDecrement = CUnaryOperatorToken("--", order=CUnaryOperatorToken.Order.After)

    class Arithmetic:
        Sum = CBinaryOperatorToken("+")
        Subtract = CBinaryOperatorToken("-")
        Multiply = CBinaryOperatorToken("*")
        Divide = CBinaryOperatorToken("/")
        Modulus = CBinaryOperatorToken("%")

        BitWiseNot = CUnaryOperatorToken("~", order=CUnaryOperatorToken.Order.Before)
        BitWiseAnd = CBinaryOperatorToken("&")
        BitWiseOr = CBinaryOperatorToken("|")
        BitWiseXor = CBinaryOperatorToken("^")
        BitWiseLeftShift = CBinaryOperatorToken("<<")
        BitWiseRightShift = CBinaryOperatorToken(">>")

    class Assignment:
        Assign = CBinaryOperatorToken("=")
        SumAssignment = CBinaryOperatorToken("+=")
        SubtractAssignment = CBinaryOperatorToken("-=")
        MultiplyAssignment = CBinaryOperatorToken("*=")
        DivideAssignment = CBinaryOperatorToken("/=")
        ModulusAssignment = CBinaryOperatorToken("%=")

        BitWiseAndAssignment = CBinaryOperatorToken("&=")
        BitWiseOrAssignment = CBinaryOperatorToken("|=")
        BitWiseXorAssignment = CBinaryOperatorToken("^=")
        BitWiseLeftShiftAssignment = CBinaryOperatorToken("<<=")
        BitWiseRightShiftAssignment = CBinaryOperatorToken(">>=")

    class Logic:
        # TODO style with not, and and or operator tokens??
        Not = CUnaryOperatorToken("!", order=CUnaryOperatorToken.Order.Before)
        And = CBinaryOperatorToken("&&")
        Or = CBinaryOperatorToken("||")

    class Comparisson:
        EqualTo = CBinaryOperatorToken("==")
        NotEqualTo = CBinaryOperatorToken("!=")
        LessThan = CBinaryOperatorToken("<")
        GreaterThan = CBinaryOperatorToken(">")
        LessThanOrEqualTo = CBinaryOperatorToken("<=")
        GreatherThanOrEqualTo = CBinaryOperatorToken(">=")

    class MemberAccess:
        SubScript = CBinaryOperator(subscript_render)
        Indirection = CUnaryOperatorToken("*", order=CUnaryOperatorToken.Order.Before)
        AddressOf = CUnaryOperatorToken('&', order=CUnaryOperatorToken.Order.Before)
        MemberOfObject = CBinaryOperatorToken('.')
        MemberOfPointer = CBinaryOperatorToken('->')
        PointerToMemberOfObject = CBinaryOperatorToken('.*')
        PointerToMemberOfPointer = CBinaryOperatorToken('->*')

    Parentheses = CUnaryOperator(parentheses_render)
