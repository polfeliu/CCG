from typing import TYPE_CHECKING, Callable
from enum import Enum

from .Cexpression import CExpressionFreeStyle

if TYPE_CHECKING:
    from .Cexpression import CExpression


class COperator:
    pass


class CUnaryOperator(COperator):
    def __init__(self, generator_function: Callable[['CExpression'], CExpression]):
        self.operate = generator_function


class CUnaryOperatorToken(CUnaryOperator):
    class Order(Enum):
        Before = 0
        After = 1

    def __init__(self, operator_token: str, order: Order):
        super(CUnaryOperatorToken, self).__init__(
            lambda a: CExpressionFreeStyle("")  # TODO
        )

    def operate(self, a: 'CExpression') -> 'CExpression':
        raise NotImplemented


class CBinaryOperator(COperator):
    def __init__(self, generator_function: Callable[['CExpression', 'CExpression'], CExpression]):
        self.operate = generator_function


class CBinaryOperatorToken(CBinaryOperator):
    def __init__(self, operator_token: str):
        super(CBinaryOperatorToken, self).__init__(
            lambda a, b: CExpressionFreeStyle("")  # TODO
        )


class COperators:
    class CIncrementDecrementOperators:
        CPreIncrementOperator = CUnaryOperatorToken("++", order=CUnaryOperatorToken.Order.Before)
        CPreDecrementOperator = CUnaryOperatorToken("--", order=CUnaryOperatorToken.Order.Before)
        CPostIncrementOperator = CUnaryOperatorToken("++", order=CUnaryOperatorToken.Order.After)
        CPostDecrementOperator = CUnaryOperatorToken("--", order=CUnaryOperatorToken.Order.After)

    class CArithmeticOperators:
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

    class CAssignmentOperators:
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

    class CLogicOperators:
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
