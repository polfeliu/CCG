from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .Cexpression import CExpression


class COperator:
    def __init__(self, operator_token: str):
        self.operator_token = operator_token


class CUnaryOperator(COperator):
    class Order(Enum):
        Before = 0
        After = 1

    def __init__(self, operator_token: str, order: Order):
        super(CUnaryOperator, self).__init__(operator_token)
        self.order = order

    def operate(self, a: CExpression) -> CExpression:
        raise NotImplemented


class CBinaryOperator(COperator):
    def operate(self, a: CExpression, b: CExpression) -> CExpression:
        raise NotImplemented


CAssignOperator = CBinaryOperator("=")

CPreIncrementOperator = CUnaryOperator("++", order=CUnaryOperator.Order.Before)
CPreDecrementOperator = CUnaryOperator("--", order=CUnaryOperator.Order.Before)
CPostIncrementOperator = CUnaryOperator("++", order=CUnaryOperator.Order.After)
CPostDecrementOperator = CUnaryOperator("--", order=CUnaryOperator.Order.After)

CSumOperator = CBinaryOperator("+")
CSubtractOperator = CBinaryOperator("-")
CMultiplyOperator = CBinaryOperator("*")
CDivideOperator = CBinaryOperator("/")
CModulusOperator = CBinaryOperator("%")

CBitWiseNotOperator = CUnaryOperator("~", order=CUnaryOperator.Order.Before)
CBitWiseANDOperator = CBinaryOperator("&")
CBitWiseOROperator = CBinaryOperator("|")
CBitWiseXOROperator = CBinaryOperator("^")
CBitWiseLeftShiftOperator = CBinaryOperator("<<")
CBitWiseRightShiftOperator = CBinaryOperator(">>")

CSumAssignmentOperator = CBinaryOperator("+=")
CSubtractAssignmentOperator = CBinaryOperator("-=")
CMultiplyAssignmentOperator = CBinaryOperator("*=")
CDivideAssignmentOperator = CBinaryOperator("/=")
CModulusAssignmentOperator = CBinaryOperator("%=")

CBitWiseANDAssignmentOperator = CBinaryOperator("&=")
CBitWiseORAssignmentOperator = CBinaryOperator("|=")
CBitWiseXORAssignmentOperator = CBinaryOperator("^=")
CBitWiseLeftShiftAssignmentOperator = CBinaryOperator("<<=")
CBitWiseRightShiftAssignmentOperator = CBinaryOperator(">>=")

# TODO style with not, and and or operator tokens??
CNegateOperator = CUnaryOperator("!", order=CUnaryOperator.Order.Before)
CANDOperator = CBinaryOperator("&&")
COROperator = CBinaryOperator("||")

# TODO Comparisson

# TODO Member access
