from ast import literal_eval
from typing import Union

from libcst import matchers
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor
import libcst as cst


class ColorToColourCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Converts usage of wx.Color into wx.Colour"

    matcher = matchers.Attribute(
        value=matchers.Name(value="wx"), attr=matchers.Name(value="Color")
    )

    def leave_Attribute(
        self, original_node: cst.Attribute, updated_node: cst.Attribute
    ) -> cst.Attribute:
        if matchers.matches(updated_node, self.matcher):
            return updated_node.with_changes(attr=cst.Name(value="Colour"))

        return updated_node
