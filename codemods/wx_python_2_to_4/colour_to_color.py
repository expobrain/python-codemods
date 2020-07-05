from ast import literal_eval
from typing import Union

from libcst import matchers
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor
import libcst as cst


class ColourToColorCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Converts usage of wx.Colour into wx.Color"

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if matchers.matches(
            updated_node.func,
            matchers.Attribute(
                value=matchers.Name(value="wx"), attr=matchers.Name(value="Colour")
            ),
        ):
            return updated_node.with_changes(
                func=cst.Attribute(value=cst.Name(value="wx"), attr=cst.Name(value="Color"))
            )

        return updated_node
