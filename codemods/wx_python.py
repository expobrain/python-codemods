from ast import literal_eval
from typing import List, Optional, Union
import textwrap

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


class MenuAppendCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Rename arguments for wx.menu.Append() method"

    args_map = {"help": "helpString", "text": "item"}
    args_matchers_map = {
        matchers.Arg(keyword=matchers.Name(value=value)): renamed
        for value, renamed in args_map.items()
    }
    call_matcher = matchers.Call(
        func=matchers.Attribute(attr=matchers.Name(value="Append")),
        args=matchers.MatchIfTrue(
            lambda args: bool(
                set(arg.keyword.value for arg in args if arg and arg.keyword).intersection(
                    MenuAppendCommand.args_map.keys()
                )
            )
        ),
    )

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if matchers.matches(updated_node, self.call_matcher):
            updated_node_args = list(updated_node.args)

            for arg_matcher, renamed in self.args_matchers_map.items():
                for i, node_arg in enumerate(updated_node.args):
                    if matchers.matches(node_arg, arg_matcher):
                        updated_node_args[i] = node_arg.with_changes(
                            keyword=cst.Name(value=renamed)
                        )

                updated_node = updated_node.with_changes(args=updated_node_args)

        return updated_node


class ToolbarAddToolCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Transforms wx.Toolbar.DoAddTool method into AddTool"

    args_map = {"id": "toolId"}
    args_matchers_map = {
        matchers.Arg(keyword=matchers.Name(value=value)): renamed
        for value, renamed in args_map.items()
    }
    call_matcher = matchers.Call(
        func=matchers.Attribute(attr=matchers.Name(value="DoAddTool")),
        args=matchers.MatchIfTrue(
            lambda args: bool(
                set(arg.keyword.value for arg in args if arg and arg.keyword).intersection(
                    ToolbarAddToolCommand.args_map.keys()
                )
            )
        ),
    )

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if matchers.matches(updated_node, self.call_matcher):
            # Update method's call
            updated_node = updated_node.with_changes(
                func=updated_node.func.with_changes(attr=cst.Name(value="AddTool"))
            )

            # Transform keywords
            updated_node_args = list(updated_node.args)

            for arg_matcher, renamed in self.args_matchers_map.items():
                for i, node_arg in enumerate(updated_node.args):
                    if matchers.matches(node_arg, arg_matcher):
                        updated_node_args[i] = node_arg.with_changes(
                            keyword=cst.Name(value=renamed)
                        )

                updated_node = updated_node.with_changes(args=updated_node_args)

        return updated_node


class SizerAddCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Transforms wx.Sizer.AddWindow method into Add"

    matcher = matchers.Call(func=matchers.Attribute(attr=matchers.Name(value="AddWindow")))

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if matchers.matches(updated_node, self.matcher):
            return updated_node.with_changes(
                func=updated_node.func.with_changes(attr=cst.Name(value="Add"))
            )

        return updated_node


class MakeModalCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Replace built-in method MAkeModal with helper"

    method_matcher = matchers.FunctionDef(
        name=matchers.Name(value="MakeModal"),
        params=matchers.Parameters(
            params=[matchers.Param(name=matchers.Name(value="self")), matchers.ZeroOrMore()]
        ),
    )
    call_matcher = matchers.Call(
        func=matchers.Attribute(
            value=matchers.Name(value="self"), attr=matchers.Name(value="MakeModal")
        )
    )

    method_cst = cst.parse_statement(
        textwrap.dedent(
            """
            def MakeModal(self, modal=True):
                if modal and not hasattr(self, '_disabler'):
                    self._disabler = wx.WindowDisabler(self)
                if not modal and hasattr(self, '_disabler'):
                    del self._disabler
            """
        )
    )

    def __init__(self, context: CodemodContext):
        super().__init__(context)

        self.stack: List[cst.ClassDef] = []

    def visit_ClassDef(self, node: cst.ClassDef):
        self.stack.append(node)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        return self.stack.pop()

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if matchers.matches(updated_node, self.call_matcher):
            # Search for MakeModal() method
            current_class = self.stack[-1]
            has_make_modal_method = False

            for method in current_class.body.body:
                if matchers.matches(method, self.method_matcher):
                    has_make_modal_method = True

            # If not, add it to the current class
            if not has_make_modal_method:
                current_class = current_class.with_changes(
                    body=current_class.body.with_changes(
                        body=[*current_class.body.body, self.method_cst]
                    )
                )

                self.stack[-1] = current_class

        return updated_node
