from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Callable

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


def not_render(style: 'Style', a: 'CExpression') -> str:
    if style.not_operator_style == style.NotOperatorsStyles.Explicit:
        # Space before expression is important to not merge "not" with variables
        space = " "
    else:
        space = str(style.vspace_unary_operator)

    return (
        f"{style.not_operator_style.value}"
        f"{space}"
        f"{a.render()}"
    )


def and_render(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
    if style.and_operator_style == style.AndOperatorStyles.Explicit:
        before_space = " "
        after_space = " "
    else:
        before_space = str(style.vspace_before_binary_operator)
        after_space = str(style.vspace_after_binary_operator)

    return (
        f"{a.render()}"
        f"{before_space}"
        f"{style.and_operator_style.value}"
        f"{after_space}"
        f"{b.render()}"
    )


def or_render(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
    if style.or_operator_style == style.OrOperatorStyles.Explicit:
        before_space = " "
        after_space = " "
    else:
        before_space = str(style.vspace_before_binary_operator)
        after_space = str(style.vspace_after_binary_operator)

    return (
        f"{a.render()}"
        f"{before_space}"
        f"{style.and_operator_style.value}"
        f"{after_space}"
        f"{b.render()}"
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
        Not = CUnaryOperator(not_render)
        And = CBinaryOperator(and_render)
        Or = CBinaryOperator(or_render)

    class Comparison:
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
