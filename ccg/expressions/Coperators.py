from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Callable

from .Cexpression import CExpression
from ..statements import CStatement
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style


class CExpressionOperation(CExpression):
    """Operation that yields and expression"""

    @abstractmethod
    def render(self, style: 'Style' = default_style) -> str:
        raise NotImplementedError


class CStatementOperation(CStatement):
    """Operation that yields a statement"""

    @abstractmethod
    def render(self, style: 'Style' = default_style) -> str:
        raise NotImplementedError


class CUnaryOperation:
    """Operation to one element"""

    def __init__(self,
                 render_function: Callable[['Style', 'CExpression'], str],
                 a: 'CExpression'
                 ):
        self.render_function = render_function
        self.a = a

    def render(self, style: 'Style' = default_style) -> str:
        return self.render_function(style, self.a)


class CExpressionUnaryOperation(CUnaryOperation, CExpressionOperation):
    pass


class CStatementUnaryOperation(CUnaryOperation, CStatementOperation):
    pass


class CBinaryOperation(CExpressionOperation):
    """Operation between two elements"""

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


class CExpressionBinaryOperation(CBinaryOperation, CExpressionOperation):
    pass


class CStatementBinaryOperation(CBinaryOperation, CStatementOperation):
    pass


class COperator:
    """Operator. Object that can operate between one or more expressions and create a new operation object"""
    pass


class CExpressionUnaryOperator(COperator):
    """Unary Operator that outputs an expression"""

    def __init__(self, render_function: Callable[['Style', 'CExpression'], str]):
        self.render_function = render_function

    def __call__(self, a: 'CExpression') -> 'CExpressionUnaryOperation':
        return CExpressionUnaryOperation(self.render_function, a)


class CExpressionBinaryOperator(COperator):
    """Binary Operator that outputs an expression"""

    def __init__(self, render_function: Callable[['Style', 'CExpression', 'CExpression'], str]):
        self.render_function = render_function

    def __call__(self, a: 'CExpression', b: 'CExpression') -> 'CExpressionOperation':
        return CExpressionBinaryOperation(self.render_function, a, b)


class CStatementBinaryOperator(COperator):
    """Binary Operator that outputs a statement"""

    def __init__(self, render_function: Callable[['Style', 'CExpression', 'CExpression'], str]):
        self.render_function = render_function

    def __call__(self, a: 'CExpression', b: 'CExpression') -> 'CStatement':
        return CStatementBinaryOperation(self.render_function, a, b)


class Order(Enum):
    Before = 0
    After = 1


def unary_operator_token_curry(operator_token: str, order: Order) -> Callable[['Style', 'CExpression'], str]:
    """Currying function to construct render functions"""

    if order == Order.Before:
        def unary_operator_render(style: 'Style', a: 'CExpression') -> 'str':
            return (
                f"{operator_token}"
                f"{style.vspace_unary_operator}"
                f"{a.render(style)}"
            )
    elif order == Order.After:
        def unary_operator_render(style: 'Style', a: 'CExpression') -> 'str':
            return (
                f"{a.render(style)}"
                f"{style.vspace_unary_operator}"
                f"{operator_token}"
            )
    else:
        raise ValueError

    return unary_operator_render


class CExpressionUnaryOperatorToken(CExpressionUnaryOperator):
    """Helper class to create unary operators with a token. Outputs Expression"""

    def __init__(self, operator_token: str, order: Order):
        super(CExpressionUnaryOperatorToken, self).__init__(unary_operator_token_curry(operator_token, order))


class CStatementUnaryOperatorToken(CExpressionUnaryOperator):
    """Helper class to create unary operators with a token. Outputs Statement"""

    def __init__(self, operator_token: str, order: Order):
        super(CStatementUnaryOperatorToken, self).__init__(unary_operator_token_curry(operator_token, order))


def binary_operator_token_curry(operator_token: str) -> Callable[['Style', 'CExpression', 'CExpression'], str]:
    """Currying function to construct render functions"""

    def binary_operator_render(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
        return (
            f"{a.render(style)}"
            f"{style.vspace_before_binary_operator}"
            f"{operator_token}"
            f"{style.vspace_after_binary_operator}"
            f"{b.render(style)}"
        )

    return binary_operator_render


class CExpressionBinaryOperatorToken(CExpressionBinaryOperator):
    """Helper class to create binary operators with a token. Outputs Expression"""

    def __init__(self, operator_token: str):
        super(CExpressionBinaryOperatorToken, self).__init__(binary_operator_token_curry(operator_token))


class CStatementBinaryOperatorToken(CStatementBinaryOperator):
    """Helper class to create binary operators with a token. Outputs Statement"""

    def __init__(self, operator_token: str):
        super(CStatementBinaryOperatorToken, self).__init__(binary_operator_token_curry(operator_token))


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
        f"{a.render(style)}"
    )


def and_render(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
    if style.and_operator_style == style.AndOperatorStyles.Explicit:
        before_space = " "
        after_space = " "
    else:
        before_space = str(style.vspace_before_binary_operator)
        after_space = str(style.vspace_after_binary_operator)

    return (
        f"{a.render(style)}"
        f"{before_space}"
        f"{style.and_operator_style.value}"
        f"{after_space}"
        f"{b.render(style)}"
    )


def or_render(style: 'Style', a: 'CExpression', b: 'CExpression') -> str:
    if style.or_operator_style == style.OrOperatorStyles.Explicit:
        before_space = " "
        after_space = " "
    else:
        before_space = str(style.vspace_before_binary_operator)
        after_space = str(style.vspace_after_binary_operator)

    return (
        f"{a.render(style)}"
        f"{before_space}"
        f"{style.and_operator_style.value}"
        f"{after_space}"
        f"{b.render(style)}"
    )


class COperators:
    class IncrementDecrement:
        PreIncrementExpression = CExpressionUnaryOperatorToken("++", order=Order.Before)
        PreDecrementExpression = CExpressionUnaryOperatorToken("--", order=Order.Before)
        PostIncrementExpression = CExpressionUnaryOperatorToken("++", order=Order.After)
        PostDecrementExpression = CExpressionUnaryOperatorToken("--", order=Order.After)

        PreIncrementStatement = CStatementUnaryOperatorToken("++", order=Order.Before)
        PreDecrementStatement = CStatementUnaryOperatorToken("--", order=Order.Before)
        PostIncrementStatement = CStatementUnaryOperatorToken("++", order=Order.After)
        PostDecrementStatement = CStatementUnaryOperatorToken("--", order=Order.After)

    class Arithmetic:
        Sum = CExpressionBinaryOperatorToken("+")
        Subtract = CExpressionBinaryOperatorToken("-")
        Multiply = CExpressionBinaryOperatorToken("*")
        Divide = CExpressionBinaryOperatorToken("/")
        Modulus = CExpressionBinaryOperatorToken("%")

        BitWiseNot = CExpressionUnaryOperatorToken("~", order=Order.Before)
        BitWiseAnd = CExpressionBinaryOperatorToken("&")
        BitWiseOr = CExpressionBinaryOperatorToken("|")
        BitWiseXor = CExpressionBinaryOperatorToken("^")
        BitWiseLeftShift = CExpressionBinaryOperatorToken("<<")
        BitWiseRightShift = CExpressionBinaryOperatorToken(">>")

    class Assignment:
        Assign = CStatementBinaryOperatorToken("=")
        SumAssignment = CStatementBinaryOperatorToken("+=")
        SubtractAssignment = CStatementBinaryOperatorToken("-=")
        MultiplyAssignment = CStatementBinaryOperatorToken("*=")
        DivideAssignment = CStatementBinaryOperatorToken("/=")
        ModulusAssignment = CStatementBinaryOperatorToken("%=")

        BitWiseAndAssignment = CStatementBinaryOperatorToken("&=")
        BitWiseOrAssignment = CStatementBinaryOperatorToken("|=")
        BitWiseXorAssignment = CStatementBinaryOperatorToken("^=")
        BitWiseLeftShiftAssignment = CStatementBinaryOperatorToken("<<=")
        BitWiseRightShiftAssignment = CStatementBinaryOperatorToken(">>=")

    class Logic:
        Not = CExpressionUnaryOperator(not_render)
        And = CExpressionBinaryOperator(and_render)
        Or = CExpressionBinaryOperator(or_render)

    class Comparison:
        EqualTo = CExpressionBinaryOperatorToken("==")
        NotEqualTo = CExpressionBinaryOperatorToken("!=")
        LessThan = CExpressionBinaryOperatorToken("<")
        GreaterThan = CExpressionBinaryOperatorToken(">")
        LessThanOrEqualTo = CExpressionBinaryOperatorToken("<=")
        GreaterThanOrEqualTo = CExpressionBinaryOperatorToken(">=")

    class MemberAccess:
        SubScript = CExpressionBinaryOperator(subscript_render)
        Indirection = CExpressionUnaryOperatorToken("*", order=Order.Before)
        AddressOf = CExpressionUnaryOperatorToken('&', order=Order.Before)
        MemberOfObject = CExpressionBinaryOperatorToken('.')
        MemberOfPointer = CExpressionBinaryOperatorToken('->')
        PointerToMemberOfObject = CExpressionBinaryOperatorToken('.*')
        PointerToMemberOfPointer = CExpressionBinaryOperatorToken('->*')

    Parentheses = CExpressionUnaryOperator(parentheses_render)
