from abc import abstractmethod
from typing import TYPE_CHECKING, Callable
from enum import Enum

from .Cexpression import CExpression, CExpressionFreeStyle
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style


# TODO Styling, mainly spaces


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
                return f"{operator_token}{a.render(style)}"  # TODO Spaces
        elif self.order == self.Order.After:
            def generator(style: 'Style', a: 'CExpression') -> 'str':
                return f"{a.render(style)}{operator_token}"  # TODO Spaces
        else:
            raise ValueError

        super(CUnaryOperatorToken, self).__init__(generator)


class CBinaryOperatorToken(CBinaryOperator):
    def __init__(self, operator_token: str):
        def generator(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
            return f"{a.render(style)}{operator_token}{b.render(style)}"  # TODO Spaces

        super(CBinaryOperatorToken, self).__init__(generator)


class COperators:
    class IncrementDecrementOperators:
        CPreIncrementOperator = CUnaryOperatorToken("++", order=CUnaryOperatorToken.Order.Before)
        CPreDecrementOperator = CUnaryOperatorToken("--", order=CUnaryOperatorToken.Order.Before)
        CPostIncrementOperator = CUnaryOperatorToken("++", order=CUnaryOperatorToken.Order.After)
        CPostDecrementOperator = CUnaryOperatorToken("--", order=CUnaryOperatorToken.Order.After)

    class ArithmeticOperators:
        CSumOperator = CBinaryOperatorToken("+")
        CSubtractOperator = CBinaryOperatorToken("-")
        CMultiplyOperator = CBinaryOperatorToken("*")
        CDivideOperator = CBinaryOperatorToken("/")
        CModulusOperator = CBinaryOperatorToken("%")

        CBitWiseNotOperator = CUnaryOperatorToken("~", order=CUnaryOperatorToken.Order.Before)
        CBitWiseANDOperator = CBinaryOperatorToken("&")
        CBitWiseOROperator = CBinaryOperatorToken("|")
        CBitWiseXOROperator = CBinaryOperatorToken("^")
        CBitWiseLeftShiftOperator = CBinaryOperatorToken("<<")
        CBitWiseRightShiftOperator = CBinaryOperatorToken(">>")

    class AssignmentOperators:
        CAssignOperator = CBinaryOperatorToken("=")
        CSumAssignmentOperator = CBinaryOperatorToken("+=")
        CSubtractAssignmentOperator = CBinaryOperatorToken("-=")
        CMultiplyAssignmentOperator = CBinaryOperatorToken("*=")
        CDivideAssignmentOperator = CBinaryOperatorToken("/=")
        CModulusAssignmentOperator = CBinaryOperatorToken("%=")

        CBitWiseANDAssignmentOperator = CBinaryOperatorToken("&=")
        CBitWiseORAssignmentOperator = CBinaryOperatorToken("|=")
        CBitWiseXORAssignmentOperator = CBinaryOperatorToken("^=")
        CBitWiseLeftShiftAssignmentOperator = CBinaryOperatorToken("<<=")
        CBitWiseRightShiftAssignmentOperator = CBinaryOperatorToken(">>=")

    class LogicOperators:
        # TODO style with not, and and or operator tokens??
        CNegateOperator = CUnaryOperatorToken("!", order=CUnaryOperatorToken.Order.Before)
        CANDOperator = CBinaryOperatorToken("&&")
        COROperator = CBinaryOperatorToken("||")

    class ComparissonOperators:
        CEqualToOperator = CBinaryOperatorToken("==")
        CNotEqualToOperator = CBinaryOperatorToken("!=")
        CLessThanOperator = CBinaryOperatorToken("<")
        CGreaterThanOperator = CBinaryOperatorToken(">")
        CLessThanOrEqualToOperator = CBinaryOperatorToken("<=")
        CGreatherThanOrEqualToOperator = CBinaryOperatorToken(">=")

    class MemberAccessOperators:
        @staticmethod
        def _subscriptoperator(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
            return f"{a.render()}[{b.render()}]"

        CSubScriptOperator = CBinaryOperator(_subscriptoperator)
        CIndirectionOperator = CUnaryOperatorToken("*", order=CUnaryOperatorToken.Order.Before)
        CAddressOfOperator = CUnaryOperatorToken('&', order=CUnaryOperatorToken.Order.Before)
        CMemberOfObjectOperator = CBinaryOperatorToken('.')
        CMemberOfPointerOperator = CBinaryOperatorToken('->')
        CPointerToMemberOfObject = CBinaryOperatorToken('.*')
        CPointerToMemberOfPointer = CBinaryOperatorToken('->*')
