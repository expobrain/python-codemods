from libcst.codemod import CodemodTest

from codemods.wx_python import ColorToColourCommand, ConstantsRenameCommand


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
