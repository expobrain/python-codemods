import textwrap

from libcst.codemod import CodemodTest

from codemods.wx_python import (
    ColorToColourCommand,
    ConstantsRenameCommand,
    FixImportFromAdvCommand,
    FlexGridSizerCommand,
    MenuAppendCommand,
    ToolbarAddToolCommand,
)


class ColorToColourCommandTests(CodemodTest):

    TRANSFORM = ColorToColourCommand

    def test_call_substitution(self) -> None:
        before = "wx.Color(255, 255, 255)"
        after = "wx.Colour(255, 255, 255)"

        self.assertCodemod(before, after)

    def test_reference_substitution(self) -> None:
        before = "isinstance(a, wx.Color)"
        after = "isinstance(a, wx.Colour)"

        self.assertCodemod(before, after)


class ConstantsRenameCommandTests(CodemodTest):

    TRANSFORM = ConstantsRenameCommand

    def test_WXK_PRIOR_substitution(self) -> None:
        before = "wx.WXK_PRIOR"
        after = "wx.WXK_PAGEUP"

        self.assertCodemod(before, after)

    def test_WXK_NEXT_substitution(self) -> None:
        before = "wx.WXK_NEXT"
        after = "wx.WXK_PAGEDOWN"

        self.assertCodemod(before, after)

    def test_WXK_NUMPAD_PRIOR_substitution(self) -> None:
        before = "wx.WXK_NUMPAD_PRIOR"
        after = "wx.WXK_NUMPAD_PAGEUP"

        self.assertCodemod(before, after)

    def test_WXK_NUMPAD_NEXT_substitution(self) -> None:
        before = "wx.WXK_NUMPAD_NEXT"
        after = "wx.WXK_NUMPAD_PAGEDOWN"

        self.assertCodemod(before, after)

    def test_OPEN_substitution(self) -> None:
        before = "wx.OPEN"
        after = "wx.FD_OPEN"

        self.assertCodemod(before, after)

    def test_FILE_MUST_EXIST_substitution(self) -> None:
        before = "wx.FILE_MUST_EXIST"
        after = "wx.FD_FILE_MUST_EXIST"

        self.assertCodemod(before, after)


class FixImportFromAdvCommandTests(CodemodTest):

    TRANSFORM = FixImportFromAdvCommand

    def test_add_import_once_substitution(self) -> None:
        before = textwrap.dedent(
            """
            import wx.adv

            wx.DP_ALLOWNONE
            """
        )
        after = textwrap.dedent(
            """
            import wx.adv

            wx.adv.DP_ALLOWNONE
            """
        )

        self.assertCodemod(before, after)

    def test_constants_DP_ALLOWNONE_substitution(self) -> None:
        before = "wx.DP_ALLOWNONE"
        after = textwrap.dedent(
            """
            import wx.adv

            wx.adv.DP_ALLOWNONE
            """
        )

        self.assertCodemod(before, after)

    def test_constants_DP_DROPDOWN_substitution(self) -> None:
        before = "wx.DP_DROPDOWN"
        after = textwrap.dedent(
            """
            import wx.adv

            wx.adv.DP_DROPDOWN
            """
        )

        self.assertCodemod(before, after)

    def test_constants_DP_SHOWCENTURY_substitution(self) -> None:
        before = "wx.DP_SHOWCENTURY"
        after = textwrap.dedent(
            """
            import wx.adv

            wx.adv.DP_SHOWCENTURY
            """
        )

        self.assertCodemod(before, after)

    def test_symbols_DatePickerCtrl_substitution(self) -> None:
        before = "wx.DatePickerCtrl"
        after = textwrap.dedent(
            """
            import wx.adv

            wx.adv.DatePickerCtrl
            """
        )

        self.assertCodemod(before, after)


class FlexGridSizerCommandTests(CodemodTest):

    TRANSFORM = FlexGridSizerCommand

    def test_no_op(self) -> None:
        before = "wx.FlexGridSizer(1, 0, 0)"
        after = "wx.FlexGridSizer(1, 0, 0)"

        self.assertCodemod(before, after)

    def test_substitution(self) -> None:
        before = "wx.FlexGridSizer(1, 0)"
        after = "wx.FlexGridSizer(1, 0, 0)"

        self.assertCodemod(before, after)


class MenuAppendCommandTests(CodemodTest):

    TRANSFORM = MenuAppendCommand

    def test_substitution(self) -> None:
        before = textwrap.dedent(
            """
            menu.Append(
                help="",
                id=1,
                kind=wx.ITEM_NORMAL,
                text="Menu item",
            )
            """
        )
        after = textwrap.dedent(
            """
            menu.Append(
                helpString="",
                id=1,
                kind=wx.ITEM_NORMAL,
                item="Menu item",
            )
            """
        )

        self.assertCodemod(before, after)


class ToolbarAddToolCommandTests(CodemodTest):

    TRANSFORM = ToolbarAddToolCommand

    def test_substitution(self) -> None:
        before = textwrap.dedent(
            """
            toolbar.DoAddTool(
                bitmap=my_bitmap,
                id=1,
                label="Toolbar tool"
            )
            """
        )
        after = textwrap.dedent(
            """
            toolbar.AddTool(
                bitmap=my_bitmap,
                toolId=1,
                label="Toolbar tool"
            )
            """
        )

        self.assertCodemod(before, after)
