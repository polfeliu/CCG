from typing import TYPE_CHECKING, Callable
from enum import Enum

from .Cexpression import CExpression, CExpressionFreeStyle
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style


# TODO Styling, mainly spaces

class COperator:
    pass


class CUnaryOperator(COperator):
    def __init__(self, generator_function: Callable[['CExpression'], CExpression]):
        self.operate = generator_function

    def __call__(self, a: 'CExpression') -> 'CExpression':
        return self.operate(a)


class CBinaryOperator(COperator):
    def __init__(self, generator_function: Callable[['CExpression', 'CExpression'], CExpression]):
        self.operate = generator_function

    def __call__(self, a: 'CExpression', b: 'CExpression') -> 'CExpression':
        return self.operate(a, b)


class CUnaryOperatorToken(CUnaryOperator):
    class Order(Enum):
        Before = 0
        After = 1

    def __init__(self, operator_token: str, order: Order):
        self.operator_token = operator_token
        self.order = order

        if self.order == self.Order.Before:
            def generator(a: 'CExpression') -> 'CExpression':
                return CExpressionFreeStyle(f"{operator_token}{a.render()}")
        elif self.order == self.Order.After:
            def generator(a: 'CExpression') -> 'CExpression':
                return CExpressionFreeStyle(f"{a.render()}{operator_token}")
        else:
            raise ValueError

        super(CUnaryOperatorToken, self).__init__(generator)


class CBinaryOperatorToken(CBinaryOperator):
    def __init__(self, operator_token: str):
        super(CBinaryOperatorToken, self).__init__(
            lambda a, b: CExpressionFreeStyle(
                f"{a.render()}{operator_token}{b.render()}"
            )
        )


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
        CSubScriptOperator = CBinaryOperator(lambda a, b: CExpressionFreeStyle(f"{a}[{b}]"))
        CIndirectionOperator = CUnaryOperatorToken("*", order=CUnaryOperatorToken.Order.Before)
        CAddressOfOperator = CUnaryOperatorToken('&', order=CUnaryOperatorToken.Order.Before)
        CMemberOfObjectOperator = CBinaryOperatorToken('.')
        CMemberOfPointerOperator = CBinaryOperatorToken('->')
        CPointerToMemberOfObject = CBinaryOperatorToken('.*')
        CPointerToMemberOfPointer = CBinaryOperatorToken('->*')
