from abc import ABC, abstractmethod
from copy import copy
from typing import TYPE_CHECKING, List, Any, Optional

from ..Cnamespace import CSpace
from ..statements import CStatement, CDeclaration
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style
    from ..doc import Doc


class HungarianNotationError(Exception):
    pass


class CGenericItem(CSpace, ABC):
    """Generic Item

    Object that can be declared: Function, Class, Variable, Struct...
    """

    def __init__(self,
                 name: str,
                 in_space: Optional['CSpace'] = None,
                 doc: Optional['Doc'] = None
                 ):
        super(CGenericItem, self).__init__(
            name=name,
            in_space=in_space
        )
        self.doc = doc

    def declare(self, from_space: 'CSpace' = None) -> 'CDeclaration':
        return CDeclaration(
            render_function=self.declaration,
            from_space=from_space
        )

    @abstractmethod
    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None
                    ) -> str:
        raise NotImplemented

    def doc_render(self, style: 'Style') -> str:
        if self.doc is None:
            return ""

        return self.doc.render(style, content=None)


class CItemDefinable(ABC):
    """Generic Item that can be defined"""

    @abstractmethod
    def definition(self,
                   style: 'Style' = default_style,
                   from_space: 'CSpace' = None,
                   doc: bool = False
                   ) -> str:
        return ""

    def define(self, from_space: 'CSpace' = None) -> 'CDeclaration':
        return CDeclaration(
            render_function=self.definition,
            from_space=from_space,
        )


class CGenericType(CGenericItem):
    """Item that is or generates a type"""

    def __init__(self,
                 name: str,
                 bit_size: Optional[int] = None,
                 hungarian_prefixes: Optional[List[str]] = None,
                 derived_from: Optional['CGenericType'] = None,
                 in_space: Optional['CSpace'] = None,
                 doc: Optional['Doc'] = None
                 ):
        super(CGenericType, self).__init__(
            name=name,
            in_space=in_space,
            doc=doc
        )
        if hungarian_prefixes is None:
            hungarian_prefixes = ["t"]
        self.hungarian_prefixes = hungarian_prefixes
        self.derived_from = derived_from
        self._bit_size = bit_size

    @property
    def bit_size(self) -> int:
        if self._bit_size is None:
            raise ValueError("Cannot determine bit_size")
        return self._bit_size

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None,
                    without_arguments: bool = False,
                    for_variable: bool = False
                    ) -> str:
        """Type declaration

        Args:
            style: generating style
            semicolon: include semicolon in declaration
            doc: include documentation
            from_space: relative to space
            without_arguments: include arguments if any
            for_variable: if the declaration is for a variable

        Returns:

        """
        return self.name + (';' if semicolon else '')

    def check_value(self, value: Any) -> bool:
        """Checks that a value is correct for the type

        Args:
            value: value to check

        Returns:
            boolean indicating if value fits type (True) or not
        """
        return True  # Generic type accept everything. Override this method to check custom types

    def style_checks(self, style: 'Style') -> None:

        if style.check_hungarian:
            if not issubclass(type(self), CStdType):
                if not self.name.startswith('T'):
                    raise HungarianNotationError(
                        f"Generic Type ({self.name}) Doesn't start with T hungarian style prefix")
                else:
                    start_letter = self.name[1]
                    if not start_letter.isupper():
                        raise HungarianNotationError(f"{self.name} first letter is not uppercase")

    def type(self, name: str) -> 'CGenericType':
        """Create a copy of the type with a new name"""
        new_type = copy(self)
        new_type.name = name
        new_type.derived_from = self
        new_type.hungarian_prefixes = ["t"]

        return new_type

    def typedef_render(self,
                       style: 'Style' = default_style,
                       from_space: 'CSpace' = None,
                       doc: Optional['Doc'] = None
                       ) -> str:
        if self.derived_from is None:
            raise TypeError(f"Cannot typedef type {self.name} that is not derived from another type")
        return (
            f"{doc.render(style) if doc is not None else ''}"
            f"typedef "
            f"{self.derived_from.declaration(style=style, semicolon=False, doc=False, from_space=from_space)} "
            f"{self.name};"
        )

    def typedef(self, doc: Optional['Doc'] = None) -> CStatement:
        return CStatement(
            render_function=self.typedef_render,
            doc=doc
        )


# Late import to avoid circular import
from .CstdTypes import CStdType
