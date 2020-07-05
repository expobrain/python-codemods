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


class ConstantsRenameCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Rename constants"

    matchers_map = {
        matchers.Attribute(
            value=matchers.Name(value="wx"), attr=matchers.Name(value=name)
        ): renamed
        for name, renamed in [
            ("WXK_PRIOR", "WXK_PAGEUP"),
            ("WXK_NEXT", "WXK_PAGEDOWN"),
            ("WXK_NUMPAD_PRIOR", "WXK_NUMPAD_PAGEUP"),
            ("WXK_NUMPAD_NEXT", "WXK_NUMPAD_PAGEDOWN"),
            ("OPEN", "FD_OPEN"),
            ("FILE_MUST_EXIST", "FD_FILE_MUST_EXIST"),
        ]
    }

    def leave_Attribute(
        self, original_node: cst.Attribute, updated_node: cst.Attribute
    ) -> cst.Attribute:
        for matcher, renamed in self.matchers_map.items():
            if matchers.matches(updated_node, matcher):
                return updated_node.with_changes(attr=cst.Name(value=renamed))

        return updated_node


class FixImportFromAdvCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Fix importing symbols now moved into wx.adv package"

    matchers = [
        matchers.Attribute(value=matchers.Name(value="wx"), attr=matchers.Name(value=name))
        for name in ["DatePickerCtrl", "DP_ALLOWNONE", "DP_DROPDOWN", "DP_SHOWCENTURY"]
    ]

    def leave_Attribute(
        self, original_node: cst.Attribute, updated_node: cst.Attribute
    ) -> cst.Attribute:
        for matcher in self.matchers:
            if matchers.matches(updated_node, matcher):
                # Ensure that wx.adv is imported
                AddImportsVisitor.add_needed_import(self.context, "wx.adv")

                # Return modified node
                return updated_node.with_changes(
                    value=cst.Attribute(value=cst.Name(value="wx"), attr=cst.Name(value="adv"))
                )

        return updated_node


class FlexGridSizerCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Updates wx.FlexGridSize constructor's calls"

    matcher = matchers.Call(
        func=matchers.Attribute(
            value=matchers.Name(value="wx"), attr=matchers.Name(value="FlexGridSizer")
        ),
        args=[matchers.DoNotCare(), matchers.DoNotCare()],
    )

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if matchers.matches(updated_node, self.matcher):
            return updated_node.with_changes(
                args=[*updated_node.args, cst.Arg(value=cst.Integer(value="0"))]
            )

        return updated_node
